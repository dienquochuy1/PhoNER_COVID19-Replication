# ner_model.py
import os
import json
from typing import List, Dict, Any
from collections import Counter
from dotenv import load_dotenv
from openai import AzureOpenAI
from seqeval.metrics import f1_score, classification_report
from tqdm import tqdm

from params import temperature, max_tokens
from prompts import SYSTEM_PROMPT, DEFINITIONS, PROMPT_TEMPLATE, POS_PROMPT
from utils import (format_sentence, format_entity_descriptions, clean_json_response, 
                  extract_json_from_text, get_valid_tags, clean_tags, 
                  align_tags_length, save_incorrect_samples, merge_tags_from_decomposed)

class COVID_NER_AzureOpenAI:
    def __init__(self, use_decomposed: bool = False, use_syntactic_prompting: bool = False, 
                 use_tool_augmentation: bool = False, sc_samples: int = 1):
        load_dotenv()
        self.client = AzureOpenAI(
            api_key=os.getenv('AZURE_OPENAI_API_KEY'),
            azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT'),
            api_version=os.getenv('AZURE_OPENAI_API_VERSION')
        )
        self.model_name = os.getenv('AZURE_OPENAI_DEPLOYMENT')
        self.entity_definitions = DEFINITIONS
        self.labels = list(DEFINITIONS.keys())
        self.use_decomposed = use_decomposed
        self.use_syntactic_prompting = use_syntactic_prompting
        self.use_tool_augmentation = use_tool_augmentation
        self.sc_samples = sc_samples

    def extract_pos(self, sentence: List[str]) -> List[str]:
        """Extract POS tags using the model as a 'tool'."""
        text = format_sentence(sentence)
        prompt = POS_PROMPT.format(text=text)
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
                max_tokens=max_tokens,
            )
            result_text = response.choices[0].message.content
            cleaned_text = clean_json_response(result_text)
            json_result = extract_json_from_text(cleaned_text)
            pos = json_result.get("pos", ["UNK"] * len(sentence))
            return pos
        except Exception as e:
            print(f"Lỗi extract POS: {str(e)}")
            return ["UNK"] * len(sentence)

    def generate_prompt(self, text: str, label: str = None) -> str:
        """Generate prompt based on flags."""
        if label:
            label_specific = f"chỉ các thực thể loại {label}"
            entity_descriptions = f"- {label}: {self.entity_definitions[label]}"
            entities = label
        else:
            label_specific = "các thực thể"
            entity_descriptions = format_entity_descriptions(self.entity_definitions)
            entities = ', '.join(self.labels)

        syntactic_hint = ""
        if self.use_syntactic_prompting:
            syntactic_hint = "Làm từng bước: Đầu tiên, xác định loại của từng từ trong câu (Part-of-Speech). Sau đó, dựa vào các loại từ đó để tìm và nhận dạng các tên riêng (các nhãn POS)"

        syntactic_info = ""
        if self.use_tool_augmentation:
            syntactic_hint = "Sử dụng thông tin cú pháp được cung cấp (nhãn POS) sau để nhận dạng thực thể từng bước."
            # POS will be added in extract_entities

        prompt = PROMPT_TEMPLATE.format(
            label_specific=label_specific,
            entity_descriptions=entity_descriptions,
            entities=entities,
            syntactic_hint=syntactic_hint,
            syntactic_info=syntactic_info,
            text=text
        )
        return prompt

    def extract_entities(self, sentence: List[str], label: str = None) -> List[str]:
        """Extract tags, with tool augmentation if enabled."""
        text = format_sentence(sentence)
        if self.use_tool_augmentation:
            pos_tags = self.extract_pos(sentence)
            syntactic_info = "\nThông tin cú pháp (POS tags):\n" + "\n".join(f"{w}: {p}" for w, p in zip(sentence, pos_tags))
        else:
            syntactic_info = ""
        
        # Update prompt with syntactic_info if applicable
        prompt = self.generate_prompt(text, label)
        if self.use_tool_augmentation:
            prompt = prompt.replace("{syntactic_info}", syntactic_info)  # Since template has {syntactic_info}, but we replaced earlier to ""

        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature if self.sc_samples == 1 else 0.7,
                max_tokens=max_tokens,
            )
            result_text = response.choices[0].message.content
            cleaned_text = clean_json_response(result_text)
            json_result = extract_json_from_text(cleaned_text)
            tags = json_result.get("tags", ["O"] * len(sentence))
            return tags
        except Exception as e:
            print(f"Lỗi khi gọi API: {str(e)}")
            return ["O"] * len(sentence)

    def predict_tags_single(self, sentence: List[str]) -> List[str]:
        """Predict tags without SC."""
        if self.use_decomposed:
            all_label_tags = {label: self.extract_entities(sentence, label) for label in self.labels}
            final_tags = merge_tags_from_decomposed(all_label_tags, len(sentence))
        else:
            final_tags = self.extract_entities(sentence)
        return final_tags

    def predict_tags(self, sentence: List[str]) -> List[str]:
        """Predict with optional self-consistency."""
        if self.sc_samples == 1:
            tags = self.predict_tags_single(sentence)
        else:
            all_tags = []
            for _ in range(self.sc_samples):
                tags_sample = self.predict_tags_single(sentence)
                all_tags.append(tags_sample)
            
            # Two-stage majority voting
            entity_spans = []
            for tags in all_tags:
                start = None
                for i, tag in enumerate(tags):
                    if tag.startswith("B-"):
                        if start is not None:
                            entity_spans.append((start, i))
                        start = i
                    elif tag.startswith("I-") and start is None:
                        continue
                    elif tag == "O" and start is not None:
                        entity_spans.append((start, i))
                        start = None
                if start is not None:
                    entity_spans.append((start, len(tags)))
            
            span_counter = Counter(entity_spans)
            voted_spans = [span for span, count in span_counter.items() if count > self.sc_samples // 2]
            
            final_tags = ["O"] * len(sentence)
            for start, end in voted_spans:
                label_votes = []
                for tags in all_tags:
                    span_tags = tags[start:end]
                    if span_tags and span_tags[0].startswith("B-"):
                        label = span_tags[0].split("-")[1]
                        label_votes.append(label)
                if label_votes:
                    most_common_label = Counter(label_votes).most_common(1)[0][0]
                    final_tags[start] = f"B-{most_common_label}"
                    for i in range(start + 1, end):
                        final_tags[i] = f"I-{most_common_label}"
            
            tags = final_tags
        
        valid_tags = get_valid_tags(self.entity_definitions)
        return clean_tags(tags, valid_tags)

    def evaluate(self, test_data: List[Dict]) -> tuple:
        y_true = []
        y_pred = []
        incorrect_samples = []

        for sample in tqdm(test_data):
            words = sample["words"]
            true_tags = sample["tags"]
            pred_tags = self.predict_tags(words)
            
            pred_tags = align_tags_length(pred_tags, true_tags)
            
            if pred_tags != true_tags:
                incorrect_samples.append({
                    "text": " ".join(words),
                    "true_tags": true_tags,
                    "pred_tags": pred_tags
                })

            y_true.append(true_tags)
            y_pred.append(pred_tags)

        try:
            f1 = f1_score(y_true, y_pred)
            report = classification_report(y_true, y_pred)
            
            save_incorrect_samples(incorrect_samples)
            
            print(f"F1 Score: {f1:.4f}")
            print("Classification Report:")
            print(report)
            return f1, report
        except ValueError as e:
            print(f"Error in evaluation: {e}")
            return 0.0, "Evaluation failed"
# utils.py 
import json
import re
from typing import List, Dict

def load_data(file_path: str) -> List[Dict]:
    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            data.append(json.loads(line))
    return data

def format_sentence(words: List[str]) -> str:
    return " ".join(words)

def format_entity_descriptions(entity_definitions: Dict[str, str]) -> str:
    return "\n".join([f"- {entity}: {desc}" for entity, desc in entity_definitions.items()])

def clean_json_response(response_text: str) -> str:
    return response_text.replace("```json", "").replace("```", "").strip()

def extract_json_from_text(text: str) -> dict:
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if json_match:
            json_str = json_match.group(0)
            if not json_str.strip().endswith('}'):
                json_str = json_str.rstrip(',') + '}'
            try:
                return json.loads(json_str)
            except json.JSONDecodeError:
                json_str = re.sub(r',\s*}$', '}', json_str)
                try:
                    return json.loads(json_str)
                except:
                    pass
    print(f"Failed to parse JSON: {text[:200]}...")
    return {}

def get_valid_tags(entity_definitions: Dict[str, str]) -> set:
    valid_entities = list(entity_definitions.keys())
    full_valid_tags = set(["O"])
    for ent in valid_entities:
        full_valid_tags.add(f"B-{ent}")
        full_valid_tags.add(f"I-{ent}")
    return full_valid_tags

def clean_tags(tags: List[str], valid_tags: set) -> List[str]:
    cleaned_tags = []
    for tag in tags:
        if tag in valid_tags:
            cleaned_tags.append(tag)
        else:
            cleaned_tags.append("O")
    return cleaned_tags

def align_tags_length(pred_tags: List[str], true_tags: List[str]) -> List[str]:
    if len(pred_tags) > len(true_tags):
        return pred_tags[:len(true_tags)]
    elif len(pred_tags) < len(true_tags):
        return pred_tags + ["O"] * (len(true_tags) - len(pred_tags))
    return pred_tags

def save_incorrect_samples(incorrect_samples: List[Dict], file_path: str = 'error_analysis.json'):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(incorrect_samples, f, ensure_ascii=False, indent=2)

def merge_tags_from_decomposed(all_label_tags: Dict[str, List[str]], length: int) -> List[str]:
    """Merge tags from decomposed predictions. Prioritize first non-O if conflict."""
    final_tags = ["O"] * length
    for label, tags in all_label_tags.items():
        for i, tag in enumerate(tags):
            if tag != "O" and final_tags[i] == "O":
                # Replace B/I with correct label
                if tag.startswith("B-"):
                    final_tags[i] = f"B-{label}"
                elif tag.startswith("I-"):
                    final_tags[i] = f"I-{label}"
            # If conflict, keep existing (prioritize earlier labels)
    return final_tags
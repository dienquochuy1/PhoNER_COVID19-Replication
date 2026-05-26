# Prompt Templates for Vietnamese NER Benchmark

This document outlines the prompt templates used in the benchmark evaluation of Named Entity Recognition (NER) with Large Language Models (LLMs) in Vietnamese. These templates are designed for various prompting strategies: Few-Shot, Zero-Shot, Zero-Shot Chain-of-Thought (CoT), and Few-Shot adapted for VLSP dataset.

Each template includes placeholders like `{label_specific}`, `{entity_descriptions}`, `{entities}`, and `{text}` for customization. The output format is strictly JSON with BIO tagging scheme.

## Few-Shot Prompt (General)

This prompt uses multiple examples to guide the model in identifying entities from the PhoNER_COVID19 dataset style.

```plaintext
You are a linguistic expert in Vietnamese. Your task is to find all unique named entities from the text and return them.

Let's identify {label_specific} in this sentence:

{entity_descriptions}

Example:

Example 1:
"words": ["Bệnh_nhân", "523", "và", "chồng", "là", "bệnh_nhân", "522", ",", "67", "tuổi", ",", "được", "Bộ", "Y_tế", "ghi_nhận", "nhiễm", "nCoV", "hôm", "31/7", "."], "tags": ["O", "B-PATIENT_ID", "O", "O", "O", "B-PATIENT_ID", "O", "O", "B-AGE", "O", "O", "O", "B-ORGANIZATION", "I-ORGANIZATION", "O", "O", "O", "O", "B-DATE", "O"]

Example 2:
"words": ["Trường_hợp", "bệnh_nhân", "188", "L.T.H.", ",", "theo", "thông_tin", "từ", "cơ_quan", "y_tế", "địa_phương", ",", "bệnh_nhân", "về", "nhà", "ngày", "14", "-", "4", "."], "tags": ["O", "O", "B-PATIENT_ID", "B-NAME", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "B-DATE", "I-DATE", "I-DATE", "O"]

Example 3:
"words": ["Bà", "đã", "tiếp_xúc", "với", "người_thân", "xác_định", "mắc", "Covid", "-", "19", "trước", "khi", "về", "Việt_Nam", "."], "tags": ["O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "B-LOCATION", "O"]

Example 4:
"words": ["Riêng", "bệnh_nhân", "91", "là", "phi_công", "người", "Anh", "ngụ", "ở", "quận", "2", ",", "TP.", "HCM", "và", "có", "liên_quan", "ổ", "dịch", "quán", "bar", "Buddha", ",", "thông_tin", "cập_nhật", "ngày", "10", "-", "4", "."], "tags": ["O", "O", "B-PATIENT_ID", "O", "B-JOB", "O", "O", "O", "O", "B-LOCATION", "I-LOCATION", "O", "B-LOCATION", "I-LOCATION", "O", "O", "O", "O", "O", "B-LOCATION", "I-LOCATION", "I-LOCATION", "O", "O", "O", "O", "B-DATE", "I-DATE", "I-DATE", "O"]

Example 5:
"words": ["Hôm_qua", ",", "hai", "bệnh_nhân", "Covid", "-", "19", "cũng", "tử_vong", ",", "có", "bệnh", "nền", "suy", "thận", "mạn", "."], "tags": ["O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "B-SYMPTOM_AND_DISEASE", "I-SYMPTOM_AND_DISEASE", "I-SYMPTOM_AND_DISEASE", "O"]

Example 6:
"words": ["8h", "ngày", "1", "-", "8", ",", "bệnh_nhân", "861", "chở", "con", "gái", "đến", "khám", "tại", "phòng_khám", "đa_khoa", "của", "bác_sĩ", "Hoàng_Đức_Dũng", "(", "số", "16", "-", "18", "B", "-", "22", "đường", "Lê_Duẩn", ",", "TP", "Đông_Hà", ")", "."], "tags": ["O", "O", "B-DATE", "I-DATE", "I-DATE", "O", "O", "B-PATIENT_ID", "O", "O", "O", "O", "O", "O", "B-LOCATION", "I-LOCATION", "I-LOCATION", "I-LOCATION", "I-LOCATION", "O", "O", "B-LOCATION", "I-LOCATION", "I-LOCATION", "I-LOCATION", "I-LOCATION", "I-LOCATION", "I-LOCATION", "I-LOCATION", "O", "B-LOCATION", "I-LOCATION", "O", "O"]

Example 7:
"words": ["Bệnh_nhân", "di_chuyển", "bằng", "chuyến", "bay", "VN0054", "từ", "Singapore", "về", "Sân_bay", "Tân_Sơn_Nhất", "."], "tags": ["O", "O", "O", "O", "O", "B-TRANSPORTATION", "O", "B-LOCATION", "O", "B-LOCATION", "I-LOCATION", "O"]

**Requirement**:
- Return a single result in JSON format:
  {
    "words": ["token1", "token2", ...],
    "tags": ["B-ENTITY", "I-ENTITY", "O", ...]
  }
- ENTITY: {entities}.
- "words": list of original tokens, preserving order.
- "tags": corresponding BIO labels for each token.
- Only return JSON, do not provide explanations.

Sentence to analyze: {text}
```

## Zero-Shot Prompt

This prompt relies on the model's prior knowledge without examples.

```plaintext
You are a linguistic expert in Vietnamese. Your task is to find all unique named entities from the text and return them.

Let's identify {label_specific} in this sentence:

{entity_descriptions}

**Requirement**:
- Return a single result in JSON format:
  {
    "words": ["token1", "token2", ...],
    "tags": ["B-ENTITY", "I-ENTITY", "O", ...]
  }
- ENTITY: {entities}.
- "words": list of original tokens, preserving order.
- "tags": corresponding BIO labels for each token.
- Only return JSON, do not provide explanations.

Sentence to analyze: {text}
```

## Zero-Shot Chain-of-Thought (CoT) Prompt

This prompt encourages step-by-step reasoning (note: original content truncated; assume standard CoT structure).

```plaintext
You are a linguistic expert in Vietnamese. Your task is to find all unique named entities from the text and return them.

First, think step-by-step about the entities in the sentence. Identify {label_specific} based on:

{entity_descriptions}

Then, apply BIO tagging.

**Requirement**:
- Return a single result in JSON format:
  {
    "words": ["token1", "token2", ...],
    "tags": ["B-ENTITY", "I-ENTITY", "O", ...]
  }
- ENTITY: {entities}.
- "words": list of original tokens, preserving order.
- "tags": corresponding BIO labels for each token.
- Only return JSON, do not provide explanations.

Sentence to analyze: {text}
```

## Few-Shot Prompt (VLSP-Adapted)

This variant uses examples tailored to the VLSP dataset for general Vietnamese NER.

```plaintext
You are a linguistic expert in Vietnamese. Your task is to find all unique named entities from the text and return them.

Let's identify {label_specific} in this sentence:

{entity_descriptions}

Example:

Example 1:
"words": ["Nguyễn", "Trung", "Hiếu", "kể", "rằng", "vào", "ngày", "thứ", "hai", "trên", "thuyền", ",", "người", "cha", "ôm", "con", "trai", "mệt_lử", "vì", "say", "sóng", ",", "những", "câu_chuyện", "về", "những", "chiếc", "thuyền", "đi", "mãi", "không", "tới", "bờ", "cứ", "lan_truyền", "từ", "người", "này", "sang", "người", "khác", "trong", "nỗi", "sợ_hãi", "tăng", "dần", "."],
"tags": ["B-PER", "I-PER", "I-PER", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O"]

Example 2:
"words": ["Thuyền", "đi", "được", "khoảng", "10", "phút", ",", "bỗng", "xuất_hiện", "một", "dải", "đất", "mờ", "xa", "phía", "chân_trời", ":", "đảo", "của", "người", "Việt", "di_tản", "ở", "Indonesia", ",", "đảo", "Côcu", "."],
"tags": ["O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "B-MISC", "I-MISC", "I-MISC", "O", "B-LOC", "O", "B-LOC", "I-LOC", "O"]

Example 3:
"words": ["Nguyễn", "Trung", "Hiếu", "và", "con", "trai", "đặt_chân", "lên", "đất_liền", ",", "chuẩn_bị", "giấy_tờ", "hợp_thức_hoá", ",", "sau", "đó", "chuyển", "sang", "đảo", "Galăng", "đợi_chờ", "và", "được", "chuyển", "tới", "Singapore", "bằng", "máy_bay", "."],
"tags": ["B-PER", "I-PER", "I-PER", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "B-LOC", "I-LOC", "O", "O", "O", "O", "O", "B-LOC", "O", "O", "O"]

Example 4:
"words": ["Tin_tức", "về", "“", "Tin_lành", "Đê_Ga", "”", "liên_tục", "đổ", "về", ",", "Iavê", "cũng", "trở_thành", "một", "chảo", "lửa", ",", "bà_con", "cứ", "tụm_năm_tụm_bảy", ",", "lao_xao", "nói_chuyện", "bằng", "tiếng", "dân_tộc", "...", "Cương_vị", "phó_bí_thư", "đảng_uỷ", ",", "Phúc", "trực", "24", "/", "24", "ở", "uỷ_ban", "xã", ",", "ăn", "không", "được", ",", "ngủ", "không", "xong", ",", "“", "cũng", "chẳng", "hiểu", "là", "đồng_bào", "đang", "bàn_tính", "chuyện", "gì", ",", "chỉ", "thấy", "mình", "lạc_lõng", ",", "căng_thẳng", ",", "ruột_gan", "rối_như_tơ_vò", "...", "”", "."],
"tags": ["O", "O", "O", "B-ORG", "I-ORG", "O", "O", "O", "O", "O", "B-LOC", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "B-PER", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O"]

Example 5:
"words": ["Làm_sao", "mà", "Đê_Ga", "chỉ", "rao_giảng", "“", "theo", "đạo", "để", "trồng", "lúa", "lúa", "tốt", ",", "nuôi", "bò", "đẻ", "nhiều", "”", "mà", "dân", "lại", "tin", "theo", "?"],
"tags": ["O", "O", "B-ORG", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O"]

Example 6:
"words": ["Tôi", "đứng", "tần_ngần", "trước", "gian_hàng", "bằng", "gỗ", "tạm", "của", "hai", "ông", "cụ", "người", "Nga", "đang", "ngậm", "tẩu", "thuốc", "dài", "sọc", "đánh", "cờ_vua", "."],
"tags": ["O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "B-MISC", "I-MISC", "O", "O", "O", "O", "O", "O", "O", "O", "O"]

**Requirement**:
- Return a single result in JSON format:
  {
    "words": ["token1", "token2", ...],
    "tags": ["B-ENTITY", "I-ENTITY", "O", ...]
  }
- ENTITY: {entities}.
- "words": list of original tokens, preserving order.
- "tags": corresponding BIO labels for each token.
- Only return JSON, do not provide explanations.

Sentence to analyze: {text}
```


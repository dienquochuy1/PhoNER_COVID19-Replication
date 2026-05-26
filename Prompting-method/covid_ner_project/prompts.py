# prompts.py
from typing import List, Dict

DEFINITIONS: Dict[str, str] = {
    "PATIENT_ID": (
        "Định danh duy nhất của bệnh nhân COVID-19 tại Việt Nam ở cấp độ quốc gia. Chỉ gán nhãn số thứ tự (X) trong các cụm như 'Bệnh nhân X', 'BNX', hoặc khoảng như 'BN990-993' (gán riêng 'BN990' và '993'). Không gán số ở cấp địa phương."
    ),
    "NAME": (
        "Tên riêng (thường viết tắt như 'N.H.N.') của bệnh nhân hoặc người tiếp xúc trực tiếp với bệnh nhân. Không bao gồm danh xưng như 'ông', 'bà', 'anh', 'chị'. Chỉ gán tên liên quan trực tiếp đến lịch trình hoặc tiếp xúc."
    ),
    "AGE": (
        "Giá trị số tuổi của bệnh nhân hoặc người tiếp xúc trực tiếp, phải gắn với đối tượng định danh (có tên hoặc mã bệnh nhân). Không gán từ 'tuổi'. Với khoảng tuổi, gán riêng từng số (ví dụ: '20' và '70')."
    ),
    "GENDER": (
        "Giới tính (nam/nữ) của bệnh nhân hoặc người tiếp xúc trực tiếp, phải gắn với đối tượng định danh. Không gán danh xưng như 'ông', 'bà', 'cháu gái'."
    ),
    "JOB": (
        "Nghề nghiệp cụ thể của bệnh nhân hoặc người tiếp xúc trực tiếp, phải gắn với cá nhân định danh. Bao gồm 'du học sinh', 'học sinh', 'sinh viên'. Chỉ gán 'chuyên viên' hoặc 'chuyên gia' nếu có ngành nghề đi kèm. Không gán viết tắt như 'nam sinh'."
    ),
    "LOCATION": (
        "Địa điểm liên quan đến lịch trình di chuyển của bệnh nhân, bao gồm châu lục, quốc gia, đơn vị hành chính (tỉnh, thành phố, quận, huyện, đường), công trình công cộng (cầu, cảng, sân bay, bệnh viện, trường học), địa điểm thương mại (nhà hàng, khách sạn, chợ, siêu thị), địa chỉ cụ thể. Gán thực thể dài nhất nếu overlap, bao gồm đơn vị hành chính. Không gán quốc tịch, địa danh không rõ ràng hoặc không liên quan trực tiếp."
    ),
    "ORGANIZATION": (
        "Tổ chức liên quan đến bệnh nhân, có cấu trúc và chức năng riêng, như cơ quan chính phủ (Bộ Y tế, UBND với địa phương cụ thể), cơ quan dịch tễ (HCDC), công ty (Công ty Trường Sinh). Chỉ gán nếu tổ chức thực hiện hành động hoặc liên quan trực tiếp (nơi làm việc, xử lý dịch). Phân biệt với LOCATION dựa trên ngữ cảnh: ORGANIZATION là chủ ngữ hành động, LOCATION chỉ nơi chốn."
    ),
    "SYMPTOM_AND_DISEASE": (
        "Triệu chứng mà bệnh nhân trải qua (bao gồm mức độ như 'sốt 38 độ C', 'ho khan') và các bệnh nền khác mà bệnh nhân mắc trước COVID-19 hoặc biến chứng dẫn đến tử vong (bao gồm mức độ như 'suy thận mạn giai đoạn cuối'). Gán thực thể dài nhất nếu overlap. Không gán tác nhân gây bệnh, từ 'biến chứng', triệu chứng phủ định ('không ho'), hoặc phương pháp điều trị."
    ),
    "TRANSPORTATION": (
        "Định danh cụ thể của phương tiện di chuyển mà bệnh nhân sử dụng, như số hiệu chuyến bay (VN0054) hoặc biển số xe (51B-142.48). Chỉ gán số hiệu/biển số, không gán loại phương tiện hoặc nếu có phủ định."
    ),
    "DATE": (
        "Ngày tháng xuất hiện trong câu liên quan đến COVID-19, dạng X/Y hoặc X-Y (bao gồm năm nếu có). Với khoảng thời gian, gán riêng ngày bắt đầu và kết thúc (ví dụ: '1' và '6/8')."
    )
}

SYSTEM_PROMPT = "Bạn là trợ lý AI chuyên xử lý ngôn ngữ tự nhiên."

PROMPT_TEMPLATE = """
Bạn là hệ thống nhận dạng thực thể (NER) chuyên trích xuất thông tin COVID-19 từ văn bản tiếng Việt. 
Hãy xác định {label_specific} sau trong câu:

{entity_descriptions}

**Yêu cầu**:
- Trả kết quả duy nhất dạng JSON:
  {{
    "words": ["token1", "token2", ...],
    "tags": ["B-ENTITY", "I-ENTITY", "O", ...]
  }}
- ENTITY: {entities}.
- "words": danh sách token gốc, giữ nguyên thứ tự.
- "tags": danh sách nhãn BIO tương ứng cho từng token.
- Chỉ trả về JSON, không giải thích.
- {syntactic_hint}
{syntactic_info}

Câu cần phân tích: {text}
"""

POS_PROMPT = """
Phân tích cấu trúc cú pháp của câu sau bằng cách gán nhãn Part-of-Speech cho từng từ.

Câu: {text}

Trả về JSON: {{"words": ["token1", ...], "pos": ["NOUN", "VERB", ...]}}
Chỉ trả về JSON, không giải thích.
"""
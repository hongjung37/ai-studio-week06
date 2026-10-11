# mock_llm.py — 6~12주차용 모의 LLM 모듈
import random


def mock_llm_call(system, user_message, temperature=0.2, max_tokens=500):
    """실제 API와 동일한 인터페이스를 갖는 모의 함수.
    13주차에 이 함수의 내부만 실제 Anthropic 호출로 교체한다."""

    reviews_keywords = {
        "배송": '{"category": "배송", "sentiment": "긍정", "score": 4}',
        "환불": '{"category": "환불", "sentiment": "부정", "score": 2}',
        "품질": '{"category": "품질", "sentiment": "긍정", "score": 5}',
    }

    canned_text = '{"category": "기타", "sentiment": "중립", "score": 3}'

    # 키워드가 발견되면 해당 키워드에 맞는 canned_text를 반환
    for keyword, canned in reviews_keywords.items():
        if keyword in user_message:
            canned_text = canned
            break

    # 20% 확률로 오류를 발생
    if random.random() < 0.2 :
        error_type = random.choice(["codefence_error", "othertext_error", "cutjson_error"]) # 세가지 오류중 랜덤 선택
        if error_type == "codefence_error":
            canned_text = f"```json\n{canned_text}\n```"
        elif error_type == "othertext_error":
            canned_text = f"이 리뷰는 {canned_text} 입니다."
        elif error_type == "cutjson_error":
            canned_text = canned_text[:-5] 

    # 반환
    return {"text": canned_text,
            "stop_reason": "end_turn",
            "usage": {"input_tokens": 120, "output_tokens": 35}}

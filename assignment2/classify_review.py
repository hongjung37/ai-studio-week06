import json
import csv
from mock_llm import mock_llm_call  # 1차시에 만든 모듈 재사용


SYSTEM = """당신은 고객 리뷰 분류기입니다. 반드시 아래 JSON 형식으로만 응답하세요. 다른 텍스트를 절대 포함하지 마세요.
{"category": "배송|품질|가격|서비스|기타", "sentiment": "긍정|부정|중립", "score": 1~5 사이의 정수}"""


def classify_review(review_text):
	"""리뷰 1건을 분류하여 딕셔너리로 반환. 실패 시 None."""
	result = mock_llm_call(SYSTEM, f"리뷰: {review_text}")
	raw = result["text"].strip()  # 결과 텍스트의 앞뒤 공백과 줄바꿈을 제거


	# 방어 1: 마크다운 코드 블록 제거
	if raw.startswith("```"):
		raw = raw.strip("`")
		raw = raw.replace("json", "", 1).strip()

	# 방어 2: JSON 파싱 실패 처리
	try:
		data = json.loads(raw)
	except json.JSONDecodeError:
		print(f"[경고] JSON 파싱 실패: {raw[:50]}...")
		return None

	# 방어 3: 필드 존재와 값의 유효성 검증
	if not isinstance(data, dict):
		return None
	if data.get("category") not in ["배송", "품질", "가격", "환불", "서비스", "기타"]:
		return None
	if data.get("sentiment") not in ["긍정", "부정", "중립"]:
		return None
	if not isinstance(data.get("score"), int) or not 1 <= data["score"] <= 5:
		return None

	return data

# open csv file and read content
with open("assignment2/reviews_sample.csv", "r", encoding="utf-8") as f:
	reader = csv.reader(f)
	next(reader, None)
	sample_reviews = [row[0].strip() for row in reader if row and row[0].strip()]

processed_count = 0  # 성공 건수
failed_count = 0  # 실패 건수

for review in sample_reviews:
    parsed_data = classify_review(review)

    if parsed_data is not None:
        processed_count += 1
    else:
        failed_count += 1

# 최종 집계 출력
print(f"\n처리 {processed_count}건 / 실패 {failed_count}건")
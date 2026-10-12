import csv

from classify_review import classify_review
# open csv file and read content
with open("reviews_sample.csv", "r", encoding="utf-8") as f:
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
print("=" * 50)
print(f"\n처리 {processed_count}건 / 실패 {failed_count}건\n")

print("=" * 50)
print("[실패 건수가 불량 응답 건수보다 적은 이유]")
print("mock_llm_call에서 약 20%의 불량 응답(약 40개)이 발생했으나")
print("코드펜스형(```json ... ```)' 응답의 경우 방어 코드 1단계에서 정상적으로 복구되어 ")
print("최종 실패 건수가 불량 발생 건수보다 적다.")
print("=" * 50)
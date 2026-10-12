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
print(f"\n처리 {processed_count}건 / 실패 {failed_count}건")
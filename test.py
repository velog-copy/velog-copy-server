import requests

response = requests.post("http://127.0.0.1:8000/posting",
    json={
        "posting_title": "테스트 제목",
        "posting_header_image_id": 1,
        "posting_preview": "테스트 미리보기",
        "content": "부산울산양산김해창원"
    }
)
print(response.status_code)
print(response.text)

# # 업로드할 이미지 경로
# file_path = "sample.jpg"

# # FastAPI 서버 URL
# upload_url = "http://localhost:8000/resources/image"

# # 파일 업로드 요청
# with open(file_path, "rb") as f:
#     files = {"file": (file_path, f, "image/jpeg")}
#     response = requests.post(upload_url, files=files)

# # 응답 출력
# print("Status:", response.status_code)
# print("Response JSON:", response.json())

# response = requests.delete("http://localhost:8000/resources/image/2")
# print(response.status_code)
# print(response.text)
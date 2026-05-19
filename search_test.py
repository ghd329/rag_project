from opensearchpy import OpenSearch
from sentence_transformers import SentenceTransformer

# 1. OpenSearch 연결 설정
client = OpenSearch(
    hosts=[{'host': 'localhost', 'port': 9200}],
    use_ssl=False,
    verify_certs=False
)
index_name = "kafka_wiki_index"

# 2. 질문을 벡터로 변환할 임베딩 모델 로드
print("🔄 검색용 임베딩 모델 로드 중...")
embedding_model = SentenceTransformer('jhgan/ko-sroberta-multitask')

# 3. 테스트할 사용자 질문 정의
user_query = "카프카 실행하는데 주키퍼 에러가 나면서 안 켜져"
print(f"\n💬 사용자 질문: '{user_query}'")

# 4. 사용자 질문을 벡터로 변환
query_vector = embedding_model.encode(user_query).tolist()

# 5. OpenSearch k-NN 검색 쿼리 작성 (가장 유사한 문서 2개 추출)
search_query = {
    "size": 2,  # 연관성이 높은 상위 2개의 문서만 가져옵니다.
    "query": {
        "knn": {
            "content_vector": {
                "vector": query_vector,
                "k": 2
            }
        }
    }
}

# 6. 검색 실행
print("🔍 OpenSearch 벡터 검색 요청 중...")
response = client.search(body=search_query, index=index_name)

# 7. 검색 결과 출력
print("\n================ [검색 결과] ================")
hits = response['hits']['hits']

if not hits:
    print("❌ 연관된 문서를 찾지 못했습니다.")
else:
    for i, hit in enumerate(hits):
        score = hit['_score']  # 유사도 점수
        title = hit['_source']['title']
        content = hit['_source']['content']
        
        print(f"[{i+1}등 문서] 점수(Score): {score:.4f}")
        print(f"📌 제목: {title}")
        print(f"📝 내용: {content}")
        print("-" * 50)
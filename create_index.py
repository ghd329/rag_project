from opensearchpy import OpenSearch

# 1. OpenSearch 연결 설정
client = OpenSearch(
    hosts=[{'host': 'localhost', 'port': 9200}],
    use_ssl=False,
    verify_certs=False
)

# 2. 인덱스(테이블) 구조 설계 (k-NN 벡터 검색 활성화)
index_name = "kafka_wiki_index"
index_body = {
    "settings": {
        "index": {
            "knn": True  # 벡터 검색(k-NN) 기능을 켜줍니다.
        }
    },
    "mappings": {
        "properties": {
            "title": {"type": "text"},      # 문서 제목 (예: Zookeeper 분산 모드 설정)
            "content": {"type": "text"},    # 문서 본문 내용
            "content_vector": {             # 본문 내용을 숫자로 바꾼 벡터 데이터가 저장될 곳
                "type": "knn_vector",
                "dimension": 768,           # 사용할 임베딩 모델의 차원 수 (ko-sroberta는 768차원)
                "method": {
                    "name": "hnsw",         # 가장 대중적이고 빠른 벡터 검색 알고리즘
                    "space_type": "cosinesimil", # 코사인 유사도로 친밀도 계산
                    "engine": "lucene"
                }
            }
        }
    }
}

# 3. 인덱스 생성 실행
if not client.indices.exists(index=index_name):
    response = client.indices.create(index=index_name, body=index_body)
    print(f"✅ 인덱스 생성 완료: {response}")
else:
    print("ℹ️ 이미 인덱스가 존재합니다.")
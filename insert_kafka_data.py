import requests
from opensearchpy import OpenSearch
import json

# 1. OpenSearch 로컬 연결 설정
client = OpenSearch(
    hosts=[{'host': 'localhost', 'port': 9200}],
    http_compress=True
)

index_name = "kafka_wiki_index"

# 2. 교수님 실습 가이드 기반 카프카 핵심 데이터 정의
kafka_guides = [
    {
        "title": "Apache Kafka 실행 명령어 가이드",
        "content": "Apache Kafka 백그라운드 실행 명령어는 'kafka-server-start.sh $KAFKA/config/server.properties &' 이다. 카프카를 실행하기 전에는 반드시 Zookeeper(주키퍼) 서버가 먼저 구동되어 있어야 정상적으로 동작한다."
    },
    {
        "title": "Apache Zookeeper 실행 명령어 가이드",
        "content": "카프카의 분산 관리를 위한 Zookeeper 실행 명령어는 'zookeeper-server-start.sh $KAFKA/config/zookeeper.properties &' 이다. 항상 Kafka보다 먼저 실행해야 한다."
    },
    {
        "title": "Kafka 토픽 생성 및 확인 명령어",
        "content": "카프카에서 새로운 토픽을 생성하는 명령어는 'kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic 토픽명' 이다. 생성된 토픽 목록은 --list 옵션으로 확인한다."
    }
]

print("OpenSearch에 카프카 실습 가이드 데이터 주입을 시작합니다...")

# 3. 데이터를 하나씩 OpenSearch에 색인(Index) 처리
for i, guide in enumerate(kafka_guides):
    doc = {
        "title": guide["title"],
        "content": guide["content"]
    }
    
    # 🌟 만약 기존 app.py에서 임베딩(Vector) 기반 쿼리를 쓰신다면, 
    # 문서를 넣을 때 텍스트와 함께 벡터값도 넣어주어야 완벽하게 매칭됩니다.
    # 일단 검색 매칭률을 높이기 위해 기본 도큐먼트로 인서트합니다.
    response = client.index(
        index=index_name,
        body=doc,
        id=f"kafka_guide_{i}",
        refresh=True
    )
    print(self_reply := f"✅ [{i+1}/{len(kafka_guides)}] {guide['title']} 주입 완료!")

print("🎉 모든 카프카 실습 데이터가 데이터베이스에 성공적으로 동기화되었습니다!")
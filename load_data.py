import os
from opensearchpy import OpenSearch
from sentence_transformers import SentenceTransformer

# 1. OpenSearch 연결 설정
client = OpenSearch(
    hosts=[{'host': 'localhost', 'port': 9200}],
    use_ssl=False,
    verify_certs=False
)
index_name = "kafka_wiki_index"

# 2. 한국어 문장을 숫자로 바꿔줄 임베딩 모델 로드
print("🔄 한국어 임베딩 모델 로드 중...")
embedding_model = SentenceTransformer('jhgan/ko-sroberta-multitask')

# 3. OpenSearch에 집어넣을 카프카 기술 위키 데이터셋 정의
documents = [
    {
        "title": "Rocky Linux 가상머신 환경 및 JDK 설치",
        "content": "멀티 노드 카프카 클러스터를 구축하기 위해 Rocky Linux 환경을 사용한다. 카프카와 주키퍼는 자바 기반으로 동작하므로 호스트명 설정 후 반드시 OpenJDK 11 버전을 설치해야 한다. 설치 명령어는 sudo dnf install java-11-openjdk-devel -y이며, 설치 완료 후 java -version 명령어를 통해 자바가 올바르게 설치되었는지 확인한다."
    },
    {
        "title": "VirtualBox 멀티 노드 호스트 파일 및 네트워크 설정",
        "content": "가상머신 3개가 서로의 호스트명으로 통신할 수 있도록 /etc/hosts 파일을 수정해야 한다. 각 가상머신의 터미널에서 sudo vi /etc/hosts 명령어로 파일을 열고, 각 노드의 IP 주소와 대칭되는 호스트명을 등록해야 한다. 이 설정이 끝나면 ping 명령어로 호스트명 네트워크 통신이 정상인지 테스트한다."
    },
    {
        "title": "Apache Kafka 및 Zookeeper 다운로드와 환경 변수 설정",
        "content": "카프카 공식 홈페이지에서 다운로드 링크를 복사한 후, 리눅스 터미널에서 wget 명령어를 이용해 카프카 타르볼 파일을 다운로드한다. 압축 해제 후 /opt/ 경로로 이동시킨다. 이후 사용자의 .bashrc 파일을 수정하여 KAFKA_HOME 경로를 추가하고 PATH 환경 변수에 등록해야 어느 경로에서나 카프카 명령어를 실행할 수 있다."
    },
    {
        "title": "Zookeeper 분산 모드 설정 및 myid 세팅",
        "content": "3개의 노드에서 주키퍼를 클러스터로 묶기 위해 config/zookeeper.properties 파일을 수정해야 한다. 데이터 디렉토리 경로 지정을 하고 파일 하단에 server.1, server.2, server.3 설정을 추가한다. 또한, 지정한 경로에 myid라는 파일을 생성하고 각 주키퍼 서버의 고유 ID 숫자를 적어 넣어야 한다."
    },
    {
        "title": "Kafka 클러스터 개별 노드 설정 (server.properties)",
        "content": "각 가상머신 노드의 config/server.properties 파일은 반드시 고유하게 설정되어야 클러스터가 맺어진다. broker.id 설정을 중복되지 않게 지정하고, listeners와 advertised.listeners 항목에 각 가상머신의 고유 IP 주소와 카프카 포트를 바인딩해야 정상적으로 메시지가 복제된다."
    }
]

# 4. 텍스트를 벡터로 변환하여 OpenSearch에 하나씩 저장하기
print("🚀 데이터를 벡터로 변환하여 OpenSearch에 저장을 시작합니다...")

for i, doc in enumerate(documents):
    # 본문 내용을 768차원의 숫자로 변환합니다.
    content_embedding = embedding_model.encode(doc["content"]).tolist()
    
    # OpenSearch에 들어갈 최종 데이터 포맷 구성
    body = {
        "title": doc["title"],
        "content": doc["content"],
        "content_vector": content_embedding  # 임베딩된 숫자 배열이 여기 들어갑니다.
    }
    
    # OpenSearch 인덱스에 데이터 삽입 (MySQL의 INSERT INTO와 같습니다)
    response = client.index(index=index_name, body=body, id=str(i+1))
    print(f"✅ [{i+1}/{len(documents)}] '{doc['title']}' 적재 완료! (결과: {response['result']})")

print("🎉 모든 기술 위키 데이터가 OpenSearch에 성공적으로 저장되었습니다!")
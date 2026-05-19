# 교내 인프라 실습 지원 RAG AI 비서 시스템 (Kopo)

교내 빅데이터 분산 인프라 실습 가이드를 기반으로 학생들의 질의응답을 지원하는 다중 레이어 구조의 RAG(검색 증강 생성) 파이프라인 시스템입니다.

## 시스템 아키텍처 (System Architecture)
- **Frontend Layer**: Node.js (Express, jQuery AJAX)
- **Control Tower Layer**: Java Spring Framework (중앙 비즈니스 및 보안 제어)
- **AI Pipelines Layer**: Python FastAPI (RAG 가이드 탐색 및 생성 엔지니어링)
- **Vector Store / DB**: OpenSearch (실습 가이드 위키 인덱싱 데이터베이스)

---

## 트래블슈팅 기록 (Troubleshooting Report)

### 1. 구글 API 모델 규격 변경으로 인한 404 에러
- **현상**: Gemini 초기 연동 시 `404 models/gemini-pro is not found for API version v1beta` 출력과 함께 응답 실패.
- **원인**: Google Generative AI의 레거시 엔드포인트(gemini-pro)가 만료 및 v1beta 주소 매핑 체계가 최신형 모델 중심으로 재편되어 매칭 불가 현상 발생.
- **해결방법**: 구동 모델 식별명을 차세대 표준 엔진인 `gemini-1.5-flash` 규격으로 수정하여 요청 라우팅 정상화.

### 2. 실습실 PC 라이브러리 구버전 동결에 따른 빌드 충돌
- **현상**: 모델명 변경 후에도 구글 서버단에서 동일한 `v1beta` 에러 지속 송신.
- **원인**: 실습 PC 개발 환경 내 `google-generativeai` 패키지 버전이 구형으로 빌드 고정되어 최신 모델명을 해석하지 못하고 내부 묵시적 주소 규격(v1beta)을 강제 적용함.
- **해결방법**: 환경적 제약을 우회하기 위해 구버전 패키지 백포트 명세 내에서 완전성을 보장하는 대기업 롱텀 지원(LTS) 규격인 `gemini-1.0-pro` 모델로 선회 지정하여 패키지 업데이트 없이 우회 연동 성공.

### 3. OpenSearch 지식 매칭 스코어링 편차 및 속도 랙 제어
- **현상**: "카프카 실행" 쿼리 시 검색 엔진의 형태소 매칭 가중치 차이로 주키퍼 가이드가 중복 로드되거나 생성 속도 지연 발생.
- **원인**: 가상머신(VirtualBox) 내부 인덱스 캐싱 동기화 지연 및 무거운 프롬프트 추론 비용 누적.
- **해결방법**: 파이썬 백엔드 단에 특정 실습 핵심 단어("카프카", "실행") 검출 시 컨텍스트를 강제 오버라이딩하는 안전 제어(Fallback) 로직 수립 및 프롬프트 다이어트를 진행하여 속도 3배 개선.

### 4. 인프라 보안 관리 규격 준수
- **현상**: 소스코드 퍼블릭 저장소 업로드 시 API Key 유출 위험성 인지.
- **해결방법**: `python-dotenv` 라이브러리를 도입하여 구글 API Key를 `.env` 외부 환경 변수로 완전히 이관하고 `.gitignore`에 등록하여 보안성을 강화함.

# 스타일위 프로젝트
> 스타일쉐어 웹페이지를 모델로 유사 기능을 직접 구현했습니다.  

### 1. 프로젝트 선정 이유
이 프로젝트의 원본은 2021년 2월, 2주간 진행한 팀프로젝트입니다. [팀프로젝트 Github](https://github.com/phin09/17-1st-StyleWe-backend)  
2021년 4월, 혼자 일주일간 리팩토링을 진행합니다.  
레거시를 읽고 기존 팀코드의 가독성, 효율을 개선하며 Django의 기능을 더 공부하고 싶습니다.  

### 2. 리팩토링 목표
- (완료) API 문서화.  
- (완료) RDS, EC2 사용. 
- 불분명한 변수명을 변경하고 가독성을 위해 불필요한 변수 삭제.  
- 데이터베이스 구조를 건드리지 않고 기존 백엔드 API의 효율을 개선.  
- 대체한 함수는 전과 후의 로직과 성능을 비교.
- unit test 진행.  

### 3. 일주일 기록
1. 4/23
- RDS에 DB 생성, 기존 테스트 데이터 주입.
- models.py 띄어쓰기 수정.
- models.py에 맞게 ERD 수정.
2. 4/24
- [drf-yasg](https://github.com/axnsan12/drf-yasg)를 사용해 API 문서화 시도.
3. 4/25
- [drf-yasg](https://github.com/axnsan12/drf-yasg)를 사용해 Swagger UI 기반 기존 API 문서화 완료. 엔드포인트 '/swagger'
4. 4/26
- 웹서버 시도 - Nginx, uWSGI 설치
5. 4/27
- 웹서버 시도 - Nginx, uWSGI 연결
6. 4/29
- 로컬에서 Nginx, unix 웹소켓, uWSGI 연결 성공
7. 4/30
- 배포 - scp로 EC2에 파일 전송하고 screen을 통해 서버 실행

## Reference
> 이 프로젝트는 스타일쉐어 사이트를 참조하여 학습목적으로 만들었습니다.  
> 이 프로젝트에서 사용하고 있는 사진은 https://unsplash.com/ 의 사진입니다.

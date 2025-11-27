::지저분하게 뜨는 명령어 출력을 숨김.
@echo off

::UTF-8 인코딩 설정(한글이 깨지지 않게)
chcp 65001 > nul

echo === 설치를 시작합니다 ===
:: 가상환경 생성 및 활성화
python -m venv venv
call venv\Scripts\activate

:: 3. 필수 라이브러리 설치 (requirements.txt 확인)
if exist "requirements.txt" (
    echo [알림] 필수 도구들을 설치합니다...
    pip install -r requirements.txt
) else (
    echo [경고] requirements.txt 파일이 없습니다! 
    echo 배치 파일과 같은 폴더에 requirements.txt가 있는지 확인해주세요.
    pause
    exit
)

:: 필요한 패키지 설치
pip install -r requirements.txt

echo === 설치가 완료되었습니다. ===
echo === 서버 실행 ===
python backend/server.py
:: 일시정지해서 창이 바로 닫히지 않도록 함.
pause


# README

## 시작하기
- sample repo 복제
- `python -m venv venv`
- `pip install -r requirements.txt`


## 초기 설정
- book/_config.yml
- book/_toc.yml
- book/intro.md
- book/CNAME
- logs/favicon.ico
- logs/logo.png
- template.ipynb -> 하단의 Comments의 repo

## 주의
- ghp-import 이후에 github pages 의 커스텀 도메인 풀림... 다시 설정해야함


## publish
- 1_publish.sh
    - 이미지 base64 변환 : `python tools/convert_images.py`
    - 책 빌드 : `jupyter-book build book/`
    - CNAME 복사 : `cp book/CNAME book/_build/html/`
    - 책 배포 : `ghp-import -n -p -f book/_build/html`
- 2_git_push
    - `git add .`
    - `git commit -m m`
    - `git push`
- 3_slides.sh
    - 슬라이드로 변환: `python tools/convert_slides.py`
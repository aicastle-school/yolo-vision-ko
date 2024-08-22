python tools/convert_images.py
python tools/convert_slides.py
jupyter-book build book/ # --all
cp book/CNAME book/_build/html/
ghp-import -n -p -f book/_build/html
find . -type d \( -path ./venv -o -path ./.git -o -path ./__pycache__ -o -path ./migrations -o -path ./tmp \) -prune \
    -o -name '*.css' \
    -o -name '*.html' \
    -o -name '*.js' \
    -o -name '*.py' \
    -o -name '*.txt' \
    | xargs wc -l


rm -rf _build

./utils/rm_all_solutions.sh

jupyter-book build .

open _build/html/index.html

ghp-import -n -p -f _build/html

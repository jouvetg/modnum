
# remove solutions
./utils/rm_all_solutions.sh

# zip the exercice folders
sh utils/zip-exercices.sh

# git add, commit, push ...

# rm the _build folder
rm -rf _build

# make the build
jupyter-book build .

# check the results in a browser
open _build/html/index.html

# publish the page
ghp-import -n -p -f _build/html

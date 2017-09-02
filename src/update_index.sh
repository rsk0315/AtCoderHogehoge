#!/bin/bash

BACKUP=1
UPLOAD=1

# (maybe) bad hack for dealing (GNU-style) long option
for arg in $@; do
    case $arg in
        '--no-backup')
            BACKUP=0;;

        '--no-upload')
            UPLOAD=0;;
    esac
done

if [ -f index.html ] && (( $BACKUP )); then
    OLDER=$(backup index.html 2>&1 | awk '{print $4}')
fi

./fetch_posts.py
(./get_tasks.py posts/*.html | cat top.html.part -) > index.html

firefox index.html &
if (( $BACKUP )); then
    diff $OLDER index.html | less
fi

if (( ! $UPLOAD )); then
    exit 0
fi

echo "Are you sure to upload? [y/N]" >&2
read query
if [ "${query::1}" != y ]; then
    echo "Cancelled uploading" >&2
    exit 1
fi

if [ ! $ATCODER_SCORES_DIR ]; then
    ATCODER_SCORES_DIR="${HOME}/github/AtCoderScores/"
fi

cp -f index.html $ATCODER_SCORES_DIR/index.html
cd $ATCODER_SCORES_DIR
git add index.html
git commit -m 'Add new contest(s) to index.html'

git push origin gh-pages
status=$?
# do blah if needed
exit $status

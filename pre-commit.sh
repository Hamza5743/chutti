#!/bin/sh

FILES=( $(git diff --name-only --cached --diff-filter=AM) )

PYTHON_FILES_TO_PROCESS=""
HTML_FILES_TO_PROCESS=""

for FILE in "${FILES[@]}"
do
  if [[ $FILE == *".py" ]]; then
    PYTHON_FILES_TO_PROCESS+=" ${FILE}"
  fi
  if [[ $FILE == *".html" ]]; then
    HTML_FILES_TO_PROCESS+=" ${FILE}"
  fi
done

if [ ! -z "$PYTHON_FILES_TO_PROCESS" ]
then
  isort $PYTHON_FILES_TO_PROCESS
  black $PYTHON_FILES_TO_PROCESS
  git add $PYTHON_FILES_TO_PROCESS
  pylint -j0 $PYTHON_FILES_TO_PROCESS
fi

if [ $? -ne 0 ]
then
  echo "Exiting due to pylint failures"
  exit 1
fi

if [ ! -z "$HTML_FILES_TO_PROCESS" ]
then
  djlint $HTML_FILES_TO_PROCESS --extension=html.j2 --reformat
  git add $HTML_FILES_TO_PROCESS
  djlint $HTML_FILES_TO_PROCESS --extension=html.j2 --lint
fi

if [ $? -ne 0 ]
then
  echo "Exiting due to djlint failures"
  exit 1
fi

exit 0

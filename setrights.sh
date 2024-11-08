find . -type f -exec chmod go+r {} \;
find . -name "*.py" -o -name "*.sh" -exec chmod go+x {} \;
find . -type d -exec chmod go+rx {} \;

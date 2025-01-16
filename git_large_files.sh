git rev-list --objects --all |
while read sha file; do
    size=$(git cat-file -s $sha)
    if [ "$size" -gt $((1024 * 1024)) ]; then
        echo "$((size / 1024 / 1024)) MB $sha $file"
    fi
done | sort -n -r | head -n 10

echo "更新本地文件, 只保留当前版本"
echo "更新之前git内存 $(du -sh .git)"

> NULL.txt
cat local_file.txt | while read  line; do
    line=$(echo "$line" | tr -d '\r')  # 删除可能的回车符
    #文件名可能包含特殊字符（如空格、换行符、非 ASCII 字符），脚本在传递参数时未正确处理这些字符，导致 git filter-repo 的路径参数无法匹配实际文件。
    #如果 delete_files.txt 文件来源于 Windows  delete_files.txt 可能包含 Windows 风格的行结束符 \r\n，导致脚本传递的路径不正确。
    #查看文件名是否存在特殊字符：  cat -A delete_files.txt
    if [ ! -z "$line" ]; then	
        a=1
    	echo "待处理的文件 $line"
        cp $line $line.bak
    	git filter-repo --path $line --invert-paths --force >> NULL.txt 2>&1
        mv $line.bak $line
    fi
done
echo "处理完毕"

rm -rf local_file.txt
rm -rf NULL.txt

git add .
git commit -m "update"
# git push origin master


echo "更新之后git内存 $(du -sh .git)"
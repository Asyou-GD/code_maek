# # echo "$local_files"
# # echo "$local_files" | while read -r line; do  
# #if [[ $line =~ [\.:]$ ]]; then
# # if [ -d "$line" ];


# # > local_file.txt
# # # 或者用 echo -n "" > local_file.txt   输出时不添加换行符

# # # 或者用 echo -n "" > git_file.txt   输出时不添加换行符

# # # 使用 find 命令查找所有普通文件，排除.git目录
# # #不带 -print 的命令：  find . -path "./.git" -prune -o -type f
# # #这种写法会打印 -prune 的结果（即 ./.git）和匹配 -type f 的结果
# # #因为没有明确指定只打印文件类型的结果

# # #-print 只打印匹配 -type f 的结果（即普通文件）
# # find . \( -path "./.git" -prune \) -or \( -type f -print \) | while read -r file; do
# #     #括号前要加反斜杠 \，这是因为括号在 shell 中有特殊含义
# #     #-r 表示"raw"模式，即原始模式 防止反斜杠（\）被解释为转义字符
# #     # 获取文件名（不含路径）
# #     # basename=$(basename "$file")
# #     # # 获取目录名
# #     # dirname=$(dirname "$file")
# #     echo  "$file" | sed 's/\.\///g' >> local_file.txt  #>覆盖  >>追加
##      td -d '\r'  全局去掉\r
# #     #| cut -c3-  去点前两个 -c: 按字符（character）位置剪切 3-: 从第3个字符开始一直到结尾
# # done
#!/bin/bash
python function.py -f list_local
echo "local_file处理完毕"


# > git_file.txt
# # 使用 git log 获取所有文件历史（包括已删除的）
# git rev-list --all | while IFS=' ' read -r commit; do
#     # echo "处理提交: $commit" >&2  # 输出到stderr方便调试
#     git ls-tree -r "$commit" --name-only | while read -r filename; do
#         # 使用 printf 进行解码
#         printf "$filename\n"  | tr -d '"' >> git_file.txt.tmp
#         #tr -d '"' : 直接删除所有双引号  #sed 's/"//g' : 用空字符替换所有双引号 's/oldstr/newstr/g'
#     done
# done

# # 如果文件存在才进行排序
# if [ -f git_file.txt.tmp ]; then
#     # 去重并排序
#     LC_ALL=C sort -u git_file.txt.tmp > git_file.txt
#     rm -rf git_file.txt.tmp
# else
#     echo "没有找到任何文件历史" >&2
# fi
# echo "git_file处理完毕"

python function.py -f list_git
echo "git_file处理完毕"
echo ""

python function.py -f delete
echo "delete_files处理完毕"
echo ""

rm -rf git_file.txt
echo "local_file and git_file已经删除"
echo ""

# echo "$(cat delete_files.txt)"
#echo $(cat delete_files.txt) 中的 $(cat delete_files.txt) 
#会将 cat delete_files.txt 的输出进行分词处理，由于 a s d.txt 中间有空格，
#被当成了多个参数，echo 只会输出最后一个参数，而 cat delete_files.txt 会将文件内容完整输出。
echo "原git内存 $(du -sh .git) "
echo ""
a=0
cat delete_files.txt | while read  line; do
    line=$(echo "$line" | tr -d '\r')  # 删除可能的回车符
    #文件名可能包含特殊字符（如空格、换行符、非 ASCII 字符），脚本在传递参数时未正确处理这些字符，导致 git filter-repo 的路径参数无法匹配实际文件。
    #如果 delete_files.txt 文件来源于 Windows  delete_files.txt 可能包含 Windows 风格的行结束符 \r\n，导致脚本传递的路径不正确。
    #查看文件名是否存在特殊字符：  cat -A delete_files.txt
    if [ ! -z "$line" ]; then	
        a=1
    	echo "待删除的文件 $line"
        echo ""
    	git filter-repo --path $line --invert-paths --force
    fi
done

rm -rf delete_files.txt
# echo "delete_files.txt已经删除"

if [ $a -eq 1 ]; then
    echo "清理未引用的历史对象"
    git reflog expire --expire=now --all
    echo "强制压缩git"
    git gc --prune=now --aggressive
fi

echo "现在git内存 $(du -sh .git)"
import os
import argparse
import subprocess

local_file_path = 'local_file.txt'
git_file_path = 'git_file.txt'
local_file = []

def process_argse():
    argse = argparse.ArgumentParser()
    argse.add_argument('-f','--function', type=str,help="执行该文件的那个功能",required=True)
    args = argse.parse_args()
    return args

def list_local_files(start_path='.'):
    global local_file
    # 排除.git目录
    for root, dirs, files in os.walk(start_path):
        # print(root, dirs, files)
        # 如果当前目录是.git，跳过
        if '.git' in dirs:
            dirs.remove('.git')
        
        for file in files:
            # 获取完整路径
            full_path = os.path.join(root, file)
            # 转换为相对路径
            rel_path = os.path.relpath(full_path, start_path)
            # 使用正斜杠替换反斜杠（统一格式）
            rel_path = rel_path.replace('\\', '/')
            local_file.append(rel_path)
    local_file = '\n'.join(local_file)
    with open(local_file_path,'w',encoding='utf-8') as f:
        f.write(local_file)

def list_git_files():
    result = subprocess.run(
        ["git", "rev-list", "--all"],
        stdout=subprocess.PIPE,
        text=True,
        encoding='utf-8'  # 指定编码为 utf-8
    )
    files = set()
    for commit in result.stdout.splitlines():
        size_result = subprocess.run(
            ["git", "ls-tree", "-r", commit,"--name-only"],
            stdout=subprocess.PIPE,
            text=True,
            encoding='utf-8'  # 指定编码为 utf-8
        )
        for filename in size_result.stdout.splitlines():
            files.add(filename.replace('"',''))

    files = list(files)
    newfiles = []
    for file in files:
        newfiles.append(bytes(file, "utf-8").decode("unicode_escape").encode("latin1").decode("utf-8"))
    with open('git_file.txt','w',encoding='utf8') as f:
        f.write('\n'.join(newfiles))

    # # 示例解码
    # raw_filename = "\\344\\270\\255\\350\\200\\203\\350\\257\\215\\346\\261\\207\\351\\227\\252\\350\\277\\207\\347\\262\\276\\347\\274\\226\\346\\234\\254.pdf"
    # decoded_filename = bytes(raw_filename, "utf-8").decode("unicode_escape").encode("latin1").decode("utf-8")
    # print(decoded_filename)

def delete_files():
    with open(local_file_path,'r',encoding='utf-8') as f:
        local_file = set(f.read().split('\n'))
    with open(git_file_path,'r',encoding='utf-8') as f:
        git_file = set(f.read().strip().split('\n'))
    public_file = local_file.intersection(git_file)
    delete_files = '\n'.join(list(git_file.difference(public_file)))+'\n'
    with open('delete_files.txt','w',encoding='utf8') as f:
        f.write(delete_files)
    

if __name__ == '__main__':
    # 从当前目录开始
    args = process_argse()
    try:
        if args.function == 'list_local':
            list_local_files()
        elif args.function == 'list_git':
            list_git_files()
        elif args.function == 'delete':
            delete_files()
    except Exception as e:
        print(e)
        pass
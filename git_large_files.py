import subprocess
import codecs

# 获取所有文件的 SHA 和路径
result = subprocess.run(
    ["git", "rev-list", "--objects", "--all"],
    stdout=subprocess.PIPE,
    text=True,
    encoding='utf-8'  # 指定编码为 utf-8
)
#print(result.stdout.splitlines())
#['e4b4499bf78c42af0437cadff2af5c63519d06f6', '6544bdd96b2082d8a0fac3199f01855cb8b83b60',
#'c62652d0ebfb125e69fc6a6842644e97fe272637 ', '56ae254be1b217a4967f920c4ab67a2a75f6ab0e dir',
#'59a744c0ce52d89c02bf6b064d648638cd721c7a dir/1.dat', '41bf941ab17ee186925b4d0bd07928d5593a369f test.pdf',
#'fd9a196a4a2b1ffce83b7689d7614f916e1a206c ']
files = []
for line in result.stdout.splitlines():
    sha, *filename = line.split()
    filename = " ".join(filename)
    size_result = subprocess.run(
        ["git", "cat-file", "-s", sha],
        stdout=subprocess.PIPE,
        text=True
    )
    size = int(size_result.stdout.strip())  # 文件大小（字节）
    files.append((size, sha, filename))

# 按文件大小排序并输出前 10 大文件
for size, sha, filename in sorted(files, reverse=True, key=lambda x: x[0])[:10]:
    print(f"{size / 1024 / 1024:.2f} MB {sha} {filename}")

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
    print(newfiles)

    # # 示例解码
    # raw_filename = "\\344\\270\\255\\350\\200\\203\\350\\257\\215\\346\\261\\207\\351\\227\\252\\350\\277\\207\\347\\262\\276\\347\\274\\226\\346\\234\\254.pdf"
    # decoded_filename = bytes(raw_filename, "utf-8").decode("unicode_escape").encode("latin1").decode("utf-8")
    # print(decoded_filename)
list_git_files()



import os
import sys

# 从命令行获取输入和输出文件路径
input_file_path = sys.argv[1]
output_file_path = sys.argv[2]

# Read the content of the input file
with open(input_file_path, 'r') as infile:
    content = infile.readlines()
    
    # 用于记录新命名的序列编号
    count = 1
    new_content = []
    for line in content:
        if line.startswith('>'):
            new_content.append(f'>{count}\n')
            count += 1
        else:
            new_content.append(line)
    
    # Write the modified content to the output file
    with open(output_file_path, 'w') as outfile:
        outfile.writelines(new_content)

print("Renaming finished!")

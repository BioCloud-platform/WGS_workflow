import os
import pandas 
import numpy 
import argparse
import time

parser = argparse.ArgumentParser(description='VFDB annotations reshape')
parser.add_argument('-i', '--input', dest='InF', type=str, required=True,
                    help="the path of the merge file")
parser.add_argument('-l', '--list', dest='InList', type=str, required=True,
                    help="the path of the strain list file")
parser.add_argument('-o', '--output', dest='OutF', type=str, required=True,
                    help="the output path of the reshape file")
args = parser.parse_args()

#file_in="VFDB_merged.tsv"
file_in=os.path.abspath(args.InF)
#file_list="VFDB_setA_strains_list.txt"
file_list=os.path.abspath(args.InList)
#file_out="VFDB_merged_reshape.tsv"
file_out=os.path.abspath(args.OutF)

import pandas as pd
start = time.time()

# 读取数据，避免内存占用过大
df_ori = pd.read_csv(file_in, dtype=str, sep="\t", header=None, low_memory=True)

df_ori.columns = ["qID","VFDB_ID","pident","length","mismatch","gapopen","qstart","qend","sstart","send","evalue","bitscore"]
df_ori[['SampleID', 'ppID']] = df_ori["qID"].str.split('|', expand = True) #expand 才会出列

# 用 groupby() 代替 pivot_table，提高效率
df_out = df_ori.groupby(["VFDB_ID", "SampleID"])["bitscore"].agg(lambda x: "|".join(map(str, x))).unstack(fill_value="0")
end = time.time()
print(f"groupby运行时间: {end - start:.2f} 秒")

# 读取样品列表
df_list = pd.read_csv(file_list, dtype=str, sep="\t", header=None, names=["SampleID"], low_memory=True)
# 确保 df_list 是一维 Series
all_samples = df_list["SampleID"].unique()
# 使用 reindex 补充缺失样品列，并填充 0
df_out = df_out.reindex(columns=all_samples, fill_value="0")

# 写出转换后的表格
df_out.T.to_csv(file_out, sep="\t",encoding="utf8")
print("优化后内存占用：", df_out.memory_usage(deep=True).sum() / 1024**2, "MB")
# 计算 df_out_numeric（hit_score 计数） & df_out_binary（是否有 hit_score）
df_out_numeric = df_out.applymap(lambda x: len(x.split("|")) if x != "0" else 0)
df_out_binary = df_out_numeric.applymap(lambda x: 1 if x > 0 else 0)
end2 = time.time()
print(f"表格转换运行时间: {end2 - end:.2f} 秒")

# 输出文件路径
df_out_binary.T.to_csv(file_out+"_binary.tsv",sep="\t",encoding = 'utf8')
df_out_numeric.T.to_csv(file_out+"_numeric.tsv",sep="\t",encoding = 'utf8')
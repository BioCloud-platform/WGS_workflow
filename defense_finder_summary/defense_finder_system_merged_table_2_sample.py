import os
import pandas as pd
import numpy 
import argparse
import time

parser = argparse.ArgumentParser(description='defense finder system reshape')
parser.add_argument('-i', '--input', dest='InF', type=str, required=True,
                    help="the path of the merge file")
parser.add_argument('-l', '--list', dest='InList', type=str, required=True,
                    help="the path of the strain list file")
parser.add_argument('-o', '--output', dest='OutF', type=str, required=True,
                    help="the output path of the reshape file")
args = parser.parse_args()

#file_in="/data/Xianjinyuan/LD_lab/public_datasets/culturomics_datasets/public_isolate_proj/miBC_others_AntiPhage/GCF_000364225.2_ASM36422v2_genomic/GCF_000364225.2_ASM36422v2_genomic_defense_finder_systems.tsv"
file_in=os.path.abspath(args.InF)
file_list=os.path.abspath(args.InList)
#file_out="/data/Xianjinyuan/LD_lab/public_datasets/culturomics_datasets/public_isolate_proj/miBC_others_AntiPhage/GCF_000364225.2_ASM36422v2_genomic/GCF_000364225.2_ASM36422v2_genomic_defense_finder_systems_anno.tsv"
file_out=os.path.abspath(args.OutF)

start = time.time()

# 读取数据，避免内存占用过大
df_ori = pd.read_csv(file_in, dtype=str, sep="\t", header=None, low_memory=True)
df_ori.columns = ["SampleID","sys_id","type","subtype","activity","sys_beg","sys_end","protein_in_syst","genes_count","name_of_profiles_in_sys"]

# 用 groupby() 代替 pivot_table，提高效率
df_out = df_ori.groupby(["subtype", "SampleID"])["genes_count"].agg(lambda x: "|".join(map(str, x))).unstack(fill_value="0") #用subtype是因为它才是每一行实际的代表，如果用type，就可以把多行再进一步压缩
#正常来说，system是个汇总表，因此每个样品就该只出现一次，因此不应该再有多个gene count的情况
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

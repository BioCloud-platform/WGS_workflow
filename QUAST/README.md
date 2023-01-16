# QUAST

## 使用场景：基因组组装效果的评估
QUAST主要用于统计contigs数目、长度、GC含量、N50、L50等参数。一般认为N50越长，基因组拼接效果越好。

## 解读PPT
QUAST解读.pptx

## 代码例子

## 注意事项

## 测试数据例子
#例子一，每个项目的fna都在目录下单独的各项目文件夹里，此时可以通过该范例一次全部跑完（其中脚本中有识别文件夹中所有fasta文件的代码）
```
cd /data/Xianjinyuan/LD_lab/public_datasets/culturomics_datasets/public_MAGs
conda activate MAG_snakemake
snakemake -np -s snakefile_quast_all_MAG.txt #测试
snakemake -s snakefile_quast_all_MAG.txt -c 80 --use-singularity
```
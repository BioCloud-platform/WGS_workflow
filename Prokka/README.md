# prokka

## 使用场景：对原核基因组进行基因预测和注释的主流工具
已经整合prodigal和相关数据库，其输出结果包含多种格式的文件：.gff 基因注释文件，.gbk Genebank格式，.faa 翻译CDS的氨基酸序列，.ffn所有转录本核酸序列，.tsv所有注释基因特征表格等。 <br>
prodigal是基因组上ORF的预测的主流工具，使用动态规划算法，特别关注改善基因结构预测，改善翻译起始位点识别和减少假阳性三个目标，预测准确度较好，被众多分析流程整合。

## 解读PPT
prokka.pptx

## 代码例子
```
prokka --addgenes --outdir {outpath} --prefix {sample_name} --force --cpus {threads} {input} #add prefix to control the output name, or it will be the date, which is hard to connect to the downstream analysis
```

## snakemake的格式
```
#根据具体情况修改config.yaml
#然后就直接运行snakefile_prokka
#例子，注路径要根据实际情况修改。
conda activate snakemake
cd /nasdir/xinyi/202207-SZChildrenHospital/script
snakemake -s snakefile_prokka -c 8 --use-singularity --singularity-args "--bind /nasdir/xinyi" #此处没使用cluster，需要的话要加相关参数；--singularity-args是为了识别上层目录的内容
#当前逻辑是每个样品分别跑
```

## 注意事项


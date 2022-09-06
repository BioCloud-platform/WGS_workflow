# antiSMASH

## 使用场景：基因组中次级代谢基因簇（BGC）注释
antiSMASH算是领域内目前的金标准。

## 代码例子
```
conda activate /home/licun/miniconda3/antismash
antismash --cb-general --cb-knownclusters --cb-subclusters --asf --pfam2go --smcog-trees --genefinding-tool prodigal -c 12 DA*.gbk
```

## 注意事项

## snakemake的格式
```
#根据具体情况修改config.yaml
#然后就直接运行snakefile_antiSMASH
#例子，注路径要根据实际情况修改。
conda activate snakemake
cd /nasdir/xinyi/202207-SZChildrenHospital/script
snakemake -s snakefile_antiSMASH -c 8 --use-singularity --singularity-args "--bind /nasdir/xinyi" #此处没使用cluster，需要的话要加相关参数；--singularity-args是为了识别上层目录的内容
#当前逻辑是每个样品分别跑。结果是网页格式，目前只能人工解读，没有想到什么好的自动化方式。
```

## 结果解读，主要就是index.html
详见：https://docs.antismash.secondarymetabolites.org/understanding_output/
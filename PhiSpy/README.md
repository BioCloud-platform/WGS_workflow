# PhiSpy

## 使用场景：基因组中prophage预测
貌似是目前唯一基于命令行的相关工具。

## 代码例子
```
conda activate /home/licun/miniconda3/prophage 
PhiSpy.py -o outfile DA*.gbk --output_choice 512
```

## snakemake的格式
```
#根据具体情况修改config.yaml
#然后就直接运行snakefile_PhiSpy
#例子，注路径要根据实际情况修改。
conda activate snakemake
cd /nasdir/xinyi/202207-SZChildrenHospital/script
snakemake -s snakefile_PhiSpy -c 8 --use-singularity --singularity-args "--bind /nasdir/xinyi" #此处没使用cluster，需要的话要加相关参数；--singularity-args是为了识别上层目录的内容
#当前逻辑是每个样品分别跑，然后通过把每个prophage_coordinates.tsv里的pp替换成样品名，最后通过PhiSpy_merged_table_2_sample.py转换成汇总表格。
## 汇总表内数值为预测的前噬菌体长度；行头是att左右位点串接的序列
```

## 注意事项

## 结果解读
```
prophage_coordinates.tsv的merge结果：Phispy的merged.tsv：
The columns of the file are:

Prophage number #这个似乎并没有实际含义，就是排序而已（已经替换成样品名|编号的格式）
The contig upon which the prophage resides
The start location of the prophage
The stop location of the prophage 
If we can detect the att sites, the additional columns are:
start of attL;
end of attL;
start of attR;
end of attR;
sequence of attL; #这个和attR，结合长度，可能才是真正有价值识别的地方
sequence of attR; #这个和attL，结合长度，可能才是真正有价值识别的地方
The explanation of why this att site was chosen for this prophage.

```

参考资料：https://github.com/linsalrob/PhiSpy
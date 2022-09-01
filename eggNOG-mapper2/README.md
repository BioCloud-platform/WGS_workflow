# eggNOG-mapper2

## 使用场景：细菌全基因组的功能全面注释，做为prokka结果的进一步补充

## 需要另外下载数据库
### conda安装方式，然后通过download_eggnog_data.py来进行下载
```
mamba create -c bioconda eggnog-mapper=2.1.8 -n eggnog-2.1.8
conda activate eggnog-mapper=2.1.8
download_eggnog_data.py #需要手动选择y
#如果提醒无法访问目标目录，需要自己提前创建。总数据库大小超过10G
#如果要强制执行，可以用-y选项
download_eggnog_data.py --data_dir {数据库路径} -y  
```
对应的docker版本是：docker://dataspott/eggnog-mapper:2.1.8--2022-07-11

## 代码例子
```
conda activate eggnog-mapper=2.1.8
emapper.py -i {input} --output {output} -d bact --usemem --cpu {threads} --data_dir {数据库路径}
```
## 注意事项

## 输出结果的格式
```
#query  seed_ortholog   evalue  score   eggNOG_OGs  max_annot_lvl   COG_category    Description Preferred_name  GOs EC  KEGG_ko KEGG_Pathway    KEGG_Module KEGG_Reaction   KEGG_rclass BRITE   KEGG_TC CAZy    BiGG_Reaction   PFAMs
```

## snakemake的格式
```
#根据具体情况修改config.yaml
#然后就直接运行snakefile_checkm
#例子，注路径要根据实际情况修改。
conda activate snakemake
cd /nasdir/xinyi/202207-SZChildrenHospital/script
snakemake -s snakefile_checkm -c 8 --use-singularity --singularity-args "--bind /nasdir/xinyi" #此处没使用cluster，需要的话要加相关参数；--singularity-args是为了识别上层目录的内容
#当前逻辑是每个样品分别跑，然后最后通过combine.sh把两类结果都合并起来。
```

## 参考资料：
https://blog.csdn.net/woodcorpse/article/details/83144768
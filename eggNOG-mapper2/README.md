# eggNOG-mapper2

## 使用场景：细菌全基因组的功能全面注释，做为prokka结果的进一步补充

## 若本地无数据库，需要另外下载数据库（但很大，尽可能用公用已有的）
### conda安装方式，然后通过download_eggnog_data.py来进行下载
```
mamba create -c bioconda eggnog-mapper=2.1.8 -n eggnog-2.1.8
conda activate eggnog-2.1.8
download_eggnog_data.py #需要手动选择y
#如果提醒无法访问目标目录，需要自己提前创建。总数据库大小超过10G
#如果要强制执行，可以用-y选项
download_eggnog_data.py --data_dir {数据库路径} -y  
download_eggnog_data.py --data_dir {数据库路径} -y -P #下载pfam，不是必须
download_eggnog_data.py --data_dir {数据库路径} -y -M #下载MMseq2，不是必须
download_eggnog_data.py --data_dir {数据库路径} -y -H -d taxid #下载HMMER对应taxid,要给具体的，如Bacteria是2，Archaea是2157，Eukaryota是2759，目前这三个都下了
```
对应的docker版本是：docker://dataspott/eggnog-mapper:2.1.8--2022-07-11

参考资料：https://blog.csdn.net/woodcorpse/article/details/83144768

## 代码例子
```
conda activate eggnog-2.1.8
emapper.py -i {input} --itype {type} --output {output} -d bact --usemem --cpu {threads} --data_dir {数据库路径}
```

例子路径：/nasdir/xinyi/3-databases/eggnog2/v2.1.8，使用时需要用 --data_dir 参数来指定

## 注意事项
根据输入的类型不同，需要设置--itype， {CDS,proteins,genome,metagenome} ，默认是proteins

执行时最好把--resume加上，不然有些任务断了以后，会影响未来通过snakemake重新跑。


## 输出结果的格式
```
#query  seed_ortholog   evalue  score   eggNOG_OGs  max_annot_lvl   COG_category    Description Preferred_name  GOs EC  KEGG_ko KEGG_Pathway    KEGG_Module KEGG_Reaction   KEGG_rclass BRITE   KEGG_TC CAZy    BiGG_Reaction   PFAMs
```

## snakemake的格式
```
#根据具体情况修改config.yaml
#然后就直接运行snakefile_eggnog
#例子，注路径要根据实际情况修改。
conda activate snakemake
cd /nasdir/xinyi/202207-SZChildrenHospital/script
snakemake -s snakefile_eggnog -c 8 --use-singularity --singularity-args "--bind /nasdir/xinyi" #此处没使用cluster，需要的话要加相关参数；--singularity-args是为了识别上层目录的内容
#当前逻辑是每个样品分别跑，且输入用的组装的fa，然后通过把每个.emapper.annotations里的#query替换成样品名，最后进行合并就可以获取汇总表格。

#后续也会尝试用prokka的CDS，输入和--itype都要修改
```

## 结果解读。
主要有用的列：COG_category、GOs、EC、KEGG_ko、KEGG_Pathway、KEGG_Module、KEGG_Reaction、KEGG_rclass、BRITE、KEGG_TC、CAZy（和CAZy的对比？估计不一样,CAZy的结果有67条，而eggnog只有36，所以不使用）、BiGG_Reaction、PFAMs

通过汇总表格分析，

下游富集分析参考思路：https://cloud.tencent.com/developer/article/1607669
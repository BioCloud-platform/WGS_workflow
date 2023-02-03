# GUNC

## 使用场景：细菌全基因组的嵌合程度判定，属于组装结果的质控步骤之一

## 若本地无数据库，需要另外下载数据库（但很大，尽可能用公用已有的）
### conda安装方式，然后通过gunc download_db来进行下载，但失败，显示ModuleNotFoundError: No module named 'plotly.graph_objects'，检查发现是该module已经改名为“plotly.graph_objs”，因此很难修正，建议用镜像的方法
```
mamba create gunc -c bioconda -y -n gunc 
conda activate gunc
gunc download_db /data/Xianjinyuan/LD_lab/databases
```
### singularity安装方式：
```
singularity pull gunc.sif docker://quay.io/biocontainers/gunc:1.0.5--pyhdfd78af_0 
singularity shell --bind /data/Xianjinyuan/LD_lab/ gunc.sif
gunc download_db /data/Xianjinyuan/LD_lab/databases #/path/to/output/dir/
#It will take around 4 hours depending on the speed of the network
```

对应的docker版本是：docker://quay.io/biocontainers/gunc:1.0.5--pyhdfd78af_0 

参考资料：https://grp-bork.embl-community.io/gunc/installation.html

## 注意事项
1. 目前使用的是默认数据库，是progenome的，而非GTDB的

2. /data/Xianjinyuan/LD_lab/databases是数据库的路径，根据实际情况修改

3. --input_dir和--file_suffix经常要连用，例如：--input_dir {input.folder_in} --file_suffix fna

3.1 为了能更自动化识别suffix，下面的示例脚本（snakefile_GUNC_all_MAG.txt）里增加了一段自动识别suffix的判断语句

## 输出结果的格式
```
#genome n_genes_called  n_genes_mapped  n_contigs   taxonomic_level proportion_genes_retained_in_major_clades   genes_retained_index    clade_separation_score  contamination_portion   n_effective_surplus_clades  mean_hit_identity   reference_representation_score  pass.GUNC
```
#参考链接：https://grp-bork.embl-community.io/gunc/output.html

## snakemake的格式
```
conda activate MAG_snakemake
cd /data/Xianjinyuan/LD_lab/public_datasets/culturomics_datasets/public_MAGs
snakemake -s snakefile_GUNC_all_MAG.txt -c 80 --use-singularity --singularity-args "--bind /data/Xianjinyuan/LD_lab/databases" #bing the database #此处没使用cluster，需要的话要加相关参数；--singularity-args是为了识别其他目录的内容
```

## 结果解读。
主要有用的列：genome（需要注意名字是吧suffix切掉以后的），contamination_portion（反映污染程度），pass.GUNC（pass代表不太可能是嵌合体，其参考标准其实就直接是clade_separation_score，小于0.45就认为不是嵌合，但是从数据库的角度yes or not会更清晰。）

# PADLOC

## 使用场景：基因组的噬菌体抗性分析
目前比较新的软件，自带数据库，更新比较频繁。

## 代码例子
conda activate /home/tanyuxiang/.conda/envs/padloc

### 基于蛋白序列
padloc --faa /home/tanyuxiang/.conda/envs/padloc//test/GCF_001688665.2.faa --gff /home/tanyuxiang/.conda/envs/padloc/test//GCF_001688665.2.gff

### 基于全基因组序列
padloc --fna /home/tanyuxiang/.conda/envs/padloc/test/GCF_004358345.1.fna

## 注意事项
使用docker时，必须加--data 选项指定数据库路径。
输出使用--outdir的话，必须先创建该目录

## padloc数据库下载
理论上可以用git clone数据库，不过貌似实操下来基本都会失败

所以还是通过conda安装padloc以后下载比较稳定；

```
mamba create -n padloc -c conda-forge -c bioconda -c padlocbio padloc -y
conda activate padloc
padloc --db-update
```

conda装的路径一般在padloc下，可以通过which padloc查看，例如查看后的绝对路径是：/nasdir/home/Node129/xinyi/miniconda3/envs/padloc/data/

然后把他移到公共的数据库路径下比较好：mv /nasdir/home/Node129/xinyi/miniconda3/envs/padloc/data /nasdir/xinyi/3-databases/padloc; mv /nasdir/xinyi/3-databases/padloc/data /nasdir/xinyi/3-databases/padloc/v1.4.0 

## snakemake的格式
```
#根据具体情况修改config.yaml
#然后就直接运行snakefile_PADLOC
#例子，注路径要根据实际情况修改。
conda activate snakemake
cd /nasdir/xinyi/202207-SZChildrenHospital/script
snakemake -s snakefile_PADLOC -c 8 --use-singularity --singularity-args "--bind /nasdir/xinyi" #此处没使用cluster，需要的话要加相关参数；--singularity-args是为了识别上层目录的内容
#当前逻辑是每个样品分别跑，然后通过把每个*_padloc.csv里的行首增加样品名后进行cat合并，最后通过PADLOC_merged_table_2_sample.py把结果转换成汇总表格。
```

## 结果解读
从全基因组的角度，padloc.csv文件就是核心输出。

因此当前生成了PADLOC_merged.csv，是所有输入样品的结果汇总，然后转换成两类表格：1.针对抗性system的表格（以system为列名，样品为行名，里面的value是gene ID），及其附属的定量及定性文件；2.针对具体的protein的表格（里面的格式通system，只是列名是protein层级的）

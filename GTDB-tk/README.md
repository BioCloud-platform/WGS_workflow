# GTDB-tk

## 使用场景：基于全基因组数据进行物种分类注释的金标准方法
GTDB-tk基于GTDB数据库，这个数据库中包含了纯培养基因组和宏基因组组装的基因组，这个数据库最大的特点在于对基因组分类地位的准确定位，与NCBI相比，约58%在NCBI分类系统中已收录基因组的分类地位有变动。并且数据库会定期更新，添加新发现的基因组以及对已有基因组的重新命名。<br>
GTDBtk的分类系统以细菌中普遍存在的120个单拷贝蛋白质（bac120）为基础，在大量氨基酸水平差异的基础上构建新的分类系统，<br>
目前此工具支持对细菌和古菌进行物种分类，对于真菌没有涉及。

## 解读PPT
GTDB-tk.pptx

## 数据库下载(v2.1.1对应)
```
wget -c https://data.ace.uq.edu.au/public/gtdb/data/releases/release207/207.0/auxillary_files/gtdbtk_r207_v2_data.tar.gz
tar -zxvf gtdbtk_r207_v2_data.tar.gz
```
路径例子：/nasdir/xinyi/3-databases/gtdbtk

## 代码例子
conda activate /home/chenjunyu/miniconda3/envs/gtdbtk 
gtdbtk classify_wf --genome_dir fna/ --out_dir classify_wf --extension fna --cpus 8

## 注意事项
注意：每个gtdbtk的环境，会固定对应某个gtdb的版本，注意不要弄混了。

该软件不支持另外指定数据库路径，但是可以通过环境变量进行设定

文件夹里的目标输入文件（如fasta)的后缀名字一定要跟其他文件的后缀名区分开，不然会识别错误报错。

## 数据库指定
### docker形式，实际上就是把数据库路径指定到docker的/refdata
参考：https://ecogenomics.github.io/GTDBTk/installing/docker.html

### conda形式
参考：原文链接：https://blog.csdn.net/woodcorpse/article/details/108924563
```
# 设置数据库位置，注意修改软件安装位置
locate gtdbtk.sh # 查找配置文件位置
# 修改PATH=后面的路径为数据库解压目录，如/home/meta/db/gtdb/release95/
vim /conda/envs/gtdbtk/etc/conda/activate.d/gtdbtk.sh
```

## snakemake的格式
```
#根据具体情况修改config.yaml
#然后就直接运行snakefile_gtdb
#例子，注路径要根据实际情况修改。
conda activate snakemake
cd /nasdir/xinyi/202207-SZChildrenHospital/script
snakemake -s snakefile_gtdb -c 8 --use-singularity --singularity-args "--bind /nasdir/xinyi --bind /nasdir/xinyi/3-databases/gtdbtk/release207_v2/:/refdata/" #此处没使用cluster，需要的话要加相关参数；--singularity-args是为了识别上层目录的内容
#当前逻辑是每个样品分别跑,然后通过把每个gtdbtk.bac120.summary.tsv里的(#因为用的是assembly.fasta)替换成样品名，最后进行合并就可以获取汇总表格。
```


## 参考资料：

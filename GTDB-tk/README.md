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

## 数据库下载(v2.3.2对应)
```
wget -c https://data.gtdb.ecogenomic.org/releases/release214/214.1/auxillary_files/gtdbtk_r214_data.tar.gz
tar -zxvf gtdbtk_r214_data.tar.gz
```

```
注意，2.3.2版本需要增加一个--skip_ani_screen 参数（这样就和旧版本一致）
What is the difference between the mutually exclusive options --mash_db and --skip_ani_screen?
Starting with GTDB-Tk v2.2+, the classify_wf and classify function require an extra parameter to run: --mash_db or --skip_ani_screen.
With this new version of Tk, The first stage of classify pipelines (classify_wf and classify) is to compare all user genomes to all reference genomes and annotate them, if possible, based on ANI matches.
Using the --mash_db option will indicate to GTDB-Tk the path of the sketched Mash database require for ANI screening.
If no database are available ( i.e. this is the first time running classify ), the --mash_db option will sketch a new Mash database that can be used for subsequent calls.
The --skip_ani_screen option will skip the pre-screening step and classify all genomes similar to previous versions of GTDB-Tk.

此外，新的镜像，要手动设定参考基因组路径：export GTDBTK_DATA_PATH=/refdata，所以我直接在snakefile里面加了这一步。
```

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
### 按每个样品分开跑，对应unicycler组装的方式
```
#根据具体情况修改config.yaml
#然后就直接运行snakefile_gtdb
#例子，注路径要根据实际情况修改。
conda activate snakemake
cd /nasdir/xinyi/202207-SZChildrenHospital/script
snakemake -s snakefile_gtdb -c 8 --use-singularity --singularity-args "--bind /nasdir/xinyi --bind /nasdir/xinyi/3-databases/gtdbtk/release207_v2/:/refdata/" #此处没使用cluster，需要的话要加相关参数；--singularity-args是为了识别上层目录的内容
#当前逻辑是每个样品分别跑,然后通过把每个gtdbtk.bac120.summary.tsv里的(#因为用的是assembly.fasta)替换成样品名，最后进行合并就可以获取汇总表格。
```

### 所有样品在一个文件夹，对应基因组下载的结果
```
conda activate MAG_snakemake_518
cd /data/Xianjinyuan/LD_lab/public_datasets/culturomics_datasets
snakemake -s snakefile_gtdb_in1fd --use-singularity --singularity-args "--bind /data/Xianjinyuan/LD_lab/databases/GTDBTk/release207_v2/:/refdata/" --jobs 1 --cores 120 
#似乎这个版本一定要输入jobs的数量，好处是就算不利用cluster也能并行,然后--cores设置一定要放在最后，放在前面居然会报错
```

## 参考资料：

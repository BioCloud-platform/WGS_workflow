# DBCAN2: CAZy annotation for pangenome or WGS genes

## Notes：最新版本是dbCAN4，沿用dbCAN3的snakemake脚本,可以直接跳到该部分，前面的都基本过期了

### 目前泛基因组只测试过panphlan，WGS只测试过prokka的输出

### 注释逻辑：三大步骤：

1. seqtk从基因序列生成可能的6种蛋白序列；如果输入的是prokka的faa文件，则应该跳过（通过-p参数设置）
2. 使用dbcan2，对蛋白序列进行三种方法的注释
3. 对注释结果进行整理：只有2种或以上方法都注释的才考虑。其中，最优先使用HMMER的结果，其次是Hotpep的结果，DIAMOND的结果不被考虑。【这个需要检查 一下逻辑】
4. 最新版本的dbCAN，似乎不用Hotpep，而是用了eCAMI（适合EC对应的，和CAZY注释其实没什么关系），导致其结果可读性很奇怪。



## How to run: (in WZJ machines)

Location: /data/Xianjinyuan/LD_lab/pipelines/DBCAN2/run_dbcan.py

ENV:  (need to build a public version of environment in the future, docker might be better)

```
conda activate /home/chenjunyu/miniconda3/envs/anno/
```

Former ENV building note:

```
conda activate anno
conda install -c bioconda seqkit
conda install -c bioconda diamond hmmer prodigal
pip install run-dbcan==2.0.11
```

Database: /data/Xianjinyuan/LD_lab/databases/CAZy_dbCAN2_db/dbCAN2_db_2021_03_15/

### Running example:

```
conda activate /home/chenjunyu/miniconda3/envs/anno/

python /data/Xianjinyuan/tanyuxiang/YT_scripts/run_dbcan.py -i . -o cazy -d /data/Xianjinyuan/LD_lab/databases/CAZy_dbCAN2_db/dbCAN2_db_2021_03_15/
```

Key optional parameters:

```
-s 需要识别的文件后缀名,因为脚本是文件夹内遍历的模式，必须确定这个后缀是能唯一识别对象文件的。
-p 标注是否蛋白序列，默认是False，任何其他字符串都会被认为是True。主要用于注释WGS的基因时，通过prokka的faa蛋白文件，就不需要再跑第一步骤了。
```

### Results:

当前文件夹会有Hotpep文件夹（中间文件）

#### output文件夹内，主要有用的是dbcan和cazy文件夹：

dbcan里是每个样品的三种注释方法的结果，其汇总在overview.txt里

cazy文件夹是每个样品整理后的最终注释(利用的是assign_dbcan_snakemake.py,原理是每个GH在三种注释里出现了最少两次的就会保留。注意，是每个GH，不是整个字段串)

cazy_final_out.csv 是所有样品的汇总结果 （利用的是CAZy_merged_table_2_sample.py）



## Test Example:

1. prokka ffn做为输入：

```
conda activate /home/chenjunyu/miniconda3/envs/anno/

cd /data/Xianjinyuan/tanyuxiang/2-tooltest/CAZy_dbCAN2

python /data/Xianjinyuan/tanyuxiang/YT_scripts/run_dbcan.py -i . -o cazy -d /data/Xianjinyuan/LD_lab/databases/CAZy_dbCAN2_db/dbCAN2_db_2021_03_15/ -s .ffn
```

2. prokka faa做为输入：注意输入是遍历，如果没法保障输入的文件识别是唯一，就应该把相关文件放到一个地方

```
conda activate /home/chenjunyu/miniconda3/envs/anno/

cd /data/Xianjinyuan/tanyuxiang/2-tooltest/CAZy_dbCAN2

time python /data/Xianjinyuan/tanyuxiang/YT_scripts/run_dbcan.py -i vfdb_in -o cazy -d /data/Xianjinyuan/LD_lab/databases/CAZy_dbCAN2_db/dbCAN2_db_2021_03_15/ -s .faa -p TRUE
```



## Real Example

panphlan的泛基因组注释，可以一次把所有的物种都分别注释

```
conda activate /home/chenjunyu/miniconda3/envs/anno/

cd /data/Xianjinyuan/LD_lab/databases/xstrain/panphlan_ref202009_all_merged/

time python /data/Xianjinyuan/tanyuxiang/YT_scripts/run_dbcan.py -i panphlan_ref202009_all_merged -o cazy_all_merged -d /data/Xianjinyuan/LD_lab/databases/CAZy_dbCAN2_db/dbCAN2_db_2021_03_15/
```



## Database generation history (only works in the anno env)

```
cd /data/Xianjinyuan/LD_lab/databases/CAZy_dbCAN2_db/dbCAN2_db_2021_03_15/ \
    && wget http://bcb.unl.edu/dbCAN2/download/CAZyDB.07312019.fa.nr && diamond makedb --in CAZyDB.07312019.fa.nr -d CAZy \
    && wget http://bcb.unl.edu/dbCAN2/download/Databases/dbCAN-HMMdb-V8.txt && mv dbCAN-HMMdb-V8.txt dbCAN.txt && hmmpress dbCAN.txt \
    && wget http://bcb.unl.edu/dbCAN2/download/Databases/tcdb.fa && diamond makedb --in tcdb.fa -d tcdb \
    && wget http://bcb.unl.edu/dbCAN2/download/Databases/tf-1.hmm && hmmpress tf-1.hmm \
    && wget http://bcb.unl.edu/dbCAN2/download/Databases/tf-2.hmm && hmmpress tf-2.hmm \
    && wget http://bcb.unl.edu/dbCAN2/download/Databases/stp.hmm && hmmpress stp.hmm
```

see [Index of /dbCAN2/download (unl.edu)](https://bcb.unl.edu/dbCAN2/download/) for updates and instructions

v11,实际上就是后面dbCAN4的数据库构建方式
```
cd /nasdir/xinyi/3-databases/CAZy/v11-20220806
wget http://bcb.unl.edu/dbCAN2/download/Databases/V11/CAZyDB.08062022.fa \
    && wget https://bcb.unl.edu/dbCAN2/download/Databases/V11/dbCAN-HMMdb-V11.txt && mv dbCAN-HMMdb-V11.txt dbCAN.txt && hmmpress dbCAN.txt \
    && wget https://bcb.unl.edu/dbCAN2/download/Databases/V11/tcdb.fa \
    && wget http://bcb.unl.edu/dbCAN2/download/Databases/V11/tf-1.hmm && hmmpress tf-1.hmm \
    && wget http://bcb.unl.edu/dbCAN2/download/Databases/V11/tf-2.hmm && hmmpress tf-2.hmm \
    && wget https://bcb.unl.edu/dbCAN2/download/Databases/V11/stp.hmm && hmmpress stp.hmm \
    && cd ../ && wget http://bcb.unl.edu/dbCAN2/download/Samples/EscheriaColiK12MG1655.fna \
    && wget http://bcb.unl.edu/dbCAN2/download/Samples/EscheriaColiK12MG1655.faa \
    && wget http://bcb.unl.edu/dbCAN2/download/Samples/EscheriaColiK12MG1655.gff
#因为中间有涉及建库的步骤,但是又不能用别的版本进行建库，所以必须使用docker进行构建
singularity shell /nasdir/xinyi/202207-SZChildrenHospital/script/.snakemake/singularity/3550290a77877f1bf737eff7746e0a55.simg
diamond makedb --in CAZyDB.08062022.fa -d CAZy 
diamond makedb --in tcdb.fa -d tcdb
```



## Other similar script versions

In SimStr, the cazy_anno.py is the frozen version at 2022-05-23


## 官方github：https://github.com/linnabrown/run_dbcan

## snakemake的格式
```
#根据具体情况修改config.yaml
#然后就直接运行snakefile_CAZy
#例子，注路径要根据实际情况修改。
conda activate snakemake
cd /nasdir/xinyi/202207-SZChildrenHospital/script
snakemake -s snakefile_CAZy -c 8 --use-singularity --singularity-args "--bind /nasdir/xinyi" #此处没使用cluster，需要的话要加相关参数；--singularity-args是为了识别上层目录的内容
#当前逻辑是每个样品分别跑，然后最后assign_dbcan_snakemake.py脚本把注释结果整理的同时也加了样品信息,最后通过CAZy_merged_table_2_sample.py转换成样品对酶族的表格，可用于下游作图分析。
```

目前只是直接用的dbCAN3，和上面提供的run_dbcan.py里的dbCAN不一样，3重比较是有的，但是Hotpep被换成eCAMI，就没法投票机制了。但是最新的版本似乎eCAMI也是可以参与投票的，和HMM的结果类似，所以又加回去了
```
V3.0.2: Added eCAMI tool, remove Hotpep from run_dbCAN;
v2.0.11:Add ec number prediction to hotpep result;
```
见：https://github.com/linnabrown/run_dbcan/wiki/Update-information-Archive

目前只有HMMER有结果的才会被使用，如果HMMER有结果，但是跟diamond不一样，也会被扔掉。

貌似最后生成的cazy_final_out.csv里的conflict其实还不少，目前并没有进行处理，相当于被扔掉了。

### 最新版本是dbCAN4，沿用dbCAN3的snakemake脚本，下面是建库的方式
```
singularity pull /data/Xianjinyuan/LD_lab/singularity_images/run_dbcan-4.0.0.sif docker://haidyi/run_dbcan:latest
#里面不包含数据库，所以还是要自建
cd /data/Xianjinyuan/LD_lab/databases/CAZy_dbCAN2_db/dbCAN2_db_2023_08_28/db
wget http://bcb.unl.edu/dbCAN2/download/Databases/fam-substrate-mapping-08252022.tsv
wget http://bcb.unl.edu/dbCAN2/download/Databases/PUL.faa 
wget http://bcb.unl.edu/dbCAN2/download/Databases/dbCAN-PUL_07-01-2022.xlsx
wget http://bcb.unl.edu/dbCAN2/download/Databases/dbCAN-PUL_07-01-2022.txt
wget http://bcb.unl.edu/dbCAN2/download/Databases/dbCAN-PUL.tar.gz 
wget http://bcb.unl.edu/dbCAN2/download/Databases/dbCAN_sub.hmm 
wget http://bcb.unl.edu/dbCAN2/download/Databases/V11/CAZyDB.08062022.fa 
wget https://bcb.unl.edu/dbCAN2/download/Databases/V11/dbCAN-HMMdb-V11.txt
wget https://bcb.unl.edu/dbCAN2/download/Databases/V11/tcdb.fa 
wget http://bcb.unl.edu/dbCAN2/download/Databases/V11/tf-1.hmm 
wget http://bcb.unl.edu/dbCAN2/download/Databases/V11/tf-2.hmm 
wget https://bcb.unl.edu/dbCAN2/download/Databases/V11/stp.hmm 
tar xvf dbCAN-PUL.tar.gz
##database
singularity shell --bind /data/ /data/archive/LD_lab/singularity_images/run_dbcan-4.0.0.sif
diamond makedb --in CAZyDB.08062022.fa -d CAZy
diamond makedb --in tcdb.fa -d tcdb
hmmpress dbCAN_sub.hmm
hmmpress tf-1.hmm
hmmpress tf-2.hmm
hmmpress stp.hmm
mv dbCAN-HMMdb-V11.txt dbCAN.txt && hmmpress dbCAN.txt
exit
##不知道为什么里面没blast，然后还得建，不确定版本会不会影响
singularity shell --bind /data/ /data/archive/LD_lab/singularity_images/blast-2.13.0.sif
makeblastdb -in PUL.faa -dbtype prot
exit
#下面这个我不是非常确定用途是什么，感觉其实不太相关
cd ..
wget http://bcb.unl.edu/dbCAN2/download/Samples/EscheriaColiK12MG1655.fna
wget http://bcb.unl.edu/dbCAN2/download/Samples/EscheriaColiK12MG1655.faa
wget http://bcb.unl.edu/dbCAN2/download/Samples/EscheriaColiK12MG1655.gff
```
#### 运行可以参考snakefile_CAZy_dbCAN4.py，该脚本用于对泛基因组进行注释，实际操作时可能需要根据具体需求调整，但是逻辑不用变：
先是跑run_dbcan，然后assign_dbcan_snakemake.py进行判定，最后调整格式。【因为对两个py进行了调整，原snakefile_CAZy里的后两步应该是受影响跑步了的】
# DBCAN2: CAZy annotation for pangenome or WGS genes

## Notes：

### 目前泛基因组只测试过panphlan，WGS只测试过prokka的输出

### 注释逻辑：三大步骤：

1. seqtk从基因序列生成可能的6种蛋白序列；如果输入的是prokka的faa文件，则应该跳过（通过-p参数设置）
2. 使用dbcan2，对蛋白序列进行三种方法的注释
3. 对注释结果进行整理：只有2种或以上方法都注释的才考虑。其中，最优先使用HMMER的结果，其次是Hotpep的结果，DIAMOND的结果不被考虑。【这个需要检查 一下逻辑】



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

cazy文件夹是每个样品整理后的最终注释

cazy_final_out.csv 是所有样品的汇总结果



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



## Database generation history 

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



## Other similar script versions

In SimStr, the cazy_anno.py is the frozen version at 2022-05-23

# Functional annotation using diamond(blastp) 

## Notes

方法逻辑：

1. 用seqtk从基因序列生成可能的6种蛋白序列；如果输入的是prokka的faa文件，则应该跳过（通过-p参数设置）
2. 对步骤1得到的蛋白序列，先对特殊功能的蛋白列表进行diamond建库，然后用diamond进行匹配。



## How to run

The ENV should have the required python libraries in the python script and the seqkit

```
python /data/Xianjinyuan/tanyuxiang/YT_scripts/blastp_func_anno.py -i . -o vfdb_out -db /data/Xianjinyuan/LD_lab/databases/vfdb/vfdb_2021_04_13/VFDB_setA_pro -pi 50 -cov 50
```

Key optional parameters:

```
-x 需要识别的文件后缀名,因为脚本是文件夹内遍历的模式，必须确定这个后缀是能唯一识别对象文件的。
-p 标注是否蛋白序列，默认是False，任何其他字符串都会被认为是True。主要用于注释WGS的基因时，通过prokka的faa蛋白文件，就不需要再跑第一步骤了。
```

### Results:

output文件夹内，主要有用的是final_out文件夹，每个样品一个文件；每个文件两列：基因编号，功能编号

还有All_samples_features_out.csv，是所有样品的集合



## Databases

### VFDB：/data/Xianjinyuan/LD_lab/databases/vfdb/vfdb_2021_04_13

建库例子：fas其实就是和faa类似的蛋白序列文件，从VFDB里提取(The VFDB_setA_pro.fas was downloaded from [VFDB: Virulence Factors of Bacterial Pathogens (mgc.ac.cn)](http://www.mgc.ac.cn/cgi-bin/VFs/v5/main.cgi) in the download page as the "DNA sequences of core dataset", "protein sequences of core dataset" and the "DNA sequences of full dataset" "protein sequences of full dataset" at 2021_04_13.)

2023-08-26下载：VFDB_setA_nt.fas  VFDB_setA_pro.fas  VFDB_setB_nt.fas  VFDB_setB_pro.fas
其中setA是core（实验验证的），setB是core+预测；nt是DNA，pro是蛋白，主要看输入是什么格式的数据来选用，fna对应nt，faa对应pro，

2025-01-27又下载了一次，和2023-08是类似的方式。此外，下载的时候还有vf.xls，是对vf的分类和功能进一步注释，也匹配下载了。


```
cd /data/Xianjinyuan/LD_lab/databases/vfdb/vfdb_2025_01_27
gunzip *.gz
singularity shell --bind /data /data/archive/LD_lab/singularity_images/diamond-2.0.9.sif
diamond makedb --in VFDB_setA_pro.fas -d VFDB_setA_pro
diamond makedb --in VFDB_setB_pro.fas -d VFDB_setB_pro
diamond makedb --in VFDB_setA_nt.fas -d VFDB_setA_nt
diamond makedb --in VFDB_setB_nt.fas -d VFDB_setB_nt
#2023文件夹内存在tsv、csv文件应该是通过convert.sh对anno文件进行修正（但似乎只会生成tsv，而没有csv），而anno文件就是直接通过对.fas进行grep ^>得来的。不过貌似这个不是必须用上的，主要是在需要对gene的注释进行聚类的时候才需要。
grep "^>" VFDB_setA_pro.fas > VFDB_setA_pro.anno
python /data/Xianjinyuan/tanyuxiang/YT_scripts/VFDB/VFDB_anno_parser.py VFDB_setA_pro.anno VFDB_setA_pro.tsv
#grep "^>" VFDB_setA_nt.fas > VFDB_setA_nt.anno
#python /data/Xianjinyuan/tanyuxiang/YT_scripts/VFDB/VFDB_nt_anno_parser.py VFDB_setA_nt.anno VFDB_setA_nt.tsv ##格式不适用，需要重新修正正则表达。目前我们用的是pro
```

其他数据逐步补充



## Examples

测试例子：prokka faa做为输入：注意输入是遍历，如果没法保障输入的文件识别是唯一，就应该把相关文件放到一个地方

```
conda activate /home/chenjunyu/miniconda3/envs/anno/

cd /data/Xianjinyuan/tanyuxiang/2-tooltest/CAZy_dbCAN2

python /data/Xianjinyuan/tanyuxiang/YT_scripts/blastp_func_anno.py -i vfdb_in -o vfdb_out -db /data/Xianjinyuan/LD_lab/databases/vfdb/vfdb_2021_04_13/VFDB_setA_pro -pi 50 -cov 50 -x .faa -p TRUE
```

注：如果出现：KeyError: 'ffnList' 这个错误，就是 -x设置的文件名识别失败，没有结果。



panphlan的泛基因组注释，可以一次把所有的物种都分别注释

```
conda activate /home/chenjunyu/miniconda3/envs/anno/

cd /data/Xianjinyuan/LD_lab/databases/xstrain/

time python /data/Xianjinyuan/tanyuxiang/YT_scripts/blastp_func_anno.py -i panphlan_ref202009_all_merged -o vfdb_all_out -db /data/Xianjinyuan/LD_lab/databases/vfdb/vfdb_2021_04_13/VFDB_setA_pro -pi 50 -cov 50 2>vfdb_anno.log
```



#### Former ENV building note:

```
conda activate anno
conda install -c bioconda seqkit
```



## Other similar script versions

In SimStr, the vfdb_anno.py is the frozen version at 2022-05-23


## snakemake的格式
```
#根据具体情况修改config.yaml
#然后就直接运行snakefile_VFDB
#例子，注路径要根据实际情况修改。
conda activate snakemake
cd /nasdir/xinyi/202207-SZChildrenHospital/script
snakemake -s snakefile_VFDB -c 8 --use-singularity --singularity-args "--bind /nasdir/xinyi" #此处没使用cluster，需要的话要加相关参数；--singularity-args是为了识别上层目录的内容
#当前逻辑是每个样品分别跑，然后在每行行首加样品名样品名，最后进行VFDB_merged_table_2_sample.py合并就可以获取汇总表格。
##汇总表格里的数值是score，另外也有定量表和定性表
```
当前用的是直接diamond blastp，而非上面的blastp_func_anno.py ，后面可能还是需要进一步改良。

```
#针对泛基因组分析的案例
conda activate MAG_snakemake
cd /data/archive/tanyuxiang/2-tooltest/xls2csv/merge_2023-06_all_merge/panaroo/
snakemake -s snakefile_VFDB_pangenome.py -c 10 --use-singularity --singularity-args "--bind /data/Xianjinyuan/" #此处没使用cluster，需要的话要加相关参数；--singularity-args是为了识别上层目录的内容
#另外，这个脚本，blastp是默认设置，也就是evalue是0.01的阈值。
```

## 结果解读：文件本身没header。
具体header信息见：https://www.metagenomics.wiki/tools/blast/blastn-output-format-6

主要有用的就是第二列的VFDB-ID，后面的参数值，感觉基本上都肯定是没问题的（起码一般的阈值是过了的）。
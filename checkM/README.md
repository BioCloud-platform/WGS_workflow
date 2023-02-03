# checkM

## 使用场景：拼接基因组的污染度和完整度的评估使用
checkM 可以根据基因组在参考基因组发育树中的位置来推断其精确的单拷贝标记基因集（lineage-specificmarker set），同时也提供数据库可用的基于分类学的基因集（taxonomic-specificmarker set）。CheckM利用基因的单拷贝性来有效的估计基因组完整度和污染，同时能绘制基因组关键特征（例如GC含量、编码率）的图像来评估基因组的质量。

## 解读PPT
checkM.pptx

## 代码例子
conda activate /home/chenjunyu/miniconda3/envs/wgs/ <br>
checkm lineage_wf -t 8 -x fna bin-folder output-folder -f checkm.out --tab_table<br>
根据结果对基因组进行筛选select only genomes that passed the following criteria: >50% genome completeness, <5% contamination and an estimated quality score (completeness–5×contamination)>50。<br>
加了--tab_table以后，结果会输出成为tsv格式，方便后续处理，否则是很奇怪的间隔情况，很难用一般方法读入R或python<br>
## 注意事项
新：通过增加-f选项，可以把信息直接都写入到指定文件，然后增加--tab_table选项保证结果的机器可读性

旧：CheckM会把完整度和污染度等结果输出到屏幕，因此为了保存结果，建议将输出到屏幕的结果写入到文件中。

## snakemake的格式（新）
```
#为了能更自动化识别suffix，下面的示例脚本里增加了一段自动识别suffix的判断语句,同时增加了-f和--tab_table
cd /data/Xianjinyuan/LD_lab/public_datasets/culturomics_datasets/public_MAGs
conda activate MAG_snakemake
snakemake -np -s snakefile_checkm_all_MAG.txt #测试
snakemake -s snakefile_checkm_all_MAG.txt -c 80 --use-singularity
```

## snakemake的格式（旧）
```
#根据具体情况修改config.yaml
#然后就直接运行snakefile_checkm
#例子，注路径要根据实际情况修改。
conda activate snakemake
cd /nasdir/xinyi/202207-SZChildrenHospital/script
snakemake -s snakefile_checkm -c 8 --use-singularity --singularity-args "--bind /nasdir/xinyi" #此处没使用cluster，需要的话要加相关参数；--singularity-args是为了识别上层目录的内容
#当前逻辑是每个样品分别跑，在每个log前面先输入样品名字，然后最后通过snakemake把out结果合并起来。storage里的bin_stats.analyze.tsv没有合并，因为信息跟quast基本是一样的。
```


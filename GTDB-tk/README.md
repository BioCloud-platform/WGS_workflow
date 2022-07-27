# GTDB-tk

## 使用场景：基于全基因组数据进行物种分类注释的金标准方法
GTDB-tk基于GTDB数据库，这个数据库中包含了纯培养基因组和宏基因组组装的基因组，这个数据库最大的特点在于对基因组分类地位的准确定位，与NCBI相比，约58%在NCBI分类系统中已收录基因组的分类地位有变动。并且数据库会定期更新，添加新发现的基因组以及对已有基因组的重新命名。<br>
GTDBtk的分类系统以细菌中普遍存在的120个单拷贝蛋白质（bac120）为基础，在大量氨基酸水平差异的基础上构建新的分类系统，<br>
目前此工具支持对细菌和古菌进行物种分类，对于真菌没有涉及。

## 解读PPT
GTDB-tk.pptx

## 代码例子
conda activate /home/chenjunyu/miniconda3/envs/gtdbtk 
gtdbtk classify_wf --genome_dir fna/ --out_dir classify_wf --extension fna --cpus 8

## 注意事项
注意：每个gtdbtk的环境，会固定对应某个gtdb的版本，注意不要弄混了。（因为该软件不支持另外指定数据库路径）
后期会考虑对不通版本进行打包

## 测试数据例子
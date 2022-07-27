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

## 测试数据例子

## 后续待改进地方
1. 补充如何更新数据库，因为可以通过-d选项指定数据库，使用不同版本时需要标明
2. 当前模式只能单个基因组跑
# gRodon

## 使用场景：预测基因组的生长速率
相关语雀记录：https://ldlab.yuque.com/staff-pneihk/ilx7u9/ihvqgo50vpqzp0rv

## 代码例子

## 注意事项

## 测试数据例子
#注，这里用的是prokka的输入
```
cd /data/Xianjinyuan/tanyuxiang/1-projects/prophage_detection/IMGG
conda activate MAG_snakemake
snakemake -np -s snakefile_grodon_test.py 
snakemake -s snakefile_grodon_test.py --use-singularity --singularity-args "--bind /data/" -j 3 --keep-going --rerun-triggers mtime --rerun-incomplete
```
#目前会同时生成多个genome的汇总，方便后续分析
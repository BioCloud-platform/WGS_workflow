# plasmer

## 使用场景：判定contig是否源于plasmid
相关语雀记录：https://ldlab.yuque.com/staff-pneihk/ilx7u9/py507n9wfadr3vax
## 代码例子

## 注意事项

## 测试数据例子
```
cd /data/Xianjinyuan/tanyuxiang/1-projects/prophage_detection/MGMGdb_highMI
conda activate MAG_snakemake
snakemake -s snakefile_plasmer_MGMGdb_highMI.py --use-singularity --singularity-args "--bind /data/Xianjinyuan/ --bind /home" -j 80 --keep-going --rerun-triggers mtime 
```
#注，这里已经进行了结果的汇总

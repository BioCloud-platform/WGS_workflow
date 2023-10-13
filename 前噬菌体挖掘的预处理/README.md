# contig rename for fasta unification

## 使用场景：跑前噬菌体预测前，尤其是需要多种方法同时使用时，必须提前rename
相关语雀记录：https://ldlab.yuque.com/staff-pneihk/ilx7u9/hsmh7rr1vhplcfg3#GFItt

## 注意事项

## 测试数据例子
```
cd /data/Xianjinyuan/tanyuxiang/1-projects/prophage_detection/MGMGdb_highMI
conda activate MAG_snakemake
snakemake -s rename_snakemake.py -j 20 --rerun-triggers mtime
```

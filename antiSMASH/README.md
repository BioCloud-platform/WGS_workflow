# antiSMASH

## 使用场景：基因组中次级代谢基因簇（BGC）注释
antiSMASH算是领域内目前的金标准。

## 代码例子
```
conda activate /home/licun/miniconda3/antismash
antismash --cb-general --cb-knownclusters --cb-subclusters --asf --pfam2go --smcog-trees --genefinding-tool prodigal -c 12 DA*.gbk
```

## 注意事项

## 测试数据例子
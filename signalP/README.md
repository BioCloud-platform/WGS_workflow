# signalP

## 使用场景：信号肽预测
相关语雀记录：https://ldlab.yuque.com/staff-pneihk/ilx7u9/fxv6tmwee1sr620g

## 代码例子

## 注意事项

## 测试数据例子
#例子一，每个项目的fna都在目录下单独的各项目文件夹里，此时可以通过该范例一次全部跑完（其中脚本中有识别文件夹中所有fasta文件的代码）
```
cd /data/Xianjinyuan/tanyuxiang/1-projects/prophage_detection/IMGG
conda activate MAG_snakemake
snakemake -np -s snakefile_signalP_test.py --use-conda -j 8 --keep-going
# snakemake -s snakefile_signalP_test.py --use-conda -j 8 --keep-going 这个是conda版本，现在换成singularity版本了
snakemake -s snakefile_signalP_test.py --use-singularity --singularity-args "--bind /data/Xianjinyuan/" -j 8 --keep-going
```
# Nanopore assembly by unicycler
Pipelines used for WGS assembly using nanopore sequencing data.

## 运行环境
建议conda装，最新版本0.5.0

或者用make的方法装到docker里面

不建议直接在自己账户下用make安装。

docker: quay.io/biocontainers/unicycler:0.5.0--py310h2e03b76_0 或者 docker://staphb/unicycler:0.5.0

## 运行逻辑：
unicycler -1 二代R1 -2 二代R2 -o 输出目录 -t 60 --spades_path spades.py所在路径<br>


## 运行例子：
```
unicycler -1 "/home/shenjuntao/Rawdata/gutbacteria_rawdata/8_GutBacteria_WGS_SJT/8_bacteria_WGS_SJT/clean_data/CSC8_R1.fq.gz" -2 "/home/shenjuntao/Rawdata/gutbacteria_rawdata/8_GutBacteria_WGS_SJT/8_bacteria_WGS_SJT/clean_data/CSC8_R2.fq.gz" -o /home/shenjuntao/nanopore/data/20220602-00163_nanopore_20220602/CSC8_short -t 60 --spades_path /home/shenjuntao/nanopore/spades/SPAdes-3.15.4-Linux/bin/spades.py
```

## snakemake的格式
```
#根据具体情况修改config.yaml
#然后就直接运行snakefile_unicycler（纯二代）。如果有三代数据，还需要相应修改。
#例子，注路径要根据实际情况修改。
conda activate snakemake
cd /nasdir/xinyi/202207-SZChildrenHospital/script
snakemake -s snakefile_unicycler -c 8 --use-singularity --singularity-args "--bind /nasdir/xinyi" #此处没使用cluster，需要的话要加相关参数；--singularity-args是为了识别上层目录的内容
```
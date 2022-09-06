# plasforest

## 使用场景：基因组contig归属的判断（是基因组还是质粒）
plasforest是目前比较常用，杨丽丽推荐。

对每个contig进行了是否质粒的判定，其结果一般无法单独使用，需要结合别的结果信息共同使用

## 运行环境：
docker镜像：docker pull dbest/plasforest:v1.0 （必须用这个版本，latest的是没有数据库的，运行不了。目前在未知君107机子上）

## 代码例子
```
docker run -u $(id -u):$(id -g) --cpus=1 --rm -t -i -w / -v /data:/data dbest/plasforest:v1.0
cd PlasForest
python3 PlasForest.py -i /data/genome.fasta -o out.csv
```

## snakemake的格式
```
#根据具体情况修改config.yaml
#然后就直接运行snakefile_plasforest
#例子，注路径要根据实际情况修改。
conda activate snakemake
cd /nasdir/xinyi/202207-SZChildrenHospital/script
snakemake -s snakefile_plasforest -c 8 --use-singularity --singularity-args "--bind /nasdir/xinyi" #此处没使用cluster，需要的话要加相关参数；--singularity-args是为了识别上层目录的内容
#当前逻辑是每个样品分别跑，
```

## 注意事项


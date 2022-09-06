# digIS

## 使用场景：基因组的转座酶区域识别
待补充，玉灿说该软件可能有点旧。<br>
最新工具：TransposonUltimate （https://academic.oup.com/nar/article/50/11/e64/6541023 、 https://github.com/DerKevinRiehl/TransposonUltimate ），有待玉灿补充。

## 解读PPT
digIS.pptx

## 代码例子
```
conda activate /home/licun/miniconda3/digIS
python /home/licun/biosoft/digIS-digISv1.2/digIS_search.py -i sequence.fna -g annotation.gbk -o digIS_output 
```
## 注意事项

## snakemake的格式
```
#根据具体情况修改config.yaml
#然后就直接运行snakefile_digIS
#例子，注路径要根据实际情况修改。
conda activate snakemake
cd /nasdir/xinyi/202207-SZChildrenHospital/script
snakemake -s snakefile_digIS -c 8 --use-singularity --singularity-args "--bind /nasdir/xinyi" #此处没使用cluster，需要的话要加相关参数；--singularity-args是为了识别上层目录的内容
#当前逻辑是每个样品分别跑，然后最后通过combine.sh把两类结果都合并起来。
```

其中，通过singularity shell可以进入sif去看具体执行命令的路径


## 似乎程序内部有bug，暂时不处理了
ValueError: GRange: start or end position is out of the range.

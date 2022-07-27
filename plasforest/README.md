# plasforest

## 使用场景：基因组contig归属的判断（是基因组还是质粒）
plasforest是目前比较常用，杨丽丽推荐。

## 运行环境：
docker镜像：docker pull dbest/plasforest:v1.0 （目前在未知君107机子上）

## 代码例子
```
docker run -u $(id -u):$(id -g) --cpus=1 --rm -t -i -w / -v /data:/data dbest/plasforest:v1.0
cd PlasForest
python3 PlasForest.py -i genome.fasta -o out.csv
```

## 注意事项

## 测试数据例子
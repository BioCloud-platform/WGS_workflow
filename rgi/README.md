# rgi

## 使用场景：抗性基因注释
使用CARD（目前最权威的抗性基因数据库），对基因组进行注释；新版也开发了利用宏基因组数据进行挖掘的功能。

## 解读PPT
rgi.pptx

正式的Github：https://github.com/arpcard/rgi

## 代码例子
conda activate /home/chenjunyu/miniconda3/envs/rgi/ <br>
rgi main --input_sequence sequence.faa --output_file rgi.out --input_type protein --alignment_tool DIAMOND --clean -d wgs <br>

## 主要涉及的参数设置：
--input_sequence 必须是contig或者蛋白，fasta格式 <br>
--input_type contig或者protein，默认是contig（和input的实际情况对应） <br>
--alignment_tool Blast或者DIAMOND，默认是Blast <br>
--clean 是不保留中间文件 <br>
-d wgs 其他选择是plasmid,chromosome，一般我们都是用wgs <br>


## 数据库下载：
```
wget https://card.mcmaster.ca/latest/data
tar -xvf data ./card.json
```

例子路径：/nasdir/xinyi/3-databases/CARD

#https://github.com/arpcard/rgi#id42

## 注意事项
使用时需要注意记录软件版本和数据库版本号。

使用前要先load数据库,并检查版本：/rgi/rgi load --card_json {params.database_dir}; rgi database --version;


## snakemake的格式
```
#根据具体情况修改config.yaml
#然后就直接运行snakefile_RGI
#例子，注路径要根据实际情况修改。
conda activate snakemake
cd /nasdir/xinyi/202207-SZChildrenHospital/script
snakemake -s snakefile_RGI -c 8 --use-singularity --singularity-args "--bind /nasdir/xinyi" #此处没使用cluster，需要的话要加相关参数；--singularity-args是为了识别上层目录的内容
#当前逻辑是每个样品分别跑，然后通过把每个txt里的ORF_ID前加上样品名来识别，最后进行合并。在尝试格式转换的时候发现，其Drug Class、Resistance Mechanism和AMR Gene Family似乎有可能多对多的关系，不是太方便整理，所以放弃。尤其是通过heatmap功能，其实rgi会帮忙生成整理的csv。所以最后通过heatmap功能直接产生图和表。
```

注：当前用的是官网对应的biocontainer的5.2.1版。然后自带的card是3.1.4（2021-10-05版本，虽然目前似乎出到3.2.4了），但是docker里面无法简单进行更新（可能需要用root更新docker才可以，因为load的路径无法写入），因此无法用新的数据库版本。

## 结果解读
当前生成了RGI_merged.csv，是所有输入样品的结果汇总。每个样品都有具体的header，这个只做为信息汇总表，最终有价值的表格分别是三个具体功能的csv。
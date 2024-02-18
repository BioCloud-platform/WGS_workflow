# rgi

## 使用场景：抗性基因注释
使用CARD（目前最权威的抗性基因数据库），对基因组进行注释；新版也开发了利用宏基因组数据进行挖掘的功能。

## 解读PPT
rgi.pptx

正式的Github：https://github.com/arpcard/rgi

## 语雀记录
https://ldlab.yuque.com/staff-pneihk/ilx7u9/adz5allpf7zlc09v

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
#教程里错误的例子
wget https://card.mcmaster.ca/latest/data
tar -xvf data ./card.json

#实操正确的做法：
cd /data/Xianjinyuan/LD_lab/databases/CARD-ARG/
conda activate rgi-6.0.2
rgi auto_load #然后把下载的文件重命名成下载日期，例如：
mv rgi_autoload_w_lvd3ln v2023-05-18
#auto_load后，才会有正确的数据库版本号。靠复制还是别的方式构建的，都会没有版本号。根本原因其实是在conda目录下，rgi是通过conda环境下的lib/python3.8/site-packages/app/_data/loaded_databases.json文件来识别的（例如：/home/tanyuxiang/.conda/envs/rgi-6.0.2/lib/python3.8/site-packages/app/_data/loaded_databases.json），必须保证这里所有的版本号都匹配了，才能显示正确的版本号。
#因此，要正确load的方式如下：
rgi load \
  --card_json /data/Xianjinyuan/LD_lab/databases/CARD-ARG/v2023-07-28/card_data/card.json \
  --card_annotation /data/Xianjinyuan/LD_lab/databases/CARD-ARG/v2023-07-28/card_database_v3.2.7.fasta \
  --card_annotation_all_models /data/Xianjinyuan/LD_lab/databases/CARD-ARG/v2023-07-28/card_database_v3.2.7_all.fasta \
  --wildcard_annotation /data/Xianjinyuan/LD_lab/databases/CARD-ARG/v2023-07-28/wildcard_database_v4.0.1.fasta \
  --wildcard_annotation_all_models /data/Xianjinyuan/LD_lab/databases/CARD-ARG/v2023-07-28/wildcard_database_v4.0.1_all.fasta \
  --wildcard_index /data/Xianjinyuan/LD_lab/databases/CARD-ARG/v2023-07-28/card_variants/index-for-model-sequences.txt \
  --wildcard_version 4.0.1 \
  --amr_kmers /data/Xianjinyuan/LD_lab/databases/CARD-ARG/v2023-07-28/card_variants/all_amr_61mers.txt \
  --kmer_database /data/Xianjinyuan/LD_lab/databases/CARD-ARG/v2023-07-28/card_variants/61_kmer_db.json \
  --kmer_size 61

#注：2023-05-18下的3.2.6，没有那几个fasta文件,最后发现，只能自己生成：https://github.com/arpcard/rgi/issues/70#issuecomment-548803889
cd /data/Xianjinyuan/LD_lab/databases/CARD-ARG/v2023-05-18
rgi card_annotation -i card_data/card.json
rgi wildcard_annotation -i card_variants --card_json card_data/card.json -v 4.0.0
```

#https://github.com/arpcard/rgi#id42

## 注意事项
使用时需要注意记录软件版本和数据库版本号。

使用前要先检查版本：rgi database --version;如果要load，要用上面的方式load完整，理论上来说，在conda环境下load好一次，snakemake调用的时候就不用重复load了，因为其识别是conda里的路径。

此外，rgi似乎没办法用singularity镜像，主要是数据库太大，而且其文件还要跟着镜像，导致镜像oversize.【数据库可以不加到里面，每次用的时候加载】


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

注：当前用的是官网对应的biocontainer的5.2.1版。然后自带的card是3.1.4（2021-10-05版本，虽然目前似乎出到3.2.4了），但是docker里面无法简单进行更新（可能需要用root更新docker才可以，因为load的路径无法写入），因此无法用新的数据库版本。##好像这个版本还是有问题。

目前还是用conda比较方便：mamba create rgi=6.0.2 -c bioconda -y -n rgi-6.0.2

## 结果解读
当前生成了RGI_merged.csv，是所有输入样品的结果汇总。每个样品都有具体的header，这个只做为信息汇总表，最终有价值的表格分别是三个具体功能的csv。

当前，针对每个样品，进行了Drug Class、Resistance Mechanism和AMR Gene Family，以及单纯的Best_Hit_ARO和ARO（这两者应该是1对1的关系？）的汇总整理（包括数量、位置信息等），见：RGI_result_summary.R

其中，Best_Hit_ARO和ARO都能在数据库的aro_index.tsv文件里对应上（注意：aro_categories_index.tsv和aro_categories.tsv里的ID不是ARO ID）

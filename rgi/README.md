# rgi

## 使用场景：抗性基因注释
使用CARD（目前最权威的抗性基因数据库），对基因组进行注释；新版也开发了利用宏基因组数据进行挖掘的功能。

## 解读PPT
rgi.pptx

## 代码例子
conda activate /home/chenjunyu/miniconda3/envs/rgi/ <br>
rgi main --input_sequence sequence.faa --output_file rgi.out --input_type protein --alignment_tool DIAMOND --clean -d wgs <br>

## 主要涉及的参数设置：
--input_sequence 必须是contig或者蛋白，fasta格式 <br>
--input_type contig或者protein，默认是contig（和input的实际情况对应） <br>
--alignment_tool Blast或者DIAMOND，默认是Blast <br>
--clean 是不保留中间文件 <br>
-d wgs 其他选择是plasmid,chromosome，一般我们都是用wgs <br>


## 注意事项
使用时需要注意记录软件版本和数据库版本号。

## 测试数据例子
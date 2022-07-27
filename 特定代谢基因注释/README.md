# 特定代谢基因
实际上就是我们内部针对特别感兴趣的功能所自建的数据库

## 主要分类及对应的数据库路径：
原核生物的KEGG: /home/chenjunyu/databases/kegg/prokaryotes_filter <br>
BileAcide: <br>
&emsp;  a) bai基因簇、BSH、7aHSDH、7bHSDH : /home/licun/Data/Blastp_0829/ZCH/zch_three_strain/bile_acid <br>
&emsp;  b) 5AR、5BR、3bHSDH、3aHSDH : /home/licun/Data/Blastp_0829/WGS_LDlab/WGS3.0/muban_seq/BileAcid <br>
&emsp;  后面可以考虑把两者融合，并把路径更新到公共数据库里面<br>
<br>
SCFA: /data/Xianjinyuan/LD_lab/databases/SCFA，分为acetate_protein、butyrate_protein、propionate_protein 三个子库<br>
&emsp;scfa kegg genes.xlsx 是我们内部整理的gene list ； http://fungene.cme.msu.edu/scfa/browse.jsp 是刘红宾提供的源数据库网址 <br>
<br>
特定代谢酶: 肠道菌：酪氨酸脱羧酶TyrDC，Futc岩藻糖转移酶；植物菌：8-羟基喹啉代谢酶；IAA代谢基因簇<br>
&emsp;  a)8-羟基喹啉代谢酶&emsp;/home/nihaoran/blastp/8_hydroxy/8_hydroxy<br>
&emsp;  b)喹啉2-氧化酶&emsp;/home/nihaoran/blastp/quinoline/uniprot_quinoline+2_oxidoreductase<br>
&emsp;  c)喹啉4-氧化基因簇&emsp;/home/nihaoran/blastp/quinaldine_4_oxidase/quinaldine_4_oxidase<br>
&emsp;  d)IAA代谢基因簇&emsp;/home/nihaoran/blastp/lac_gut/iac<br>
&emsp;  e)α-1,2-岩藻糖转移酶&emsp;/home/nihaoran/blastp/HMO/FUTC<br>
&emsp;  f)酪氨酸脱羧酶  /home/nihaoran/blastp/L_Dopa_MBGC<br>
<br>
噬菌体裂解酶：收集了信息，但是还没整理<br>
<br>
其他功能有待补充 <br>
可参考FunGene：http://fungene.cme.msu.edu/index.spr;jsessionid=E5A3AC6093A533638C9B89D0B7347F6E.10.0.0.29<br>
<br>

## 解读PPT
特定代谢基因注释.pptx

# 代码例子
参考blastp_func_anno-VFDB模块里的： Functional annotation using diamond(blastp) 

## Notes

方法逻辑：

对prokka得到的蛋白序列，先对特殊功能的蛋白列表进行diamond建库，然后用diamond进行匹配。<br>


## How to run

The ENV should have the required python libraries in the python script and the seqkit

```
conda activate /home/chenjunyu/miniconda3/envs/anno/
python /data/Xianjinyuan/tanyuxiang/YT_scripts/blastp_func_anno.py -i . -o 输出目录 -db 数据库路径 -pi 50 -cov 50 -p faa
```

Key optional parameters:

```
-x 需要识别的文件后缀名,因为脚本是文件夹内遍历的模式，必须确定这个后缀是能唯一识别对象文件的。
-p 标注是否蛋白序列，默认是False，任何其他字符串都会被认为是True。主要用于注释WGS的基因时，通过prokka的faa蛋白文件，就不需要再跑第一步骤了。
```

### Results:

output文件夹内，主要有用的是final_out文件夹，每个样品一个文件；每个文件两列：基因编号，功能编号

还有All_samples_features_out.csv，是所有样品的集合

#### Former ENV building note:
```
conda activate anno
conda install -c bioconda seqkit
```

#### database generation example
```
diamond makedb --in seq.faa --db database_name
```
seq.faa是要提前准备好的数据格式:faa 或者fasta，实际就是注释一行，蛋白序列一行。<br>
例子：<br>
```
cd /data/Xianjinyuan/LD_lab/databases/SCFA
diamond makedb --in acetate_protein.fasta --db acetate_protein
diamond makedb --in butyrate_protein.fasta --db butyrate_protein
diamond makedb --in propionate_protein.fasta --db propionate_protein
```

## 注意事项

## 测试数据例子

## 后续需要测试和改良的地方
1. 目前blastp用的参数是--max-target-seqs 1，而不是-max_hsps 1，可能会对结果有影响，需要进一步核对
2. 数据库需要进一步补充并整理到公有库
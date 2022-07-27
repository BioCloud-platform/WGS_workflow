# 特定代谢基因
实际上就是我们内部针对特别感兴趣的功能所自建的数据库

## 主要分类及对应的数据库路径：
原核生物的KEGG: /home/chenjunyu/databases/kegg/prokaryotes_filter <br>
BileAcide: <br>
    a) bai基因簇、BSH、7aHSDH、7bHSDH : /home/licun/Data/Blastp_0829/ZCH/zch_three_strain/bile_acid <br>
    b) 5AR、5BR、3bHSDH、3aHSDH : /home/licun/Data/Blastp_0829/WGS_LDlab/WGS3.0/muban_seq/BileAcid <br>
    后面可以考虑把两者融合，并把路径更新到公共数据库里面<br>
肠道菌：酪氨酸脱羧酶TyrDC，Futc岩藻糖转移酶；<br>
植物菌：8-羟基喹啉代谢酶；IAA代谢基因簇<br>
SCFA: scfa kegg genes.xlsx 是我们内部整理的gene list ； http://193.175.244.101/Butyrate/ 有序列（匹配https://journals.asm.org/doi/10.1128/msystems.00130-17?permanently=true 的文章   ） <br>
其他功能有待补充 <br>
可参考FunGene：http://fungene.cme.msu.edu/index.spr;jsessionid=E5A3AC6093A533638C9B89D0B7347F6E.10.0.0.29

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
seq.faa是要提前准备好的数据格式

## 注意事项

## 测试数据例子
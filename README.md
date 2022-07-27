# WGS_workflow for 2nd generation NGS
From clean reads to genome with annotations

## 现有指南
WGS_SOP_2022.06.30.docx，但是里面不少步骤没有整合，还需要另外单独运行。因此主要让大家看背景，其里面各部分会逐步整合。

## 主要步骤 
1）组装：unicycler，基本上就是 -1 -2 和 -o 三个参数，例子见子文件夹 <br>
2）质控1：QUAST，主要看N50等统计指标 <br>
3）质控2：checkM，主要看完整性、污染性指标 <br>
4）分类学注释：GTDB-tk<br>
5）基因初步注释：Prokka<br>
6）全面基因功能注释：EggNOG，当前最新的应该是eggNOG-mapper2，当前资料都没整理，参考：https://github.com/xbiome/StrainPanDA/tree/main/custom_db#readme<br>
7）基因通路注释：kofamscan 【这个先不加也行】<br>
8）代谢基因注释<br>
    a) CAZy注释：dbCAN2 【见CAZy_dbCAN2子文件夹，里面的python不是针对snakemake的，整合到snakemake时需要进行修改另外保存在scripts文件夹里，这个原始版本不要改】<br>
    b) 特定代谢基因注释【这个先不加】<br>
9）毒力基因：VFDB 【见blastp_func_anno-VFDB子文件夹】<br>
10）抗性基因：<br>
    a）抗生素抗性：RGI<br>
    b）抗噬菌体抗性：PADLOC【见PADLOC子文件夹】<br>
    c) CRISPR：CRSPRDetect【这个先不加】<br>
11) 水平转移:<br>
    a) digIS转座酶(insertion sequence elements)注释：<br>
    b) mgefinder【这个先不加】<br>
    c) https://pypi.org/project/MobileElementFinder/ 【这个先不加】<br>
12) 其他特性预测<br>
    a) 质粒分析：plasforest<br>
    b）prophage预测：PhiSpy<br>
    c）蛋白的细胞内定位：psortb 【这个先不加】<br>
    d）转运蛋白（TCDB） 【这个先不加】<br>
    e）病原菌与宿主：PHI 【这个先不加】<br>
    d）未来待补充的：耐酸耐碱耐氧、细菌凝集素、革兰氏阴阳性【还需要调研】<br>
13) 基因簇分析：<br>
    a）antiSMASH：次级代谢基因簇（BGC）注释<br>
    b）gutSMASH：肠道菌初级代谢基因簇（MGC）注释<br>
    c）抗性基因的基因簇预测ARTS 【这个先不加】<br>
14）单基因组可视化：CGView （比较简单的命令行，参考：https://github.com/paulstothard/cgview ）<br>

（流程按主要步骤的顺序，细节参考WGS-Pipeline.py文件里，以及SOP里的相关部分）<br>
【每个子项，参考dbCAN2和VFDB的子文件进行创建和补充】<br>


## 代码例子

## 注意事项

## 测试数据例子
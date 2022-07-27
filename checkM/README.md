# checkM

## 使用场景：拼接基因组的污染度和完整度的评估使用
checkM 可以根据基因组在参考基因组发育树中的位置来推断其精确的单拷贝标记基因集（lineage-specificmarker set），同时也提供数据库可用的基于分类学的基因集（taxonomic-specificmarker set）。CheckM利用基因的单拷贝性来有效的估计基因组完整度和污染，同时能绘制基因组关键特征（例如GC含量、编码率）的图像来评估基因组的质量。

## 解读PPT
checkM.pptx

## 代码例子
conda activate /home/chenjunyu/miniconda3/envs/wgs/ <br>
checkm lineage_wf -t 8 -x fna bin folder output folder >checkm.out <br>
根据结果对基因组进行筛选select only genomes that passed the following criteria: >50% genome completeness, <5% contamination and an estimated quality score (completeness–5×contamination)>50。<br>
## 注意事项
CheckM会把完整度和污染度等结果输出到屏幕，因此为了保存结果，建议将输出到屏幕的结果写入到文件中。

## 测试数据例子
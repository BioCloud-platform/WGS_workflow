import pandas 
import numpy 

#file_in="VFDB_merged.tsv"
file_in=snakemake.input.merge_file
#file_out="VFDB_merged_reshape.csv"
file_out=snakemake.output.table_file

df_ori = pandas.read_csv(file_in,dtype=str,sep="\t",header=None) 
df_ori.columns = ["qID","VFDB_ID","pident","length","mismatch","gapopen","qstart","qend","sstart","send","evalue","bitscore"]
df_ori[['SampleID', 'ppID']] = df_ori["qID"].str.split('|', expand = True) #expand 才会出列

df_out = pandas.pivot_table(df_ori,index="VFDB_ID", columns="SampleID", values="bitscore")#, aggfunc="|".join)


#输出带index的df_out
df_out.to_csv(file_out,encoding = 'utf8')

df_out_binary = df_out.copy(deep=True)
df_out_numeric = df_out.copy(deep=True)

for i_row in df_out.index.to_list():
    for i_col in list(df_out):
        if pandas.isnull(df_out[i_col][i_row]):
            df_out_numeric[i_col][i_row]=0
            df_out_binary[i_col][i_row]=0
        else:
            df_out_numeric[i_col][i_row]=len(str(df_out[i_col][i_row]).split("|"))
            df_out_binary[i_col][i_row]=1

df_out_binary.to_csv(file_out+"_binary.csv",encoding = 'utf8')
df_out_numeric.to_csv(file_out+"_numeric.csv",encoding = 'utf8')

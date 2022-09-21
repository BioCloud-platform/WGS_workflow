import pandas 
import numpy 

#file_in="cazy_final_out.csv"
file_in=snakemake.input.merge_file
#file_out="cazy_final_out_reshape.csv"
file_out=snakemake.output.table_file

df_ori = pandas.read_csv(file_in,dtype=str) 

df_out = pandas.pivot_table(df_ori,index="SampleID", columns="CAZy", values="GeneID", aggfunc="|".join)

df_out = df_out[df_out.columns.drop('Conflict')]

df_out_numeric = df_out.copy(deep=True)

df_out_binary = df_out.copy(deep=True)

for i_row in df_out.index.to_list():
    for i_col in list(df_out):
        if pandas.isnull(df_out[i_col][i_row]):
            df_out_numeric[i_col][i_row]=0
            df_out_binary[i_col][i_row]=0
        else:
            df_out_numeric[i_col][i_row]=len(df_out[i_col][i_row].split("|"))
            df_out_binary[i_col][i_row]=1


#输出带index的df_out
df_out.to_csv(file_out,encoding = 'utf8')

df_out_numeric.to_csv(file_out+"_numeric.csv",encoding = 'utf8')

df_out_binary.to_csv(file_out+"_binary.csv",encoding = 'utf8')

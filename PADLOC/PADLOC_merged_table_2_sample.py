import pandas 
import numpy 

#file_in="PADLOC_merged.csv"
file_in=snakemake.input.merge_file
#file_out_sys="PADLOC_merged_reshape_system.csv"
file_out_sys=snakemake.output.table_file_sys
#file_out_protein ="PADLOC_merged_reshape_protein.csv"
file_out_protein =snakemake.output.table_file_protein

df_ori = pandas.read_csv(file_in,dtype=str) 
col_names = list(df_ori)
col_names[0] = "qID"
df_ori.columns = col_names

df_ori[['SampleID', 'ppID']] = df_ori["qID"].str.split('|', expand = True) #expand 才会出列

#target.name 是value， system 和 protein.name 分别是两个层次的列名
df_out_sys = pandas.pivot_table(df_ori,index="SampleID", columns="system", values="target.name", aggfunc="|".join)
df_out_protein = pandas.pivot_table(df_ori,index="SampleID", columns="protein.name", values="target.name", aggfunc="|".join)

df_out_sys = df_out_sys[df_out_sys.columns.drop('system')]
df_out_protein = df_out_protein[df_out_protein.columns.drop('protein.name')]


def numer_table(df_out,df_out_numeric,df_out_binary):
    pass
    for i_row in df_out.index.to_list():
        for i_col in list(df_out):
            if pandas.isnull(df_out[i_col][i_row]):
                df_out_numeric[i_col][i_row]=0
                df_out_binary[i_col][i_row]=0
            else:
                df_out_numeric[i_col][i_row]=len(df_out[i_col][i_row].split("|"))
                df_out_binary[i_col][i_row]=1
    return(df_out,df_out_numeric,df_out_binary)

df_out_sys_numeric = df_out_sys.copy(deep=True)

df_out_sys_binary = df_out_sys.copy(deep=True)

df_out_sys_all = numer_table(df_out_sys, df_out_sys_numeric,df_out_sys_binary)
#输出带index的df_out_sys
df_out_sys.to_csv(file_out_sys,encoding = 'utf8')

df_out_sys_numeric.to_csv(file_out_sys+"_numeric.csv",encoding = 'utf8')

df_out_sys_binary.to_csv(file_out_sys+"_binary.csv",encoding = 'utf8')


df_out_protein_numeric = df_out_protein.copy(deep=True)

df_out_protein_binary = df_out_protein.copy(deep=True)

df_out_protein_all = numer_table(df_out_protein, df_out_protein_numeric,df_out_protein_binary)
#输出带index的df_out_protein
df_out_protein.to_csv(file_out_protein,encoding = 'utf8')

df_out_protein_numeric.to_csv(file_out_protein+"_numeric.csv",encoding = 'utf8')

df_out_protein_binary.to_csv(file_out_protein+"_binary.csv",encoding = 'utf8')


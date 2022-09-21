import pandas 
import numpy 

#file_in="merged.tsv"
file_in=snakemake.input.merge_file
#file_out="PhiSpy_merged_reshape.csv"
file_out=snakemake.output.table_file

df_ori = pandas.read_csv(file_in,dtype=str,sep="\t",header=None) 
df_ori.columns = ["ID","contig","Start_phage","Stop_phage","Start_attL","Stop_attL","Start_attR","Stop_attR","Seq_attL","Seq_attR","Anno"]
df_ori[['SampleID', 'ppID']] = df_ori["ID"].str.split('|', expand = True) #expand 才会出列
df_ori[["Start_phage","Stop_phage","Start_attL","Stop_attL","Start_attR","Stop_attR"]] = df_ori[["Start_phage","Stop_phage","Start_attL","Stop_attL","Start_attR","Stop_attR"]].astype('float')
df_ori.eval('Length = Stop_phage - Start_phage' , inplace=True)
df_ori['Seq_att']=df_ori['Seq_attL']+"|"+df_ori['Seq_attR']

#col_out = df_ori["Seq_att"].drop_duplicates().to_list()
#index_out = df_ori["SampleID"].drop_duplicates().to_list()
#df_out = pd.DataFrame(columns=col_out, index=index_out)

df_out = pandas.pivot_table(df_ori,index="Seq_att", columns="SampleID", values="Length")#, aggfunc="|".join)


#输出带index的df_out
df_out.to_csv(file_out,encoding = 'utf8')


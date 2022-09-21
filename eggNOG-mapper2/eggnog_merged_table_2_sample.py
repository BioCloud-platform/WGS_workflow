import pandas 
import numpy 

#file_in="eggnog_merged.tsv"
file_in=snakemake.input.merge_file
#file_out_head="eggnog_merged_reshape"
file_out_head=snakemake.params.table_file

df_ori = pandas.read_csv(file_in,dtype=str,sep="\t",header=None) 
df_ori.columns = ["qID",'seed_ortholog','evalue','score','eggNOG_OGs','max_annot_lvl','COG_category','Description','Preferred_name','GOs','EC','KEGG_ko','KEGG_Pathway','KEGG_Module','KEGG_Reaction','KEGG_rclass','BRITE','KEGG_TC','CAZy','BiGG_Reaction','PFAMs']
df_ori[['SampleID', 'ppID']] = df_ori["qID"].str.split('|', expand = True) #expand 才会出列

df_out_eggNOG_OGs = pandas.pivot_table(df_ori,index="eggNOG_OGs", columns="SampleID", values="ppID", aggfunc="|".join) #unique
df_out_COG_category = pandas.pivot_table(df_ori,index="COG_category", columns="SampleID", values="ppID", aggfunc="|".join) #unique
df_out_Description = pandas.pivot_table(df_ori,index="Description", columns="SampleID", values="ppID", aggfunc="|".join) #unique
df_out_Preferred_name = pandas.pivot_table(df_ori,index="Preferred_name", columns="SampleID", values="ppID", aggfunc="|".join) #unique
df_out_GOs = pandas.pivot_table(df_ori,index="GOs", columns="SampleID", values="ppID", aggfunc="|".join)
df_out_EC = pandas.pivot_table(df_ori,index="EC", columns="SampleID", values="ppID", aggfunc="|".join)
df_out_KEGG_ko = pandas.pivot_table(df_ori,index="KEGG_ko", columns="SampleID", values="ppID", aggfunc="|".join)
df_out_KEGG_Pathway = pandas.pivot_table(df_ori,index="KEGG_Pathway", columns="SampleID", values="ppID", aggfunc="|".join)
df_out_KEGG_Module = pandas.pivot_table(df_ori,index="KEGG_Module", columns="SampleID", values="ppID", aggfunc="|".join)
df_out_KEGG_Reaction = pandas.pivot_table(df_ori,index="KEGG_Reaction", columns="SampleID", values="ppID", aggfunc="|".join)
df_out_KEGG_rclass = pandas.pivot_table(df_ori,index="KEGG_rclass", columns="SampleID", values="ppID", aggfunc="|".join)
df_out_BRITE = pandas.pivot_table(df_ori,index="BRITE", columns="SampleID", values="ppID", aggfunc="|".join)
df_out_KEGG_TC = pandas.pivot_table(df_ori,index="KEGG_TC", columns="SampleID", values="ppID", aggfunc="|".join)
df_out_CAZy = pandas.pivot_table(df_ori,index="CAZy", columns="SampleID", values="ppID", aggfunc="|".join)
df_out_BiGG_Reaction = pandas.pivot_table(df_ori,index="BiGG_Reaction", columns="SampleID", values="ppID", aggfunc="|".join)
df_out_PFAMs = pandas.pivot_table(df_ori,index="PFAMs", columns="SampleID", values="ppID", aggfunc="|".join)

#对唯一的表，把"-"和index名字本身的行去掉
#df_out_eggNOG_OGs=df_out_eggNOG_OGs[df_out_eggNOG_OGs.columns.drop("-")]
df_out_COG_category=df_out_COG_category.T[df_out_COG_category.T.columns.drop("-")].T
df_out_Description=df_out_Description.T[df_out_Description.T.columns.drop("-")].T
df_out_Preferred_name=df_out_Preferred_name.T[df_out_Preferred_name.T.columns.drop("-")].T

def find_str(list_str,str_to_find):
    ori_count=0
    example_dict=dict()
    for i_str in range(len(list_str)):
        if str(list_str[i_str]).lower().find(str_to_find.lower())!= -1:
            ori_count=ori_count+1
            example_dict[list_str[i_str]] = i_str
    return ori_count,example_dict

#把重名的列进行移除
def remove_dup_columns(frame):
    keep_names = set()
    keep_icols = list()
    name_icols_dict = dict()
    for icol, name in enumerate(frame.columns):
        if name not in keep_names:
            keep_names.add(name)
            keep_icols.append(icol)
            name_icols_dict[name] = icol
        else:
            #把新一列的结果加到原列里去
            frame.iloc[:, name_icols_dict[name]]=merge_two_columns(frame,name_icols_dict,name,icol)
    return frame.iloc[:, keep_icols]

def merge_two_columns(frame,name_icols_dict,name,icol):
    new_column = frame.iloc[:, name_icols_dict[name]].to_list()
    dup_column = frame.iloc[:, icol].to_list()
    for i_col in range(len(new_column)):
        if not pandas.isnull(dup_column[i_col]):
            if pandas.isnull(new_column[i_col]):
                new_column[i_col]=dup_column[i_col]
            else:
                if not new_column[i_col]==dup_column[i_col]:
                    new_column[i_col]=new_column[i_col]+"|"+dup_column[i_col]
    return new_column

#对名字中含有","的行进行拆分
def clean_complex_columns(frame):
    T_frame = frame.T
    T_frame_row_names = list(frame)
    T_frame_col_names = list(T_frame)
    complex_turple = find_str(T_frame_col_names,",")
    out_count = complex_turple[0]
    out_dict = complex_turple[1]
    out_col = list(out_dict.keys())
    #释放里面的内容
    for i_col in out_col:
        sub_col = i_col.split(",")
        new_frame = pandas.DataFrame([T_frame[i_col].to_list()]*len(sub_col)).T
        new_frame.columns = sub_col
        new_frame.index = T_frame_row_names
        T_frame = pandas.concat([T_frame, new_frame], axis=1)
    T_frame=remove_dup_columns(T_frame)
    T_frame=T_frame[T_frame.columns.drop(out_col)] #对于大矩阵，这个似乎居然是个瓶颈，会跑非常非常久，有点难以理解.本来df_out_GOs10分钟内能跑完的，就是这个没先remove_dup_columns的话，跑了48小时都没跑完。
    T_frame=T_frame[T_frame.columns.drop("-")]
    return T_frame.T

df_out_GOs=clean_complex_columns(df_out_GOs) 

#输出带index的df_out
def df_out_write(df_out,file_out):
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
    df_out.to_csv(file_out+".csv",encoding = 'utf8')
    df_out_binary.to_csv(file_out+"_binary.csv",encoding = 'utf8')
    df_out_numeric.to_csv(file_out+"_numeric.csv",encoding = 'utf8')

df_out_write(df_out_eggNOG_OGs,file_out_head+"_eggNOG_OGs")
df_out_write(df_out_COG_category,file_out_head+"_COG_category")
df_out_write(df_out_Description,file_out_head+"_Description")
df_out_write(df_out_Preferred_name,file_out_head+"_Preferred_name")
df_out_write(df_out_GOs,file_out_head+"_GOs")
print("GOs done")

df_out_EC=clean_complex_columns(df_out_EC)
df_out_write(df_out_EC,file_out_head+"_EC")
print("_EC done")
df_out_KEGG_ko=clean_complex_columns(df_out_KEGG_ko)
df_out_write(df_out_KEGG_ko,file_out_head+"_KEGG_ko")
print("_KEGG_ko done")
df_out_KEGG_Pathway=clean_complex_columns(df_out_KEGG_Pathway) 
df_out_write(df_out_KEGG_Pathway,file_out_head+"_KEGG_Pathway")
print("_KEGG_Pathway done")
df_out_KEGG_Module=clean_complex_columns(df_out_KEGG_Module)
df_out_write(df_out_KEGG_Module,file_out_head+"_KEGG_Module")
print("_KEGG_Module done")
df_out_KEGG_Reaction=clean_complex_columns(df_out_KEGG_Reaction)
df_out_write(df_out_KEGG_Reaction,file_out_head+"_KEGG_Reaction")
print("_KEGG_Reaction done")
df_out_KEGG_rclass=clean_complex_columns(df_out_KEGG_rclass)
df_out_write(df_out_KEGG_rclass,file_out_head+"_KEGG_rclass")
print("_KEGG_rclass done")
df_out_BRITE=clean_complex_columns(df_out_BRITE) 
df_out_write(df_out_BRITE,file_out_head+"_BRITE")
print("_BRITE done")
df_out_KEGG_TC=clean_complex_columns(df_out_KEGG_TC)
df_out_write(df_out_KEGG_TC,file_out_head+"_KEGG_TC")
print("_KEGG_TC done")
df_out_CAZy=clean_complex_columns(df_out_CAZy)
df_out_write(df_out_CAZy,file_out_head+"_CAZy")
print("_CAZy done")
df_out_BiGG_Reaction=clean_complex_columns(df_out_BiGG_Reaction)
df_out_write(df_out_BiGG_Reaction,file_out_head+"_BiGG_Reaction")
print("_BiGG_Reaction done")
df_out_PFAMs=clean_complex_columns(df_out_PFAMs)
df_out_write(df_out_PFAMs,file_out_head+"_PFAMs")
print("_PFAMs done")

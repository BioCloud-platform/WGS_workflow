import os
import pandas 
import numpy 
import argparse

parser = argparse.ArgumentParser(description='CAZy annotations reshape')
parser.add_argument('-i', '--input', dest='InF', type=str, required=True,
                    help="the path of the merge file")
parser.add_argument('-o', '--output', dest='OutF', type=str, required=True,
                    help="the output path of the reshape file")
args = parser.parse_args()

#file_in="cazy_final_out.csv"
file_in=os.path.abspath(args.InF)
#file_out="cazy_final_out_reshape.csv"
file_out=os.path.abspath(args.OutF)

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


col_names = list(df_out)

dupe_map = {}

for header in col_names:
    parts = header.split('+')
    for part in parts:
        dupe_map.setdefault(part, []).append(header)

dupe_columns = list(dupe_map.keys())
df_new = pandas.DataFrame(index=df_out.index,columns=dupe_columns)
df_new_numeric = df_new.copy(deep=True)
df_new_binary = df_new.copy(deep=True)

for i_row in df_new.index.to_list():
    for i_col in list(df_new):
        values = df_out.loc[i_row,dupe_map[i_col]].tolist()
        valid_values = [v for v in values if not pandas.isna(v)]
        if len(valid_values) == 0:
            df_new[i_col][i_row] = numpy.nan
        else:
            df_new[i_col][i_row] = "|".join(valid_values)
        if pandas.isnull(df_new[i_col][i_row]):
            df_new_numeric[i_col][i_row]=0
            df_new_binary[i_col][i_row]=0
        else:
            df_new_numeric[i_col][i_row]=len(df_new[i_col][i_row].split("|"))
            df_new_binary[i_col][i_row]=1

df_new.T.to_csv(file_out.replace(".csv", "")+"_regrouped.csv",encoding = 'utf8')

df_new_numeric.T.to_csv(file_out.replace(".csv", "")+"_regrouped_numeric.csv",encoding = 'utf8')

df_new_binary.T.to_csv(file_out.replace(".csv", "")+"_regrouped_binary.csv",encoding = 'utf8')

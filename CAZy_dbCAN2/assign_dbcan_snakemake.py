'''
Copyright {2020} Junyu Chen

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

#updata log
#2022-05-20 by Yuxiang Tan
#add the checkpoint of the seqID format in seqFilter function to avoid error when processing WGS genes.
#add the parameter of faa, for WGS genes should use the faa file directly rather than running SeqkitTranslate
#update the way to get sample infor in the data processing section

#updata log
#2022-09-05 by Yuxiang Tan
#Clean up run_dbcan.py, which was run by snakemake
#update the output processing for dbcan3, which is using eCAMI instead of Hotpep
#modified for the use of snakemake.

#updata log
#2023-08-26 by Yuxiang Tan
#modified for the use back to python, because of the general usage need.


import os
import re
import argparse
import subprocess
import pandas as pd
#from itertools import repeat
#from multiprocessing import Pool, freeze_support

## parse dbCAN result
def parseDbcan(dbcanDir):
    filePathList = []
    frames = []
    dirs = [dI for dI in os.listdir(dbcanDir) if os.path.isdir(os.path.join(dbcanDir,dI))]
    #print(dirs)
    for dir in dirs:
        filePath = os.path.join(dbcanDir, dir, "overview.txt")
        #print(filePath)
        if os.path.getsize(filePath) > 0:
            df_f=pd.read_table(filePath)
            df_f["SampleID"]=dir
            frames.append(df_f)
    df_concat = pd.concat(frames)
    return df_concat


# Function to clean the names 
def Clean_names(CAZy_name): 
    # Search for opening bracket in the name followed by 
    # any characters repeated any number of times 
    if re.search('\(.*', CAZy_name): 
        # Extract the position of beginning of pattern 
        pos = re.search('\(.*', CAZy_name).start() 
        # return the cleaned name 
        return CAZy_name[:pos] 
    else: 
        # if clean up needed return the same name 
        return CAZy_name 
# Function to clean hmm names 
def Clean_hmm_names(CAZy_name): 
    CAZy_name = str(CAZy_name).split("_")[0]
    return CAZy_name
def removeTail(string):
    pattern = "_frame=" + r'[0-9]'
    # Match all digits in the string and replace them by empty string
    mod_string = re.sub(pattern, '', string)
    return mod_string


parser = argparse.ArgumentParser(description='CAZy annotations')
parser.add_argument('-i', '--input', dest='InDir', type=str, required=True,
                    help="the path of the CAZy folder")
parser.add_argument('-o', '--output', dest='OutF', type=str, required=True,
                    help="the output path of merge file")
args = parser.parse_args()

InDir = os.path.abspath(args.InDir)
OutF = os.path.abspath(args.OutF)


#####data processing####################
#df_concat = parseDbcan(snakemake.input.dbcanDir)
df_concat = parseDbcan(InDir)
df = df_concat.loc[df_concat["#ofTools"] >= 2]
df.loc[:, 'HMMER'] = df['HMMER'].apply(Clean_names)
df.loc[:, 'eCAMI'] = df['eCAMI'].apply(Clean_names)
df.loc[:, 'HMMER'] = df['HMMER'].apply(Clean_hmm_names)
df = df.reset_index()

#rename
for i in range(len(df)):
    if df.loc[i, "HMMER"] == "-":
        if df.loc[i, "eCAMI"] == df.loc[i, "DIAMOND"]: 
            df.loc[i, "cazy"] = df.loc[i, "eCAMI"]
        else:
            df.loc[i, "cazy"] = "Conflict"
    else:
        if df.loc[i, "HMMER"] == df.loc[i, "eCAMI"]: 
            df.loc[i, "cazy"] = df.loc[i, "HMMER"]
        else:
            if df.loc[i, "HMMER"] == df.loc[i, "DIAMOND"]: 
                df.loc[i, "cazy"] = df.loc[i, "HMMER"]
            else:
                if df.loc[i, "eCAMI"] == df.loc[i, "DIAMOND"]: 
                    df.loc[i, "cazy"] = df.loc[i, "eCAMI"]
                else:
                    df.loc[i, "cazy"] = "Conflict"

#for contig import, removeTail is misleading, but for CDS, it maybe necessary
#df["GeneID"] = df["Gene ID"].apply(removeTail)
#df = df.drop_duplicates(subset=['GeneID'], keep='first')
#final out for all the samples together
final = pd.DataFrame()
final["SampleID"] = df["SampleID"]
final["GeneID"] = df["Gene ID"]
final["CAZy"] = df["cazy"]
#final.to_csv(snakemake.output.merge_file, index=None)
final.to_csv(OutF, index=None)

#sep output for each sample
sampleList = list(df["SampleID"].unique())
for sample in sampleList:
    df1 = pd.DataFrame()
    df2 = final[final["SampleID"] == sample]
    df1["GeneID"] = df2["GeneID"]
    df1["CAZy"] = df2["CAZy"]
    #df1.to_csv(os.path.join(snakemake.input.dbcanDir, sample + ".csv"), index=None)
    df1.to_csv(os.path.join(InDir, sample + ".csv"), index=None)

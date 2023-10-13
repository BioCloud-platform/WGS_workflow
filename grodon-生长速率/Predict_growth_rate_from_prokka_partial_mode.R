#   Copyright {2023} Yuxiang Tan
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

library("gRodon")
library("Biostrings")

#this script is to run gRodon from the prokka annotation file for each prokaryote genome at patrial mode (which excludes pair-bias from the prediction )

#check arguments
for (e in commandArgs()) {
        ta = strsplit(e,"=",fixed=TRUE)
        if(! is.na(ta[[1]][2])) {
                temp = ta[[1]][2]
                if(substr(ta[[1]][1],nchar(ta[[1]][1]),nchar(ta[[1]][1])) == "I") {
                temp = as.integer(temp)
                }
        if(substr(ta[[1]][1],nchar(ta[[1]][1]),nchar(ta[[1]][1])) == "N") {
                temp = as.numeric(temp)
                }
        assign(ta[[1]][1],temp)
        } else {
        assign(ta[[1]][1],TRUE)
        }
}

#check whether file in is exist
if (!exists("path_to_genome")) {
    stop("\n\nWarning: Usage: the parameter path_to_genome is not given. \n\n")
}

if (!exists("sample_name")) {
    stop("\n\nWarning: Usage: the parameter sample_name is not given. \n\n")
}

if (!exists("path_to_outtb")) {
    stop("\n\nWarning: Usage: the parameter path_to_outtb is not given. \n\n")
}


#check whether the file is exist
if (!file.exists(path_to_genome)) {
    stop(paste("\nRscript Predict_growth_rate_from_prokka_partial_mode.R path_to_genome=",path_to_genome," \nWarning: Usage: the genome path is not exist, please check the path. \n\n",sep=""))
}

#path_to_genome="/mnt/Xianjinyuan/tanyuxiang/1-projects/prophage_detection/IMGG/prokka_test/A102.bin_10/A102.bin_10.ffn"
#sample_name = "A102.bin_10"
genes <- readDNAStringSet(path_to_genome)
highly_expressed <- grepl("ribosomal protein",names(genes),ignore.case = T)
out_predict = predictGrowth(genes, highly_expressed, mode="partial")
out_tb <- data.frame(out_predict)
rownames(out_tb) <- sample_name
write.table(out_tb, file=(path_to_outtb),sep=",", quote=F, row.names= TRUE, col.names= TRUE, fileEncoding="UTF-8" )

















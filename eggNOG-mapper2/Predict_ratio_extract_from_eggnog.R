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

library("stringr")

#this script is to extract unannotated ratio from the eggnog annotation file

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
if (!exists("file_in")) {
    stop("\n\nWarning: Usage: the parameter file_in is not given. \n\n")
}

if (!exists("sample_name")) {
    stop("\n\nWarning: Usage: the parameter sample_name is not given. \n\n")
}


#check whether the file is exist
if (!file.exists(file_in)) {
    stop(paste("\nRscript Predict_ratio_extract_from_eggnog file_in=",file_in," \nWarning: Usage: the input matrix is not exist, please check the path. \n\n",sep=""))
}


#file_in <- "/data/Xianjinyuan/LD_lab/public_datasets/culturomics_datasets/public_MAGs/PRJEB39057_eggnog2/S52T80_bins.89.STRAINS.emapper.annotations"
#sample_name <- "S52T80_bins.89"
eggnog_tsv <- read.table(file_in, sep='\t',colClasses = "character",comment.char = "", quote="", header=FALSE) #quote is very important in reading functional annotation files

COG_emp = subset(eggnog_tsv, eggnog_tsv[,"V7"] == "-") #get the most possible empty annotations.
COG_emp_ann <- COG_emp[,7:21] # double check whether they are all empty
check_emp <- function(list){
    if(sum(list=="-")==15){
        #sum==15 means all "-"
        emp_stat=TRUE
    }else{
        emp_stat=FALSE
    }
    return(emp_stat)
}

emp_anno_rows<-sum(apply(COG_emp_ann,1,check_emp))

hypothetical_rate <- emp_anno_rows/dim(eggnog_tsv)[1]

out_line <- paste(sample_name,as.character(hypothetical_rate),emp_anno_rows,dim(eggnog_tsv)[1],sep="\t") # header: sample_name, empty_rate, empty_num, total_gene_num

cat(paste0(out_line,"\n"),file=paste0(file_in,".hypo_rate.tsv"))












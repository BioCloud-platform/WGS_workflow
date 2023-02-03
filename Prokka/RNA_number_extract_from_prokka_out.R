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

#this script is to extract tRNA and rRNA numbers from the prokka tsv file

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
    stop(paste("\nRscript RNA_number_extract_from_prokka_out.R file_in=",file_in," \nWarning: Usage: the input matrix is not exist, please check the path. \n\n",sep=""))
}


#file_in <- "/data/Xianjinyuan/LD_lab/public_datasets/culturomics_datasets/115.genomes_hGMB_LC_prokka/Taxon_100.genome/Taxon_100.genome.tsv"
#sample_name <- "Taxon_100.genome"
prokka_tsv <- read.table(file_in, sep='\t',colClasses = "character",comment.char = "", quote="", header=TRUE) #quote is very important in reading functional annotation files
tRNA_list <- unique(str_split(unique(prokka_tsv[which(prokka_tsv[,"ftype"]=="tRNA"),"product"]),fixed("("),simplify=TRUE)[,1])
rRNA_list <- prokka_tsv[which(prokka_tsv[,"ftype"]=="rRNA"),"product"]
rRNA5S_list <- rRNA_list[which(grepl("5S",rRNA_list))]
rRNA16S_list <- rRNA_list[which(grepl("16S",rRNA_list))]
rRNA23S_list <- rRNA_list[which(grepl("23S",rRNA_list))]

out_line <- paste(sample_name,as.character(length(rRNA5S_list)),as.character(length(rRNA16S_list)),as.character(length(rRNA23S_list)),as.character(length(tRNA_list)),sep="\t")

cat(paste0(out_line,"\n"),file=paste0(file_in,".trRNA_counts.tsv"))












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


#this script is to merge plasmer result with seqkit tab to generate general stat (sample_name,contigs_num,full_length,plamid_num,plamid_content,plamid_length,plamid_length_content)
#Usage: Rscript plasmer_result_stat.R path_to_plasmer= path_to_seqkit= sample_name= path_to_outtb= path_to_outstat=

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
if (!exists("path_to_plasmer")) {
    stop("\n\nWarning: Usage: the parameter path_to_plasmer is not given. \n\n")
}

if (!exists("path_to_seqkit")) {
    stop("\n\nWarning: Usage: the parameter path_to_seqkit is not given. \n\n")
}

if (!exists("sample_name")) {
    stop("\n\nWarning: Usage: the parameter sample_name is not given. \n\n")
}

if (!exists("path_to_outtb")) {
    stop("\n\nWarning: Usage: the parameter path_to_outtb is not given. \n\n")
}

if (!exists("path_to_outstat")) {
    stop("\n\nWarning: Usage: the parameter path_to_outstat is not given. \n\n")
}

#check whether the file is exist
if (!file.exists(path_to_plasmer)) {
    stop(paste("\nRscript plasmer_result_stat.R path_to_plasmer=",path_to_plasmer," \nWarning: Usage: the plasmer.predClass.tsv path is not exist, please check the path. \n\n",sep=""))
}

if (!file.exists(path_to_seqkit)) {
    stop(paste("\nRscript plasmer_result_stat.R path_to_seqkit=",path_to_seqkit," \nWarning: Usage: the fa2tab.tsv path is not exist, please check the path. \n\n",sep=""))
}

# path_to_plasmer="/data/Xianjinyuan/LD_lab/public_datasets/culturomics_datasets/public_isolate_proj/miBC_others_plasmer/GCF_000364185.2_ASM36418v2_genomic/results/GCF_000364185.2_ASM36418v2_genomic.plasmer.predClass.tsv"
# path_to_seqkit="/data/Xianjinyuan/LD_lab/public_datasets/culturomics_datasets/public_isolate_proj/miBC_others_seqkit/GCF_000364185.2_ASM36418v2_genomic.fa2tab.tsv"
# path_to_outtb="/data/Xianjinyuan/LD_lab/public_datasets/culturomics_datasets/public_isolate_proj/miBC_others_plasmid_stat/GCF_000364185.2_ASM36418v2_genomic.merged.csv"
# sample_name = "GCF_000364185.2_ASM36418v2_genomic"
#path_to_outstat=gsub(".merged.csv",".stat.csv",path_to_outtb)

plasmer_out <- read.table(path_to_plasmer)
colnames(plasmer_out) <- c("ID","predClass")

seqkit_out <- read.table(path_to_seqkit)
colnames(seqkit_out) <- c("ID","length","GC", "GC-Skew", "A-count", "T-count", "C-count", "G-count", "N-count")

merge_out <- merge(plasmer_out,seqkit_out)
write.table(merge_out, file=(path_to_outtb),sep=",", quote=F, row.names= FALSE, col.names= TRUE, fileEncoding="UTF-8" )

contigs_num <- nrow(seqkit_out)
full_length <- sum(merge_out$length)
plamid_num <- sum(merge_out$predClass =="plasmid")
plamid_content <- plamid_num/contigs_num
plamid_length <- sum(merge_out[which(merge_out$predClass =="plasmid"), "length"])
plamid_length_content <- plamid_length/full_length
table_stat <- paste(sample_name,contigs_num,full_length,plamid_num,plamid_content,plamid_length,plamid_length_content,sep=",")
write.table(table_stat, file=(path_to_outstat),sep=",", quote=F, row.names= FALSE, col.names= FALSE, fileEncoding="UTF-8" )












#create log:202320603
#Objective: To summary the RGI result into class with  counts

#usage example: Rscript /data/Xianjinyuan/tanyuxiang/YT_scripts/RGI_result_summary.R rgi_file= aro_index_f= sample_name= out_name=
#the output will five csv files per strain

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

#check whether the file in para is exist
if (!exists("rgi_file")) {
    stop(paste("\nRscript RGI_result_summary.R rgi_file=",rgi_file," \nWarning: Usage: The rgi_file para is not given, please check the input para. \n\n",sep=""))
}

if (!exists("aro_index_f")) {
    stop(paste("\nRscript RGI_result_summary.R aro_index_f=",aro_index_f," \nWarning: Usage: The aro_index_f para is not given, please check the input para. \n\n",sep=""))
}

if (!exists("sample_name")) {
    stop(paste("\nRscript RGI_result_summary.R sample_name=",sample_name," \nWarning: Usage: sample_name  para is not given, please check the input para. \n\n",sep=""))
}

if (!exists("out_name")) {
    stop(paste("\nRscript RGI_result_summary.R out_name=",out_name," \nWarning: Usage: out_name  para is not given, please check the input para. \n\n",sep=""))
}

#check whether the file in is exist
if (!file.exists(rgi_file)) {
    stop(paste("\nRscript RGI_result_summary.R rgi_file=",rgi_file," \nWarning: Usage: The RGI output file is not exist, please check the path. \n\n",sep=""))
}

if (!file.exists(aro_index_f)) {
    stop(paste("\nRscript RGI_result_summary.R aro_index_f=",aro_index_f," \nWarning: Usage: The aro_index from the CARD database is not exist, please check the path. \n\n",sep=""))
}


#rgi_file = "RGI/3353001_submission.assembly.txt"
#aro_index_f = "aro_index.tsv"
#sample_name ="3353001_submission.assembly"
#out_name = "3353001_submission.assembly"

rgi_matr <- read.table(rgi_file,comment.char="",na.strings = c("NA","NAN"),sep="\t",header=TRUE,fill=TRUE, quote ="")
aro_matr <- read.table(aro_index_f,comment.char="",na.strings = c("NA","NAN"),sep="\t",header=TRUE,fill=TRUE, quote ="")

rgi_features <- c("ARO.Accession","ARO.Name","AMR.Gene.Family","Drug.Class","Resistance.Mechanism")
aro_matr_deduplicate <- unique(aro_matr[,rgi_features]) # to deduplicate
rownames(aro_matr_deduplicate) <- aro_matr_deduplicate[,"ARO.Accession"]

if (dim(rgi_matr)[1]>0){
    ARO_ID_list <-paste0("ARO:",rgi_matr[,"ARO"]) # the format of RGI output is somehow different from the database file

    rgi_matr_extract <- aro_matr_deduplicate[ARO_ID_list,]

    for (rgi_name in rgi_features){
        feature_matr<- matrix(0,nrow=1,ncol=length(unique(aro_matr_deduplicate[,rgi_name])))
        colnames(feature_matr) <- unique(aro_matr_deduplicate[,rgi_name])
        feature_summary<- summary(as.factor(rgi_matr_extract[,rgi_name]),maxsum=length(levels(as.factor(rgi_matr_extract[,rgi_name]))))
        feature_matr[,names(feature_summary)] <- feature_summary
        rownames(feature_matr)<-sample_name
        write.csv(feature_matr,paste0(out_name,"_",rgi_name,".csv"),quote=FALSE)
    }
} else{
    for (rgi_name in rgi_features){
        feature_matr<- matrix(0,nrow=1,ncol=length(unique(aro_matr_deduplicate[,rgi_name])))
        colnames(feature_matr) <- unique(aro_matr_deduplicate[,rgi_name])
        rownames(feature_matr)<-sample_name
        write.csv(feature_matr,paste0(out_name,"_",rgi_name,".csv"),quote=FALSE)
    }
}

# Test example:
# Drug.Class_matr<- matrix(0,nrow=1,ncol=length(unique(aro_matr_deduplicate[,"Drug.Class"])))
# colnames(Drug.Class_matr) <- unique(aro_matr_deduplicate[,"Drug.Class"])
# Drug.Class_summary<- summary(as.factor(rgi_matr_extract[,"Drug.Class"]))
# Drug.Class_matr[,names(Drug.Class_summary)] <- Drug.Class_summary
# rownames(Drug.Class_matr)<-sample_name
# write.csv(Drug.Class_matr,paste0(out_name,"_","Drug.Class",".csv"))

# Drug.Class_summary<- summary(as.factor(rgi_matr_extract[,"Drug.Class"]))
# Resistance.Mechanism_summary<- summary(as.factor(rgi_matr_extract[,"Resistance.Mechanism"]))
# AMR.Gene.Family_summary<- summary(as.factor(rgi_matr_extract[,"AMR.Gene.Family"]))
# Best_Hit_ARO_summary<- summary(as.factor(rgi_matr_extract[,"ARO.Name"]))
# ARO_summary<- summary(as.factor(rgi_matr_extract[,"ARO.Accession"]))

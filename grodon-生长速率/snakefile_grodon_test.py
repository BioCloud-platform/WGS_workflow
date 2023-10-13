import os

inputdir ="/data/Xianjinyuan/LD_lab/public_datasets/culturomics_datasets/public_human_datasets/test"
prokka_dir = "/data/Xianjinyuan/tanyuxiang/1-projects/prophage_detection/IMGG/prokka_test/"
outputdir = "grodon_test/"
gRodon_script = "/data/Xianjinyuan/tanyuxiang/YT_scripts/gRodon/Predict_growth_rate_from_prokka_partial_mode.R"


SAMPLE = glob_wildcards(os.path.join(inputdir,"{sample}.fa")).sample

rule all:                                             
    input: 	      
        expand(os.path.join(outputdir,"{SAMPLE}.grodon.csv"),SAMPLE=SAMPLE),
        os.path.join(outputdir, "all_grodon_merged.csv"),

rule grodon:
    input:
        os.path.join(prokka_dir,"{SAMPLE}","{SAMPLE}.ffn"),
    output:
        os.path.join(outputdir,"{SAMPLE}.grodon.csv"),
    singularity:
        "/data/archive/LD_lab/singularity_images/grodon-v1.0.sif"
    benchmark:
        os.path.join(outputdir,"benchmarks/{SAMPLE}.grodon.benchmark.txt")
    shell:
        "Rscript {gRodon_script} path_to_genome={input} sample_name={wildcards.SAMPLE} path_to_outtb={output} "

#Rscript  path_to_genome="/data/Xianjinyuan/tanyuxiang/1-projects/prophage_detection/IMGG/prokka_test/A102.bin_10/A102.bin_10.ffn" sample_name="A102.bin_10" path_to_outtb="/data/Xianjinyuan/tanyuxiang/1-projects/prophage_detection/IMGG/prokka_test/A102.bin_10.grodon.csv"

rule grodon_merge:
    input:
        expand(os.path.join(outputdir,"{SAMPLE}.grodon.csv"),SAMPLE=SAMPLE),
    output:
        os.path.join(outputdir, "all_grodon_merged.csv"),
    params:
        os.path.join(outputdir, "temp_all_grodon_merged.csv"),
    shell:
        "cat {input} > {params};"
        "head -1 {params} > {output};"
        "grep -v 'd,LowerCI,UpperCI' {params} >> {output};"
        "rm {params};"

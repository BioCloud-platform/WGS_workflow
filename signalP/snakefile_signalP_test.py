import os

inputdir ="/data/Xianjinyuan/LD_lab/public_datasets/culturomics_datasets/public_human_datasets/test"
outputdir = "signalP_test/"
outputdir_group = "signalP_clean_test/"


SAMPLE = glob_wildcards(os.path.join(inputdir,"{sample}.fa")).sample

rule all:                                             
    input: 	      
        expand(os.path.join(outputdir,"signalP_{SAMPLE}","prediction_results.txt"),SAMPLE=SAMPLE),
        #expand(os.path.join(outputdir_group, "logs", "{SAMPLE}_cp.log"), SAMPLE = SAMPLE),

rule signalP:
    input:                                                
        os.path.join(inputdir,"{SAMPLE}.fa")                         
    output:
        os.path.join(outputdir,"signalP_{SAMPLE}","prediction_results.txt")
    params:
        os.path.join(outputdir,"signalP_{SAMPLE}")
    # conda:
    #     "signalP-6.0h"
    singularity:
        "/data/archive/LD_lab/singularity_images/signalp-v6.0h.sif"
    benchmark:
        os.path.join(outputdir,"benchmarks/{SAMPLE}.signalP.benchmark.txt")
    threads:
        8
        #must set 8, because --torch_num_threads {threads} is not setable, and its default is 8.
    shell:
        "signalp6 --fastafile {input} --organism other --output_dir {params} --format txt --mode fast --write_procs {threads} --bsize {threads} "



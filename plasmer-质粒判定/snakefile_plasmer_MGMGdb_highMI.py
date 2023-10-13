import os

inputdir ="highMI_fa_ln_rename"
outputdir = "plasmer_MGMGdb_highMI/"
seqkit_outdir = "seqkit_MGMGdb_highMI"
plasmer_db ="/data/Xianjinyuan/LD_lab/databases/Plasmer_db"
plaser_stat_script = "/data/Xianjinyuan/tanyuxiang/YT_scripts/plasmer/plasmer_result_stat.R"

SAMPLE = glob_wildcards(os.path.join(inputdir,"{sample}.fasta")).sample

ori_fa_type="fasta"
fasta_type="fa"

rule all:
  input:
    expand(os.path.join(outputdir, "{SAMPLE}", "results","{SAMPLE}.plasmer.predClass.tsv"), SAMPLE = SAMPLE),
    #seqkit paired with plasmer for stat
    expand(os.path.join(seqkit_outdir, "{SAMPLE}.fa2tab.tsv"), SAMPLE = SAMPLE),
    expand(os.path.join(seqkit_outdir, "{SAMPLE}","{SAMPLE}.stat.csv"), SAMPLE = SAMPLE),
    expand(os.path.join(seqkit_outdir, "{SAMPLE}","{SAMPLE}.merged.csv"), SAMPLE = SAMPLE),
    os.path.join(seqkit_outdir, "all_merged.csv"),
 	
rule plasmer:
  input:
    os.path.join(inputdir,"{SAMPLE}.fasta")
  output:
    os.path.join(outputdir, "{SAMPLE}", "results","{SAMPLE}.plasmer.predClass.tsv")
  params:
    os.path.join(outputdir, "{SAMPLE}")
  benchmark:
    os.path.join(outputdir,"benchmarks/{SAMPLE}.benchmark.txt")
  singularity:
    "/data/Xianjinyuan/LD_lab/singularity_images/plasmer-23.04.20.sif"
  threads:
    20
  shell:
    "/scripts/Plasmer -g {input} -o {params} -d {plasmer_db} -t {threads} -p {wildcards.SAMPLE}"


rule seqkit:
  input:
    os.path.join(inputdir,"{SAMPLE}."+ori_fa_type)
  output:
    os.path.join(seqkit_outdir, "{SAMPLE}.fa2tab.tsv")
  singularity:
    "/data/archive/LD_lab/singularity_images/seqkit-2.5.1.sif"
  shell:
    "seqkit fx2tab --length --name --only-id --header-line --gc --gc-skew --base-count A --base-count T --base-count C --base-count G --base-count N {input} > {output}"

rule plasmer_stat:
  input:
    plasmer = os.path.join(outputdir, "{SAMPLE}", "results","{SAMPLE}.plasmer.predClass.tsv"),
    seqkit = os.path.join(seqkit_outdir, "{SAMPLE}.fa2tab.tsv"),
  output:
    stat = os.path.join(seqkit_outdir, "{SAMPLE}","{SAMPLE}.stat.csv"),
    merged = os.path.join(seqkit_outdir, "{SAMPLE}","{SAMPLE}.merged.csv"),
  singularity:
    "/data/archive/LD_lab/singularity_images/tidyverse-4.2.2.sif"
  shell:
    "Rscript {plaser_stat_script} path_to_plasmer={input.plasmer} path_to_seqkit={input.seqkit} sample_name={wildcards.SAMPLE} path_to_outtb={output.merged} path_to_outstat={output.stat}"

rule plasmer_stat_merge:
  input:
    expand(os.path.join(seqkit_outdir, "{SAMPLE}","{SAMPLE}.stat.csv"), SAMPLE = SAMPLE),
  output:
    os.path.join(seqkit_outdir, "all_merged.csv"),
  shell:
    "cat {input} > {output}"

inputdir = "merge_2023-06_all_merge/species/"
panaroo_outdir = "merge_2023-06_all_merge/panaroo/"

VFDB_script_fd = "/data/Xianjinyuan/tanyuxiang/YT_scripts/VFDB"
VFDB_core_index = "/data/Xianjinyuan/LD_lab/databases/vfdb/vfdb_2023_08_26/VFDB_setA_nt.dmnd"
VFDB_setB_index = "/data/Xianjinyuan/LD_lab/databases/vfdb/vfdb_2023_08_26/VFDB_setB_nt.dmnd"

SPECIES = glob_wildcards(inputdir+"{species}.csv").species


rule all:
  input:
    expand(os.path.join(panaroo_outdir, "VFDB_setA", "{sample}_vf_anno.txt"), sample = SPECIES),
    expand(os.path.join(panaroo_outdir, "VFDB_setA", "{sample}_vf_sample_anno.txt"), sample = SPECIES),
    os.path.join(panaroo_outdir, "VFDB_setA", "VFDB_merged.tsv"),
    os.path.join(panaroo_outdir, "VFDB_setA", "VFDB_merged_reshape.csv"),
    expand(os.path.join(panaroo_outdir, "VFDB_setB", "{sample}_vf_anno.txt"), sample = SPECIES),
    expand(os.path.join(panaroo_outdir, "VFDB_setB", "{sample}_vf_sample_anno.txt"), sample = SPECIES),
    os.path.join(panaroo_outdir, "VFDB_setB", "VFDB_merged.tsv"),
    os.path.join(panaroo_outdir, "VFDB_setB", "VFDB_merged_reshape.csv"),

# Annotation
rule VFDB_setA:
  input:
    GF_fa = os.path.join(panaroo_outdir, "{SPECIES}", "pan_genome_reference.fa"),
  output:
    os.path.join(panaroo_outdir, "VFDB_setA","{SPECIES}_vf_anno.txt"),
  singularity:
    "/data/archive/LD_lab/singularity_images/diamond-2.0.9.sif"
  threads:
    10
  shell:
    "diamond blastp --db {VFDB_core_index} --query {input.GF_fa} --out {output} --threads {threads}"

rule VFDB_setB:
  input:
    GF_fa = os.path.join(panaroo_outdir, "{SPECIES}", "pan_genome_reference.fa"),
  output:
    os.path.join(panaroo_outdir, "VFDB_setB","{SPECIES}_vf_anno.txt"),
  singularity:
    "/data/archive/LD_lab/singularity_images/diamond-2.0.9.sif"
  threads:
    10
  shell:
    "diamond blastp --db {VFDB_setB_index} --query {input.GF_fa} --out {output} --threads {threads}"

rule add_sample_name_setA:
  input:
    os.path.join(panaroo_outdir, "VFDB_setA", "{SPECIES}_vf_anno.txt"),
  output:
    os.path.join(panaroo_outdir, "VFDB_setA", "{SPECIES}_vf_sample_anno.txt"),
  shell:
    "sed 's/^/'{wildcards.SPECIES}'|&/g' {input} > {output}" #在每行行首加样品名

rule out_merged_setA:
  input:
    expand(os.path.join(panaroo_outdir, "VFDB_setA", "{SPECIES}_vf_sample_anno.txt"), SPECIES = SPECIES),
  output:
    os.path.join(panaroo_outdir, "VFDB_setA", "VFDB_merged.tsv"),
  shell:
    "cat {input} > {output}" 

rule merged_reshape_setA:
  input:
    merge_file = os.path.join(panaroo_outdir, "VFDB_setA", "VFDB_merged.tsv"),
  output:
    table_file = os.path.join(panaroo_outdir, "VFDB_setA", "VFDB_merged_reshape.csv"),
  script:
    "python {VFDB_script_fd}/VFDB_merged_table_2_sample.py -i {input.merge_file} -o {output.table_file}" 

rule add_sample_name_setB:
  input:
    os.path.join(panaroo_outdir, "VFDB_setB", "{SPECIES}_vf_anno.txt"),
  output:
    os.path.join(panaroo_outdir, "VFDB_setB", "{SPECIES}_vf_sample_anno.txt"),
  shell:
    "sed 's/^/'{wildcards.SPECIES}'|&/g' {input} > {output}" #在每行行首加样品名

rule out_merged_setB:
  input:
    expand(os.path.join(panaroo_outdir, "VFDB_setB", "{SPECIES}_vf_sample_anno.txt"), SPECIES = SPECIES),
  output:
    os.path.join(panaroo_outdir, "VFDB_setB", "VFDB_merged.tsv"),
  shell:
    "cat {input} > {output}" 

rule merged_reshape_setB:
  input:
    merge_file = os.path.join(panaroo_outdir, "VFDB_setB", "VFDB_merged.tsv"),
  output:
    table_file = os.path.join(panaroo_outdir, "VFDB_setB", "VFDB_merged_reshape.csv"),
  script:
    "python {VFDB_script_fd}/VFDB_merged_table_2_sample.py -i {input.merge_file} -o {output.table_file}" 

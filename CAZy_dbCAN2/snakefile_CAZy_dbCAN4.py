inputdir = "merge_2023-06_all_merge/species/"
panaroo_outdir = "merge_2023-06_all_merge/panaroo/"

dbCAN_script_fd = "/data/Xianjinyuan/tanyuxiang/YT_scripts/dbCAN"
db_dir = "/data/Xianjinyuan/LD_lab/databases/CAZy_dbCAN2_db/dbCAN2_db_2023_08_28/db"

SPECIES = glob_wildcards(inputdir+"{species}.csv").species

rule all:
  input:
    expand(os.path.join(panaroo_outdir, "CAZy", "{SPECIES}"), SPECIES = SPECIES),
    expand(os.path.join(panaroo_outdir, "CAZy", "{SPECIES}_cazy_out_reshape.csv"), SPECIES = SPECIES),
    #os.path.join(panaroo_outdir, "CAZy", "cazy_final_out.csv"),
    #os.path.join(panaroo_outdir, "CAZy", "cazy_final_out_reshape.csv"),

# Annotation
rule CAZy:
  input:
    GF_fa = os.path.join(panaroo_outdir, "{SPECIES}", "pan_genome_reference.fa"),
  output:
    directory(os.path.join(panaroo_outdir, "CAZy","{SPECIES}"))
  singularity:
    "/data/archive/LD_lab/singularity_images/run_dbcan-4.0.0.sif"
  threads:
    20
  shell:
    "run_dbcan {input.GF_fa} prok --out_dir {output} --db_dir {db_dir} --dia_cpu {threads} --hmm_cpu {threads} --tf_cpu {threads} --stp_cpu {threads}"

#this is for all merge, but for pangenome, it is better for each species, and it also provides
rule CAZy_merge:
  input:
    dbcanDir=directory(os.path.join(panaroo_outdir, "CAZy"))
  output:
    merge_file=os.path.join(panaroo_outdir, "CAZy", "cazy_final_out.csv")
  shell:
    "python {dbCAN_script_fd}/assign_dbcan_snakemake.py -i {input.dbcanDir} -o {output.merge_file}"

rule CAZy_reshape:
  input:
    merge_file=os.path.join(panaroo_outdir, "CAZy", "cazy_final_out.csv")
  output:
    table_file=os.path.join(panaroo_outdir, "CAZy", "cazy_final_out_reshape.csv")
  shell:
    "python {dbCAN_script_fd}/CAZy_merged_table_2_sample.py -i {input.merge_file} -o {output.table_file}"
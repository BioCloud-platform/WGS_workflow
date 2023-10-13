import os

# 定义的目录
#pwd = "/data/Xianjinyuan/tanyuxiang/1-projects/prophage_detection/MGMGdb_highMI/"
rename_dir = "highMI_fa_ln"
rename_output_dir = "highMI_fa_ln_rename"

rename_script = "/data/Xianjinyuan/tanyuxiang/YT_scripts/fasta_process/contig_rename.py"

# 获取要重命名的fasta文件
FASTA_FILES = [f for f in os.listdir(rename_dir) if f.endswith('.fa') or f.endswith('.fasta')]

rule all:
    input:
        expand(os.path.join(rename_output_dir, "{file}"), file=FASTA_FILES)

rule rename_fasta:
    input:
        fasta_file=os.path.join(rename_dir, "{file}")
    output:
        renamed_file=os.path.join(rename_output_dir, "{file}")
    shell:
        """
        python {rename_script} {input.fasta_file} {output.renamed_file}
        """
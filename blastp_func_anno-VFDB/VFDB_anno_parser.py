import re
import argparse

def parse_line(line):
    # 调整后的正则表达式
    pattern = re.compile(r'>(.*?)\((.*?)\)\s*\((.*?)\)\s*(.*?)\s*\[(.*?)\s*\(([^)]+)\)\s*-\s*(.*?)\s*\(([^)]+)\)\]\s*\[(.*?)\]')
    match = pattern.match(line)
    
    if not match:
        raise ValueError(f"Line does not match expected format: {line}")
    
    # 提取各个部分
    gene_id = f"{match.group(1)}({match.group(2)})"  # 列1：VFG037302(gb|WP_001018264)
    gene_name = match.group(3)  # 列2：basF
    gene_function = match.group(4)  # 列3：aryl carrier protein BasF
    gene_category = match.group(5)  # 列4：Acinetobactin
    vf_id = match.group(6)  # 列5：VF0467
    vf_category_name = match.group(7)  # 列6：Nutritional/Metabolic factor
    vfc_id = match.group(8)  # 列7：VFC0272
    type_strain = match.group(9)  # 列8：Acinetobacter baumannii ACICU
    
    return gene_id, gene_name, gene_function, gene_category, vf_id, vf_category_name, vfc_id, type_strain

def process_file(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        # 写入列名（TSV格式，以\t分隔）
        outfile.write("Gene_ID\tGene_name\tGene_function\tGene_category\tVF_ID\tVF_category_name\tVFC_ID\tType_strain\n")
        
        for line in infile:
            line = line.strip()
            if line:
                try:
                    # 解析每一行
                    gene_id, gene_name, gene_function, gene_category, vf_id, vf_category_name, vfc_id, type_strain = parse_line(line)
                    # 写入解析后的数据（TSV格式，以\t分隔）
                    outfile.write(f"{gene_id}\t{gene_name}\t{gene_function}\t{gene_category}\t{vf_id}\t{vf_category_name}\t{vfc_id}\t{type_strain}\n")
                except ValueError as e:
                    print(e)

if __name__ == "__main__":
    # 设置命令行参数解析
    parser = argparse.ArgumentParser(description="Parse the annotation file extracted from the VFDB fas file.")
    parser.add_argument("input_file", help="Path to the input file: .anno")
    parser.add_argument("output_file", help="Path to the output file: .tsv")
    args = parser.parse_args()

    # 调用处理函数
    process_file(args.input_file, args.output_file)
    print(f"Processing complete. Output saved to {args.output_file}")
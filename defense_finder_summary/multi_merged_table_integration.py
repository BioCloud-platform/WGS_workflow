import os
import pandas as pd
import argparse

def get_all_columns(file_list, primary_cols):
    """ 遍历所有文件，求全集列名，并确保 primary_cols 在前面 """
    all_columns = set()
    for file in file_list:
        df = pd.read_csv(file, sep="\t", dtype=str, nrows=1)  # 只读取第一行，提高效率
        all_columns.update(df.columns)

    all_columns = sorted(all_columns)  # 按字母排序，确保列顺序一致

    # 确保 primary_cols 在前面
    final_columns = [col for col in primary_cols if col in all_columns]  # 先提取 primary_cols 中存在的
    final_columns += [col for col in all_columns if col not in primary_cols]  # 其余列保持排序

    return final_columns

def load_and_pad(file, all_columns):
    """ 读取 TSV 文件，并补全缺失列 """
    df = pd.read_csv(file, sep="\t", dtype=str, low_memory=True)
    df = df.reindex(columns=all_columns, fill_value="0")  # 补全列，缺失填充 '0'
    return df

def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="Merge multiple TSV files with complete columns")
    parser.add_argument('-i', '--input', nargs='+', dest='input_files', required=True, help="List of input TSV files")
    parser.add_argument('-o', '--output', dest='output_file', required=True, help="Path to save merged TSV file")
    parser.add_argument('--primary-cols', nargs='+', default=["SampleID"], help="Columns to keep in front (default: SampleID)")
    args = parser.parse_args()

    file_list = [os.path.abspath(f) for f in args.input_files]  # 获取所有输入文件路径
    output_file = os.path.abspath(args.output_file)  # 获取输出文件路径
    primary_cols = args.primary_cols  # 允许用户自定义关键列

    # **1. 计算全集列名**
    all_columns = get_all_columns(file_list, primary_cols)

    # **2. 逐个读取文件，补全列，并高效合并**
    df_list = (load_and_pad(file, all_columns) for file in file_list)  # 生成器，节省内存
    df_merged = pd.concat(df_list, ignore_index=True)  # 高效合并

    # **3. 输出结果**
    df_merged.to_csv(output_file, sep="\t", encoding="utf8", index=False)

    # **4. 生产numeric和binary文件
    #df_out_numeric = df_merged.applymap(lambda x: len(x.split("|")) if x != "0" else 0)
    #df_out_binary = df_out_numeric.applymap(lambda x: 1 if x > 0 else 0)

if __name__ == "__main__":
    main()


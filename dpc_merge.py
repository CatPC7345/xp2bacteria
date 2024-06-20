import pandas as pd
import os
from tqdm import tqdm

def merge_csv_files(input_folder, output_file):
    # 入力フォルダ内のすべてのCSVファイルを取得
    csv_files = [f for f in os.listdir(input_folder) if f.endswith('.csv')]

    # 空のリストを作成してデータフレームを格納
    dataframes = []

    # 各CSVファイルを読み込んでデータフレームリストに追加
    for file in tqdm(csv_files):
        file_path = os.path.join(input_folder, file)
        df = pd.read_csv(file_path, encoding='cp932')
        dataframes.append(df)

    # すべてのデータフレームを結合
    merged_df = pd.concat(dataframes, ignore_index=True)

    # 結合したデータフレームをUTF-8エンコードで出力
    merged_df.to_csv(output_file, index=False, encoding='utf-8')

# 入力フォルダと出力ファイルのパスを設定
input_folder = '/Users/hirotaka_takita/Desktop/database/original/OMU_dpc/OLDDWH'  # CSVファイルが保存されているフォルダのパス
output_file = 'OMU_dpc_merged.csv'  # 出力するCSVファイルのパス

# マージ関数を実行
merge_csv_files(input_folder, output_file)

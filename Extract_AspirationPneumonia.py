import pandas as pd
from tqdm import tqdm

# adjust here #
src_csv_path = 'OMU_dpc_merged.csv'
pneumonia_csv_path = 'OMU_pneumonia.csv'
keyword_col = '病名'
include_keywords_val = ['肺炎']
exclude_keywords_val = ['間質性肺炎', '肺炎の疑い']
###############

df = pd.read_csv(src_csv_path)

# '病名'を含む列をすべて抽出
columns_with_byomei = [col for col in df.columns if keyword_col in col]

# '肺炎'を含むが、'間質性肺炎'および'肺炎の疑い'を含まない行を抽出
def contains_pneumonia_excluding_terms(value):
    if isinstance(value, str):
        includes = any(keyword in value for keyword in include_keywords_val)
        excludes = any(keyword in value for keyword in exclude_keywords_val)
        return includes and not excludes
    return False

# '誤嚥性肺炎'を含むが、'誤嚥性肺炎の疑い'を含まない行をチェック
def contains_aspiration_pneumonia(value):
    if isinstance(value, str):
        return '誤嚥性肺炎' in value and '誤嚥性肺炎の疑い' not in value
    return False

# 各行に対してチェックを行う
mask = pd.Series([False] * len(df))
aspiration_mask = pd.Series([False] * len(df))

for col in tqdm(columns_with_byomei):
    mask = mask | df[col].apply(contains_pneumonia_excluding_terms)
    aspiration_mask = aspiration_mask | df[col].apply(contains_aspiration_pneumonia)

# マスクを適用してデータをフィルタリング
filtered_df = df[mask]

# 'aspiration_pneumonia'列を追加
filtered_df['aspiration_pneumonia'] = aspiration_mask[mask]

# 結果を表示または保存
print(filtered_df)
filtered_df.to_csv(pneumonia_csv_path, index=False)



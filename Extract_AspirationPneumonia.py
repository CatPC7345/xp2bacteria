import pandas as pd
from collections import Counter

def contains_pneumonia_excluding_terms(value, include_keywords_val, exclude_keywords_val):
    if isinstance(value, str):
        includes = any(keyword in value for keyword in include_keywords_val)
        excludes = any(keyword in value for keyword in exclude_keywords_val)
        return includes and not excludes
    return False

def contains_aspiration_pneumonia(value):
    if isinstance(value, str):
        return '誤嚥性肺炎' in value and '誤嚥性肺炎の疑い' not in value
    return False

if __name__ == '__main__':
    src_csv_path = 'dpc.csv'
    pneumonia_csv_path = 'pneumonia.csv'
    pneumonia_counts_csv_path = 'pneumonia_counts.csv'
    keyword_col = '病名'
    include_keywords_val = ['肺炎']
    exclude_keywords_val = ['間質性肺炎', '肺炎の疑い']

    df = pd.read_csv(src_csv_path)
    columns_with_byomei = [col for col in df.columns if keyword_col in col]
    mask = pd.Series([False] * len(df))
    aspiration_mask = pd.Series([False] * len(df))

    for col in columns_with_byomei:
        mask = mask | df[col].apply(contains_pneumonia_excluding_terms, include_keywords_val=include_keywords_val, exclude_keywords_val=exclude_keywords_val)
        aspiration_mask = aspiration_mask | df[col].apply(contains_aspiration_pneumonia)

    filtered_df = df[mask].copy()
    filtered_df.loc[:, 'aspiration_pneumonia'] = aspiration_mask[mask].values
    pneumonia_counts = Counter()

    for col in columns_with_byomei:
        for value in filtered_df[col].dropna():
            if contains_pneumonia_excluding_terms(value, include_keywords_val, exclude_keywords_val):
                pneumonia_counts.update([value])

    pneumonia_counts_df = pd.DataFrame(pneumonia_counts.items(), columns=['Type', 'Count'])
    print(pneumonia_counts_df)
    pneumonia_counts_df.to_csv(pneumonia_counts_csv_path, index=False)
    filtered_df.to_csv(pneumonia_csv_path, index=False)

import pandas as pd

ICD10_csvpath = 'ICD-10_2013.csv'
ICD10CM_csvpath = 'DXCCSR_v2024-1.csv'

df_ICD10 = pd.read_csv(ICD10_csvpath)
df_ICD10 = df_ICD10.rename(columns={'分類コード': 'ICD10_Code', '項目名': 'ICD10_Description'})
df_ICD10['ICD10_Code'] = df_ICD10['ICD10_Code'].str.replace('.', '')
df_ICD10 = df_ICD10[~df_ICD10['ICD10_Code'].str.contains('-')]
df_ICD10['ICD10_Code'] = df_ICD10['ICD10_Code'].str.replace('†', '').str.replace('*', '')

df_ICD10CM = pd.read_csv(ICD10CM_csvpath)
df_ICD10CM["ICD10_Code"] = df_ICD10CM["'ICD-10-CM CODE'"].copy()
df_ICD10CM['ICD10_Code'] = df_ICD10CM['ICD10_Code'].str.replace("'", "").str[:4]

df_merged = pd.merge(df_ICD10, df_ICD10CM, on='ICD10_Code', how='left')
df_merged.to_csv('ICD10_merged.csv', index=False)

df_unmatched = df_merged[df_merged["'ICD-10-CM CODE'"].isna() | (df_merged["'ICD-10-CM CODE'"] == '')]
df_unmatched.to_csv('ICD10_unmatched.csv', index=False)
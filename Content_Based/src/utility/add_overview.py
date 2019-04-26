from src.utility.preprocess import handle_dataset
import pandas as pd
import sys
sys.path.append('..')

def complete_data():
    handle_dataset()
    clean_data = pd.read_csv('../movies_dataset/metadata_clean.csv')
    origin_data = pd.read_csv('../movies_dataset/movies_metadata.csv', low_memory=False)
    # 加入'overview'字段
    clean_data['overview'] = origin_data['overview']
    clean_data['overview'] = clean_data['overview'].fillna('')
    return clean_data
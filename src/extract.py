import pandas as pd
from config import INPUT_DATA_PATH, SHEET_NAME

def load_clinic_data():
    df = pd.read_excel(INPUT_DATA_PATH, sheet_name=SHEET_NAME)
    return df

# test_df = load_clinic_data()
# print(test_df.head())
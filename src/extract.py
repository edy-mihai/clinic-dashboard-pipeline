import pandas as pd
from config import CURRENT_MONTH_PATH, PREV_MONTH_PATH, LAST_YEAR_PATH, SHEET_NAME

def load_clinic_data(file_path):
    df = pd.read_excel(file_path, sheet_name=SHEET_NAME, skiprows=6)
    return df

# test_df = load_clinic_data(CURRENT_MONTH_PATH)
# print(test_df.head())
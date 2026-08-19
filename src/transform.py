import pandas
from config import EURO_RATE

def calculate_summary_metrics(df):
    total_lei = df['Platit'].sum()
    total_euro = total_lei / EURO_RATE

    total_discount = df['Discount'].sum()
    total_signal_iduna = df['SIGNAL IDUNA'].sum()

    total_pacienti_unici = df['COD PACIENT'].nunique()

    pacienti_platitori_df = df[ df['Platit'] > 0 ]
    total_pacienti_platitori = pacienti_platitori_df['COD PACIENT'].nunique()

    pacienti_neplatitori_df = df[ df['Platit'] == 0 ]
    total_pacienti_neplatitori = pacienti_neplatitori_df['COD PACIENT'].nunique()

    incasare_medie = total_lei / total_pacienti_platitori

    data = {
        "total lei" : total_lei,
        "total euro" : total_euro,
        "total discount": total_discount,
        "total signal iduna" : total_signal_iduna,
        "total pacienti unici" : total_pacienti_unici,
        "total pacienti platitori" : total_pacienti_platitori,
        "total pacienti neplatitori" : total_pacienti_neplatitori,
        "incasare medie" : incasare_medie
    }

    return data

from extract import load_clinic_data

raw_df = load_clinic_data()
final_data = calculate_summary_metrics(raw_df)
print(final_data)
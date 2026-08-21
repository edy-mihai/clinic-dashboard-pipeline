import pandas
from config import EURO_RATE

def calculate_summary_metrics(df):
    total_lei = df['Platit'].sum()
    total_euro = total_lei / EURO_RATE

    total_discount = df['Discount'].sum()
    total_signal_iduna = df['SIGNAL IDUNA'].sum()

    total_pacienti_unici = df['Cod Pacient'].nunique()

    pacienti_noi_df = df[ df['Pacient nou'] == "da" ]
    total_pacienti_noi = pacienti_noi_df['Cod Pacient'].nunique()

    pacienti_platitori_df = df[ df['Platit'] > 0 ]
    total_pacienti_platitori = pacienti_platitori_df['Cod Pacient'].nunique()

    pacienti_neplatitori_df = df[ df['Platit'] == 0 ]
    total_pacienti_neplatitori = pacienti_neplatitori_df['Cod Pacient'].nunique()

    incasare_medie = total_lei / total_pacienti_platitori

    data = {
        "total lei" : total_lei,
        "total euro" : total_euro,
        "total discount": total_discount,
        "total signal iduna" : total_signal_iduna,
        "total pacienti noi" : total_pacienti_noi,
        "total pacienti unici" : total_pacienti_unici,
        "total pacienti platitori" : total_pacienti_platitori,
        "total pacienti neplatitori" : total_pacienti_neplatitori,
        "incasare medie" : incasare_medie
    }

    return data

def calculate_variances(current_dict, past_dict):
    variances = {}

    for key in current_dict:
        dif_absoluta = current_dict[key] - past_dict[key]

        if past_dict[key] == 0:
            dif_procent = 0
        else:
            dif_procent = dif_absoluta / past_dict[key]

        variances[f"diferenta {key}"] = dif_absoluta
        variances[f"procent diferenta {key}"] = dif_procent    

    return variances

from extract import load_clinic_data
from config import CURRENT_MONTH_PATH, PREV_MONTH_PATH, LAST_YEAR_PATH

curr_df = load_clinic_data(CURRENT_MONTH_PATH)
prev_df = load_clinic_data(PREV_MONTH_PATH)
last_df = load_clinic_data(LAST_YEAR_PATH)

curr_metrics = calculate_summary_metrics(curr_df)
prev_metrics = calculate_summary_metrics(prev_df)
last_matrics = calculate_summary_metrics(last_df)

curr_prev = calculate_variances(curr_metrics, prev_metrics)
curr_last = calculate_variances(curr_metrics, last_matrics)

print(curr_prev)
print(curr_last)
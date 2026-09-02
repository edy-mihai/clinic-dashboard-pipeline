import pandas
from config import EURO_RATE

def clean_clinic_data(df):
    df.loc[df['Doctor'] == 'CLINICA CLINICA', 'Specialitate medicala'] = 'OBSTETRICA-GINECOLOGIE'
    df.loc[df['Doctor'] == 'PRODUSE SUPORT', 'Specialitate medicala'] = 'PRODUSE SUPORT'

    return df

def calculate_summary_metrics(df):
    total_lei = df['Platit'].sum()
    total_euro = total_lei / EURO_RATE

    total_discount = df['Discount'].sum()
    total_signal_iduna = df['SIGNAL IDUNA'].sum()

    total_pacienti_unici = df['Cod Pacient'].nunique()

    pacienti_noi_df = df[ df['Pacient nou'] == "da" ]
    total_pacienti_noi = pacienti_noi_df['Cod Pacient'].nunique()

    patient_totals = df.groupby('Cod Pacient')['Platit'].sum()

    total_pacienti_platitori = (patient_totals > 0).sum()

    total_pacienti_neplatitori = (patient_totals == 0).sum()

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

def calculate_group_rankings(curr_df, prev_df, last_df, category_col, grand_total):
    current_ranking = curr_df.groupby(category_col)['Platit'].sum().sort_values(ascending=False)
    ordered_names = current_ranking.index.tolist()

    results = {}

    for name in ordered_names:
        curr_revenue_df = curr_df[ curr_df[ category_col ] == name]
        curr_revenue = curr_revenue_df['Platit'].sum()

        if grand_total != 0:
            percentage = curr_revenue / grand_total
        else:
            percentage = 0    

        prev_revenue_df = prev_df[ prev_df[ category_col ] == name]
        prev_revenue = prev_revenue_df['Platit'].sum()

        last_revenue_df = last_df[ last_df[ category_col ] == name]
        last_revenue = last_revenue_df['Platit'].sum()

        curr_prev_abs = curr_revenue - prev_revenue

        if prev_revenue == 0:
            curr_prev_prt = 0
        else:
            curr_prev_prt = curr_prev_abs / prev_revenue


        curr_last_abs = curr_revenue - last_revenue
        
        if last_revenue == 0:
            curr_last_prt = 0
        else:
            curr_last_prt = curr_last_abs / last_revenue

        results[name] = {
            "percent total": percentage,
            "current": curr_revenue,
            "prev": prev_revenue,
            "last": last_revenue,
            "current previous abs": curr_prev_abs,
            "current previous prt": curr_prev_prt,
            "current last abs": curr_last_abs,
            "current last prt": curr_last_prt
        }

    return results

def calculate_detailed_breakdown(curr_df, prev_df, last_df, grand_total, total_patients):
    current_ranking = curr_df.groupby('Specialitate medicala')['Platit'].sum().sort_values(ascending=False)
    ordered_names = current_ranking.index.tolist()

    if 'PRODUSE SUPORT' in ordered_names:
        ordered_names.remove('PRODUSE SUPORT')
        ordered_names.insert(0, 'PRODUSE SUPORT')

    if 'ANALIZE MEDICALE' in ordered_names:
            ordered_names.remove('ANALIZE MEDICALE')
            ordered_names.insert(0, 'ANALIZE MEDICALE')

    

    detailed_results = {}

    for name in ordered_names:
        spec_curr_df = curr_df[ curr_df['Specialitate medicala'] == name ]
        spec_prev_df = prev_df[ prev_df['Specialitate medicala'] == name ]
        spec_last_df = last_df[ last_df['Specialitate medicala'] == name ]

        # METRICS FOR FIRST ROW (REVENUE)
        spec_curr_rev = spec_curr_df['Platit'].sum()
        spec_prev_rev = spec_prev_df['Platit'].sum()
        spec_last_rev = spec_last_df['Platit'].sum()

        if grand_total != 0:
            spec_percentage = spec_curr_rev / grand_total
        else:
            spec_percentage = 0

        spec_curr_prev_abs = spec_curr_rev - spec_prev_rev
        
        if spec_prev_rev == 0:
            spec_curr_prev_prt = 0
        else:
            spec_curr_prev_prt = spec_curr_prev_abs / spec_prev_rev
        
        
        spec_curr_last_abs = spec_curr_rev - spec_last_rev
        
        if spec_last_rev == 0:
            spec_curr_last_prt = 0
        else:
            spec_curr_last_prt = spec_curr_last_abs / spec_last_rev

        # METRICS FOR PATIENTS (NUMBER & AVERAGE)
        spec_curr_pat = spec_curr_df['Cod Pacient'].nunique()
        spec_prev_pat = spec_prev_df['Cod Pacient'].nunique()
        spec_last_pat = spec_last_df['Cod Pacient'].nunique()

        if total_patients != 0:
            spec_percent_patients = spec_curr_pat / total_patients
        else:
            spec_percent_patients = 0

        # write a function for these
        if spec_curr_pat == 0:
            spec_curr_avg = 0
        else:
            spec_curr_avg = spec_curr_rev / spec_curr_pat

        if spec_prev_pat == 0:
            spec_prev_avg = 0
        else:        
            spec_prev_avg = spec_prev_rev / spec_prev_pat

        if spec_last_pat == 0:
            spec_last_avg = 0
        else:        
            spec_last_avg = spec_last_rev / spec_last_pat


        spec_curr_prev_pat_abs = spec_curr_pat - spec_prev_pat
        
        if spec_prev_pat == 0:
            spec_curr_prev_pat_prt = 0
        else:
            spec_curr_prev_pat_prt = spec_curr_prev_pat_abs / spec_prev_pat
        
        
        spec_curr_last_pat_abs = spec_curr_pat - spec_last_pat
        
        if spec_last_pat == 0:
            spec_curr_last_pat_prt = 0
        else:
            spec_curr_last_pat_prt = spec_curr_last_pat_abs / spec_last_pat        



        spec_curr_prev_avg_abs = spec_curr_avg - spec_prev_avg
        
        if spec_prev_avg == 0:
            spec_curr_prev_avg_prt = 0
        else:
            spec_curr_prev_avg_prt = spec_curr_prev_avg_abs / spec_prev_avg
        
        
        spec_curr_last_avg_abs = spec_curr_avg - spec_last_avg
        
        if spec_last_avg == 0:
            spec_curr_last_avg_prt = 0
        else:
            spec_curr_last_avg_prt = spec_curr_last_avg_abs / spec_last_avg


        detailed_results[name] = {
            "metrics": {
                # SPECIALTY METRICS FIRST ROW
                "percent total": spec_percentage,
                "current": spec_curr_rev,
                "prev": spec_prev_rev,
                "last": spec_last_rev,

                "current previous abs": spec_curr_prev_abs,
                "current previous prt": spec_curr_prev_prt,

                "current last abs": spec_curr_last_abs,
                "current last prt": spec_curr_last_prt,


                # SECOND ROW
                "percent total pat": spec_percent_patients,
                "current nr patient": spec_curr_pat,
                "previous nr patient": spec_prev_pat,
                "last nr patient": spec_last_pat,

                "current previous nr pat abs": spec_curr_prev_pat_abs,
                "current previous nr pat prt": spec_curr_prev_pat_prt,

                "current last nr pat abs": spec_curr_last_pat_abs,
                "current last nr pat prt": spec_curr_last_pat_prt,


                # THRID ROW
                "current avg patient": spec_curr_avg,
                "previous avg patient": spec_prev_avg,
                "last avg patient": spec_last_avg,

                "current previous avg pat abs": spec_curr_prev_avg_abs,
                "current previous avg pat prt": spec_curr_prev_avg_prt,

                "current last avg pat abs": spec_curr_last_avg_abs,
                "current last avg pat prt": spec_curr_last_avg_prt
            },
            "doctors" : {}
        }

        doctor_current_ranking = spec_curr_df.groupby('Doctor')['Platit'].sum().sort_values(ascending=False)
        doctor_names = doctor_current_ranking.index.tolist()

        if name in ['ANALIZE MEDICALE', 'PRODUSE SUPORT']:
            continue
            
        for doctor in doctor_names:
            # METRICS FOR DOCTOR REVENUE (FIRST ROW)
            doc_curr_df = spec_curr_df[ spec_curr_df['Doctor'] == doctor ]
            doc_prev_df = spec_prev_df[ spec_prev_df['Doctor'] == doctor ]
            doc_last_df = spec_last_df[ spec_last_df['Doctor'] == doctor ]

            doc_curr_rev = doc_curr_df['Platit'].sum()
            doc_prev_rev = doc_prev_df['Platit'].sum()
            doc_last_rev = doc_last_df['Platit'].sum()

            if grand_total != 0:
                doc_percentage = doc_curr_rev / grand_total
            else:
                doc_percentage = 0
            
            doc_curr_prev_abs = doc_curr_rev - doc_prev_rev
            
            if doc_prev_rev == 0:
                doc_curr_prev_prt = 0
            else:
                doc_curr_prev_prt = doc_curr_prev_abs / doc_prev_rev
            
            
            doc_curr_last_abs = doc_curr_rev - doc_last_rev
            
            if doc_last_rev == 0:
                doc_curr_last_prt = 0
            else:
                doc_curr_last_prt = doc_curr_last_abs / doc_last_rev


            # METRICS FOR NR OF PATIENTS (ROW 2 & 3)
            doc_curr_pat = doc_curr_df['Cod Pacient'].nunique()
            doc_prev_pat = doc_prev_df['Cod Pacient'].nunique()
            doc_last_pat = doc_last_df['Cod Pacient'].nunique()

            if total_patients != 0:
                doc_percent_patients = doc_curr_pat / total_patients
            else:
                doc_percent_patients = 0

            if doc_curr_pat == 0:
                doc_curr_avg = 0
            else:
                doc_curr_avg = doc_curr_rev / doc_curr_pat
            
            if doc_prev_pat == 0:
                doc_prev_avg = 0
            else:        
                doc_prev_avg = doc_prev_rev / doc_prev_pat
            
            if doc_last_pat == 0:
                doc_last_avg = 0
            else:        
                doc_last_avg = doc_last_rev / doc_last_pat
            
            
            doc_curr_prev_pat_abs = doc_curr_pat - doc_prev_pat
            
            if doc_prev_pat == 0:
                doc_curr_prev_pat_prt = 0
            else:
                doc_curr_prev_pat_prt = doc_curr_prev_pat_abs / doc_prev_pat
            
            
            doc_curr_last_pat_abs = doc_curr_pat - doc_last_pat
            
            if doc_last_pat == 0:
                doc_curr_last_pat_prt = 0
            else:
                doc_curr_last_pat_prt = doc_curr_last_pat_abs / doc_last_pat        
            
            
            
            doc_curr_prev_avg_abs = doc_curr_avg - doc_prev_avg
            
            if doc_prev_avg == 0:
                doc_curr_prev_avg_prt = 0
            else:
                doc_curr_prev_avg_prt = doc_curr_prev_avg_abs / doc_prev_avg
            
            
            doc_curr_last_avg_abs = doc_curr_avg - doc_last_avg
            
            if doc_last_avg == 0:
                doc_curr_last_avg_prt = 0
            else:
                doc_curr_last_avg_prt = doc_curr_last_avg_abs / doc_last_avg

            
            detailed_results[name]["doctors"][doctor] = {
                # FIRST ROW
                "percent total": doc_percentage, 
                "current": doc_curr_rev,
                "prev": doc_prev_rev,
                "last": doc_last_rev,

                "current previous abs": doc_curr_prev_abs,
                "current previous prt": doc_curr_prev_prt,
                "current last abs": doc_curr_last_abs,
                "current last prt": doc_curr_last_prt,

                # SECOND ROW
                "percent total pat": doc_percent_patients,
                "current nr patient": doc_curr_pat,
                "previous nr patient": doc_prev_pat,
                "last nr patient": doc_last_pat,
                
                "current previous nr pat abs": doc_curr_prev_pat_abs,
                "current previous nr pat prt": doc_curr_prev_pat_prt,
                
                "current last nr pat abs": doc_curr_last_pat_abs,
                "current last nr pat prt": doc_curr_last_pat_prt,
                
                
                # THRID ROW
                "current avg patient": doc_curr_avg,
                "previous avg patient": doc_prev_avg,
                "last avg patient": doc_last_avg,
                
                "current previous avg pat abs": doc_curr_prev_avg_abs,
                "current previous avg pat prt": doc_curr_prev_avg_prt,
                
                "current last avg pat abs": doc_curr_last_avg_abs,
                "current last avg pat prt": doc_curr_last_avg_prt
            }

    return detailed_results

from extract import load_clinic_data
from config import CURRENT_MONTH_PATH, PREV_MONTH_PATH, LAST_YEAR_PATH

curr_df = load_clinic_data(CURRENT_MONTH_PATH)
prev_df = load_clinic_data(PREV_MONTH_PATH)
last_df = load_clinic_data(LAST_YEAR_PATH)

curr_df = clean_clinic_data(curr_df)
prev_df = clean_clinic_data(prev_df)
last_df = clean_clinic_data(last_df)

curr_metrics = calculate_summary_metrics(curr_df)
prev_metrics = calculate_summary_metrics(prev_df)
last_metrics = calculate_summary_metrics(last_df)

curr_prev = calculate_variances(curr_metrics, prev_metrics)
curr_last = calculate_variances(curr_metrics, last_metrics)

top_specialitati = calculate_group_rankings(curr_df, prev_df, last_df, 'Specialitate medicala', curr_metrics["total lei"])
top_medici = calculate_group_rankings(curr_df, prev_df, last_df, 'Doctor', curr_metrics["total lei"])

detailed_breakdown = calculate_detailed_breakdown(curr_df, prev_df, last_df, curr_metrics["total lei"], curr_metrics["total pacienti unici"])

# treat database edge cases
# TAKE CARE OF STORNARI

# print(curr_prev)
# print(curr_last)
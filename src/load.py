from openpyxl import load_workbook
from config import OUTPUT_DIR, TEMPLATE_PATH
from transform import curr_metrics, prev_metrics, last_metrics, curr_prev, curr_last

def generate_dashboard(template_path, current_data, prev_data, last_data, prev_variance, last_year_variance):
    wb = load_workbook(template_path)
    ws = wb['dashboard']
    row_map = {
        "total lei": 2,
        "total euro": 3,
        "total pacienti unici": 4,
        "total pacienti noi": 5,
        "total pacienti platitori": 6,
        "incasare medie": 7,
        "total pacienti neplatitori": 8,
        "total discount": 9,
        "total signal iduna": 10
    }

    for key, row in row_map.items():
        ws[f'D{row}'].value = current_data[key]
        ws[f'E{row}'].value = last_data[key]
        ws[f'F{row}'].value = prev_data[key]
        ws[f'G{row}'].value = last_year_variance[f'diferenta {key}']
        ws[f'H{row}'].value = last_year_variance[f'procent diferenta {key}']
        ws[f'J{row}'].value = prev_variance[f'diferenta {key}']
        ws[f'K{row}'].value = prev_variance[f'procent diferenta {key}']

    wb.save(OUTPUT_DIR + "Dashboard_Generated.xlsx")

generate_dashboard(TEMPLATE_PATH, curr_metrics, prev_metrics, last_metrics, curr_prev, curr_last)
    
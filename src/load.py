from openpyxl import load_workbook
from config import OUTPUT_DIR, TEMPLATE_PATH
from transform import curr_metrics, prev_metrics, last_metrics, curr_prev, curr_last, top_medici, top_specialitati
from copy import copy

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

    fill_dynamic_table(ws, top_medici, 17)
    fill_dynamic_table(ws, top_specialitati, 13)

    wb.save(OUTPUT_DIR + "Dashboard_Generated.xlsx")

    

def fill_dynamic_table(worksheet, data_dict, start_row):
    rows_to_insert = len(data_dict) - 1

    if rows_to_insert > 0:
        worksheet.insert_rows(start_row + 1, rows_to_insert)
        for i in range(start_row + 1, start_row + rows_to_insert + 1):
            for j in range(2, 12):
                source_cell = worksheet.cell(row=start_row, column=j)
                target_cell = worksheet.cell(row=i, column=j)

                target_cell.font = copy(source_cell.font)
                target_cell.border = copy(source_cell.border)
                target_cell.fill = copy(source_cell.fill)
                target_cell.number_format = copy(source_cell.number_format)
                target_cell.alignment = copy(source_cell.alignment)

    current_row = start_row

    for name, metrics in data_dict.items():
        worksheet.cell(row=current_row, column=2).value = name
        worksheet.cell(row=current_row, column=4).value = metrics["current"]
        worksheet.cell(row=current_row, column=5).value = metrics["last"]
        worksheet.cell(row=current_row, column=6).value = metrics["prev"]
        worksheet.cell(row=current_row, column=7).value = metrics["current last abs"]
        worksheet.cell(row=current_row, column=8).value = metrics["current last prt"]
        worksheet.cell(row=current_row, column=10).value = metrics["current previous abs"]
        worksheet.cell(row=current_row, column=11).value = metrics["current previous prt"]

        current_row += 1
        
# INDEX INCEPUT DE RAND PT FIECARE ENTRY LA TOPURI

generate_dashboard(TEMPLATE_PATH, curr_metrics, prev_metrics, last_metrics, curr_prev, curr_last)
    
import openpyxl
from openpyxl.styles import PatternFill, Font
from openpyxl.formatting.rule import Rule
from openpyxl.styles.differential import DifferentialStyle

wb = openpyxl.load_workbook('scratch/test_out.xlsx')
ws1 = wb['Header & Ringkasan']
ws2 = wb['Tabel_Mutasi']

red_fill = PatternFill(start_color='FFC7CE', end_color='FFC7CE', fill_type='solid')
font_red = Font(name='Calibri', size=11, bold=True, color='9C0006')
dxf_red = DifferentialStyle(fill=red_fill, font=font_red)
rule_red = Rule(type="containsText", operator="containsText", text="SELISIH", dxf=dxf_red)
rule_red.formula = ['NOT(ISERROR(SEARCH("SELISIH", B17)))']

green_fill = PatternFill(start_color='C6EFCE', end_color='C6EFCE', fill_type='solid')
font_green = Font(name='Calibri', size=11, bold=True, color='006100')
dxf_green = DifferentialStyle(fill=green_fill, font=font_green)
rule_green = Rule(type="containsText", operator="containsText", text="MATCH", dxf=dxf_green)
rule_green.formula = ['NOT(ISERROR(SEARCH("MATCH", B17)))']

ws1.conditional_formatting.add('B17:B20', rule_red)
ws1.conditional_formatting.add('B17:B20', rule_green)

# For sheet 2 column H
rule_h_red = Rule(type="containsText", operator="containsText", text="SELISIH", dxf=dxf_red)
rule_h_red.formula = ['NOT(ISERROR(SEARCH("SELISIH", H6)))']
rule_h_green = Rule(type="containsText", operator="containsText", text="OK", dxf=dxf_green)
rule_h_green.formula = ['NOT(ISERROR(SEARCH("OK", H6)))']

ws2.conditional_formatting.add('H6:H100', rule_h_red)
ws2.conditional_formatting.add('H6:H100', rule_h_green)

wb.save('scratch/test_out_cf.xlsx')
print('CF successfully created and saved!')

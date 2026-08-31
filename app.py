import sys, os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# %%
from extract.sheets_extractor import extractor_all_sheets
from transform.transform_data import transform_teacher_data
from transform.transform_data import transform_parents_data
from load.database_loader import (load_parents_data, load_teacher_data)

# %%
extract = extractor_all_sheets()

for i in extract:
    print(f"Processando: {i['name']} | tipo: {i['type']} | fase: {i['fase']} | registros: {len(i['value']) - 1 if i['value'] else 0}")
    if i['type'] == 'PROFESSOR':
        df_registro, df_resposta, df_checkbox, df_texto = transform_teacher_data(i)
        load_teacher_data(df_registro, df_resposta, df_checkbox, df_texto)
    elif i['type'] == 'RESPONSAVEL':
        df_registro, df_resposta = transform_parents_data(i)
        load_parents_data(df_registro, df_resposta)





# %%
from extract.sheets_extractor import extractor_all_sheets
from transform.transform_data import transform_teacher_data
from transform.transform_data import transform_parents_data
from load.database_loader import (load_parents_data, load_teacher_data)

# %%
extract = extractor_all_sheets()

for i in extract:
    if i['type'] == 'PROFESSOR':
        df_registro, df_resposta, df_checkbox, df_texto = transform_teacher_data(i)
        load_teacher_data(df_registro, df_resposta, df_checkbox, df_texto)
    elif i['type'] == 'RESPONSAVEL':
        df_registro, df_resposta = transform_parents_data(i)
        load_parents_data(df_registro, df_resposta)






import pandas as pd

def transform_teacher_data(form):
    data = form["value"]
    header = data[0]
    rows = [row + [""] * (len(header) - len(row)) for row in data[1:]]
    df = pd.DataFrame(rows, columns=header)
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.split()
        .str.join("_")
    )
    
    colunas_metadados = ["carimbo_de_data/hora", "qual_o_código_da_criança_que_está_sendo_observada?"]
    colunas_checkbox = ["nesta_semana:"]
    colunas_texto = ["descreva_sua_observação:"]
    colunas_escala = [i for i in df.columns if i not in colunas_metadados and i not in colunas_checkbox and i not in colunas_texto]
        
    df["carimbo_de_data/hora"] = pd.to_datetime(df["carimbo_de_data/hora"], dayfirst=True).dt.date

    df_registro = df[colunas_metadados].assign(fase=form["fase"]).rename(columns={
        "carimbo_de_data/hora": "data",
        "qual_o_código_da_criança_que_está_sendo_observada?": "codigo"
    }).reset_index(drop=True)
    
    df_resposta = pd.melt(
        df,
        id_vars=colunas_metadados,
        value_vars=colunas_escala,
        var_name="pergunta",
        value_name="resposta"
    ).reset_index(drop=True)
    
    OPCOES_CHECKBOX = [
        "o aluno faltou algum dia",
        "houve alteração na rotina (evento, passeio, prova, etc.)",
        "houve alguma intercorrência comportamental relevante"
    ]

    df_checkbox = df[colunas_metadados + colunas_checkbox].copy()
    df_checkbox = df_checkbox.explode(colunas_checkbox[0])
    df_checkbox[colunas_checkbox[0]] = df_checkbox[colunas_checkbox[0]].apply(
        lambda cell: [op for op in OPCOES_CHECKBOX if op in (cell or "").lower()]
    )
    df_checkbox = df_checkbox.explode(colunas_checkbox[0])
    df_checkbox = df_checkbox[df_checkbox[colunas_checkbox[0]].notna() & (df_checkbox[colunas_checkbox[0]] != "")].reset_index(drop=True)
    
    df_texto = df[colunas_metadados + colunas_texto].reset_index(drop=True)
    
    return df_registro, df_resposta, df_checkbox, df_texto

def transform_parents_data(form):
    data = form["value"]
    header = data[0]
    rows = [row + [""] * (len(header) - len(row)) for row in data[1:]]
    df = pd.DataFrame(rows, columns=header)
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.split()
        .str.join("_")
    )
    df["carimbo_de_data/hora"] = pd.to_datetime(df["carimbo_de_data/hora"], dayfirst=True).dt.date
    
    colunas_metadados = ["carimbo_de_data/hora", "qual_o_código_da_criança_que_está_sendo_observada?", "dia_de_avaliação"]
    colunas_resposta = [
        "período_de_sono:",
        "apresentou_agitação_e/ou_acordou_durante_a_noite?",
        "houve_mudanças_na_rotina_(como_visitas_ou_atividades_foram_do_comum)?",
        "apresentou_sinais_de_ansiedade_(ex.:_inquietação,_irritabilidade_etc.)?",
        "comportamento_ao_ir_para_a_escola:",
        "comportamento_ao_voltar_da_escola:",
        "como_os_pais/responsáveis_se_sentiram_hoje?",
        "demonstrou_resistência_ao_aplicar_o_óleo?"
        ]
    
    df_registro = df[colunas_metadados].assign(fase=form["fase"]).rename(columns={
        "carimbo_de_data/hora":"data",
        "qual_o_código_da_criança_que_está_sendo_observada?": "codigo",
        "dia_de_avaliação":"dia_avaliacao"
    }).reset_index(drop=True)
    
    df_resposta = pd.melt(
        df,
        id_vars=colunas_metadados,
        value_vars=colunas_resposta,
        var_name="pergunta",
        value_name="resposta"
    ).reset_index(drop=True)
    
    return df_registro, df_resposta

    

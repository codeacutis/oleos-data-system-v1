from load.db_connection import get_connection

def get_id_fase(cursor, nome_fase):
    select_query = "SELECT id_fase FROM Fase_Estudo WHERE nome_fase = (%s)"
    cursor.execute(select_query, (nome_fase,))
    result = cursor.fetchone()
    
    if result is None:
        raise ValueError (f"Não foi possível encontrar o id para a pergunta: {nome_fase}")
    else:
        return result[0]

def get_id_form(cursor, tipo_formulario, fase_formulario):
    select_query = "SELECT id_formulario FROM Formulario WHERE tipo = (%s) AND id_fase = (%s)"
    cursor.execute(select_query, (tipo_formulario, fase_formulario))
    result = cursor.fetchone()
    
    if result is None:
        raise ValueError (f"Não foi possível encontrar o id para o tipo: {tipo_formulario} e a fase: {fase_formulario}")
    else:
        return result[0]

def get_id_child(cursor, codigo):
    select_query = "SELECT id_crianca FROM Crianca WHERE codigo = (%s)"
    cursor.execute(select_query, (codigo,))
    result = cursor.fetchone()

    if result is None:
        raise ValueError (f"Não foi possível encontrar o id para o código: {codigo}")
    else:
        return result[0]

def get_id_observer(cursor, id_crianca, tipo):
    select_query = "SELECT o.id_observador FROM Observador AS o INNER JOIN Observador_Crianca AS obs ON o.id_observador = obs.id_observador WHERE obs.id_crianca = (%s) AND o.tipo = (%s)"
    cursor.execute(select_query, (id_crianca, tipo))
    result = cursor.fetchone()

    if result is None:
        raise ValueError (f"Não foi possível encontrar o id do {tipo} referente à criança: {id_crianca}")
    else:
        return result[0]

def get_id_item(cursor, descricao):
    descricao_normalizada = descricao.replace("_", " ")
    select_query = "SELECT id_item FROM Item_Escala WHERE descricao = (%s)"
    cursor.execute(select_query, (descricao_normalizada,))
    result = cursor.fetchone()
    
    if result is None:
        raise ValueError (f"Não foi possível encontrar o id do item para a descrição: {descricao_normalizada}")
    else:
        return result[0]

def get_id_opcao(cursor, descricao):
    select_query = "SELECT id_opcao FROM Opcao_Categorica WHERE descricao = (%s)"
    cursor.execute(select_query, (descricao,))
    result = cursor.fetchone()
    
    if result is None:
        print(f"Não foi possível encontrar o id da opção para a descrição: {descricao}")
        return None
    else:
        return result[0]
    
def get_id_opcao_checkbox(cursor, descricao):
    select_query = "SELECT id_opcao_checkbox FROM Opcao_Checkbox WHERE descricao = (%s)"
    cursor.execute(select_query, (descricao,))
    result = cursor.fetchone()

    if result is None:
        raise ValueError (f"Não foi possível encontrar o id da opção checkbox para a descrição: {descricao}")
    else:
        return result[0]

#funções principais

def load_teacher_data(df_registro, df_resposta, df_checkbox, df_texto):
    mydb = get_connection()
    mycursor = mydb.cursor()
    
    #inserir em Registro
    insert_query_registro = "INSERT IGNORE INTO Registro (data, id_crianca, id_observador, id_fase, id_formulario) VALUES (%s, %s, %s, %s, %s)"
    ids_registro = []
    
    for i in range(len(df_registro)):
        id_crianca = get_id_child(mycursor, df_registro["codigo"][i])
        id_observer = get_id_observer(mycursor, id_crianca, 'PROFESSOR')
        id_fase = get_id_fase(mycursor, df_registro['fase'][i])
        id_form = get_id_form(mycursor, 'PROFESSOR', id_fase)
        value = (
            df_registro["data"][i],
            id_crianca, 
            id_observer,
            id_fase,
            id_form
            )
        mycursor.execute(insert_query_registro, value)

        if mycursor.lastrowid != 0:
            ids_registro.append(mycursor.lastrowid)
        else:
            mycursor.execute("SELECT id_registro FROM Registro WHERE data = %s AND id_crianca = %s AND id_formulario = %s",
                            (df_registro["data"][i], id_crianca, id_form))
            ids_registro.append(mycursor.fetchone()[0])

    #inserir em Resposta
    insert_query_resposta = "INSERT IGNORE INTO Resposta (id_registro, id_item, valor_numerico, id_opcao, valor_texto) VALUES (%s, %s, %s, %s, %s)"
    for i in range(len(df_resposta)):
        idx = df_registro[
        (df_registro["codigo"] == df_resposta["qual_o_código_da_criança_que_está_sendo_observada?"][i]) &
        (df_registro["data"] == df_resposta["carimbo_de_data/hora"][i])].index[0]
        value = (
            ids_registro[idx],
            get_id_item(mycursor, df_resposta["pergunta"][i]),
            df_resposta["resposta"][i],
            None,
            None
            )
        mycursor.execute(insert_query_resposta, value)
    
    #inserir em Resposta_Checkbox
    insert_query_resposta_checkbox = "INSERT IGNORE INTO Resposta_Checkbox (id_registro, id_item, id_opcao_checkbox) VALUES (%s, %s, %s)"
    for i in range(len(df_checkbox)):
        idx = df_registro[
        (df_registro["codigo"] == df_checkbox["qual_o_código_da_criança_que_está_sendo_observada?"][i]) &
        (df_registro["data"] == df_checkbox["carimbo_de_data/hora"][i])].index[0]
        value = (
            ids_registro[idx],
            get_id_item(mycursor, "nesta_semana:"),
            get_id_opcao_checkbox(mycursor, df_checkbox["nesta_semana:"][i])
        )
        mycursor.execute(insert_query_resposta_checkbox, value)
    
    #inserir em Resposta (textual)
    for i in range(len(df_texto)):
        idx = df_registro[
        (df_registro["codigo"] == df_texto["qual_o_código_da_criança_que_está_sendo_observada?"][i]) &
        (df_registro["data"] == df_texto["carimbo_de_data/hora"][i])].index[0]
        value = (
            ids_registro[idx],
            get_id_item(mycursor, "descreva_sua_observação:"),
            None,
            None,
            df_texto["descreva_sua_observação:"][i]
            )
        mycursor.execute(insert_query_resposta, value)
        
    
    mydb.commit()
    print(mycursor.rowcount, "was inserted.")
    mycursor.close()
    mydb.close()



def load_parents_data(df_registro, df_resposta):
    mydb = get_connection()
    mycursor = mydb.cursor()
    
    #inserir em Registro
    insert_query_registro = "INSERT IGNORE INTO Registro (data, id_crianca, id_observador, id_fase, id_formulario) VALUES (%s, %s, %s, %s, %s)"
    ids_registro = []
    
    for i in range(len(df_registro)):
        id_crianca = get_id_child(mycursor, df_registro["codigo"][i])
        id_observer = get_id_observer(mycursor, id_crianca, 'RESPONSAVEL')
        id_fase = get_id_fase(mycursor, df_registro['fase'][i])
        id_form = get_id_form(mycursor, 'PAIS', id_fase)
        value = (
            df_registro["data"][i],
            id_crianca, 
            id_observer,
            id_fase,
            id_form
            )
        mycursor.execute(insert_query_registro, value)

        if mycursor.lastrowid != 0:
            ids_registro.append(mycursor.lastrowid)
        else:
            mycursor.execute("SELECT id_registro FROM Registro WHERE data = %s AND id_crianca = %s AND id_formulario = %s",
                            (df_registro["data"][i], id_crianca, id_form))
            ids_registro.append(mycursor.fetchone()[0])
        
    #inserir em Resposta
    insert_query_resposta = "INSERT IGNORE INTO Resposta (id_registro, id_item, valor_numerico, id_opcao, valor_texto) VALUES (%s, %s, %s, %s, %s)"
    for i in range(len(df_resposta)):
        idx = df_registro[
        (df_registro["codigo"] == df_resposta["qual_o_código_da_criança_que_está_sendo_observada?"][i]) &
        (df_registro["data"] == df_resposta["carimbo_de_data/hora"][i]) &
        (df_registro["dia_avaliacao"] == df_resposta["dia_de_avaliação"][i])].index[0]
        resposta = df_resposta["resposta"][i]
        id_opcao_result = get_id_opcao(mycursor, resposta)
        id_opcao = id_opcao_result if id_opcao_result else None
        valor_texto = resposta if id_opcao is None else None

        value = (
            ids_registro[idx],
            get_id_item(mycursor, df_resposta["pergunta"][i]),
            None,
            id_opcao,
            valor_texto
            )
        mycursor.execute(insert_query_resposta, value)

    mydb.commit()
    print(mycursor.rowcount, "was inserted.")
    mycursor.close()
    mydb.close()


from load.db_connection import get_connection
from datetime import date

def oleos_insert():
    mydb = get_connection()
    mycursor = mydb.cursor()
    insert_query = "INSERT INTO Oleo (nome) VALUES (%s)"
    values = [("lavanda",), ("mandarina",), ("patchouli",), ("ylang",)]
    mycursor.executemany(insert_query, values)

    mydb.commit()
    mycursor.close()
    mydb.close()
    print(mycursor.rowcount, "was inserted.")

def fase_insert():
    mydb = get_connection()
    mycursor = mydb.cursor()
    insert_query = "INSERT INTO Fase_Estudo (nome_fase, ordem, data_inicio, data_fim, id_oleo) VALUES (%s, %s, %s, %s, %s)"
    values = [
        ("linha_base", 1, None, None, None), 
        ("lavanda", 2, None, None, 1), 
        ("mandarina", 3, None, None, 2), 
        ("patchouli", 4, None, None, 3), 
        ("ylang", 5, None, None, 4)
        ]
    mycursor.executemany(insert_query, values)

    mydb.commit()
    mycursor.close()
    mydb.close()
    print(mycursor.rowcount, "was inserted.")

def form_insert():
    mydb = get_connection()
    mycursor = mydb.cursor()
    insert_query = "INSERT INTO Formulario (nome, tipo, id_fase) VALUES (%s, %s, %s)"
    values = [
        ("professor_fase_linha_base", "PROFESSOR", 1), 
        ("professor_fase_lavanda", "PROFESSOR", 2), 
        ("professor_fase_mandarina", "PROFESSOR", 3), 
        ("professor_fase_patchouli", "PROFESSOR", 4), 
        ("professor_fase_ylang", "PROFESSOR", 5), 
        ("pais_fase_linha_base", "PAIS", 1), 
        ("pais_fase_lavanda", "PAIS", 2), 
        ("pais_fase_mandarina", "PAIS", 3), 
        ("pais_fase_patchouli", "PAIS", 4), 
        ("pais_fase_ylang", "PAIS", 5)
        ]
    mycursor.executemany(insert_query, values)

    mydb.commit()
    mycursor.close()
    mydb.close()
    print(mycursor.rowcount, "was inserted.")

def domination_insert():
    mydb = get_connection()
    mycursor = mydb.cursor()
    insert_query = "INSERT INTO Dominio_Escala (nome) VALUES (%s)"
    values = [
        ("interação social",), 
        ("ansiedade e estresse",), 
        ("aprendizado",),
        ("verificação semanal",),
        ("observações",)
        ]
    mycursor.executemany(insert_query, values)

    mydb.commit()
    mycursor.close()
    mydb.close()
    print(mycursor.rowcount, "was inserted.")
    
def categorical_insert():
    mydb = get_connection()
    mycursor = mydb.cursor()
    insert_query = "INSERT INTO Opcao_Categorica (descricao) VALUES (%s)"
    values = [
        ("calmo",), 
        ("ansioso/agitado",), 
        ("agressivo",),
        ("triste",),
        ("alegre",),
        ("menos de 4h",),
        ("4h",),
        ("6h",),
        ("8h",),
        ("mais de 8h",),
        ("sim",),
        ("não",),
        ("calmos",),
        ("preocupados",),
        ("nervosos",),
        ("estressados",)
        ]
    mycursor.executemany(insert_query, values)

    mydb.commit()
    mycursor.close()
    mydb.close()
    print(mycursor.rowcount, "was inserted.")
    
def checkbox_insert():
    mydb = get_connection()
    mycursor = mydb.cursor()
    insert_query = "INSERT INTO Opcao_Checkbox (descricao) VALUES (%s)"
    values = [
        ("o aluno faltou algum dia",), 
        ("houve alteração na rotina (evento, passeio, prova, etc.)",), 
        ("houve alguma intercorrência comportamental relevante",)
        ]
    mycursor.executemany(insert_query, values)

    mydb.commit()
    mycursor.close()
    mydb.close()
    print(mycursor.rowcount, "was inserted.")

def item_escala_teachers_insert():
    mydb = get_connection()
    mycursor = mydb.cursor()
    insert_query = "INSERT INTO Item_Escala (descricao, tipo_resposta, tipo_observador, id_dominio) VALUES (%s, %s, %s, %s)"
    values = [
        ("durante aulas expositivas, evita contato visual ou evita/prejudica interação:", "ESCALA_0_4", "PROFESSOR", 1),
        ("durante atividades em grupo, não compartilha materiais ou não interage com os colegas:", "ESCALA_0_4", "PROFESSOR", 1),
        ("não demonstra empatia com colegas (tristeza, necessidade de ajuda). se mostra mais indiferente que os demais:", "ESCALA_0_4", "PROFESSOR", 1),
        ("em atividades interativas, não participa adequadamente e não demonstra interesse em falar ou engajar com outro colega:", "ESCALA_0_4", "PROFESSOR", 1),
        
        ("em sala de aula, no recreio ou em atividades extracurriculares, tem dificuldade em esperar sua vez:", "ESCALA_0_4", "PROFESSOR", 2),
        ("age/fala sem pedir permissão:", "ESCALA_0_4", "PROFESSOR", 2),
        ("fala excessivamente quando não deve falar e/ou interrompe a fala dos outros:", "ESCALA_0_4", "PROFESSOR", 2),
        ("demonstra comportamento impulsivo/agressivo:", "ESCALA_0_4", "PROFESSOR", 2),
        ("apresenta oscilações de humor que sejam repentinas ou intensas e que não tenham motivo específico para tal reação:", "ESCALA_0_4", "PROFESSOR", 2),
        ("apresenta comportamento disperso, demonstrando falta de atenção na brincadeira ou na aula, quando deveria estar concentrado:", "ESCALA_0_4", "PROFESSOR", 2),
        ("durante a aula, se movimenta muito ou apresenta inquietação e agitação motora em momentos inadequados, prejudicando o andamento da aula/atividade:", "ESCALA_0_4", "PROFESSOR", 2),
        ("apresenta sinais de ansiedade (maior agitação, batimentos cardíacos acelerados e sudorese excessiva) em situações que não deveriam gerar ansiedade/medo:", "ESCALA_0_4", "PROFESSOR", 2),

        ("durante as aulas/atividades, não demonstra interesse em aprender, não se mostra dedicado e esforçado, mesmo que tenha facilidade no assunto:", "ESCALA_0_4", "PROFESSOR", 3),
        ("não inicia as tarefas propostas, demonstra resistência em fazer as atividades e/ou não consegue concluir as atividades:", "ESCALA_0_4", "PROFESSOR", 3),
        ("não mantém atenção em atividades lúdicas ou interessantes:", "ESCALA_0_4", "PROFESSOR", 3),

        ("nesta semana:", "CHECKBOX", "PROFESSOR", 4),
        
        ("descreva sua observação:", "TEXTO_LIVRE", "PROFESSOR", 5)
        ]
    mycursor.executemany(insert_query, values)

    mydb.commit()
    mycursor.close()
    mydb.close()
    print(mycursor.rowcount, "was inserted.")

def item_escala_parents_insert():
    mydb = get_connection()
    mycursor = mydb.cursor()
    insert_query = "INSERT INTO Item_Escala (descricao, tipo_resposta, tipo_observador, id_dominio) VALUES (%s, %s, %s, %s)"
    values = [
        ("período de sono:", "SONO", "PAIS", None),
        ("apresentou agitação e/ou acordou durante a noite?", "SIM_NAO", "PAIS", None),
        ("houve mudanças na rotina (como visitas ou atividades foram do comum)?", "SIM_NAO", "PAIS", None),
        ("apresentou sinais de ansiedade (ex.: inquietação, irritabilidade etc.)?", "SIM_NAO", "PAIS", None),
        ("comportamento ao ir para a escola:", "CATEGORICO", "PAIS", None),
        ("comportamento ao voltar da escola:", "CATEGORICO", "PAIS", None),
        ("como os pais/responsáveis se sentiram hoje?", "CATEGORICO", "PAIS", None),
        ("demonstrou resistência ao aplicar o óleo?", "SIM_NAO", "PAIS", None)
        ]
    mycursor.executemany(insert_query, values)

    mydb.commit()
    mycursor.close()
    mydb.close()
    print(mycursor.rowcount, "was inserted.")
    

def children_insert():
    mydb = get_connection()
    mycursor = mydb.cursor()
    insert_query = "INSERT INTO Crianca (codigo, data_nascimento, sexo, diagnostico, turno, regular) VALUES (%s, %s, %s, %s, %s)"
    values = [
        ("CR001", date(2021,1,2), "M", "TEA" , "MANHÃ", "MANHÃ"),
        ("CR002", date(2022,9,30), "M", "TEA", "INTEGRAL", "TARDE"),
        ("CR003", date(2020,6,7), "M", "TEA", "MANHÃ", "MANHÃ"),
        ("CR004", date(2020,4,23), "M", "TEA", "INTEGRAL", "MANHÃ"),
        ("CR005", date(2020,2,11), "F", "TEA", "TARDE", "TARDE"),
        ("CR006", date(2020,7,3), "M", "TEA", "MANHÃ", "MANHÃ"),
        ("CR007", date(2018,7,3), "M", "TEA", "TARDE", "TARDE"),
        ("CR008", date(2021,8,11), "M", "TEA", "INTEGRAL", "TARDE"),
        ("CR009", date(2020,6,16), "F", "TEA", "INTEGRAL", "MANHÃ")
    ]
    mycursor.executemany(insert_query, values)

    mydb.commit()
    mycursor.close()
    mydb.close()
    print(mycursor.rowcount, "was inserted.")

def observer_insert():
    mydb = get_connection()
    mycursor = mydb.cursor()
    insert_query = "INSERT INTO Observador (nome, tipo) VALUES (%s, %s)"
    values = [
        ("Patrícia Cássia de Souza Moreira", 'PROFESSOR'),
        ("Maria Imaculada de Souza Silva", 'PROFESSOR'),
        ("Cíntia de Cássia Fernandes Antônio", 'PROFESSOR'),
        ("Rita de Cássia Silvério Gonçalves", 'PROFESSOR'),
        ("Catarina Janete de Souza", 'PROFESSOR'),
        ("Thatiane Prado Goulart Souza", 'PROFESSOR'),
        ("Brenda Lima", 'RESPONSAVEL'),
        ("Lucidalva", 'RESPONSAVEL'),
        ("Cristiane Martins", 'RESPONSAVEL'),
        ("Tayná Martins", 'RESPONSAVEL'),
        ("Gabrieli Silva", 'RESPONSAVEL'),
        ("Aline Prado", 'RESPONSAVEL'),
        ("Caroline Bernardes", 'RESPONSAVEL'),
        ("Alexandrina Ferreira", 'RESPONSAVEL'),
        ("Cláudia", 'RESPONSAVEL'),
    ]
    mycursor.executemany(insert_query, values)

    mydb.commit()
    mycursor.close()
    mydb.close()
    print(mycursor.rowcount, "was inserted.")

def observer_child_insert():
    mydb = get_connection()
    mycursor = mydb.cursor()
    insert_query = "INSERT INTO Observador_Crianca (id_observador, id_crianca, ambiente) VALUES (%s, %s, %s)"
    values = [
        (1, 1, 'ESCOLAR'),
        (1, 6, 'ESCOLAR'),
        (2, 2, 'ESCOLAR'),
        (3, 3, 'ESCOLAR'),
        (3, 4, 'ESCOLAR'),
        (3, 9, 'ESCOLAR'),
        (4, 5, 'ESCOLAR'),
        (5, 7, 'ESCOLAR'),
        (6, 8, 'ESCOLAR'),
        (7, 1, 'DOMICILIAR'),
        (8, 2, 'DOMICILIAR'),
        (9, 3, 'DOMICILIAR'),
        (10, 4, 'DOMICILIAR'),
        (11, 5, 'DOMICILIAR'),
        (12, 6, 'DOMICILIAR'),
        (13, 7, 'DOMICILIAR'),
        (14, 8, 'DOMICILIAR'),
        (15, 9, 'DOMICILIAR')
    ]
    mycursor.executemany(insert_query, values)

    mydb.commit()
    mycursor.close()
    mydb.close()
    print(mycursor.rowcount, "was inserted.")
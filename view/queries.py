queries = {
    'total_criancas_cadastradas':'SELECT count(*) AS criancas from Crianca',
    'total_registros_por_fase':'SELECT nome_fase AS fase, count(*) as total_registros from Registro r INNER JOIN Fase_Estudo f ON r.id_fase = f.id_fase GROUP BY fase',
    'total_registros_por_tipo_observador':'SELECT tipo AS tipo, count(*) as total_registros from Registro r INNER JOIN Observador o ON r.id_observador = o.id_observador GROUP BY tipo',
    'total_pais':'SELECT count(*) AS total_pais FROM Observador WHERE tipo = "RESPONSAVEL"',
    'total_professores': 'SELECT count(*) AS total_professores FROM Observador WHERE tipo = "PROFESSOR"',
    'total_criancas_turno': 'SELECT count(*) AS criancas, turno AS turno FROM Crianca GROUP BY turno',
    'criancas_por_fase': 'SELECT count(*) AS criancas, f.nome_fase AS fase from Crianca c INNER JOIN Registro r ON c.id_crianca = r.id_crianca INNER JOIN Fase_Estudo f ON f.id_fase = r.id_fase GROUP BY fase',
    'registros_por_data': 'SELECT count(*) AS registros, data FROM Registro GROUP BY data',
    'codigos_criancas': 'SELECT codigo FROM Crianca',
    'nomes_fases': 'SELECT nome_fase FROM Fase_Estudo'
}

def find_child(option):
    return f'''
        SELECT id_crianca, codigo, data_nascimento, sexo, turno, regular
        FROM Crianca
        WHERE codigo = "{option}"
    '''

def find_observer(id_crianca):
    return f'''
        SELECT ob.codigo, ob.tipo
        FROM Observador ob
        LEFT JOIN observador_crianca oc ON oc.id_observador = ob.id_observador
        LEFT JOIN crianca c ON c.id_crianca = oc.id_crianca
        WHERE c.id_crianca = {id_crianca}
        GROUP BY ob.codigo, ob.tipo
    '''

def avg_child_items(option):
    return f'''
        SELECT c.codigo AS codigo_crianca, ie.descricao AS item, avg(r.valor_numerico) AS media_valor, fe.nome_fase AS fase
        FROM resposta r
        INNER JOIN item_escala ie ON r.id_item = ie.id_item
        INNER JOIN registro re ON r.id_registro = re.id_registro
        INNER JOIN fase_estudo fe ON re.id_fase = fe.id_fase
        INNER JOIN crianca c ON c.id_crianca = re.id_crianca
        INNER JOIN observador ob ON re.id_observador = ob.id_observador
        WHERE c.codigo = "{option}" AND ie.tipo_resposta = "ESCALA_0_4" AND ob.tipo = "PROFESSOR"
        GROUP BY codigo_crianca, item, nome_fase
    '''

def avg_sleep_by_parents(option):
    return f'''
        SELECT c.codigo AS codigo_crianca, avg(
            CASE oc.descricao
                WHEN "menos de 4h" THEN 2
                WHEN "4h" THEN 4
                WHEN "6h" THEN 6
                WHEN "8h" THEN 8
                WHEN "mais de 8h" THEN 10
            END
        ) AS media_valor, ob.tipo AS tipo_observador, fe.nome_fase AS fase
        FROM resposta r
        INNER JOIN opcao_categorica oc ON oc.id_opcao = r.id_opcao
        INNER JOIN item_escala ie ON r.id_item = ie.id_item
        INNER JOIN registro re ON r.id_registro = re.id_registro
        INNER JOIN observador ob ON re.id_observador = ob.id_observador
        INNER JOIN crianca c ON c.id_crianca = re.id_crianca
        INNER JOIN fase_estudo fe ON re.id_fase = fe.id_fase
        WHERE ob.tipo = "RESPONSAVEL" AND c.codigo = "{option}" AND ie.tipo_resposta = "SONO"
        GROUP BY codigo_crianca, tipo_observador, fase
    '''

def yes_no_frequency(option):
    return f'''
        SELECT c.codigo AS codigo_crianca, ie.descricao AS descricao, fe.nome_fase AS fase, count(*) AS frequencia
        FROM Resposta r
        INNER JOIN Item_Escala ie ON ie.id_item = r.id_item
        INNER JOIN Registro re ON r.id_registro = re.id_registro
        INNER JOIN fase_estudo fe ON re.id_fase = fe.id_fase
        INNER JOIN Crianca c ON c.id_crianca = re.id_crianca
        WHERE ie.tipo_resposta = "SIM_NAO" AND r.id_opcao IN (11) AND c.codigo = "{option}"
        GROUP BY codigo_crianca, descricao, fase
    '''

def comportamental_diference(option, fase):
    return f'''
        SELECT re.data AS data,
            MAX(CASE WHEN r.id_item = 22 THEN oc.descricao END) AS foi_para_escola,
            MAX(CASE WHEN r.id_item = 23 THEN oc.descricao END) AS voltou_da_escola
        FROM Resposta r
        INNER JOIN Registro re ON r.id_registro = re.id_registro
        INNER JOIN Opcao_Categorica oc ON oc.id_opcao = r.id_opcao
        INNER JOIN Crianca c ON c.id_crianca = re.id_crianca
        INNER JOIN Fase_Estudo fe ON fe.id_fase = re.id_fase
        WHERE r.id_item IN (22, 23) AND c.codigo = "{option}" AND fe.nome_fase = "{fase}"
        GROUP BY re.data
        ORDER BY re.data
    '''

def avg_shift(fase):
    return f'''
        SELECT fe.nome_fase AS fase, c.turno AS turno, c.regular AS regular, avg(r.valor_numerico) AS media_respostas
        FROM resposta r
        INNER JOIN item_escala ie ON r.id_item = ie.id_item
        INNER JOIN registro re ON r.id_registro = re.id_registro
        INNER JOIN observador ob ON re.id_observador = ob.id_observador
        INNER JOIN crianca c ON c.id_crianca = re.id_crianca
        INNER JOIN fase_estudo fe ON re.id_fase = fe.id_fase
        WHERE ob.tipo = "PROFESSOR" AND fe.nome_fase = "{fase}" AND ie.tipo_resposta = "ESCALA_0_4"
        GROUP BY fase, regular, turno
    '''

def avg_child_items_by_domains(option, fase):
    return f'''
        SELECT c.codigo AS codigo_crianca, de.nome AS nome_dominio, avg(r.valor_numerico) AS media_valor, fe.nome_fase AS fase
        FROM resposta r
        INNER JOIN item_escala ie ON r.id_item = ie.id_item
        INNER JOIN registro re ON r.id_registro = re.id_registro
        INNER JOIN fase_estudo fe ON re.id_fase = fe.id_fase
        INNER JOIN crianca c ON c.id_crianca = re.id_crianca
        INNER JOIN dominio_escala de ON de.id_dominio = ie.id_dominio
        WHERE c.codigo = "{option}" AND fe.nome_fase = "{fase}"
        GROUP BY codigo_crianca, nome_dominio
    '''

def avg_domains_by_oil():
    return '''
        SELECT o.nome AS oleo, de.nome AS dominio, avg(r.valor_numerico) AS media_valor
        FROM Resposta r
        INNER JOIN Item_Escala ie ON r.id_item = ie.id_item
        INNER JOIN Dominio_Escala de ON ie.id_dominio = de.id_dominio
        INNER JOIN Registro re ON r.id_registro = re.id_registro
        INNER JOIN Fase_Estudo fe ON re.id_fase = fe.id_fase
        INNER JOIN Oleo o ON fe.id_oleo = o.id_oleo
        WHERE ie.tipo_resposta = "ESCALA_0_4"
        GROUP BY oleo, dominio
    '''

def avg_sleep_by_oil():
    return '''
        SELECT o.nome AS oleo, avg(
            CASE oc.descricao
                WHEN "menos de 4h" THEN 2
                WHEN "4h" THEN 4
                WHEN "6h" THEN 6
                WHEN "8h" THEN 8
                WHEN "mais de 8h" THEN 10
            END
        ) AS media_sono
        FROM Resposta r
        INNER JOIN Opcao_Categorica oc ON oc.id_opcao = r.id_opcao
        INNER JOIN Item_Escala ie ON r.id_item = ie.id_item
        INNER JOIN Registro re ON r.id_registro = re.id_registro
        INNER JOIN Fase_Estudo fe ON re.id_fase = fe.id_fase
        INNER JOIN Oleo o ON fe.id_oleo = o.id_oleo
        WHERE ie.tipo_resposta = "SONO"
        GROUP BY oleo
    '''

def yes_no_frequency_by_oil():
    return '''
        SELECT o.nome AS oleo, ie.descricao AS pergunta, count(*) AS frequencia
        FROM Resposta r
        INNER JOIN Item_Escala ie ON r.id_item = ie.id_item
        INNER JOIN Registro re ON r.id_registro = re.id_registro
        INNER JOIN Fase_Estudo fe ON re.id_fase = fe.id_fase
        INNER JOIN Oleo o ON fe.id_oleo = o.id_oleo
        WHERE ie.tipo_resposta = "SIM_NAO" AND r.id_opcao = 11
        GROUP BY oleo, pergunta
    '''

def comportamental_by_oil():
    return '''
        SELECT o.nome AS oleo, ie.descricao AS pergunta, oc.descricao AS resposta, count(*) AS frequencia
        FROM Resposta r
        INNER JOIN Item_Escala ie ON r.id_item = ie.id_item
        INNER JOIN Opcao_Categorica oc ON oc.id_opcao = r.id_opcao
        INNER JOIN Registro re ON r.id_registro = re.id_registro
        INNER JOIN Fase_Estudo fe ON re.id_fase = fe.id_fase
        INNER JOIN Oleo o ON fe.id_oleo = o.id_oleo
        WHERE r.id_item IN (22, 23)
        GROUP BY oleo, pergunta, resposta
    '''

def avg_baseline_vs_intervention():
    return '''
        SELECT
            CASE WHEN fe.id_oleo IS NULL THEN "Linha de Base" ELSE "Intervenção" END AS periodo,
            de.nome AS dominio,
            avg(r.valor_numerico) AS media_valor
        FROM Resposta r
        INNER JOIN Item_Escala ie ON r.id_item = ie.id_item
        INNER JOIN Dominio_Escala de ON ie.id_dominio = de.id_dominio
        INNER JOIN Registro re ON r.id_registro = re.id_registro
        INNER JOIN Observador ob ON re.id_observador = ob.id_observador
        INNER JOIN Fase_Estudo fe ON re.id_fase = fe.id_fase
        WHERE ie.tipo_resposta = "ESCALA_0_4" AND ob.tipo = "PROFESSOR"
        GROUP BY periodo, dominio
    '''

def sleep_baseline_vs_intervention():
    return '''
        SELECT
            CASE WHEN fe.id_oleo IS NULL THEN "Linha de Base" ELSE "Intervenção" END AS periodo,
            avg(
                CASE oc.descricao
                    WHEN "menos de 4h" THEN 2
                    WHEN "4h" THEN 4
                    WHEN "6h" THEN 6
                    WHEN "8h" THEN 8
                    WHEN "mais de 8h" THEN 10
                END
            ) AS media_sono
        FROM Resposta r
        INNER JOIN Opcao_Categorica oc ON oc.id_opcao = r.id_opcao
        INNER JOIN Item_Escala ie ON r.id_item = ie.id_item
        INNER JOIN Registro re ON r.id_registro = re.id_registro
        INNER JOIN Observador ob ON re.id_observador = ob.id_observador
        INNER JOIN Fase_Estudo fe ON re.id_fase = fe.id_fase
        WHERE ie.tipo_resposta = "SONO" AND ob.tipo = "RESPONSAVEL"
        GROUP BY periodo
    '''

def avg_by_environment(fase):
    return f'''
        SELECT
            CASE WHEN ob.tipo = "PROFESSOR" THEN "Escolar" ELSE "Domiciliar" END AS ambiente,
            de.nome AS dominio,
            avg(r.valor_numerico) AS media_valor
        FROM Resposta r
        INNER JOIN Item_Escala ie ON r.id_item = ie.id_item
        INNER JOIN Dominio_Escala de ON ie.id_dominio = de.id_dominio
        INNER JOIN Registro re ON r.id_registro = re.id_registro
        INNER JOIN Observador ob ON re.id_observador = ob.id_observador
        INNER JOIN Fase_Estudo fe ON re.id_fase = fe.id_fase
        WHERE ie.tipo_resposta = "ESCALA_0_4" AND fe.nome_fase = "{fase}"
        GROUP BY ambiente, dominio
    '''

def sleep_by_environment(fase):
    return f'''
        SELECT
            CASE WHEN ob.tipo = "PROFESSOR" THEN "Escolar" ELSE "Domiciliar" END AS ambiente,
            avg(r.valor_numerico) AS media_sono
        FROM Resposta r
        INNER JOIN Item_Escala ie ON r.id_item = ie.id_item
        INNER JOIN Registro re ON r.id_registro = re.id_registro
        INNER JOIN Observador ob ON re.id_observador = ob.id_observador
        INNER JOIN Fase_Estudo fe ON re.id_fase = fe.id_fase
        WHERE ie.tipo_resposta = "SONO" AND fe.nome_fase = "{fase}"
        GROUP BY ambiente
    '''

def avg_sleep_by_parents_by_fase(fase):
    return f'''
        SELECT avg(
            CASE oc.descricao
                WHEN "menos de 4h" THEN 2
                WHEN "4h" THEN 4
                WHEN "6h" THEN 6
                WHEN "8h" THEN 8
                WHEN "mais de 8h" THEN 10
            END
        ) AS media_valor, fe.nome_fase AS fase
        FROM Resposta r
        INNER JOIN Opcao_Categorica oc ON oc.id_opcao = r.id_opcao
        INNER JOIN Item_Escala ie ON r.id_item = ie.id_item
        INNER JOIN Registro re ON r.id_registro = re.id_registro
        INNER JOIN Observador ob ON re.id_observador = ob.id_observador
        INNER JOIN Fase_Estudo fe ON re.id_fase = fe.id_fase
        WHERE ie.tipo_resposta = "SONO" AND ob.tipo = "RESPONSAVEL" AND fe.nome_fase = "{fase}"
        GROUP BY fase
    '''

def yes_no_frequency_by_fase(fase):
    return f'''
        SELECT ie.descricao AS descricao, count(*) AS frequencia
        FROM Resposta r
        INNER JOIN Item_Escala ie ON r.id_item = ie.id_item
        INNER JOIN Registro re ON r.id_registro = re.id_registro
        INNER JOIN Observador ob ON re.id_observador = ob.id_observador
        INNER JOIN Fase_Estudo fe ON re.id_fase = fe.id_fase
        WHERE ie.tipo_resposta = "SIM_NAO" AND r.id_opcao = 11
            AND ob.tipo = "RESPONSAVEL" AND fe.nome_fase = "{fase}"
        GROUP BY descricao
    '''

def adhesion_by_responsible():
    return '''
        SELECT ob.codigo AS responsavel, fe.nome_fase AS fase, count(*) AS total_registros
        FROM Registro re
        INNER JOIN Observador ob ON re.id_observador = ob.id_observador
        INNER JOIN Fase_Estudo fe ON re.id_fase = fe.id_fase
        WHERE ob.tipo = "RESPONSAVEL"
        GROUP BY responsavel, fase
        ORDER BY fase, responsavel
    '''

def feeling_by_fase(fase):
    return f'''
        SELECT oc.descricao AS sentimento, count(*) AS frequencia
        FROM Resposta r
        INNER JOIN Opcao_Categorica oc ON oc.id_opcao = r.id_opcao
        INNER JOIN Registro re ON r.id_registro = re.id_registro
        INNER JOIN Observador ob ON re.id_observador = ob.id_observador
        INNER JOIN Fase_Estudo fe ON re.id_fase = fe.id_fase
        WHERE r.id_item = 24 AND ob.tipo = "RESPONSAVEL" AND fe.nome_fase = "{fase}"
        GROUP BY sentimento
    '''

def feeling_evolution():
    return '''
        SELECT fe.nome_fase AS fase, fe.ordem AS ordem, oc.descricao AS sentimento, count(*) AS frequencia
        FROM Resposta r
        INNER JOIN Opcao_Categorica oc ON oc.id_opcao = r.id_opcao
        INNER JOIN Registro re ON r.id_registro = re.id_registro
        INNER JOIN Observador ob ON re.id_observador = ob.id_observador
        INNER JOIN Fase_Estudo fe ON re.id_fase = fe.id_fase
        WHERE r.id_item = 24 AND ob.tipo = "RESPONSAVEL"
        GROUP BY fase, ordem, sentimento
        ORDER BY ordem
    '''

def oil_resistance_by_fase():
    return '''
        SELECT fe.nome_fase AS fase, fe.ordem AS ordem, count(*) AS frequencia
        FROM Resposta r
        INNER JOIN Registro re ON r.id_registro = re.id_registro
        INNER JOIN Observador ob ON re.id_observador = ob.id_observador
        INNER JOIN Fase_Estudo fe ON re.id_fase = fe.id_fase
        INNER JOIN Oleo o ON fe.id_oleo = o.id_oleo
        WHERE r.id_item = 25 AND r.id_opcao = 11 AND ob.tipo = "RESPONSAVEL"
        GROUP BY fase, ordem
        ORDER BY ordem
    '''

def routine_change_by_fase():
    return '''
        SELECT fe.nome_fase AS fase, fe.ordem AS ordem, count(*) AS frequencia
        FROM Resposta r
        INNER JOIN Registro re ON r.id_registro = re.id_registro
        INNER JOIN Observador ob ON re.id_observador = ob.id_observador
        INNER JOIN Fase_Estudo fe ON re.id_fase = fe.id_fase
        WHERE r.id_item = 20 AND r.id_opcao = 11 AND ob.tipo = "RESPONSAVEL"
        GROUP BY fase, ordem
        ORDER BY ordem
    '''

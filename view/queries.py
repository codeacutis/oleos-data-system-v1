queries = {
    'total_criancas_cadastradas':'SELECT count(*) AS criancas from crianca',
    'total_registros_por_fase':'SELECT nome_fase AS fase, count(*) as total_registros from registro r INNER JOIN fase_estudo f ON r.id_fase = f.id_fase GROUP BY fase',
    'total_registros_por_tipo_observador':'SELECT tipo AS tipo, count(*) as total_registros from registro r INNER JOIN observador o ON r.id_observador = o.id_observador GROUP BY tipo',
    'total_pais':'SELECT count(*) AS total_pais FROM observador WHERE tipo = "RESPONSAVEL"',
    'total_professores': 'SELECT count(*) AS total_professores FROM observador WHERE tipo = "PROFESSOR"',
    'total_criancas_turno': 'SELECT count(*) AS criancas, turno AS turno FROM crianca GROUP BY turno',
    'criancas_por_fase': 'SELECT count(DISTINCT c.id_crianca) AS criancas, f.nome_fase AS fase from crianca c INNER JOIN registro r ON c.id_crianca = r.id_crianca INNER JOIN fase_estudo f ON f.id_fase = r.id_fase GROUP BY fase',
    'registros_por_data': 'SELECT count(*) AS registros, data FROM registro GROUP BY data',
    'codigos_criancas': 'SELECT codigo FROM crianca',
    'nomes_fases': 'SELECT nome_fase FROM fase_estudo'
}

def find_child(option):
    return (
        '''
        SELECT id_crianca, codigo, data_nascimento, sexo, turno, regular
        FROM crianca
        WHERE codigo = %s
        ''',
        (option,)
    )

def find_observer(id_crianca):
    return (
        '''
        SELECT ob.codigo, ob.tipo
        FROM observador ob
        LEFT JOIN observador_crianca oc ON oc.id_observador = ob.id_observador
        LEFT JOIN crianca c ON c.id_crianca = oc.id_crianca
        WHERE c.id_crianca = %s
        GROUP BY ob.codigo, ob.tipo
        ''',
        (id_crianca,)
    )

def avg_child_items(option):
    return (
        '''
        SELECT c.codigo AS codigo_crianca, ie.descricao AS item, avg(r.valor_numerico) AS media_valor, fe.nome_fase AS fase
        FROM resposta r
        INNER JOIN item_escala ie ON r.id_item = ie.id_item
        INNER JOIN registro re ON r.id_registro = re.id_registro
        INNER JOIN fase_estudo fe ON re.id_fase = fe.id_fase
        INNER JOIN crianca c ON c.id_crianca = re.id_crianca
        INNER JOIN observador ob ON re.id_observador = ob.id_observador
        WHERE c.codigo = %s AND ie.tipo_resposta = "ESCALA_0_4" AND ob.tipo = "PROFESSOR"
        GROUP BY codigo_crianca, item, nome_fase
        ''',
        (option,)
    )

def avg_sleep_by_parents(option):
    return (
        '''
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
        LEFT JOIN opcao_categorica oc ON oc.id_opcao = r.id_opcao
        INNER JOIN item_escala ie ON r.id_item = ie.id_item
        INNER JOIN registro re ON r.id_registro = re.id_registro
        INNER JOIN observador ob ON re.id_observador = ob.id_observador
        INNER JOIN crianca c ON c.id_crianca = re.id_crianca
        INNER JOIN fase_estudo fe ON re.id_fase = fe.id_fase
        WHERE ob.tipo = "RESPONSAVEL" AND c.codigo = %s AND ie.tipo_resposta = "SONO"
        GROUP BY codigo_crianca, tipo_observador, fase
        ''',
        (option,)
    )

def yes_no_frequency(option):
    return (
        '''
        SELECT c.codigo AS codigo_crianca,
            CASE
                WHEN ie.descricao LIKE "%ansiedade%" THEN "Sinais de ansiedade"
                WHEN ie.descricao LIKE "%rotina%" THEN "Mudanças de rotina"
                WHEN ie.descricao LIKE "%agitação%" THEN "Agitação noturna"
                WHEN ie.descricao LIKE "%resistência%" THEN "Resistência de Aplicação"
                ELSE ie.descricao
            END AS descricao,
            fe.nome_fase AS fase, count(*) AS frequencia
        FROM resposta r
        INNER JOIN item_escala ie ON ie.id_item = r.id_item
        INNER JOIN registro re ON r.id_registro = re.id_registro
        INNER JOIN fase_estudo fe ON re.id_fase = fe.id_fase
        INNER JOIN crianca c ON c.id_crianca = re.id_crianca
        WHERE ie.tipo_resposta = "SIM_NAO" AND r.id_opcao IN (11) AND c.codigo = %s
        GROUP BY codigo_crianca, descricao, fase
        ''',
        (option,)
    )

def comportamental_diference(option, fase):
    return (
        '''
        SELECT re.data AS data,
            MAX(CASE WHEN r.id_item = 22 THEN COALESCE(oc.descricao, r.valor_texto) END) AS foi_para_escola,
            MAX(CASE WHEN r.id_item = 23 THEN COALESCE(oc.descricao, r.valor_texto) END) AS voltou_da_escola
        FROM resposta r
        INNER JOIN registro re ON r.id_registro = re.id_registro
        LEFT JOIN opcao_categorica oc ON oc.id_opcao = r.id_opcao
        INNER JOIN crianca c ON c.id_crianca = re.id_crianca
        INNER JOIN fase_estudo fe ON fe.id_fase = re.id_fase
        WHERE r.id_item IN (22, 23) AND c.codigo = %s AND fe.nome_fase = %s
        GROUP BY re.data
        ORDER BY re.data
        ''',
        (option, fase)
    )

def avg_shift(fase):
    return (
        '''
        SELECT fe.nome_fase AS fase, c.turno AS turno, c.regular AS regular, avg(r.valor_numerico) AS media_respostas
        FROM resposta r
        INNER JOIN item_escala ie ON r.id_item = ie.id_item
        INNER JOIN registro re ON r.id_registro = re.id_registro
        INNER JOIN observador ob ON re.id_observador = ob.id_observador
        INNER JOIN crianca c ON c.id_crianca = re.id_crianca
        INNER JOIN fase_estudo fe ON re.id_fase = fe.id_fase
        WHERE ob.tipo = "PROFESSOR" AND fe.nome_fase = %s AND ie.tipo_resposta = "ESCALA_0_4"
        GROUP BY fase, regular, turno
        ''',
        (fase,)
    )

def avg_child_items_by_domains(option, fase):
    return (
        '''
        SELECT c.codigo AS codigo_crianca, de.nome AS nome_dominio, avg(r.valor_numerico) AS media_valor, fe.nome_fase AS fase
        FROM resposta r
        INNER JOIN item_escala ie ON r.id_item = ie.id_item
        INNER JOIN registro re ON r.id_registro = re.id_registro
        INNER JOIN fase_estudo fe ON re.id_fase = fe.id_fase
        INNER JOIN crianca c ON c.id_crianca = re.id_crianca
        INNER JOIN dominio_escala de ON de.id_dominio = ie.id_dominio
        WHERE c.codigo = %s AND fe.nome_fase = %s
        GROUP BY codigo_crianca, nome_dominio
        ''',
        (option, fase)
    )

def avg_domains_by_oil():
    return '''
        SELECT o.nome AS oleo, de.nome AS dominio, avg(r.valor_numerico) AS media_valor
        FROM resposta r
        INNER JOIN item_escala ie ON r.id_item = ie.id_item
        INNER JOIN dominio_escala de ON ie.id_dominio = de.id_dominio
        INNER JOIN registro re ON r.id_registro = re.id_registro
        INNER JOIN fase_estudo fe ON re.id_fase = fe.id_fase
        INNER JOIN oleo o ON fe.id_oleo = o.id_oleo
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
        FROM resposta r
        LEFT JOIN opcao_categorica oc ON oc.id_opcao = r.id_opcao
        INNER JOIN item_escala ie ON r.id_item = ie.id_item
        INNER JOIN registro re ON r.id_registro = re.id_registro
        INNER JOIN fase_estudo fe ON re.id_fase = fe.id_fase
        INNER JOIN oleo o ON fe.id_oleo = o.id_oleo
        WHERE ie.tipo_resposta = "SONO"
        GROUP BY oleo
    '''

def yes_no_frequency_by_oil():
    return '''
        SELECT o.nome AS oleo,
            CASE
                WHEN ie.descricao LIKE "%ansiedade%" THEN "Sinais de ansiedade"
                WHEN ie.descricao LIKE "%rotina%" THEN "Mudanças de rotina"
                WHEN ie.descricao LIKE "%agitação%" THEN "Agitação noturna"
                WHEN ie.descricao LIKE "%resistência%" THEN "Resistência de Aplicação"
                ELSE ie.descricao
            END AS pergunta,
            count(*) AS frequencia
        FROM resposta r
        INNER JOIN item_escala ie ON r.id_item = ie.id_item
        INNER JOIN registro re ON r.id_registro = re.id_registro
        INNER JOIN fase_estudo fe ON re.id_fase = fe.id_fase
        INNER JOIN oleo o ON fe.id_oleo = o.id_oleo
        WHERE ie.tipo_resposta = "SIM_NAO" AND r.id_opcao = 11
        GROUP BY oleo, pergunta
    '''

def comportamental_by_oil():
    return '''
        SELECT o.nome AS oleo,
            CASE r.id_item
                WHEN 22 THEN "Foi para Escola"
                WHEN 23 THEN "Voltou da Escola"
            END AS pergunta,
            oc.descricao AS resposta, count(*) AS frequencia
        FROM resposta r
        INNER JOIN item_escala ie ON r.id_item = ie.id_item
        INNER JOIN opcao_categorica oc ON oc.id_opcao = r.id_opcao
        INNER JOIN registro re ON r.id_registro = re.id_registro
        INNER JOIN fase_estudo fe ON re.id_fase = fe.id_fase
        INNER JOIN oleo o ON fe.id_oleo = o.id_oleo
        WHERE r.id_item IN (22, 23)
        GROUP BY oleo, pergunta, resposta
    '''

def avg_baseline_vs_intervention():
    return '''
        SELECT
            CASE WHEN fe.id_oleo IS NULL THEN "Linha de Base" ELSE "Intervenção" END AS periodo,
            de.nome AS dominio,
            avg(r.valor_numerico) AS media_valor
        FROM resposta r
        INNER JOIN item_escala ie ON r.id_item = ie.id_item
        INNER JOIN dominio_escala de ON ie.id_dominio = de.id_dominio
        INNER JOIN registro re ON r.id_registro = re.id_registro
        INNER JOIN observador ob ON re.id_observador = ob.id_observador
        INNER JOIN fase_estudo fe ON re.id_fase = fe.id_fase
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
        FROM resposta r
        LEFT JOIN opcao_categorica oc ON oc.id_opcao = r.id_opcao
        INNER JOIN item_escala ie ON r.id_item = ie.id_item
        INNER JOIN registro re ON r.id_registro = re.id_registro
        INNER JOIN observador ob ON re.id_observador = ob.id_observador
        INNER JOIN fase_estudo fe ON re.id_fase = fe.id_fase
        WHERE ie.tipo_resposta = "SONO" AND ob.tipo = "RESPONSAVEL"
        GROUP BY periodo
    '''

def avg_by_environment(fase):
    return (
        '''
        SELECT
            CASE WHEN ob.tipo = "PROFESSOR" THEN "Escolar" ELSE "Domiciliar" END AS ambiente,
            de.nome AS dominio,
            avg(r.valor_numerico) AS media_valor
        FROM resposta r
        INNER JOIN item_escala ie ON r.id_item = ie.id_item
        INNER JOIN dominio_escala de ON ie.id_dominio = de.id_dominio
        INNER JOIN registro re ON r.id_registro = re.id_registro
        INNER JOIN observador ob ON re.id_observador = ob.id_observador
        INNER JOIN fase_estudo fe ON re.id_fase = fe.id_fase
        WHERE ie.tipo_resposta = "ESCALA_0_4" AND fe.nome_fase = %s
        GROUP BY ambiente, dominio
        ''',
        (fase,)
    )

def sleep_by_environment(fase):
    return (
        '''
        SELECT
            CASE WHEN ob.tipo = "PROFESSOR" THEN "Escolar" ELSE "Domiciliar" END AS ambiente,
            avg(r.valor_numerico) AS media_sono
        FROM resposta r
        INNER JOIN item_escala ie ON r.id_item = ie.id_item
        INNER JOIN registro re ON r.id_registro = re.id_registro
        INNER JOIN observador ob ON re.id_observador = ob.id_observador
        INNER JOIN fase_estudo fe ON re.id_fase = fe.id_fase
        WHERE ie.tipo_resposta = "SONO" AND fe.nome_fase = %s
        GROUP BY ambiente
        ''',
        (fase,)
    )

def avg_sleep_by_parents_by_fase(fase):
    return (
        '''
        SELECT avg(
            CASE oc.descricao
                WHEN "menos de 4h" THEN 2
                WHEN "4h" THEN 4
                WHEN "6h" THEN 6
                WHEN "8h" THEN 8
                WHEN "mais de 8h" THEN 10
            END
        ) AS media_valor, fe.nome_fase AS fase
        FROM resposta r
        LEFT JOIN opcao_categorica oc ON oc.id_opcao = r.id_opcao
        INNER JOIN item_escala ie ON r.id_item = ie.id_item
        INNER JOIN registro re ON r.id_registro = re.id_registro
        INNER JOIN observador ob ON re.id_observador = ob.id_observador
        INNER JOIN fase_estudo fe ON re.id_fase = fe.id_fase
        WHERE ie.tipo_resposta = "SONO" AND ob.tipo = "RESPONSAVEL" AND fe.nome_fase = %s
        GROUP BY fase
        ''',
        (fase,)
    )

def yes_no_frequency_by_fase(fase):
    return (
        '''
        SELECT
            CASE
                WHEN ie.descricao LIKE "%ansiedade%" THEN "Sinais de ansiedade"
                WHEN ie.descricao LIKE "%rotina%" THEN "Mudanças de rotina"
                WHEN ie.descricao LIKE "%agitação%" THEN "Agitação noturna"
                ELSE ie.descricao
            END AS descricao,
            count(*) AS frequencia
        FROM resposta r
        INNER JOIN item_escala ie ON r.id_item = ie.id_item
        INNER JOIN registro re ON r.id_registro = re.id_registro
        INNER JOIN observador ob ON re.id_observador = ob.id_observador
        INNER JOIN fase_estudo fe ON re.id_fase = fe.id_fase
        WHERE ie.tipo_resposta = "SIM_NAO" AND r.id_opcao = 11
            AND ob.tipo = "RESPONSAVEL" AND fe.nome_fase = %s
        GROUP BY descricao
        ''',
        (fase,)
    )

def adhesion_by_responsible():
    return '''
        SELECT ob.codigo AS responsavel, fe.nome_fase AS fase, count(*) AS total_registros
        FROM registro re
        INNER JOIN observador ob ON re.id_observador = ob.id_observador
        INNER JOIN fase_estudo fe ON re.id_fase = fe.id_fase
        WHERE ob.tipo = "RESPONSAVEL"
        GROUP BY responsavel, fase
        ORDER BY fase, responsavel
    '''

def feeling_by_fase(fase):
    return (
        '''
        SELECT oc.descricao AS sentimento, count(*) AS frequencia
        FROM resposta r
        INNER JOIN opcao_categorica oc ON oc.id_opcao = r.id_opcao
        INNER JOIN registro re ON r.id_registro = re.id_registro
        INNER JOIN observador ob ON re.id_observador = ob.id_observador
        INNER JOIN fase_estudo fe ON re.id_fase = fe.id_fase
        WHERE r.id_item = 24 AND ob.tipo = "RESPONSAVEL" AND fe.nome_fase = %s
        GROUP BY sentimento
        ''',
        (fase,)
    )

def feeling_evolution():
    return '''
        SELECT fe.nome_fase AS fase, fe.ordem AS ordem, oc.descricao AS sentimento, count(*) AS frequencia
        FROM resposta r
        INNER JOIN opcao_categorica oc ON oc.id_opcao = r.id_opcao
        INNER JOIN registro re ON r.id_registro = re.id_registro
        INNER JOIN observador ob ON re.id_observador = ob.id_observador
        INNER JOIN fase_estudo fe ON re.id_fase = fe.id_fase
        WHERE r.id_item = 24 AND ob.tipo = "RESPONSAVEL"
        GROUP BY fase, ordem, sentimento
        ORDER BY ordem
    '''

def oil_resistance_by_fase():
    return '''
        SELECT fe.nome_fase AS fase, fe.ordem AS ordem, count(*) AS frequencia
        FROM resposta r
        INNER JOIN registro re ON r.id_registro = re.id_registro
        INNER JOIN observador ob ON re.id_observador = ob.id_observador
        INNER JOIN fase_estudo fe ON re.id_fase = fe.id_fase
        WHERE r.id_item = 25 AND r.id_opcao = 11 AND ob.tipo = "RESPONSAVEL"
        GROUP BY fase, ordem
        ORDER BY ordem
    '''

def routine_change_by_fase():
    return '''
        SELECT fe.nome_fase AS fase, fe.ordem AS ordem, count(*) AS frequencia
        FROM resposta r
        INNER JOIN registro re ON r.id_registro = re.id_registro
        INNER JOIN observador ob ON re.id_observador = ob.id_observador
        INNER JOIN fase_estudo fe ON re.id_fase = fe.id_fase
        WHERE r.id_item = 20 AND r.id_opcao = 11 AND ob.tipo = "RESPONSAVEL"
        GROUP BY fase, ordem
        ORDER BY ordem
    '''

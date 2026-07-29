queries = {
    'total_criancas_cadastradas':'SELECT count(*) AS criancas from Crianca',
    'total_registros_por_fase':'SELECT nome_fase AS fase, count(*) as total_registros from Registro r INNER JOIN Fase_Estudo f ON r.id_fase = f.id_fase GROUP BY fase',
    'total_registros_por_tipo_observador':'SELECT tipo AS tipo, count(*) as total_registros from Registro r INNER JOIN Observador o ON r.id_observador = o.id_observador GROUP BY tipo',
    'total_pais':'SELECT count(*) AS total_pais FROM Observador WHERE tipo = "RESPONSAVEL"',
    'total_professores': 'SELECT count(*) AS total_professores FROM Observador WHERE tipo = "PROFESSOR"',
    'total_criancas_turno': 'SELECT count(*) AS criancas, turno AS turno FROM Crianca GROUP BY turno',
    'criancas_por_fase': 'SELECT count(*) AS criancas, f.nome_fase AS fase from Crianca c INNER JOIN Registro r ON c.id_crianca = r.id_crianca INNER JOIN Fase_Estudo f ON f.id_fase = r.id_fase GROUP BY fase',
    'registros_por_data': 'SELECT count(*) AS registros, data FROM Registro GROUP BY data',
    'codigos_criancas': 'SELECT codigo FROM Crianca'
}

def find_child(option):
    return f'SELECT * FROM Crianca WHERE codigo = "{option}"'

def find_observer(id_crianca):
    return f'SELECT ob.nome, ob.tipo FROM Observador ob LEFT join observador_crianca oc on oc.id_observador = ob.id_observador left join crianca c on c.id_crianca = oc.id_crianca where c.id_crianca = {id_crianca} group by ob.nome, ob.tipo'

def avg_child_items(option):
    return f'select c.codigo as codigo_crianca, ie.descricao as item, avg(r.valor_numerico) as media_valor, fe.nome_fase as fase from resposta r inner join item_escala ie on r.id_item = ie.id_item inner join registro re on r.id_registro = re.id_registro inner join fase_estudo fe on re.id_fase = fe.id_fase inner join crianca c on c.id_crianca = re.id_crianca where c.codigo = "{option}" group by codigo_crianca, item, nome_fase'

def avg_sleep_by_parents(option):
    return f'select c.codigo as codigo_crianca, ie.descricao as item, avg(r.valor_numerico) as media_valor, ob.tipo as tipo_observador, fe.nome_fase as fase from resposta r inner join item_escala ie on r.id_item = ie.id_item inner join registro re on r.id_registro = re.id_registro inner join observador ob on re.id_observador = ob.id_observador inner join crianca c on c.id_crianca = re.id_crianca inner join fase_estudo fe on re.id_fase = fe.id_fase where ob.tipo = "RESPONSAVEL" and c.codigo = "{option}" and ie.tipo_resposta = "SONO" group by codigo_crianca, item, tipo_observador, fase'
# Paleta semântica centralizada do dashboard

# ── Cores base ────────────────────────────────────────────────────────────────
VERDE        = "#3BAA6D"
AMARELO      = "#E9B949"
LARANJA      = "#D9822B"
VERMELHO     = "#D65A5A"
AZUL         = "#3A86C8"
CINZA        = "#A7B0B7"
CINZA_ESCURO = "#5B6570"

# ── Fases do estudo ───────────────────────────────────────────────────────────
# Linha de base = cinza (referência), intervenções = cores distintas e contrastantes
FASES = {
    "linha_base": CINZA,
    "lavanda": "#9B59B6",
    "mandarina": "#E67E22",
    "patchouli": "#795548",
    "ylang": "#D4A72C",
}

# ── Períodos (baseline vs intervenção) ────────────────────────────────────────
PERIODOS = {
    "Linha de Base": CINZA,
    "Intervenção":   VERDE,
}

# ── Sentimentos dos responsáveis ──────────────────────────────────────────────
SENTIMENTOS = {
    "calmos":       VERDE,
    "preocupados":  AMARELO,
    "estressados":  LARANJA,
    "nervosos":     VERMELHO,
}

# ── Eventos adversos (SIM_NAO) ────────────────────────────────────────────────
EVENTOS_ADVERSOS = {
    "Agitação noturna": "#E88989",
    "Mudanças de rotina": "#F8B4B4",
    "Sinais de ansiedade": "#D65A5A",
    "Resistência de Aplicação": "#B83A3A",
} # vermelho único — todos são negativos

# ── Ambientes ─────────────────────────────────────────────────────────────────
AMBIENTES = {
    "Escolar":    AZUL,
    "Domiciliar": VERDE,
}

# ── Comportamento (ir/voltar escola) ─────────────────────────────────────────
# Mapeado por resposta categórica — positivo=verde, negativo=vermelho, neutro=cinza
COMPORTAMENTO = {
    "calmo": AZUL,
    "agressivo": VERMELHO,
    "ansioso/agitado": LARANJA,
    "triste": CINZA,
    "alegre": VERDE,
}

# ── Sequências neutras para comparações estruturais ───────────────────────────
# Usadas em gráficos sem julgamento semântico (turnos, domínios, óleos)
SEQUENCIA_NEUTRA   = [AZUL, CINZA, "#5DADE2", "#85C1E9", "#AED6F1"]
SEQUENCIA_DOMINIOS = ["#3498DB", "#9B59B6", "#1ABC9C", "#E67E22", "#E74C3C"]
SEQUENCIA_OLEOS    = ["#9B59B6", LARANJA, "#795548", "#00BCD4"]

import re

with open('Mockup_Honorarios_Matriz.dax', 'r', encoding='utf8') as f:
    dax = f.read()

# For Honorarios encontrados and Nao Aprovados
dax = dax.replace(
    'FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO]',
    'FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12), vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO]'
)

# For Honorarios apresentados and Honorarios aprovados
dax = dax.replace(
    'vw_powerbi_relatorio_aprovacao[DATA_RT] >= _dataInicial, vw_powerbi_relatorio_aprovacao[DATA_RT] <= _dataFinal, vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO]',
    'FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM") = _d, vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12), vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO]'
)

with open('Mockup_Honorarios_Matriz.dax', 'w', encoding='utf8') as f:
    f.write(dax)

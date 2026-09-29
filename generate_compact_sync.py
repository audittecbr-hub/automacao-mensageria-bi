import json
import subprocess
from compact_builder import build_compact_detalhe_measure

base_measures = [
    {
        "tableName": "vw_powerbi_relatorio_aprovacao",
        "name": "Honorários encontrados",
        "expression": """SUM(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_ENCONTRADO])"""
    },
    {
        "tableName": "vw_powerbi_relatorio_aprovacao",
        "name": "Honorários apresentados",
        "expression": """CALCULATE(
    SUM(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_APRESENTADO]),
    KEEPFILTERS(vw_powerbi_relatorio_aprovacao[area_anterior] = "REUNIÃO TÉCNICA"),
    KEEPFILTERS(NOT ISBLANK(vw_powerbi_relatorio_aprovacao[data_rt])),
    KEEPFILTERS(vw_powerbi_relatorio_aprovacao[data_rt] <= TODAY())
)"""
    },
    {
        "tableName": "vw_powerbi_relatorio_aprovacao",
        "name": "Honorários aprovados",
        "expression": """SUMX(
    vw_powerbi_relatorio_aprovacao,
    COALESCE(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_HONORARIOS_INICIAIS], vw_powerbi_relatorio_aprovacao[HONORARIOS_INICIAIS], 0) +
    vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_COMPENSACAO] +
    vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_RESTITUICAO] +
    vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_AJUIZAMENTO]
)"""
    },
    {
        "tableName": "vw_powerbi_relatorio_aprovacao",
        "name": "Honorário negociação",
        "expression": """CALCULATE(
    SUM(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_EM_NEGOCIACAO]),
    KEEPFILTERS(vw_powerbi_relatorio_aprovacao[AREA_ANTERIOR] = "REUNIÃO TÉCNICA"),
    KEEPFILTERS(vw_powerbi_relatorio_aprovacao[AREA_ATUAL] = "NEGOCIAÇÃO")
)"""
    },
    {
        "tableName": "vw_powerbi_relatorio_aprovacao",
        "name": "Honorários perdidos",
        "expression": """CALCULATE(
    SUM(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_NAO_APROVADO]),
    KEEPFILTERS(vw_powerbi_relatorio_aprovacao[AREA_ANTERIOR] = "NEGOCIAÇÃO"),
    KEEPFILTERS(vw_powerbi_relatorio_aprovacao[AREA_ATUAL] = "FIM")
)"""
    },
    {
        "tableName": "vw_powerbi_relatorio_aprovacao",
        "name": "Honorários não aprovados",
        "expression": """CALCULATE(
    SUM(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_NAO_APROVADO]),
    KEEPFILTERS(vw_powerbi_relatorio_aprovacao[AREA_ANTERIOR] = "REUNIÃO TÉCNICA"),
    KEEPFILTERS(vw_powerbi_relatorio_aprovacao[AREA_ATUAL] = "FIM")
)"""
    }
]

detalhes_measures = [
    {
        "tableName": "medidas_html",
        "name": "HTML_Detalhamento_Encontrados",
        "expression": build_compact_detalhe_measure(
            titulo="DETALHAMENTO <span>HONORÁRIOS ENCONTRADOS</span>",
            tipo="Encontrado",
            val_col="vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_ENCONTRADO]",
            filter_condition="vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_ENCONTRADO] > 0 && vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] >= DATE(2026, 6, 1) && vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] <= DATE(2026, 12, 31)",
            order_expr="vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_ENCONTRADO]"
        )
    },
    {
        "tableName": "medidas_html",
        "name": "HTML_Detalhamento_Apresentados",
        "expression": build_compact_detalhe_measure(
            titulo="DETALHAMENTO <span>HONORÁRIOS APRESENTADOS</span>",
            tipo="Apresentado",
            val_col="vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_APRESENTADO]",
            filter_condition="vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_APRESENTADO] > 0 && vw_powerbi_relatorio_aprovacao[AREA_ANTERIOR] = \"REUNIÃO TÉCNICA\" && vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12) && vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] >= DATE(2026, 6, 1) && vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] <= DATE(2026, 12, 31)",
            order_expr="vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_APRESENTADO]"
        )
    },
    {
        "tableName": "medidas_html",
        "name": "HTML_Detalhamento_Aprovados",
        "expression": build_compact_detalhe_measure(
            titulo="DETALHAMENTO <span>HONORÁRIOS APROVADOS</span>",
            tipo="Aprovado",
            val_col="(COALESCE(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_HONORARIOS_INICIAIS], vw_powerbi_relatorio_aprovacao[HONORARIOS_INICIAIS], 0) + vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_COMPENSACAO] + vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_RESTITUICAO] + vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_AJUIZAMENTO])",
            filter_condition="(COALESCE(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_HONORARIOS_INICIAIS], vw_powerbi_relatorio_aprovacao[HONORARIOS_INICIAIS], 0) + vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_COMPENSACAO] + vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_RESTITUICAO] + vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_AJUIZAMENTO]) > 0 && vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12) && vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] >= DATE(2026, 6, 1) && vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] <= DATE(2026, 12, 31)",
            order_expr="(COALESCE(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_HONORARIOS_INICIAIS], vw_powerbi_relatorio_aprovacao[HONORARIOS_INICIAIS], 0) + vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_COMPENSACAO] + vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_RESTITUICAO] + vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_AJUIZAMENTO])"
        )
    },
    {
        "tableName": "medidas_html",
        "name": "HTML_Detalhamento_Negociacao",
        "expression": build_compact_detalhe_measure(
            titulo="DETALHAMENTO <span>HONORÁRIOS EM NEGOCIAÇÃO</span>",
            tipo="Negociação",
            val_col="vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_EM_NEGOCIACAO]",
            filter_condition="vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_EM_NEGOCIACAO] > 0 && vw_powerbi_relatorio_aprovacao[AREA_ANTERIOR] = \"REUNIÃO TÉCNICA\" && vw_powerbi_relatorio_aprovacao[AREA_ATUAL] = \"NEGOCIAÇÃO\" && vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12) && vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] >= DATE(2026, 6, 1) && vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] <= DATE(2026, 12, 31)",
            order_expr="vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_EM_NEGOCIACAO]"
        )
    },
    {
        "tableName": "medidas_html",
        "name": "HTML_Detalhamento_Perdidos",
        "expression": build_compact_detalhe_measure(
            titulo="DETALHAMENTO <span>HONORÁRIOS PERDIDOS</span>",
            tipo="Perdido",
            val_col="vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_NAO_APROVADO]",
            filter_condition="vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_NAO_APROVADO] > 0 && vw_powerbi_relatorio_aprovacao[AREA_ANTERIOR] = \"NEGOCIAÇÃO\" && vw_powerbi_relatorio_aprovacao[AREA_ATUAL] = \"FIM\" && vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12) && vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] >= DATE(2026, 6, 1) && vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] <= DATE(2026, 12, 31)",
            order_expr="vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_NAO_APROVADO]"
        )
    },
    {
        "tableName": "medidas_html",
        "name": "HTML_Detalhamento_Nao_Aprovados",
        "expression": build_compact_detalhe_measure(
            titulo="DETALHAMENTO <span>HONORÁRIOS NÃO APROVADOS</span>",
            tipo="Não Aprov.",
            val_col="vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_NAO_APROVADO]",
            filter_condition="vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_NAO_APROVADO] > 0 && vw_powerbi_relatorio_aprovacao[AREA_ANTERIOR] = \"REUNIÃO TÉCNICA\" && vw_powerbi_relatorio_aprovacao[AREA_ATUAL] = \"FIM\" && vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12) && vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] >= DATE(2026, 6, 1) && vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] <= DATE(2026, 12, 31)",
            order_expr="vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_NAO_APROVADO]"
        )
    },
    {
        "tableName": "medidas_html",
        "name": "HTML_Detalhamento_Iniciais",
        "expression": build_compact_detalhe_measure(
            titulo="DETALHAMENTO <span>HONORÁRIOS INICIAIS</span>",
            tipo="Iniciais",
            val_col="COALESCE(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_HONORARIOS_INICIAIS], vw_powerbi_relatorio_aprovacao[HONORARIOS_INICIAIS], 0)",
            filter_condition="COALESCE(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_HONORARIOS_INICIAIS], vw_powerbi_relatorio_aprovacao[HONORARIOS_INICIAIS], 0) > 0 && vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12) && vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] >= DATE(2026, 6, 1) && vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] <= DATE(2026, 12, 31)",
            order_expr="COALESCE(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_HONORARIOS_INICIAIS], vw_powerbi_relatorio_aprovacao[HONORARIOS_INICIAIS], 0)"
        )
    },
    {
        "tableName": "medidas_html",
        "name": "HTML_Detalhamento_Restituicao",
        "expression": build_compact_detalhe_measure(
            titulo="DETALHAMENTO <span>HONORÁRIOS RESTITUIÇÃO</span>",
            tipo="Restituição",
            val_col="vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_RESTITUICAO]",
            filter_condition="vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_RESTITUICAO] > 0 && vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12) && vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] >= DATE(2026, 6, 1) && vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] <= DATE(2026, 12, 31)",
            order_expr="vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_RESTITUICAO]"
        )
    }
]

payload = base_measures + detalhes_measures

with open('compact_sync_payload.json', 'w', encoding='utf-8') as f:
    json.dump(payload, f, ensure_ascii=False, indent=2)

print(f"Generated compact_sync_payload.json with {len(payload)} measures")

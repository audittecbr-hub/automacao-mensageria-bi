# Script to verify the exact sums with the proposed filter
import json

# Let's test the queries via dax_query_operations
test_dax = """
EVALUATE
ROW(
    "Aprovados_Mockup", CALCULATE(
        [Honorários aprovados],
        vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12),
        vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] >= DATE(2026, 6, 1),
        vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] <= DATE(2026, 12, 31)
    ),
    "Negociacao_Mockup", CALCULATE(
        [Honorário negociação],
        vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12),
        vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] >= DATE(2026, 6, 1),
        vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] <= DATE(2026, 12, 31)
    ),
    "Perdidos_Mockup", CALCULATE(
        [Honorários perdidos],
        vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12),
        vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] >= DATE(2026, 6, 1),
        vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] <= DATE(2026, 12, 31)
    ),
    "NaoAprov_Mockup", CALCULATE(
        [Honorários não aprovados],
        vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12),
        vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] >= DATE(2026, 6, 1),
        vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] <= DATE(2026, 12, 31)
    )
)
"""
print("DAX test query ready")

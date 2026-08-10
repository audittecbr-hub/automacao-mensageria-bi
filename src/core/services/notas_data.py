"""
Serviço de Dados para Notas Fiscais.
Responsável por buscar a quantidade de notas emitidas no Power BI via DAX.
"""

from datetime import datetime
from src.config import POWERBI_CONFIG
from src.core.clients.powerbi_client import PowerBIClient
from src.core.services.dax_queries import get_notas_emitidas_query
from src.core.utils.logger import get_logger

logger = get_logger("notas_data")

class NotasDataFetcher:
    def __init__(self):
        # Utilizando o workspace e dataset padrão configurado
        self.client = PowerBIClient(
            workspace_id=POWERBI_CONFIG.get("metas_workspace_id", POWERBI_CONFIG.get("workspace_id")),
            dataset_id=POWERBI_CONFIG.get("metas_dataset_id")
        )
        self._authenticated = False

    def authenticate(self) -> bool:
        if not self._authenticated:
            self._authenticated = self.client.authenticate()
        return self._authenticated

    def _get_month_range(self) -> tuple[str, str]:
        now = datetime.now()
        start = datetime(now.year, now.month, 1)
        end = now
        start_str = f"DATE({start.year}, {start.month}, {start.day})"
        end_str = f"DATE({end.year}, {end.month}, {end.day})"
        return start_str, end_str

    def fetch_notas_emitidas(self) -> list[dict]:
        """Busca a contagem de notas emitidas agrupadas por empresa no mês atual."""
        if not self.authenticate():
            logger.error("Falha na autenticação com Power BI")
            return []

        start_str, end_str = self._get_month_range()
        query = get_notas_emitidas_query(start_str, end_str)

        try:
            result = self.client.execute_dax(query)
            notas_por_empresa = []
            
            if result:
                for row in result:
                    # Tenta os possíveis formatos de retorno de chave do DAX Rest API
                    empresa_nome = row.get("public contas_receber_grupo[empresa_nome]") or \
                                   row.get("'public contas_receber_grupo'[empresa_nome]") or \
                                   "Desconhecida"
                    
                    cnpj = row.get("public contas_receber_grupo[empresa_cnpj]") or \
                           row.get("'public contas_receber_grupo'[empresa_cnpj]") or \
                           ""
                    
                    qtd = row.get("[Qtd_Notas]", 0)
                    valor = row.get("[Valor_Total]", 0)
                    
                    notas_por_empresa.append({
                        "cnpj": cnpj,
                        "name": empresa_nome,
                        "value": qtd,
                        "valor": valor
                    })
                
                # Ordenar por valor decrescente ou quantidade (vamos usar valor)
                notas_por_empresa.sort(key=lambda x: x["valor"], reverse=True)
                
            return notas_por_empresa
        except Exception as e:
            logger.error(f"Erro ao buscar notas emitidas: {e}")
            return []

"""
Automação Notas Fiscais Emitidas
Extrai dados da tabela contas_receber_grupo e envia ranking de notas emitidas.
"""

import os
import argparse
import random
from datetime import datetime

from src.config import IMAGES_DIR
from src.core.services.notas_data import NotasDataFetcher
from src.core.services.image_generator import ImageGenerator
from src.core.services.supabase_service import SupabaseService
from src.core.services.notification_service import NotificationService
from src.core.utils.greeting import get_saudacao
from src.core.utils.logger import get_logger
from jinja2 import Template

logger = get_logger("run_notas")

class NotasAutomation:
    def __init__(self):
        self.fetcher = NotasDataFetcher()
        self.image_gen = ImageGenerator()
        self.supabase = SupabaseService()
        
        os.makedirs(IMAGES_DIR, exist_ok=True)
        
    def generate_image(self, data):
        logger.info("Gerando imagem de notas emitidas...")
        output_path = os.path.join(IMAGES_DIR, "notas_emitidas.png")
        return self.image_gen.generate_notas_image(data, output_path=output_path)
        
    def send_whatsapp(self, image_path, custom_recipients=None, template_content=None, dry_run=False):
        logger.info("Preparando envio para WhatsApp...")
        
        if not custom_recipients:
            logger.warning("Nenhum destinatário fornecido para notas (custom_recipients vazio).")
            # Para testes caso rode sem parâmetros de cron
            if not dry_run:
                return
            
        notification_service = NotificationService(self.supabase)
        batch = []
        
        fallback_template = (
            "{{saudacao}}, {{nome}}!\n\n"
            "Confira o fechamento parcial das Notas Fiscais emitidas neste mês até agora."
        )
        current_template = template_content or fallback_template
        
        recipients_list = custom_recipients or [{"nome": "Teste Local", "telefone": "123456"}]
        
        for pessoa in recipients_list:
            nome = pessoa.get("nome") or pessoa.get("name") or "Colaborador"
            telefone = pessoa.get("telefone") or pessoa.get("phone")
            
            if not telefone:
                continue
                
            primeiro_nome = nome.split()[0].title()
            saudacao = get_saudacao()
            
            context = {
                "nome": primeiro_nome,
                "nome_completo": nome,
                "saudacao": saudacao,
                "saudacao_lower": saudacao.lower()
            }
            
            try:
                if "{{" in current_template:
                    caption = Template(current_template).render(**context)
                else:
                    caption = current_template.format(**context)
            except Exception as e:
                logger.error(f"Erro no template de notas para {nome}: {e}")
                caption = f"{saudacao}, {primeiro_nome}!\n\nSegue o relatório de Notas."
                
            batch.append((pessoa, image_path, caption))
            
        if not dry_run:
            results = notification_service.send_batch(batch, context_tag="notas")
            logger.info(f"[Notas] Envios: {results['success']} ok, {results['failed']} falhas.")
        else:
            logger.info(f"[DRY-RUN] Simulação de envio para {len(batch)} destinatários.")
            for p, img, cap in batch:
                nome_p = p.get("nome") or p.get("name") or "Sem nome"
                logger.info(f"   -> Enviar para: {nome_p} | Imagem: {os.path.basename(img)}")
                
    def run(self, generate_only=False, recipients=None, template_content=None, dry_run=False):
        logger.info("\n=== AUTOMAÇÃO NOTAS EMITIDAS ===")
        
        data = self.fetcher.fetch_notas_emitidas()
        
        if not data:
            logger.warning("Nenhum dado de notas encontrado para o mês atual.")
            return
            
        logger.info(f"Dados obtidos: {len(data)} empresas emitiram notas.")
            
        image_path = self.generate_image(data)
        
        if not generate_only:
            self.send_whatsapp(image_path, custom_recipients=recipients, template_content=template_content, dry_run=dry_run)
            
        if generate_only:
            logger.info(f"   [INFO] Imagem de Notas gerada com sucesso em {image_path}.")
            
        logger.info("=== FIM AUTOMAÇÃO NOTAS ===\n")
        
def main():
    parser = argparse.ArgumentParser(description="Run Notas Automation")
    parser.add_argument("--generate-only", action="store_true", help="Apenas gera a imagem sem enviar.")
    parser.add_argument("--dry-run", action="store_true", help="Simula o envio.")
    args = parser.parse_args()
    
    automation = NotasAutomation()
    automation.run(generate_only=args.generate_only, dry_run=args.dry_run)
    
if __name__ == "__main__":
    main()

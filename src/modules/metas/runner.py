"""
Automação Metas (Power BI)
Extrai dados de metas do Power BI e envia imagens para WhatsApp/Email.
"""

import json
import os
import random
from datetime import datetime, timedelta

from jinja2 import Template

from src.config import EMAIL_CONFIG, IMAGES_DIR, METAS_CAPTION, POWERBI_CONFIG
from src.core.clients.email_client import EmailClient
from src.core.clients.evolution_client import EvolutionClient
from src.core.clients.powerbi_client import PowerBIClient
from src.core.services.image_generator import ImageGenerator
from src.core.services.supabase_service import SupabaseService
from src.core.utils.date_helpers import get_periodo_semanal
from src.core.utils.greeting import get_saudacao
from src.core.utils.logger import get_logger
from src.core.utils.metas_period import MetasPeriod
from pathlib import Path
from uuid import uuid4

logger = get_logger("run_metas")


class MetasAutomation:
    """
    Controlador principal da automação de Metas.
    Responsável por buscar dados, gerar imagens e enviar mensagens.
    """

    def __init__(self, period=None, *, output_dir=None):
        self.period = period or MetasPeriod.daily()
        self.run_id = uuid4().hex
        self.output_dir = Path(output_dir or IMAGES_DIR) / self.run_id
        self.snapshot = None
        metas_dataset_id = POWERBI_CONFIG.get("metas_dataset_id")
        metas_workspace_id = POWERBI_CONFIG.get("metas_workspace_id")

        # Validação para garantir que as variáveis estão configuradas antes de iniciar
        if not metas_dataset_id or not metas_workspace_id:
            raise ValueError(
                "❌ Variáveis POWERBI_METAS_DATASET_ID e POWERBI_WORKSPACE_ID não configuradas. "
                "Configure-as no Coolify antes de executar a automação Metas."
            )

        self.powerbi = PowerBIClient(workspace_id=metas_workspace_id, dataset_id=metas_dataset_id)
        self.image_gen = ImageGenerator()
        self.whatsapp = EvolutionClient()
        self.supabase = SupabaseService()
        self.email_client = EmailClient(EMAIL_CONFIG)

        self.output_dir.mkdir(parents=True, exist_ok=True)

    def get_periodo(self):
        """Retorna o período atual formatado (ex: Janeiro/2024)."""
        meses = [
            "Janeiro",
            "Fevereiro",
            "Março",
            "Abril",
            "Maio",
            "Junho",
            "Julho",
            "Agosto",
            "Setembro",
            "Outubro",
            "Novembro",
            "Dezembro",
        ]
        return self.period.label

    def get_data_referencia(self):
        """Retorna a data de referência (ontem) formatada."""
        reference = self.period.end if self.period.mode == "daily" else self.period.captured_at.date()
        return reference.strftime("%d/%m/%Y")

    def _get_periodo_semanal(self):
        """Retorna o período da semana anterior (seg-dom) formatado (ex: 15/01 a 21/01)."""
        return get_periodo_semanal()

    def fetch_data(self):
        """Busca todos os dados necessários do Power BI."""
        logger.info("Buscando dados do Power BI...")
        from src.core.services.powerbi_data import PowerBIDataFetcher

        fetcher = PowerBIDataFetcher(self.period)
        result = fetcher.fetch_all_data()
        self.snapshot = {**fetcher.snapshot, "run_id": self.run_id}
        (self.output_dir / "snapshot.json").write_text(json.dumps(self.snapshot, ensure_ascii=False, indent=2), encoding="utf-8")
        return result

    def generate_images(self, total_gs, departamentos, receitas, periodo):
        """
        Gera todas as imagens de relatòrio (Geral, Resumo e por Departamento).
        Retorna um dicionário mapeando 'cliente/departamento' -> 'caminho_da_imagem'.
        """
        logger.info("Gerando imagens...")
        images = {}

        # 1. Geral
        geral_path = str(self.output_dir / "metas_geral.png")
        self.image_gen.generate_metas_image(periodo, departamentos, total_gs, receitas, geral_path)
        images["diretoria"] = geral_path

        # 2. Resumo
        resumo_path = str(self.output_dir / "metas_resumo.png")
        self.image_gen.generate_resumo_image(periodo, total_gs, receitas, resumo_path)
        images["resumo"] = resumo_path

        return images

    def send_whatsapp(self, images, custom_recipients=None, template_content=None, dry_run=False):
        """
        Envia as imagens geradas via WhatsApp.
        :param images: Dict {dept: image_path}
        :param custom_recipients: Lista plana de destinatários do Supabase
        :param template_content: String do template (opcional)
        """

        logger.info("Enviando para WhatsApp...")
        date_ref = self.get_data_referencia()

        # Pre-fetch templates form DB
        fallback_template_str = None

        try:
            # 2. Daily Ranking Default (Fallback if no custom template provided)
            # Only needed if template_content is None (scheduler didn't find one)
            if not template_content:
                default_tmpl = self.supabase.get_template_by_name("Ranking Diário (Padrão)")
                if default_tmpl:
                    fallback_template_str = default_tmpl["content"]

        except Exception as e:
            logger.error(f"Erro ao carregar templates do DB: {e}")

        if not custom_recipients:
            raise ValueError("Nenhum destinatário fornecido para o envio de Metas.")
        unique_phones = {str(r.get("telefone") or r.get("phone")) for r in custom_recipients if r.get("active") is not False}
        resume_date = self.supabase.get_setting("metas_delivery_start_date")
        if len(unique_phones) > 1 and resume_date and self.period.captured_at.date().isoformat() < resume_date:
            raise RuntimeError(f"Programação de Metas retoma em {resume_date}; envio coletivo hoje está bloqueado.")
        if len(unique_phones) > 1 and self.supabase.get_setting("metas_broadcast_hold", True):
            raise RuntimeError("Envio de Metas para todos está aguardando a conferência do teste.")

        # Group flat list by report type (diretoria/admins receive 'geral', others 'resumo')
        recipients_map = {}
        for r in custom_recipients:
            if r.get("active") is False:
                continue
            # Roteamento baseado no departamento do contato (automation_contacts.department)
            # Contatos com department='geral' ou 'diretoria' recebem o relatório completo
            c_dept = str(r.get("department") or "").lower().strip()
            is_diretoria = c_dept in ["diretoria", "geral"]

            if is_diretoria:
                dept_key = "diretoria"
            else:
                dept_key = "resumo"

            if dept_key not in recipients_map:
                recipients_map[dept_key] = []

            recipients_map[dept_key].append(r)

        source_data = recipients_map
        logger.info(f"Processando envio para {len(custom_recipients)} destinatários dinâmicos.")

        # Instantiate Notification Service
        from src.core.services.notification_service import NotificationService

        notification_service = NotificationService(self.supabase)

        # Monta o lote completo de envios antes de disparar para permitir send_batch
        batch: list[tuple] = []
        first_time_contacts: set[str] = set()
        added_phones: set[str] = set()

        warning_msg = (
            "\n\n⚠ Aviso Importante: Por favor salve este contato. "
            "Para garantir o recebimento contínuo dos relatórios, pedimos que responda sempre "
            'todas as mensagens confirmando o recebimento (ex: "ok", "recebido").'
        )

        for grupo_key, image_path in images.items():
            destinatarios = source_data.get(grupo_key, [])
            if not destinatarios:
                continue

            for pessoa in destinatarios:
                nome = pessoa.get("nome") or pessoa.get("name") or "Colaborador"
                telefone = pessoa.get("telefone") or pessoa.get("phone")
                contact_id = pessoa.get("id")

                if not telefone:
                    raise ValueError("Destinatário de Metas sem telefone configurado.")
                if str(telefone) in added_phones:
                    continue
                added_phones.add(str(telefone))

                primeiro_nome = nome.split()[0].title()
                saudacao = get_saudacao()
                saudacao_lower = saudacao.lower()

                current_template = template_content or fallback_template_str
                is_first_time = bool(contact_id) and not self.supabase.check_welcome_sent(contact_id)
                if self.period.mode == "current_snapshot":
                    current_template = (
                        "{saudacao}, {nome}!\n\n📊 Acompanhamento Metas Caixa Grupo Studio\n\n"
                        f"📸 Fotografia atualmente carregada no BI — {self.period.label}.\n"
                        f"Capturada em {self.period.captured_at:%d/%m/%Y às %H:%M} (Brasília).\n\n"
                        "🎯 Acompanhe o progresso:\nhttps://bi.grupostudio.tec.br/"
                    )

                if current_template:
                    try:
                        context = {
                            "nome": primeiro_nome,
                            "nome_completo": nome,
                            "saudacao": saudacao,
                            "saudacao_lower": saudacao_lower,
                            "data": date_ref,
                            "data_semanal": self._get_periodo_semanal(),
                            "grupo": grupo_key.title(),
                        }
                        if "{{" in current_template:
                            caption = Template(current_template).render(**context)
                        else:
                            caption = current_template.format(**context)
                    except Exception as e:
                        logger.error(f"Erro ao formatar template para {nome}: {e}")
                        caption = f"{saudacao}, {primeiro_nome}!\n\nSegue o relatório de {date_ref}."
                else:
                    variations = [
                        f"{saudacao}, {primeiro_nome}!",
                        f"Olá, {primeiro_nome}! {saudacao}.",
                        f"{saudacao}, {primeiro_nome}, tudo bem?",
                        f"{primeiro_nome}, {saudacao_lower}!",
                        f"Oi, {primeiro_nome}. {saudacao}!",
                    ]
                    caption = f"{random.choice(variations)}\n\n" + METAS_CAPTION.format(data=date_ref)

                if is_first_time:
                    logger.info(f"   [INFO] Novo usuário: {nome}. Adicionando aviso de primeiro envio.")
                    caption += warning_msg
                    if contact_id:
                        first_time_contacts.add(contact_id)

                batch.append((pessoa, image_path, caption))

        # Envia o lote com workers paralelos (delays sobrepostos, envios sequenciais)
        if not dry_run:
            results = notification_service.send_batch(batch, context_tag="metas")
            # Marca novos usuários como notificados (apenas após o batch concluir)
            for contact_id in first_time_contacts.intersection(results["successful_contact_ids"]):
                self.supabase.mark_welcome_sent(contact_id)
            logger.info(f"[Metas] Envios: {results['success']} ok, {results['failed']} falhas.")
            snapshot = self.snapshot or {}
            self.supabase.log_event("metas_batch", {
                "run_id": self.run_id,
                "dataset_id": snapshot.get("dataset_id", POWERBI_CONFIG["metas_dataset_id"]),
                "period": self.period.metadata(),
                "source_load": snapshot.get("source_load"),
                "source_freshness": snapshot.get("source_freshness"),
                "query_sha256": snapshot.get("query_sha256"),
                "success": results["success"],
                "failed": results["failed"],
            })
            if results["failed"] or not results["success"]:
                raise RuntimeError("O lote de Metas não foi integralmente confirmado pela Evolution API.")
            return results
        else:
            logger.info(f"[DRY-RUN] Simulação de envio para {len(batch)} destinatários concluída.")
            for p, img, cap in batch:
                nome_p = p.get("nome") or p.get("name") or "Sem nome"
                logger.info(f"   -> Enviar para: {nome_p} | Imagem: {os.path.basename(img)}")
            return {"success": 0, "failed": 0, "dry_run": True}

    def send_email(self, images):
        # Email logic remains unchanged for now, using hardcoded templates or separate implementation
        pass

    def run(self, generate_only=False, recipients=None, template_content=None, dry_run=False):
        """
        Executa o fluxo completo da automação.
        :param recipients: Lista opcional de destinatários do DB.
        :param template_content: Conteúdo do template de mensagem.
        """
        logger.info("\n=== AUTOMAÇÃO METAS ===")
        total_gs, deps, receitas = self.fetch_data()
        if not total_gs or len(deps or []) != 8 or not receitas:
            raise RuntimeError("Coleta de Metas incompleta; geração e envio interrompidos.")
        periodo = self.period.header
        images = self.generate_images(total_gs, deps, receitas, periodo)
        result = {"run_id": self.run_id, "images": images, "snapshot_path": str(self.output_dir / "snapshot.json")}
        if not generate_only or dry_run:
            result.update(self.send_whatsapp(images, custom_recipients=recipients, template_content=template_content, dry_run=dry_run))
            # self.send_email(images) # Commenting out email for now to focus on WA

        if generate_only:
            logger.info("   [INFO] Imagens geradas. Verifique a pasta images/")
        logger.info("=== FIM AUTOMAÇÃO METAS ===\n")
        return result


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Run Metas Automation")
    parser.add_argument(
        "--generate-only",
        action="store_true",
        help="Only generate images, do not send.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate WhatsApp sending (logs only).",
    )
    parser.add_argument("--payload", type=str, help="JSON payload with recipients and template.")
    parser.add_argument("--current-snapshot", action="store_true", help="Fotografia do mês atualmente no BI; não usa legenda D-1.")
    parser.add_argument("--reference-date", type=str, help="Referência D-1 explícita, YYYY-MM-DD, para validação.")
    parser.add_argument("--output-dir", type=str, help="Diretório para snapshot e imagens da execução.")

    args = parser.parse_args()

    if args.current_snapshot and args.reference_date:
        parser.error("Use fotografia atual ou referência D-1, não ambas.")
    from datetime import date
    period = MetasPeriod.current_snapshot() if args.current_snapshot else MetasPeriod.daily(date.fromisoformat(args.reference_date) if args.reference_date else None)
    automation = MetasAutomation(period, output_dir=args.output_dir)

    recipients = None
    template_content = None

    if args.payload:
        try:
            data = json.loads(args.payload)
            recipients = data.get("recipients")
            template_content = data.get("template_content")
            logger.info(f"Recebido payload via CLI com {len(recipients) if recipients else 0} destinatários.")
        except Exception as e:
            logger.error(f"Erro ao fazer parse do payload JSON: {e}")
            return

    automation.run(
        generate_only=args.generate_only,
        recipients=recipients,
        template_content=template_content,
        dry_run=args.dry_run,
    )


if __name__ == "__main__":
    main()

import os
from datetime import datetime
from PIL import Image, ImageDraw

from .base_renderer import BaseRenderer

class NotasRenderer(BaseRenderer):
    """
    Renderizador para o relatório de Notas Emitidas.
    """

    def generate_notas_image(self, data: list[dict], output_path="notas.png"):
        """
        Gera uma imagem de Tabela de Notas Emitidas por empresa (Qtd e Valor).
        :param data: Lista de dicionários no formato [{"name": "Empresa A", "value": 150, "valor": 5000.50}, ...]
        """
        # Calcular altura necessária
        num_items = len(data) if data else 0
        card_height = 80 + (num_items * 45) + 60 # Header interno + itens + Footer(Total)
        height = 100 + card_height + 50 + 50 # Header + Card + Espaço + Footer

        # Criar imagem com fundo escuro (padrão)
        img = Image.new("RGB", (self.width, height), self.bg_color)
        draw = ImageDraw.Draw(img)

        # Fontes
        font_card_title = self._get_font(14, bold=True)
        font_col_header = self._get_font(12, bold=True)
        font_item = self._get_font(15)
        font_item_bold = self._get_font(15, bold=True)
        font_value = self._get_font(15, bold=True)
        font_total = self._get_font(18, bold=True)

        # Header
        now_str = datetime.now().strftime("Até %d/%m/%Y")
        header_h = self._draw_header(draw, "NOTAS FISCAIS EMITIDAS", now_str)

        y = header_h + 30

        # Card principal
        card_x = 20
        card_width = self.width - 40
        card_padding = 20

        draw.rounded_rectangle(
            [(card_x, y), (card_x + card_width, y + card_height)],
            radius=12,
            fill=self.card_color,
        )

        draw.text(
            (card_x + card_padding, y + 18),
            "VOLUME E VALOR POR EMPRESA",
            font=font_card_title,
            fill=self.accent_color,
        )

        draw.line(
            [
                (card_x + card_padding, y + 50),
                (card_x + card_width - card_padding, y + 50),
            ],
            fill=self.accent_color,
            width=1,
        )

        # Colunas X
        col_cnpj_x = card_x + card_padding
        col_nome_x = card_x + 190
        col_qtd_x = card_x + int(card_width * 0.70) # Qtd (Right aligned relative to this)
        col_val_x = card_x + card_width - card_padding # Valor (Right aligned)

        # Header das Colunas
        header_y = y + 65
        draw.text((col_cnpj_x, header_y), "CNPJ", font=font_col_header, fill=self.muted_text)
        draw.text((col_nome_x, header_y), "Empresa", font=font_col_header, fill=self.muted_text)
        
        qtd_bbox = draw.textbbox((0, 0), "Qtd", font=font_col_header)
        draw.text((col_qtd_x - (qtd_bbox[2]-qtd_bbox[0]), header_y), "Qtd", font=font_col_header, fill=self.muted_text)
        
        valor_bbox = draw.textbbox((0, 0), "Valor (R$)", font=font_col_header)
        draw.text((col_val_x - (valor_bbox[2]-valor_bbox[0]), header_y), "Valor (R$)", font=font_col_header, fill=self.muted_text)

        draw.line(
            [(col_cnpj_x, header_y + 25), (col_val_x, header_y + 25)],
            fill=(60, 60, 60),
            width=1,
        )

        item_y = header_y + 40

        total_notas = 0
        total_valor = 0.0

        for i, item in enumerate(data):
            cnpj = item.get("cnpj", "")
            name = item.get("name", "N/A")
            value = item.get("value", 0)
            valor = item.get("valor", 0.0)
            
            total_notas += value
            total_valor += valor

            # Zebrado
            if i % 2 == 0:
                draw.rectangle(
                    [(card_x + 5, item_y - 8), (card_x + card_width - 5, item_y + 28)],
                    fill=(45, 45, 45) # Leve highlight no fundo
                )

            name_color = self.text_color
            if i == 0: name_color = self.gold_color
            elif i == 1: name_color = self.silver_color
            elif i == 2: name_color = self.bronze_color
            
            # CNPJ
            draw.text(
                (col_cnpj_x, item_y),
                cnpj,
                font=font_item,
                fill=name_color,
            )

            # Truncar o nome
            display_name = name[:20] + "..." if len(name) > 22 else name
            draw.text(
                (col_nome_x, item_y),
                display_name,
                font=font_item,
                fill=name_color,
            )

            # Qtd
            value_text = str(value)
            bbox_qtd = draw.textbbox((0, 0), value_text, font=font_value)
            draw.text(
                (col_qtd_x - (bbox_qtd[2] - bbox_qtd[0]), item_y),
                value_text,
                font=font_value,
                fill=self.text_color,
            )

            # Valor
            valor_text = f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            bbox_val = draw.textbbox((0, 0), valor_text, font=font_value)
            draw.text(
                (col_val_x - (bbox_val[2] - bbox_val[0]), item_y),
                valor_text,
                font=font_value,
                fill=self.accent_color,
            )

            item_y += 45

        # Adicionar o total no final
        draw.line(
            [
                (card_x + card_padding, item_y - 5),
                (card_x + card_width - card_padding, item_y - 5),
            ],
            fill=self.accent_color,
            width=2,
        )
        
        draw.text(
            (col_cnpj_x, item_y + 10),
            "TOTAL GERAL",
            font=font_total,
            fill=self.text_color,
        )
        
        # Total Qtd
        total_qtd_str = str(total_notas)
        bbox_tq = draw.textbbox((0, 0), total_qtd_str, font=font_total)
        draw.text(
            (col_qtd_x - (bbox_tq[2] - bbox_tq[0]), item_y + 10),
            total_qtd_str,
            font=font_total,
            fill=self.text_color,
        )
        
        # Total Valor
        total_val_str = f"{total_valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        bbox_tv = draw.textbbox((0, 0), total_val_str, font=font_total)
        draw.text(
            (col_val_x - (bbox_tv[2] - bbox_tv[0]), item_y + 10),
            total_val_str,
            font=font_total,
            fill=self.accent_color,
        )

        self._draw_footer(draw, height)
        img.save(output_path, "PNG")
        return output_path

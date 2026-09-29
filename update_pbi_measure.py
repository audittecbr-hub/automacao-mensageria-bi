"""
update_pbi_measure.py
=====================
Atualiza uma medida DAX dentro de um arquivo .tmdl do Power BI
editando diretamente no disco. Isso contorna o limite de payload
do MCP measure_operations, funcionando com medidas de qualquer tamanho.

Uso:
    python update_pbi_measure.py <tmdl_file> <measure_name> <dax_file>

Exemplo:
    python update_pbi_measure.py "C:\...\medidas_html.tmdl" "Painel_Repasses" "dax_code.txt"
"""
import sys
import re
import shutil
from pathlib import Path
from datetime import datetime


def read_file(path: str) -> str:
    """Lê o arquivo com encoding UTF-8."""
    return Path(path).read_text(encoding="utf-8")


def write_file(path: str, content: str) -> None:
    """Escreve o arquivo com encoding UTF-8 e line endings CRLF."""
    # Normaliza para CRLF (padrão Windows / TMDL)
    content = content.replace("\r\n", "\n").replace("\r", "\n").replace("\n", "\r\n")
    # Usa modo binário para evitar que Python adicione \r extra no Windows
    Path(path).write_bytes(content.encode("utf-8"))


def find_measure_range(lines: list[str], measure_name: str) -> tuple[int, int, str]:
    """
    Encontra as linhas de início e fim de uma medida no TMDL.
    Suporta dois formatos:
      1. Multi-line: \tmeasure X = ```\n...\n\t\t\t```
      2. Inline:     \tmeasure X = "expression"
    
    Retorna (start_index, end_index, format_type) onde format_type é 'multiline' ou 'inline'.
    """
    start_idx = None
    format_type = None

    # Padrão multi-line: \tmeasure NomeDaMedida = ```
    pattern_multi = re.compile(
        r"^\tmeasure\s+" + re.escape(measure_name) + r"\s*=\s*```\s*$"
    )
    # Padrão inline: \tmeasure NomeDaMedida = <qualquer coisa exceto ```)
    pattern_inline = re.compile(
        r"^\tmeasure\s+" + re.escape(measure_name) + r"\s*=\s*(?!```).+"
    )

    for i, line in enumerate(lines):
        stripped = line.rstrip("\r\n")
        if pattern_multi.match(stripped):
            start_idx = i
            format_type = "multiline"
            break
        if pattern_inline.match(stripped):
            start_idx = i
            format_type = "inline"
            break

    if start_idx is None:
        raise ValueError(
            f"Medida '{measure_name}' não encontrada no arquivo TMDL."
        )

    if format_type == "multiline":
        # Procura o fechamento ``` (na indentação \t\t\t)
        end_idx = None
        for i in range(start_idx + 1, len(lines)):
            stripped = lines[i].rstrip("\r\n")
            if stripped == "\t\t\t```":
                end_idx = i
                break
        if end_idx is None:
            raise ValueError(
                f"Fechamento ``` da medida '{measure_name}' não encontrado."
            )
    else:
        # Inline: start e end são a mesma linha
        end_idx = start_idx

    return start_idx, end_idx, format_type


def format_dax_for_tmdl(dax_code: str) -> list[str]:
    """
    Formata o código DAX para inserção no TMDL.
    Cada linha recebe indentação de 3 tabs (\t\t\t) conforme o padrão TMDL.
    """
    # Remove BOM se presente
    if dax_code.startswith("\ufeff"):
        dax_code = dax_code[1:]

    # Remove backticks residuais (de artefatos markdown)
    dax_code = dax_code.strip()
    if dax_code.startswith("```"):
        # Remove primeira linha de ```dax ou ```
        dax_code = re.sub(r"^```\w*\s*\n?", "", dax_code)
    if dax_code.endswith("```"):
        dax_code = re.sub(r"\n?```\s*$", "", dax_code)

    dax_code = dax_code.strip()

    # Divide em linhas e adiciona indentação TMDL
    dax_lines = dax_code.split("\n")
    formatted = []
    for line in dax_lines:
        clean = line.rstrip("\r")
        # Linhas vazias mantém só a indentação base
        if clean.strip() == "":
            formatted.append("\t\t\t")
        else:
            formatted.append("\t\t\t" + clean)

    return formatted


def update_measure(
    tmdl_path: str, measure_name: str, dax_path: str, backup: bool = True
) -> None:
    """
    Atualiza a expressão de uma medida no arquivo TMDL.
    
    Args:
        tmdl_path: Caminho para o arquivo .tmdl
        measure_name: Nome da medida (ex: "Painel_Repasses")
        dax_path: Caminho para o arquivo com o novo código DAX
        backup: Se True, cria um backup .bak antes de alterar
    """
    tmdl_content = read_file(tmdl_path)
    dax_code = read_file(dax_path)

    # Normaliza line endings para \n para processamento
    tmdl_content = tmdl_content.replace("\r\n", "\n")
    lines = tmdl_content.split("\n")

    # Encontra o range da medida
    start_idx, end_idx, fmt = find_measure_range(lines, measure_name)

    print(f"  Medida '{measure_name}' encontrada: linhas {start_idx + 1}-{end_idx + 1} ({fmt})")
    if fmt == "multiline":
        print(f"  Tamanho antigo: {end_idx - start_idx - 1} linhas")
    else:
        print(f"  Formato inline detectado")

    # Formata o novo DAX
    new_dax_lines = format_dax_for_tmdl(dax_code)
    print(f"  Tamanho novo: {len(new_dax_lines)} linhas")

    # Backup
    if backup:
        backup_name = f"{tmdl_path}.{datetime.now().strftime('%Y%m%d_%H%M%S')}.bak"
        shutil.copy2(tmdl_path, backup_name)
        print(f"  Backup criado: {backup_name}")

    # Reconstroi o arquivo com formato multi-line (``` delimitado)
    measure_header = f"\tmeasure {measure_name} = ```"
    measure_footer = "\t\t\t```"

    if fmt == "multiline":
        # Substitui o conteúdo entre os delimitadores ``` existentes
        new_lines = (
            lines[: start_idx + 1]      # Inclui "\tmeasure X = ```"
            + new_dax_lines              # Novo DAX com indentação
            + lines[end_idx:]            # Inclui "\t\t\t```" e o resto
        )
    else:
        # Formato inline: substitui a linha inteira por bloco multi-line
        new_lines = (
            lines[: start_idx]           # Tudo antes da linha inline
            + [measure_header]           # Nova abertura ```
            + new_dax_lines              # Novo DAX com indentação
            + [measure_footer]           # Fechamento ```
            + lines[end_idx + 1:]        # Tudo depois da linha inline
        )

    new_content = "\n".join(new_lines)
    write_file(tmdl_path, new_content)

    print(f"  Arquivo TMDL atualizado com sucesso!")
    print(f"  Total de linhas: {len(lines)} -> {len(new_lines)}")


def main():
    if len(sys.argv) < 4:
        print("Uso: python update_pbi_measure.py <tmdl_file> <measure_name> <dax_file>")
        print()
        print("Exemplo:")
        print('  python update_pbi_measure.py "medidas_html.tmdl" "Painel_Repasses" "dax.txt"')
        sys.exit(1)

    tmdl_path = sys.argv[1]
    measure_name = sys.argv[2]
    dax_path = sys.argv[3]

    if not Path(tmdl_path).exists():
        print(f"ERRO: Arquivo TMDL não encontrado: {tmdl_path}")
        sys.exit(1)

    if not Path(dax_path).exists():
        print(f"ERRO: Arquivo DAX não encontrado: {dax_path}")
        sys.exit(1)

    print(f"Atualizando medida no TMDL...")
    print(f"  TMDL: {tmdl_path}")
    print(f"  Medida: {measure_name}")
    print(f"  DAX: {dax_path}")

    update_measure(tmdl_path, measure_name, dax_path)


if __name__ == "__main__":
    main()

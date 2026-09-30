# 🚀 Studio Automation Core

Hub de Automação Corporativa para envio de relatórios de **Metas (Power BI)** e **Unidades (Nexus)** via WhatsApp.

## Metas V2: dados e execução

Metas utiliza o dataset Ranking_Metas_V2 (72edf515-6d51-4fb9-ad43-be8b77c85604).
O ID legado Ranking_Metas é migrado explicitamente, com aviso no log.
O envio diário consulta do primeiro dia do mês de D-1 até D-1, em America/Sao_Paulo.
Título, legenda e consultas compartilham a mesma referência; a virada do mês fecha o mês anterior.

Uma única consulta retorna os 87 campos dos cartões do BI, sem cache. GS líquido e TOTAL geral
são métricas separadas. O diário exige uma atualização concluída e válida para sua referência.
Falhas de consulta, imagem ou envio propagam erro; a fila não registra completed nesses casos.

Para gerar uma fotografia do mês atualmente carregado no BI, sem enviar:

```bash
python -m src.modules.metas.runner --current-snapshot --generate-only
```

Esse modo informa “fotografia do BI” e a captura, sem anunciar D-1 ou disparar refresh.
Cada execução salva snapshot.json, metas_geral.png e metas_resumo.png em um diretório próprio
sob images/. Esses artefatos não devem ser versionados.

O controle system_settings.metas_broadcast_hold deve ser false para permitir lotes coletivos.
Enquanto true ou indisponível, o coletivo permanece bloqueado para conferência do teste.
O catálogo do portal e os mapas de refresh devem apontar para o mesmo dataset V2.

Validação local, sem rede ou mensagens reais:

```bash
python -m pytest tests/test_metas_contract.py -q
```

O scheduler continua com o comando python -m src.apps.scheduler.scheduler.

> Anteriormente conhecido como `ranking-metas-automation`.

---

## 📦 Arquitetura

O projeto foi refatorado para uma arquitetura modular e escalável:

```
studio-automation-core/
├── core/                 # 🔌 Infraestrutura Compartilhada
│   ├── clients/          # Conectores de API (Evolution, PowerBI, Nexus)
│   └── services/         # Lógica de Negócio (Notificação, Supabase, Imagens)
├── modules/              # 🧩 Domínios de Automação
│   ├── metas/            # Automação de Metas (Power BI)
│   │   └── runner.py
│   └── unidades/         # Automação de Unidades (Nexus)
│       └── runner.py
├── scheduler.py          # 🕒 Orquestrador Central
├── config.py             # ⚙️ Configurações
└── images/               # 📂 Saída das imagens
```

---

## ⚙️ Comandos

### Modo Servidor (Produção)

```bash
python scheduler.py
```

### Disparos Manuais

**Metas (Power BI):**

```bash
python modules/metas/runner.py                # Executar e Enviar
python modules/metas/runner.py --generate-only # Apenas Gerar Imagem
```

**Unidades (Nexus):**

```bash
python modules/unidades/runner.py --daily-only   # Diário
python modules/unidades/runner.py --weekly-only  # Semanal
python modules/unidades/runner.py --generate-only # Apenas Gerar Imagem
```

**Teste Geral:**

```bash
python scheduler.py --test-all
```

---

## 🐳 Docker

```bash
docker-compose up -d --build
```

---

## 📋 Configuração

Edite `.env` com as credenciais do Supabase, Evolution API e Power BI.

import os
import re

sb_url = 'https://tnbxmrathdctzkadekqa.supabase.co/rest/v1/dashboards'
sb_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRuYnhtcmF0aGRjdHprYWRla3FhIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3Njk5NDIyOSwiZXhwIjoyMDkyNTcwMjI5fQ.yOcU3ruc19Mg4bMnkbENxfWLRg6YHda-qnx-kCdjGAA'
doc_id = '00000000-0000-0000-0000-000000000001'

tmdl_paths = [
    r'c:\Users\cristhofer.maciel.GRUPOSTUDIO\OneDrive\repasse.SemanticModel\definition\tables\medidas_html.tmdl',
    r'c:\Users\cristhofer.maciel.GRUPOSTUDIO\Downloads\repasse (3).SemanticModel\definition\tables\medidas_html.tmdl',
    r'c:\Users\cristhofer.maciel.GRUPOSTUDIO\Downloads\repasse.SemanticModel\definition\tables\medidas_html.tmdl'
]

old_api_decl = "var API_URL = 'https://api-aprovacoes-94n5.onrender.com/api/aprovacoes';"

new_code_part1 = f"""var SB_URL = '{sb_url}';
\t\t\tvar SB_KEY = '{sb_key}';
\t\t\tvar DOC_ID = '{doc_id}';

\t\t\tfunction applySavedMap(map) {{
\t\t\t    if (!map) return;
\t\t\t    for (var i = 0; i < rawData.length; i++) {{
\t\t\t        var saved = map[String(rawData[i].id)];
\t\t\t        if (saved !== undefined) {{
\t\t\t            if (typeof saved === 'string') {{
\t\t\t                rawData[i].status = saved;
\t\t\t            }} else if (typeof saved === 'object') {{
\t\t\t                rawData[i].status = saved.status || rawData[i].status || 'Pendente';
\t\t\t                rawData[i].motivo = saved.motivo || '';
\t\t\t                if (saved.nfCliente !== undefined) rawData[i].nfCliente = saved.nfCliente;
\t\t\t                if (saved.obsNfCliente !== undefined) rawData[i].obsNfCliente = saved.obsNfCliente;
\t\t\t                if (saved.dataAprovacao !== undefined) rawData[i].dataAprovacao = saved.dataAprovacao;
\t\t\t                if (saved.dataNfCliente !== undefined) rawData[i].dataNfCliente = saved.dataNfCliente;
\t\t\t                if (saved.dataPgtoRepasse !== undefined) rawData[i].dataPgtoRepasse = saved.dataPgtoRepasse;
\t\t\t            }}
\t\t\t        }} else if (!rawData[i].status || rawData[i].status === '') {{
\t\t\t            rawData[i].status = 'Pendente';
\t\t\t        }}
\t\t\t    }}
\t\t\t    renderTable();
\t\t\t}}

\t\t\tfunction loadSaved() {{
\t\t\t    try {{
\t\t\t        var cached = localStorage.getItem('painel_repasses_cache');
\t\t\t        if (cached) {{
\t\t\t            var cachedMap = JSON.parse(cached);
\t\t\t            applySavedMap(cachedMap);
\t\t\t        }}
\t\t\t    }} catch(e) {{}}

\t\t\t    fetch(SB_URL + '?id=eq.' + DOC_ID + '&select=description', {{
\t\t\t        method: 'GET',
\t\t\t        headers: {{
\t\t\t            'apikey': SB_KEY,
\t\t\t            'Authorization': 'Bearer ' + SB_KEY
\t\t\t        }}
\t\t\t    }})
\t\t\t    .then(function(r) {{ return r.json(); }})
\t\t\t    .then(function(res) {{
\t\t\t        if (res && res.length > 0 && res[0].description) {{
\t\t\t            try {{
\t\t\t                var map = JSON.parse(res[0].description);
\t\t\t                try {{ localStorage.setItem('painel_repasses_cache', res[0].description); }} catch(e){{}}
\t\t\t                applySavedMap(map);
\t\t\t            }} catch(err) {{
\t\t\t                console.error('Erro parse JSON Supabase:', err);
\t\t\t            }}
\t\t\t        }}
\t\t\t    }})
\t\t\t    .catch(function(e) {{
\t\t\t        console.log('Erro ao carregar do Supabase:', e);
\t\t\t    }});
\t\t\t}}"""

new_code_part2 = f"""function getPayload() {{
\t\t\t    var payload = {{}};
\t\t\t    for (var i = 0; i < rawData.length; i++) {{
\t\t\t        var r = rawData[i];
\t\t\t        if (r.status !== 'Pendente' || (r.nfCliente && r.nfCliente.trim() !== '') || (r.obsNfCliente && r.obsNfCliente.trim() !== '') || (r.dataPgtoRepasse && r.dataPgtoRepasse.trim() !== '')) {{
\t\t\t            payload[String(r.id)] = {{
\t\t\t                status: r.status,
\t\t\t                motivo: r.motivo || '',
\t\t\t                nfCliente: r.nfCliente || '',
\t\t\t                obsNfCliente: r.obsNfCliente || '',
\t\t\t                dataAprovacao: r.dataAprovacao || '',
\t\t\t                dataNfCliente: r.dataNfCliente || '',
\t\t\t                dataPgtoRepasse: r.dataPgtoRepasse || ''
\t\t\t            }};
\t\t\t        }}
\t\t\t    }}
\t\t\t    return payload;
\t\t\t}}

\t\t\tfunction gravarEstadoSilencioso() {{
\t\t\t    var payload = getPayload();
\t\t\t    var payloadStr = JSON.stringify(payload);
\t\t\t    try {{ localStorage.setItem('painel_repasses_cache', payloadStr); }} catch(e){{}}

\t\t\t    fetch(SB_URL, {{
\t\t\t        method: 'POST',
\t\t\t        headers: {{
\t\t\t            'apikey': SB_KEY,
\t\t\t            'Authorization': 'Bearer ' + SB_KEY,
\t\t\t            'Content-Type': 'application/json',
\t\t\t            'Prefer': 'resolution=merge-duplicates'
\t\t\t        }},
\t\t\t        body: JSON.stringify([{{
\t\t\t            id: DOC_ID,
\t\t\t            title: 'ESTADO_REPASSE_APROVACOES',
\t\t\t            category: 'repasse_aprovacoes',
\t\t\t            description: payloadStr
\t\t\t        }}])
\t\t\t    }}).catch(function(e) {{
\t\t\t        console.log('Erro ao gravar silencioso no Supabase:', e);
\t\t\t    }});
\t\t\t}}

\t\t\tfunction gravarEstado() {{
\t\t\t    var payload = getPayload();
\t\t\t    var payloadStr = JSON.stringify(payload);
\t\t\t    try {{ localStorage.setItem('painel_repasses_cache', payloadStr); }} catch(e){{}}

\t\t\t    fetch(SB_URL, {{
\t\t\t        method: 'POST',
\t\t\t        headers: {{
\t\t\t            'apikey': SB_KEY,
\t\t\t            'Authorization': 'Bearer ' + SB_KEY,
\t\t\t            'Content-Type': 'application/json',
\t\t\t            'Prefer': 'resolution=merge-duplicates'
\t\t\t        }},
\t\t\t        body: JSON.stringify([{{
\t\t\t            id: DOC_ID,
\t\t\t            title: 'ESTADO_REPASSE_APROVACOES',
\t\t\t            category: 'repasse_aprovacoes',
\t\t\t            description: payloadStr
\t\t\t        }}])
\t\t\t    }})
\t\t\t    .then(function(resp) {{
\t\t\t        if (resp.ok) {{
\t\t\t            hasUnsaved = false;
\t\t\t            var btn = document.getElementById('btn-save');
\t\t\t            if (btn) {{ btn.classList.remove('has-changes'); btn.textContent = 'GRAVAR'; }}
\t\t\t            showToast('Estado gravado com sucesso na nuvem!');
\t\t\t        }} else {{
\t\t\t            throw new Error('Falha HTTP ' + resp.status);
\t\t\t        }}
\t\t\t    }})
\t\t\t    .catch(function(e) {{
\t\t\t        showToast('Gravado no cache local! (Nuvem indisponível)');
\t\t\t    }});
\t\t\t}}"""

for p in tmdl_paths:
    if os.path.exists(p):
        with open(p, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace part 1 (var API_URL + loadSaved)
        # Regex to match from var API_URL up to function fmtBRL
        pattern1 = re.compile(r'var API_URL = [^\n]+;\s*function loadSaved\(\)\s*\{.*?\}\s*(?=\t*function fmtBRL)', re.DOTALL)
        if pattern1.search(content):
            content = pattern1.sub(new_code_part1 + '\n\t\t\t', content)
            print(f'Part 1 replaced in {p}')
        else:
            print(f'Part 1 NOT matched in {p}')
        
        # Replace part 2 (gravarEstadoSilencioso + gravarEstado)
        # Regex to match from function gravarEstadoSilencioso up to function copyToExcel
        pattern2 = re.compile(r'function gravarEstadoSilencioso\(\)\s*\{.*?function gravarEstado\(\)\s*\{.*?\}\s*(?=\t*function copyToExcel)', re.DOTALL)
        if pattern2.search(content):
            content = pattern2.sub(new_code_part2 + '\n\t\t\t', content)
            print(f'Part 2 replaced in {p}')
        else:
            print(f'Part 2 NOT matched in {p}')
        
        with open(p, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Saved updated {p}')

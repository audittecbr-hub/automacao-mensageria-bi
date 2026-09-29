import os
import re
import json
import subprocess

exe_path = r'C:\Users\cristhofer.maciel.GRUPOSTUDIO\.vscode\extensions\analysis-services.powerbi-modeling-mcp-0.4.0-win32-x64\server\powerbi-modeling-mcp.exe'
tmdl_path = r'C:\Users\cristhofer.maciel.GRUPOSTUDIO\OneDrive\repasse.SemanticModel\definition\tables\medidas_html.tmdl'

with open(tmdl_path, 'r', encoding='utf-8') as f:
    full_tmdl = f.read()

# 1. Add var savedGlobalMap = {}; after var statusSendoDefinido = null;
if 'var savedGlobalMap = {};' not in full_tmdl:
    full_tmdl = full_tmdl.replace(
        'var hasUnsaved = false, isUnlocked = false, itemSendoAlteradoNf = null, itemSendoObservado = null, statusSendoDefinido = null;',
        'var hasUnsaved = false, isUnlocked = false, itemSendoAlteradoNf = null, itemSendoObservado = null, statusSendoDefinido = null;\n\t\t\tvar savedGlobalMap = {};\n\t\t\tfunction getCompositeKey(r) { if (!r) return ""; var j = (r.job || "").trim(); var n = (r.nf || "").trim(); var b = (r.bandeira || "").trim(); var c = (r.cnpj || "").trim(); return (j + "___" + n + "___" + b + "___" + c).toLowerCase(); }'
    )

# 2. Update applySavedMap to merge into savedGlobalMap and use composite key
old_apply_map = """function applySavedMap(map) {
\t\t\t    if (!map) return;
\t\t\t    for (var i = 0; i < rawData.length; i++) {
\t\t\t        var saved = map[String(rawData[i].id)];
\t\t\t        if (saved !== undefined) {
\t\t\t            if (typeof saved === 'string') {
\t\t\t                rawData[i].status = saved;
\t\t\t            } else if (typeof saved === 'object') {
\t\t\t                rawData[i].status = saved.status || rawData[i].status || 'Pendente';
\t\t\t                rawData[i].motivo = saved.motivo || '';
\t\t\t                if (saved.nfCliente !== undefined) rawData[i].nfCliente = saved.nfCliente;
\t\t\t                if (saved.obsNfCliente !== undefined) rawData[i].obsNfCliente = saved.obsNfCliente;
\t\t\t                if (saved.dataAprovacao !== undefined) rawData[i].dataAprovacao = saved.dataAprovacao;
\t\t\t                if (saved.dataNfCliente !== undefined) rawData[i].dataNfCliente = saved.dataNfCliente;
\t\t\t                if (saved.dataPgtoRepasse !== undefined) rawData[i].dataPgtoRepasse = saved.dataPgtoRepasse;
\t\t\t            }
\t\t\t        } else if (!rawData[i].status || rawData[i].status === '') {
\t\t\t            rawData[i].status = 'Pendente';
\t\t\t        }
\t\t\t    }
\t\t\t    renderTable();
\t\t\t}"""

new_apply_map = """function applySavedMap(map) {
\t\t\t    if (!map) return;
\t\t\t    for (var k in map) { savedGlobalMap[k] = map[k]; }
\t\t\t    for (var i = 0; i < rawData.length; i++) {
\t\t\t        var r = rawData[i];
\t\t\t        var idKey = String(r.id);
\t\t\t        var compKey = getCompositeKey(r);
\t\t\t        var saved = savedGlobalMap[idKey] || (compKey && compKey !== "______" ? savedGlobalMap[compKey] : null);
\t\t\t        if (saved) {
\t\t\t            if (typeof saved === 'string') {
\t\t\t                r.status = saved;
\t\t\t            } else if (typeof saved === 'object') {
\t\t\t                r.status = saved.status || r.status || 'Pendente';
\t\t\t                r.motivo = saved.motivo || '';
\t\t\t                if (saved.nfCliente !== undefined) r.nfCliente = saved.nfCliente;
\t\t\t                if (saved.obsNfCliente !== undefined) r.obsNfCliente = saved.obsNfCliente;
\t\t\t                if (saved.dataAprovacao !== undefined) r.dataAprovacao = saved.dataAprovacao;
\t\t\t                if (saved.dataNfCliente !== undefined) r.dataNfCliente = saved.dataNfCliente;
\t\t\t                if (saved.dataPgtoRepasse !== undefined) r.dataPgtoRepasse = saved.dataPgtoRepasse;
\t\t\t            }
\t\t\t            savedGlobalMap[idKey] = saved;
\t\t\t            if (compKey && compKey !== "______") savedGlobalMap[compKey] = saved;
\t\t\t        } else if (!r.status || r.status === '') {
\t\t\t            r.status = 'Pendente';
\t\t\t        }
\t\t\t    }
\t\t\t    renderTable();
\t\t\t}
\t\t\tfunction updateItemInGlobalMap(r) {
\t\t\t    if (!r) return;
\t\t\t    var idKey = String(r.id);
\t\t\t    var compKey = getCompositeKey(r);
\t\t\t    var isNonDefault = (r.status !== 'Pendente' || (r.nfCliente && r.nfCliente.trim() !== '') || (r.obsNfCliente && r.obsNfCliente.trim() !== '') || (r.dataPgtoRepasse && r.dataPgtoRepasse.trim() !== ''));
\t\t\t    if (isNonDefault) {
\t\t\t        var entry = { status: r.status, motivo: r.motivo || '', nfCliente: r.nfCliente || '', obsNfCliente: r.obsNfCliente || '', dataAprovacao: r.dataAprovacao || '', dataNfCliente: r.dataNfCliente || '', dataPgtoRepasse: r.dataPgtoRepasse || '', updatedAt: getNowFormatted() };
\t\t\t        savedGlobalMap[idKey] = entry;
\t\t\t        if (compKey && compKey !== "______") savedGlobalMap[compKey] = entry;
\t\t\t    } else {
\t\t\t        delete savedGlobalMap[idKey];
\t\t\t        if (compKey && compKey !== "______") delete savedGlobalMap[compKey];
\t\t\t    }
\t\t\t}
\t\t\tfunction getMergedPayload() {
\t\t\t    for (var i = 0; i < rawData.length; i++) { updateItemInGlobalMap(rawData[i]); }
\t\t\t    return savedGlobalMap;
\t\t\t}"""

full_tmdl = full_tmdl.replace(old_apply_map.replace('\r\n', '\n'), new_apply_map.replace('\r\n', '\n'))

# 3. In all action functions, add updateItemInGlobalMap
# setStatus
full_tmdl = full_tmdl.replace(
    'item.dataAprovacao = "";\n\t\t\t    }\n\t\t\t    renderTable();\n\t\t\t    gravarEstadoSilencioso();',
    'item.dataAprovacao = "";\n\t\t\t    }\n\t\t\t    updateItemInGlobalMap(item);\n\t\t\t    renderTable();\n\t\t\t    gravarEstadoSilencioso();'
)

# confirmarObservacaoStatus
full_tmdl = full_tmdl.replace(
    'itemSendoObservado.dataAprovacao = "";\n\t\t\t        renderTable();\n\t\t\t        gravarEstadoSilencioso();',
    'itemSendoObservado.dataAprovacao = "";\n\t\t\t        updateItemInGlobalMap(itemSendoObservado);\n\t\t\t        renderTable();\n\t\t\t        gravarEstadoSilencioso();'
)

# salvarNfInicial
full_tmdl = full_tmdl.replace(
    'item.obsNfCliente = ""; }\n\t\t\t    renderTable();\n\t\t\t    if (changed) gravarEstadoSilencioso();',
    'item.obsNfCliente = ""; }\n\t\t\t    updateItemInGlobalMap(item);\n\t\t\t    renderTable();\n\t\t\t    if (changed) gravarEstadoSilencioso();'
)

# confirmarAlteracaoNf
full_tmdl = full_tmdl.replace(
    'itemSendoAlteradoNf.obsNfCliente = "";\n\t\t\t        }\n\t\t\t        renderTable();\n\t\t\t        gravarEstadoSilencioso();',
    'itemSendoAlteradoNf.obsNfCliente = "";\n\t\t\t        }\n\t\t\t        updateItemInGlobalMap(itemSendoAlteradoNf);\n\t\t\t        renderTable();\n\t\t\t        gravarEstadoSilencioso();'
)

# salvarDataPgtoRepasseDirect
full_tmdl = full_tmdl.replace(
    'item.dataPgtoRepasse = formatted;\n\t\t\t    renderTable();\n\t\t\t    gravarEstadoSilencioso();',
    'item.dataPgtoRepasse = formatted;\n\t\t\t    updateItemInGlobalMap(item);\n\t\t\t    renderTable();\n\t\t\t    gravarEstadoSilencioso();'
)

# confirmarAlteracaoPgtoRep
full_tmdl = full_tmdl.replace(
    'itemSendoAlteradoPgtoRep.dataPgtoRepasse = "";\n\t\t\t    }\n\t\t\t    renderTable();\n\t\t\t    gravarEstadoSilencioso();',
    'itemSendoAlteradoPgtoRep.dataPgtoRepasse = "";\n\t\t\t    }\n\t\t\t    updateItemInGlobalMap(itemSendoAlteradoPgtoRep);\n\t\t\t    renderTable();\n\t\t\t    gravarEstadoSilencioso();'
)

# removerDataPgtoRep
full_tmdl = full_tmdl.replace(
    'itemSendoAlteradoPgtoRep.dataPgtoRepasse = "";\n\t\t\t    renderTable();\n\t\t\t    gravarEstadoSilencioso();',
    'itemSendoAlteradoPgtoRep.dataPgtoRepasse = "";\n\t\t\t    updateItemInGlobalMap(itemSendoAlteradoPgtoRep);\n\t\t\t    renderTable();\n\t\t\t    gravarEstadoSilencioso();'
)

# 4. Replace getPayload and gravarEstado / gravarEstadoSilencioso
# Remove duplicate getPayload and replace with getMergedPayload
old_get_payload = re.compile(
    r'function getPayload\(\) \{[\s\S]*?function gravarEstadoSilencioso\(\) \{',
    re.MULTILINE
)
new_save_funcs = """function gravarEstadoSilencioso() {
\t\t\t    var payload = getMergedPayload();
\t\t\t    var payloadStr = JSON.stringify(payload);
\t\t\t    try { localStorage.setItem('painel_repasses_cache', payloadStr); } catch(e){}

\t\t\t    fetch(SB_URL, {
\t\t\t        method: 'POST',
\t\t\t        headers: {
\t\t\t            'apikey': SB_KEY,
\t\t\t            'Authorization': 'Bearer ' + SB_KEY,
\t\t\t            'Content-Type': 'application/json',
\t\t\t            'Prefer': 'resolution=merge-duplicates'
\t\t\t        },
\t\t\t        body: JSON.stringify([{
\t\t\t            id: DOC_ID,
\t\t\t            title: 'ESTADO_REPASSE_APROVACOES',
\t\t\t            category: 'repasse_aprovacoes',
\t\t\t            description: payloadStr
\t\t\t        }])
\t\t\t    }).catch(function(e) {
\t\t\t        console.log('Erro ao gravar silencioso no Supabase:', e);
\t\t\t    });
\t\t\t}

\t\t\tfunction gravarEstado() {
\t\t\t    var btn = document.getElementById('btn-save');
\t\t\t    if (btn) { btn.textContent = 'GRAVANDO...'; }
\t\t\t    var payload = getMergedPayload();
\t\t\t    var payloadStr = JSON.stringify(payload);
\t\t\t    try { localStorage.setItem('painel_repasses_cache', payloadStr); } catch(e){}

\t\t\t    fetch(SB_URL, {
\t\t\t        method: 'POST',
\t\t\t        headers: {
\t\t\t            'apikey': SB_KEY,
\t\t\t            'Authorization': 'Bearer ' + SB_KEY,
\t\t\t            'Content-Type': 'application/json',
\t\t\t            'Prefer': 'resolution=merge-duplicates'
\t\t\t        },
\t\t\t        body: JSON.stringify([{
\t\t\t            id: DOC_ID,
\t\t\t            title: 'ESTADO_REPASSE_APROVACOES',
\t\t\t            category: 'repasse_aprovacoes',
\t\t\t            description: payloadStr
\t\t\t        }])
\t\t\t    })
\t\t\t    .then(function(resp) {
\t\t\t        if (resp.ok) {
\t\t\t            hasUnsaved = false;
\t\t\t            if (btn) { btn.classList.remove('has-changes'); btn.textContent = 'GRAVAR'; }
\t\t\t            showToast('Estado gravado com sucesso na nuvem!');
\t\t\t        } else {
\t\t\t            throw new Error('Falha HTTP ' + resp.status);
\t\t\t        }
\t\t\t    })
\t\t\t    .catch(function(e) {
\t\t\t        if (btn) { btn.textContent = 'GRAVAR'; }
\t\t\t        showToast('Gravado no cache local! (Nuvem indisponivel)');
\t\t\t    });
\t\t\t}
\t\t\tfunction copyToExcel() {"""

# Replace old gravarEstado block
old_save_block = re.search(r'function getPayload\(\) \{[\s\S]*?function copyToExcel\(\) \{', full_tmdl)
if old_save_block:
    full_tmdl = full_tmdl[:old_save_block.start()] + new_save_funcs + full_tmdl[old_save_block.end():]

# Write to TMDL files
for p in [r'C:\Users\cristhofer.maciel.GRUPOSTUDIO\OneDrive\repasse.SemanticModel\definition\tables\medidas_html.tmdl', r'C:\Users\cristhofer.maciel.GRUPOSTUDIO\Downloads\repasse.SemanticModel\definition\tables\medidas_html.tmdl']:
    if os.path.exists(p):
        with open(p, 'w', encoding='utf-8') as f:
            f.write(full_tmdl)
        print(f'Successfully patched TMDL: {p}')

# Extract DAX expression
pos_start = full_tmdl.find('measure Painel_Repasses =')
pos_end = full_tmdl.find('\n\tmeasure ', pos_start + 1)
if pos_end == -1: pos_end = len(full_tmdl)
painel_new = full_tmdl[pos_start:pos_end]

m = re.search(r'```([\s\S]*?)```', painel_new)
if m:
    lines = [l.replace('\t\t\t', '') for l in m.group(1).strip().splitlines()]
    raw_expr = '\n'.join(lines)
    with open('painel_repasses_fixed_expr.txt', 'w', encoding='utf-8') as ef:
        ef.write(raw_expr)

# Push live to Port 57503
p = subprocess.Popen([exe_path, '--start'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8')
msg_id = 1
def send(msg):
    global msg_id
    msg['id'] = msg_id
    msg_id += 1
    p.stdin.write(json.dumps(msg) + '\n')
    p.stdin.flush()
    res = p.stdout.readline()
    try:
        return json.loads(res)
    except:
        return res

send({'jsonrpc': '2.0', 'method': 'initialize', 'params': {'protocolVersion': '2024-11-05', 'capabilities': {}, 'clientInfo': {'name': 'sync', 'version': '1.0'}}})
conn_resp = send({'jsonrpc': '2.0', 'method': 'tools/call', 'params': {'name': 'connection_operations', 'arguments': {'request': {'operation': 'Connect', 'connectionString': 'Data Source=localhost:57503;Application Name=MCP-Direct'}}}})
print('Connect to 57503:', conn_resp.get('result', {}).get('content', [{}])[0].get('text', ''))

upd_resp = send({
    'jsonrpc': '2.0',
    'method': 'tools/call',
    'params': {
        'name': 'measure_operations',
        'arguments': {
            'request': {
                'operation': 'Update',
                'Definitions': [
                    {
                        'Name': 'Painel_Repasses',
                        'TableName': 'medidas_html',
                        'Expression': raw_expr
                    }
                ]
            }
        }
    }
})
print('Update measure result:', upd_resp.get('result', {}).get('content', [{}])[0].get('text', ''))

test_dax = send({
    'jsonrpc': '2.0',
    'method': 'tools/call',
    'params': {
        'name': 'dax_query_operations',
        'arguments': {
            'request': {
                'operation': 'Execute',
                'query': 'EVALUATE ROW("Len", LEN([Painel_Repasses]))'
            }
        }
    }
})
for c in test_dax.get('result', {}).get('content', []):
    if 'resource' in c:
        print('DAX test result:', c['resource']['text'])

p.terminate()

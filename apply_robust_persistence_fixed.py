import os
import re
import json
import subprocess

exe_path = r'C:\Users\cristhofer.maciel.GRUPOSTUDIO\.vscode\extensions\analysis-services.powerbi-modeling-mcp-0.4.0-win32-x64\server\powerbi-modeling-mcp.exe'
tmdl_path = r'C:\Users\cristhofer.maciel.GRUPOSTUDIO\OneDrive\repasse.SemanticModel\definition\tables\medidas_html.tmdl'

with open(tmdl_path, 'r', encoding='utf-8') as f:
    full_tmdl = f.read()

pos_start = full_tmdl.find('measure Painel_Repasses =')
pos_end = full_tmdl.find('\n\tmeasure ', pos_start + 1)
if pos_end == -1:
    pos_end = len(full_tmdl)

painel_def = full_tmdl[pos_start:pos_end]

# Extract JavaScript section
js_start = painel_def.find('<script>')
js_end = painel_def.find('</script>', js_start)

# We want to replace the JS section with the new robust persistence JS engine
new_js_code = """<script>
			var rawData = [" & vJsonRows & "];
			
			for (var i=0; i<rawData.length; i++) {
			    if (!rawData[i].status || rawData[i].status.trim() === '') rawData[i].status = 'Pendente';
			}
			var currentFilter = 'all';
			var currentSort = {key:'nome', asc:true};
			var hasUnsaved = false, isUnlocked = false, itemSendoAlteradoNf = null, itemSendoObservado = null, statusSendoDefinido = null;
			var savedGlobalMap = {};
			
			function getCompositeKey(r) {
			    if (!r) return '';
			    var j = (r.job || '').trim();
			    var n = (r.nf || '').trim();
			    var b = (r.bandeira || '').trim();
			    var c = (r.cnpj || '').trim();
			    return (j + '___' + n + '___' + b + '___' + c).toLowerCase();
			}

			function getNowFormatted() {
			    var now = new Date();
			    return String(now.getDate()).padStart(2, '0') + '/' + String(now.getMonth() + 1).padStart(2, '0') + '/' + now.getFullYear() + ' ' + String(now.getHours()).padStart(2, '0') + ':' + String(now.getMinutes()).padStart(2, '0');
			}
			function toggleLock() {
			    if (isUnlocked) {
			        isUnlocked = false;
			        document.getElementById('btn-lock').innerHTML = 'Desbloquear';
			        document.getElementById('btn-lock').classList.remove('unlocked');
			        document.getElementById('btn-save').style.display = 'none';
			        renderTable();
			        return;
			    }
			    document.getElementById('senha-texto').value = '';
			    document.getElementById('modal-senha').classList.add('show');
			    document.getElementById('senha-texto').focus();
			}
			function fecharSenha() { document.getElementById('modal-senha').classList.remove('show'); }
			function confirmarSenha() {
			    var senha = document.getElementById('senha-texto').value;
			    if (senha === 'Gs@2026') {
			        isUnlocked = true;
			        document.getElementById('btn-lock').innerHTML = 'Bloquear';
			        document.getElementById('btn-lock').classList.add('unlocked');
			        document.getElementById('btn-save').style.display = 'inline-block';
			        showToast('Edicao liberada!');
			        fecharSenha();
			        renderTable();
			    } else {
			        showToast('Senha incorreta!');
			        document.getElementById('senha-texto').value = '';
			        document.getElementById('senha-texto').focus();
			    }
			}
			var SB_URL = 'https://tnbxmrathdctzkadekqa.supabase.co/rest/v1/dashboards';
			var SB_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRuYnhtcmF0aGRjdHprYWRla3FhIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3Njk5NDIyOSwiZXhwIjoyMDkyNTcwMjI5fQ.yOcU3ruc19Mg4bMnkbENxfWLRg6YHda-qnx-kCdjGAA';
			var DOC_ID = '00000000-0000-0000-0000-000000000001';

			function applySavedMap(map) {
			    if (!map) return;
			    for (var k in map) {
			        savedGlobalMap[k] = map[k];
			    }
			    for (var i = 0; i < rawData.length; i++) {
			        var r = rawData[i];
			        var idKey = String(r.id);
			        var compKey = getCompositeKey(r);
			        
			        var saved = savedGlobalMap[idKey] || (compKey && compKey !== '______' ? savedGlobalMap[compKey] : null);
			        
			        if (saved) {
			            if (typeof saved === 'string') {
			                r.status = saved;
			            } else if (typeof saved === 'object') {
			                r.status = saved.status || r.status || 'Pendente';
			                r.motivo = saved.motivo || '';
			                if (saved.nfCliente !== undefined) r.nfCliente = saved.nfCliente;
			                if (saved.obsNfCliente !== undefined) r.obsNfCliente = saved.obsNfCliente;
			                if (saved.dataAprovacao !== undefined) r.dataAprovacao = saved.dataAprovacao;
			                if (saved.dataNfCliente !== undefined) r.dataNfCliente = saved.dataNfCliente;
			                if (saved.dataPgtoRepasse !== undefined) r.dataPgtoRepasse = saved.dataPgtoRepasse;
			            }
			            savedGlobalMap[idKey] = saved;
			            if (compKey && compKey !== '______') savedGlobalMap[compKey] = saved;
			        } else if (!r.status || r.status === '') {
			            r.status = 'Pendente';
			        }
			    }
			    renderTable();
			}

			function updateItemInGlobalMap(r) {
			    if (!r) return;
			    var idKey = String(r.id);
			    var compKey = getCompositeKey(r);
			    
			    var isNonDefault = (r.status !== 'Pendente' || (r.nfCliente && r.nfCliente.trim() !== '') || (r.obsNfCliente && r.obsNfCliente.trim() !== '') || (r.dataPgtoRepasse && r.dataPgtoRepasse.trim() !== ''));
			    
			    if (isNonDefault) {
			        var entry = {
			            status: r.status,
			            motivo: r.motivo || '',
			            nfCliente: r.nfCliente || '',
			            obsNfCliente: r.obsNfCliente || '',
			            dataAprovacao: r.dataAprovacao || '',
			            dataNfCliente: r.dataNfCliente || '',
			            dataPgtoRepasse: r.dataPgtoRepasse || '',
			            updatedAt: getNowFormatted()
			        };
			        savedGlobalMap[idKey] = entry;
			        if (compKey && compKey !== '______') savedGlobalMap[compKey] = entry;
			    } else {
			        delete savedGlobalMap[idKey];
			        if (compKey && compKey !== '______') delete savedGlobalMap[compKey];
			    }
			}

			function getMergedPayload() {
			    for (var i = 0; i < rawData.length; i++) {
			        updateItemInGlobalMap(rawData[i]);
			    }
			    return savedGlobalMap;
			}

			function loadSaved() {
			    try {
			        var cached = localStorage.getItem('painel_repasses_cache');
			        if (cached) {
			            var cachedMap = JSON.parse(cached);
			            applySavedMap(cachedMap);
			        }
			    } catch(e) {}

			    fetch(SB_URL + '?id=eq.' + DOC_ID + '&select=description', {
			        method: 'GET',
			        headers: {
			            'apikey': SB_KEY,
			            'Authorization': 'Bearer ' + SB_KEY
			        }
			    })
			    .then(function(r) { return r.json(); })
			    .then(function(res) {
			        if (res && res.length > 0 && res[0].description) {
			            try {
				                var map = JSON.parse(res[0].description);
			                try { localStorage.setItem('painel_repasses_cache', res[0].description); } catch(e){}
			                applySavedMap(map);
			            } catch(err) {
			                console.error('Erro parse JSON Supabase:', err);
			            }
			        }
			    })
			    .catch(function(e) {
			        console.log('Erro ao carregar do Supabase:', e);
			    });
			}

			function fmtBRL(v) { return 'R$ ' + Number(v).toLocaleString('pt-BR', {minimumFractionDigits:2, maximumFractionDigits:2}); }
			function toDateNum(dStr) {
			    if (!dStr) return 0;
			    var clean = dStr.split(' ')[0], p = clean.split('/');
			    if (p.length === 3) return parseInt(p[2] + p[1].padStart(2, '0') + p[0].padStart(2, '0'), 10);
			    var p2 = clean.split('-');
			    if (p2.length === 3) return parseInt(p2[0] + p2[1].padStart(2, '0') + p2[2].padStart(2, '0'), 10);
			    return 0;
			}
			function showToast(msg) {
			    var t = document.getElementById('toast');
			    t.textContent = msg;
			    t.classList.add('show');
			    setTimeout(function(){ t.classList.remove('show'); }, 2600);
			}
			function setFilter(f) {
			    currentFilter = f;
			    document.querySelectorAll('.filter-tab').forEach(function(el){ el.classList.remove('active'); });
			    document.getElementById('tab-' + f).classList.add('active');
			    renderTable();
			}
			function filterTable() { renderTable(); }
			function sortBy(col) {
			    if (currentSort.key === col) currentSort.asc = !currentSort.asc;
			    else { currentSort.key = col; currentSort.asc = true; }
			    renderTable();
			}
			function toggleDatePopover() {
			    var p = document.getElementById('date-popover');
			    p.classList.toggle('show');
			    if (p.classList.contains('show')) {
			        document.getElementById('date-aprov-popover').classList.remove('show');
			        document.getElementById('date-nf-popover').classList.remove('show');
			        document.getElementById('date-pgtorep-popover').classList.remove('show');
			    }
			}
			function toggleDateAprovPopover() {
			    var p = document.getElementById('date-aprov-popover');
			    p.classList.toggle('show');
			    if (p.classList.contains('show')) {
			        document.getElementById('date-popover').classList.remove('show');
			        document.getElementById('date-nf-popover').classList.remove('show');
			        document.getElementById('date-pgtorep-popover').classList.remove('show');
			    }
			}
			function toggleDateNfPopover() {
			    var p = document.getElementById('date-nf-popover');
			    p.classList.toggle('show');
			    if (p.classList.contains('show')) {
			        document.getElementById('date-popover').classList.remove('show');
			        document.getElementById('date-aprov-popover').classList.remove('show');
			        document.getElementById('date-pgtorep-popover').classList.remove('show');
			    }
			}
			function toggleDatePgtoRepPopover() {
			    var p = document.getElementById('date-pgtorep-popover');
			    p.classList.toggle('show');
			    if (p.classList.contains('show')) {
			        document.getElementById('date-popover').classList.remove('show');
			        document.getElementById('date-aprov-popover').classList.remove('show');
			        document.getElementById('date-nf-popover').classList.remove('show');
			    }
			}
			function closeAllPopovers(e) {
			    if (!e.target.closest('#date-popover') && !e.target.closest('#btn-date-trigger')) {
			        document.getElementById('date-popover').classList.remove('show');
			    }
			    if (!e.target.closest('#date-aprov-popover') && !e.target.closest('#btn-date-aprov-trigger')) {
			        document.getElementById('date-aprov-popover').classList.remove('show');
			    }
			    if (!e.target.closest('#date-nf-popover') && !e.target.closest('#btn-date-nf-trigger')) {
			        document.getElementById('date-nf-popover').classList.remove('show');
			    }
			    if (!e.target.closest('#date-pgtorep-popover') && !e.target.closest('#btn-date-pgtorep-trigger')) {
			        document.getElementById('date-pgtorep-popover').classList.remove('show');
			    }
			}
			document.addEventListener('click', closeAllPopovers);
			function applyDateFilter() {
			    updateDateTriggerLabel();
			    document.getElementById('date-popover').classList.remove('show');
			    renderTable();
			}
			function applyDateAprovFilter() {
			    updateDateAprovTriggerLabel();
			    document.getElementById('date-aprov-popover').classList.remove('show');
			    renderTable();
			}
			function applyDateNfFilter() {
			    updateDateNfTriggerLabel();
			    document.getElementById('date-nf-popover').classList.remove('show');
			    renderTable();
			}
			function applyDatePgtoRepFilter() {
			    updateDatePgtoRepTriggerLabel();
			    document.getElementById('date-pgtorep-popover').classList.remove('show');
			    renderTable();
			}
			function fmtDateShort(dStr) {
			    if (!dStr) return '';
			    var p = dStr.split('-');
			    if (p.length === 3) return p[2] + '/' + p[1];
			    return dStr;
			}
			function updateDateTriggerLabel() {
			    var dtS = document.getElementById('search-date-start').value, dtE = document.getElementById('search-date-end').value, btn = document.getElementById('btn-date-trigger'), txt = document.getElementById('btn-date-text');
			    if (dtS && dtE) { btn.classList.add('has-filter'); txt.innerHTML = fmtDateShort(dtS) + ' a ' + fmtDateShort(dtE); }
			    else if (dtS) { btn.classList.add('has-filter'); txt.innerHTML = 'A partir de ' + fmtDateShort(dtS); }
			    else if (dtE) { btn.classList.add('has-filter'); txt.innerHTML = 'Ate ' + fmtDateShort(dtE); }
			    else { btn.classList.remove('has-filter'); txt.innerHTML = 'Data Pagamento'; }
			}
			function updateDateAprovTriggerLabel() {
			    var dtS = document.getElementById('search-aprov-start').value, dtE = document.getElementById('search-aprov-end').value, btn = document.getElementById('btn-date-aprov-trigger'), txt = document.getElementById('btn-date-aprov-text');
			    if (dtS && dtE) { btn.classList.add('has-filter'); txt.innerHTML = fmtDateShort(dtS) + ' a ' + fmtDateShort(dtE); }
			    else if (dtS) { btn.classList.add('has-filter'); txt.innerHTML = 'A partir de ' + fmtDateShort(dtS); }
			    else if (dtE) { btn.classList.add('has-filter'); txt.innerHTML = 'Ate ' + fmtDateShort(dtE); }
			    else { btn.classList.remove('has-filter'); txt.innerHTML = 'Data Aprovacao'; }
			}
			function updateDateNfTriggerLabel() {
			    var dtS = document.getElementById('search-nf-start').value, dtE = document.getElementById('search-nf-end').value, btn = document.getElementById('btn-date-nf-trigger'), txt = document.getElementById('btn-date-nf-text');
			    if (dtS && dtE) { btn.classList.add('has-filter'); txt.innerHTML = fmtDateShort(dtS) + ' a ' + fmtDateShort(dtE); }
			    else if (dtS) { btn.classList.add('has-filter'); txt.innerHTML = 'A partir de ' + fmtDateShort(dtS); }
			    else if (dtE) { btn.classList.add('has-filter'); txt.innerHTML = 'Ate ' + fmtDateShort(dtE); }
			    else { btn.classList.remove('has-filter'); txt.innerHTML = 'Data NF'; }
			}
			function updateDatePgtoRepTriggerLabel() {
			    var dtS = document.getElementById('search-pgtorep-start').value, dtE = document.getElementById('search-pgtorep-end').value, btn = document.getElementById('btn-date-pgtorep-trigger'), txt = document.getElementById('btn-date-pgtorep-text');
			    if (dtS && dtE) { btn.classList.add('has-filter'); txt.innerHTML = fmtDateShort(dtS) + ' a ' + fmtDateShort(dtE); }
			    else if (dtS) { btn.classList.add('has-filter'); txt.innerHTML = 'A partir de ' + fmtDateShort(dtS); }
			    else if (dtE) { btn.classList.add('has-filter'); txt.innerHTML = 'Ate ' + fmtDateShort(dtE); }
			    else { btn.classList.remove('has-filter'); txt.innerHTML = 'Data Pgto Rep.'; }
			}
			function clearDateFilter() { document.getElementById('search-date-start').value = ''; document.getElementById('search-date-end').value = ''; updateDateTriggerLabel(); document.getElementById('date-popover').classList.remove('show'); renderTable(); }
			function clearDateAprovFilter() { document.getElementById('search-aprov-start').value = ''; document.getElementById('search-aprov-end').value = ''; updateDateAprovTriggerLabel(); document.getElementById('date-aprov-popover').classList.remove('show'); renderTable(); }
			function clearDateNfFilter() { document.getElementById('search-nf-start').value = ''; document.getElementById('search-nf-end').value = ''; updateDateNfTriggerLabel(); document.getElementById('date-nf-popover').classList.remove('show'); renderTable(); }
			function clearDatePgtoRepFilter() { document.getElementById('search-pgtorep-start').value = ''; document.getElementById('search-pgtorep-end').value = ''; updateDatePgtoRepTriggerLabel(); document.getElementById('date-pgtorep-popover').classList.remove('show'); renderTable(); }
			
			function setStatus(id, st) {
			    if (!isUnlocked) {
			        showToast('Desbloqueie o painel para alterar o status!');
			        return;
			    }
			    var item = rawData.find(function(r){return r.id===id;});
			    if (!item) return;
			
			    // Regra: Bloquear aprovacao de repasse zerado
			    if (st === 'Aprovado' && (!item.valorUnit || Number(item.valorUnit) <= 0)) {
			        showToast('Nao e permitido aprovar repasse com valor zerado (R$ 0,00)!');
			        return;
			    }
			
			    if (st === 'Reprovado' || st === 'Validando') {
			        itemSendoObservado = item;
			        statusSendoDefinido = st;
			        abrirModalObservacao(item, st);
			        return;
			    }
			
			    if (item.status === st) return;
			    item.status = st;
			    item.motivo = '';
			    if (st === 'Aprovado') {
			        if (!item.dataAprovacao) item.dataAprovacao = getNowFormatted();
			    } else {
			        item.dataAprovacao = '';
			    }
			    updateItemInGlobalMap(item);
			    renderTable();
			    gravarEstadoSilencioso();
			}
			function lerMotivo(id) {
			    var item = rawData.find(function(r){return r.id===id;});
			    if (!item) return;
			    itemSendoObservado = item;
			    statusSendoDefinido = item.status;
			    abrirModalObservacao(item, item.status);
			}
			function abrirModalObservacao(item, st) {
			    var title = st === 'Reprovado' ? 'Motivo da Reprovacao' : 'Observacao de Validacao';
			    document.getElementById('modal-title').textContent = title;
			    document.getElementById('motivo-texto').value = item.motivo || '';
			    document.getElementById('modal-reprova').classList.add('show');
			}
			function fecharModal() {
			    document.getElementById('modal-reprova').classList.remove('show');
			    itemSendoObservado = null;
			    statusSendoDefinido = null;
			}
			function confirmarObservacaoStatus() {
			    if (itemSendoObservado && statusSendoDefinido) {
			        itemSendoObservado.status = statusSendoDefinido;
			        itemSendoObservado.motivo = document.getElementById('motivo-texto').value;
			        itemSendoObservado.dataAprovacao = '';
			        updateItemInGlobalMap(itemSendoObservado);
			        renderTable();
			        gravarEstadoSilencioso();
			    }
			    fecharModal();
			}
			
			function salvarNfInicial(id, val) {
			    var item = rawData.find(function(r){return r.id===id;});
			    if (!item) return;
			    if (item.status !== 'Aprovado') {
			        showToast('Apenas repasses aprovados podem receber NF!');
			        renderTable();
			        return;
			    }
			    var cleanVal = (val || '').trim();
			    var changed = (item.nfCliente || '') !== cleanVal;
			    item.nfCliente = cleanVal;
			    if (cleanVal !== '') { if (!item.dataNfCliente || changed) item.dataNfCliente = getNowFormatted(); }
			    else { item.dataNfCliente = ''; item.obsNfCliente = ''; }
			    updateItemInGlobalMap(item);
			    renderTable();
			    if (changed) gravarEstadoSilencioso();
			}
			function abrirModalAlterarNf(id) {
			    itemSendoAlteradoNf = rawData.find(function(r){return r.id===id;});
			    if (!itemSendoAlteradoNf) return;
			    if (itemSendoAlteradoNf.status !== 'Aprovado') {
			        showToast('Apenas repasses aprovados podem receber/alterar NF!');
			        return;
			    }
			    document.getElementById('modal-nf-title').textContent = 'Alterar NF Cliente';
			    document.getElementById('nf-leitura-box').style.display = 'none';
			    document.getElementById('nf-edicao-box').style.display = 'block';
			    document.getElementById('inp-modal-nf').value = itemSendoAlteradoNf.nfCliente || '';
			    document.getElementById('inp-modal-nf-obs').value = itemSendoAlteradoNf.obsNfCliente || '';
			    document.getElementById('modal-nf').classList.add('show');
			    setTimeout(function(){ document.getElementById('inp-modal-nf-obs').focus(); }, 100);
			}
			function abrirModalVerObsNf(id) {
			    var item = rawData.find(function(r){return r.id===id;});
			    if (!item) return;
			    itemSendoAlteradoNf = item;
			    document.getElementById('modal-nf-title').textContent = 'Detalhes da NF Cliente';
			    document.getElementById('view-nf-num').textContent = item.nfCliente || '-';
			    document.getElementById('view-nf-date').textContent = item.dataNfCliente || '-';
			    document.getElementById('view-nf-obs').textContent = item.obsNfCliente || 'Sem observacao registrada.';
			    document.getElementById('nf-leitura-box').style.display = 'block';
			    document.getElementById('nf-edicao-box').style.display = 'none';
			    document.getElementById('modal-nf').classList.add('show');
			}
			function abrirEdicaoNfDoModal() {
			    if (!isUnlocked) {
			        showToast('Desbloqueie o painel para editar!');
			        return;
			    }
			    document.getElementById('modal-nf-title').textContent = 'Alterar NF Cliente';
			    document.getElementById('nf-leitura-box').style.display = 'none';
			    document.getElementById('nf-edicao-box').style.display = 'block';
			    if (itemSendoAlteradoNf) {
			        document.getElementById('inp-modal-nf').value = itemSendoAlteradoNf.nfCliente || '';
			        document.getElementById('inp-modal-nf-obs').value = itemSendoAlteradoNf.obsNfCliente || '';
			    }
			    setTimeout(function(){ document.getElementById('inp-modal-nf-obs').focus(); }, 100);
			}
			function fecharModalNf() {
			    document.getElementById('modal-nf').classList.remove('show');
			    itemSendoAlteradoNf = null;
			}
			function confirmarAlteracaoNf() {
			    if (itemSendoAlteradoNf) {
			        var novaNf = (document.getElementById('inp-modal-nf').value || '').trim();
			        var novaObs = (document.getElementById('inp-modal-nf-obs').value || '').trim();
			        itemSendoAlteradoNf.nfCliente = novaNf;
			        itemSendoAlteradoNf.obsNfCliente = novaObs;
			        if (novaNf !== '') {
			            itemSendoAlteradoNf.dataNfCliente = getNowFormatted();
			        } else {
			            itemSendoAlteradoNf.dataNfCliente = '';
			            itemSendoAlteradoNf.obsNfCliente = '';
			        }
			        updateItemInGlobalMap(itemSendoAlteradoNf);
			        renderTable();
			        gravarEstadoSilencioso();
			        showToast('NF Cliente atualizada!');
			    }
			    fecharModalNf();
			}
			
			var itemSendoAlteradoPgtoRep = null;
			function salvarDataPgtoRepasseDirect(id, val) {
			    if (!val) return;
			    var item = rawData.find(function(r){return r.id===id;});
			    if (!item) return;
			    if (item.status !== 'Aprovado') {
			        showToast('Necessario status Aprovado primeiro!');
			        renderTable();
			        return;
			    }
			    if (!item.nfCliente || item.nfCliente.trim() === '') {
			        showToast('Necessario preencher a NF Cliente primeiro!');
			        renderTable();
			        return;
			    }
			    var formatted = val;
			    if (val.indexOf('-') >= 0) {
			        var p = val.split('-');
			        formatted = p[2] + '/' + p[1] + '/' + p[0];
			    }
			    item.dataPgtoRepasse = formatted;
			    updateItemInGlobalMap(item);
			    renderTable();
			    gravarEstadoSilencioso();
			    showToast('Data de pgto repasse salva!');
			}
			function abrirModalAlterarDataPgtoRep(id) {
			    itemSendoAlteradoPgtoRep = rawData.find(function(r){return r.id===id;});
			    if (!itemSendoAlteradoPgtoRep) return;
			    if (itemSendoAlteradoPgtoRep.status !== 'Aprovado' || !itemSendoAlteradoPgtoRep.nfCliente || itemSendoAlteradoPgtoRep.nfCliente.trim() === '') {
			        showToast('Necessario aprovacao e NF preenchida!');
			        return;
			    }
			    var inp = document.getElementById('inp-modal-pgtorep');
			    if (inp) {
			        if (itemSendoAlteradoPgtoRep.dataPgtoRepasse) {
			            var p = itemSendoAlteradoPgtoRep.dataPgtoRepasse.split('/');
			            if (p.length === 3) inp.value = p[2] + '-' + p[1].padStart(2,'0') + '-' + p[0].padStart(2,'0');
			            else inp.value = '';
			        } else {
			            inp.value = '';
			        }
			    }
			    document.getElementById('modal-pgtorep').classList.add('show');
			}
			function fecharModalPgtoRep() {
			    document.getElementById('modal-pgtorep').classList.remove('show');
			    itemSendoAlteradoPgtoRep = null;
			}
			function confirmarAlteracaoPgtoRep() {
			    if (!itemSendoAlteradoPgtoRep) return;
			    var val = document.getElementById('inp-modal-pgtorep').value;
			    if (val) {
			        var p = val.split('-');
			        itemSendoAlteradoPgtoRep.dataPgtoRepasse = p[2] + '/' + p[1] + '/' + p[0];
			    } else {
			        itemSendoAlteradoPgtoRep.dataPgtoRepasse = '';
			    }
			    updateItemInGlobalMap(itemSendoAlteradoPgtoRep);
			    renderTable();
			    gravarEstadoSilencioso();
			    fecharModalPgtoRep();
			    showToast('Data de pgto repasse salva!');
			}
			function removerDataPgtoRep() {
			    if (!itemSendoAlteradoPgtoRep) return;
			    itemSendoAlteradoPgtoRep.dataPgtoRepasse = '';
			    updateItemInGlobalMap(itemSendoAlteradoPgtoRep);
			    renderTable();
			    gravarEstadoSilencioso();
			    fecharModalPgtoRep();
			    showToast('Data removida!');
			}
			
			function showTooltip(e, title, text) {
			    var tt = document.getElementById('custom-tooltip');
			    if (!tt) return;
			    tt.innerHTML = '<div class=""tt-header"">' + title + '</div><div class=""tt-body"">' + text + '</div>';
			    tt.classList.add('show');
			    moveTooltip(e);
			}
			function moveTooltip(e) {
			    var tt = document.getElementById('custom-tooltip');
			    if (!tt || !tt.classList.contains('show')) return;
			    var x = e.clientX + 12, y = e.clientY + 12;
			    if (x + 260 > window.innerWidth) x = e.clientX - 260;
			    if (y + 80 > window.innerHeight) y = e.clientY - 80;
			    tt.style.left = x + 'px';
			    tt.style.top = y + 'px';
			}
			function hideTooltip() {
			    var tt = document.getElementById('custom-tooltip');
			    if (tt) tt.classList.remove('show');
			}
			
			function gravarEstadoSilencioso() {
			    var payload = getMergedPayload();
			    var payloadStr = JSON.stringify(payload);
			    try { localStorage.setItem('painel_repasses_cache', payloadStr); } catch(e){}

			    fetch(SB_URL, {
			        method: 'POST',
			        headers: {
			            'apikey': SB_KEY,
			            'Authorization': 'Bearer ' + SB_KEY,
			            'Content-Type': 'application/json',
			            'Prefer': 'resolution=merge-duplicates'
			        },
			        body: JSON.stringify([{
			            id: DOC_ID,
			            title: 'ESTADO_REPASSE_APROVACOES',
			            category: 'repasse_aprovacoes',
			            description: payloadStr
			        }])
			    }).catch(function(e) {
			        console.log('Erro ao gravar silencioso no Supabase:', e);
			    });
			}

			function gravarEstado() {
			    var btn = document.getElementById('btn-save');
			    if (btn) { btn.textContent = 'GRAVANDO...'; }
			    
			    var payload = getMergedPayload();
			    var payloadStr = JSON.stringify(payload);
			    try { localStorage.setItem('painel_repasses_cache', payloadStr); } catch(e){}

			    fetch(SB_URL, {
			        method: 'POST',
			        headers: {
			            'apikey': SB_KEY,
			            'Authorization': 'Bearer ' + SB_KEY,
			            'Content-Type': 'application/json',
			            'Prefer': 'resolution=merge-duplicates'
			        },
			        body: JSON.stringify([{
			            id: DOC_ID,
			            title: 'ESTADO_REPASSE_APROVACOES',
			            category: 'repasse_aprovacoes',
			            description: payloadStr
			        }])
			    })
			    .then(function(resp) {
			        if (resp.ok) {
			            hasUnsaved = false;
			            if (btn) { btn.classList.remove('has-changes'); btn.textContent = 'GRAVAR'; }
			            showToast('Estado gravado com sucesso na nuvem!');
			        } else {
			            throw new Error('Falha HTTP ' + resp.status);
			        }
			    })
			    .catch(function(e) {
			        if (btn) { btn.textContent = 'GRAVAR'; }
			        showToast('Gravado no cache local! (Nuvem indisponivel)');
			    });
			}

			function copyToExcel() {
			    var tsv = 'JOB\tData Cadastro\tCliente\tBandeira\tCNPJ\tCategoria\tValor\tNF\tNF Cliente\tObs NF Cliente\tData NF Cliente\tData Pgto\tUnidade\tNome Unidade\tGrossup\tImposto Franq.\tRetencao\tVl. Retencao\t% Repasse\tVl. Repasse\tData Aprovacao\tData Pgto Repasse\tStatus\tMotivo\n';
			    var search = document.getElementById('search').value.toLowerCase();
			    var startVal = toDateNum(document.getElementById('search-date-start').value), endVal = toDateNum(document.getElementById('search-date-end').value);
			    var startAprovVal = toDateNum(document.getElementById('search-aprov-start').value), endAprovVal = toDateNum(document.getElementById('search-aprov-end').value);
			    var startNfVal = toDateNum(document.getElementById('search-nf-start').value), endNfVal = toDateNum(document.getElementById('search-nf-end').value);
			    var startPgtoRepVal = toDateNum(document.getElementById('search-pgtorep-start').value), endPgtoRepVal = toDateNum(document.getElementById('search-pgtorep-end').value);

			    var data = rawData.filter(function(r) {
			        var ms = !search || r.cnpj.toLowerCase().indexOf(search)>=0 || r.nome.toLowerCase().indexOf(search)>=0 || r.unidade.toLowerCase().indexOf(search)>=0 || r.nomeUnidade.toLowerCase().indexOf(search)>=0 || (r.categoria && r.categoria.toLowerCase().indexOf(search)>=0) || (r.nf && r.nf.toLowerCase().indexOf(search)>=0) || (r.nfCliente && r.nfCliente.toLowerCase().indexOf(search)>=0) || (r.obsNfCliente && r.obsNfCliente.toLowerCase().indexOf(search)>=0) || (r.grossup && r.grossup.toLowerCase().indexOf(search)>=0) || (r.imposto && r.imposto.toLowerCase().indexOf(search)>=0);
			        var rowDateVal = toDateNum(r.dataPagamento), md = (!startVal || rowDateVal >= startVal) && (!endVal || rowDateVal <= endVal);
			        var rowAprovDateVal = toDateNum(r.dataAprovacao), mda = (!startAprovVal || rowAprovDateVal >= startAprovVal) && (!endAprovVal || rowAprovDateVal <= endAprovVal);
			        var rowNfDateVal = toDateNum(r.dataNfCliente), mdnf = (!startNfVal || rowNfDateVal >= startNfVal) && (!endNfVal || rowNfDateVal <= endNfVal);
			        var rowPgtoRepVal = toDateNum(r.dataPgtoRepasse), mdpgtorep = (!startPgtoRepVal || rowPgtoRepVal >= startPgtoRepVal) && (!endPgtoRepVal || rowPgtoRepVal <= endPgtoRepVal);
			        var mf = currentFilter==='all' || (currentFilter==='approved' && r.status==='Aprovado') || (currentFilter==='validating' && r.status==='Validando') || (currentFilter==='pending' && r.status==='Pendente') || (currentFilter==='rejected' && r.status==='Reprovado');
			        return ms && md && mda && mdnf && mdpgtorep && mf;
			    });

			    for (var i=0; i<data.length; i++) {
			        var r = data[i], m = (r.motivo || '').replace(/\n/g, ' '), obsNf = (r.obsNfCliente || '').replace(/\n/g, ' ');
			        tsv += (r.job||'') + '\t' + (r.dataCadastro||'') + '\t' + r.nome + '\t' + (r.bandeira||'') + '\t' + r.cnpj + '\t' + (r.categoria||'') + '\t' + String(r.valor).replace('.', ',') + '\t' + (r.nf||'') + '\t' + (r.nfCliente||'') + '\t' + obsNf + '\t' + (r.dataNfCliente||'') + '\t' + (r.dataPagamento||'') + '\t' + r.unidade + '\t' + r.nomeUnidade + '\t' + (r.grossup||'') + '\t' + (r.imposto||'') + '\t' + (r.retencao ? String(r.retencao).replace('.', ',') + '%' : '0%') + '\t' + String(r.valorRetencao ? r.valorRetencao.toFixed(2) : '0').replace('.', ',') + '\t' + String(r.percHonorario).replace('.', ',') + '\t' + String(r.valorUnit ? r.valorUnit.toFixed(2) : '0').replace('.', ',') + '\t' + (r.dataAprovacao||'') + '\t' + (r.dataPgtoRepasse||'') + '\t' + r.status + '\t' + m + '\n';
			    }
			    if (navigator.clipboard && navigator.clipboard.writeText) {
			        navigator.clipboard.writeText(tsv).then(function() {
			            showToast('Dados copiados! Cole no Excel com Ctrl+V');
			        }).catch(function() {
			            fallbackCopy(tsv);
			        });
			    } else {
			        fallbackCopy(tsv);
			    }
			}
			function fallbackCopy(text) {
			    var ta = document.createElement('textarea');
			    ta.value = text;
			    ta.style.position = 'fixed';
			    ta.style.left = '-9999px';
			    document.body.appendChild(ta);
			    ta.select();
			    try {
			        document.execCommand('copy');
			        showToast('Dados copiados! Cole no Excel com Ctrl+V');
			    } catch(e) {
			        showToast('Erro ao copiar dados');
			    }
			    document.body.removeChild(ta);
			}

			function updateCards(filteredList) {
			    var list = filteredList || rawData;
			    var sumAll = 0, countAll = 0, sumRetAll = 0;
			    var sumApr = 0, countApr = 0, sumRetApr = 0;
			    var sumVal = 0, countVal = 0, sumRetVal = 0;
			    var sumPen = 0, countPen = 0, sumRetPen = 0;
			    var sumRep = 0, countRep = 0, sumRetRep = 0;

			    for (var i = 0; i < list.length; i++) {
			        var r = list[i];
			        var v = Number(r.valorUnit) || 0;
			        var vRet = Number(r.valorRetencao) || 0;
			        sumAll += v; sumRetAll += vRet; countAll++;
			        if (r.status === 'Aprovado') { sumApr += v; sumRetApr += vRet; countApr++; }
			        else if (r.status === 'Validando') { sumVal += v; sumRetVal += vRet; countVal++; }
			        else if (r.status === 'Reprovado') { sumRep += v; sumRetRep += vRet; countRep++; }
			        else { sumPen += v; sumRetPen += vRet; countPen++; }
			    }

			    document.getElementById('c-val-all').textContent = fmtBRL(sumAll);
			    document.getElementById('c-cnt-all').textContent = countAll + ' lancamentos';
			    document.getElementById('c-ret-all').textContent = 'Retencao: ' + fmtBRL(sumRetAll);

			    document.getElementById('c-val-approved').textContent = fmtBRL(sumApr);
			    document.getElementById('c-cnt-approved').textContent = countApr + ' lancamentos';
			    document.getElementById('c-ret-approved').textContent = 'Retencao: ' + fmtBRL(sumRetApr);

			    document.getElementById('c-val-validating').textContent = fmtBRL(sumVal);
			    document.getElementById('c-cnt-validating').textContent = countVal + ' lancamentos';
			    document.getElementById('c-ret-validating').textContent = 'Retencao: ' + fmtBRL(sumRetVal);

			    document.getElementById('c-val-pending').textContent = fmtBRL(sumPen);
			    document.getElementById('c-cnt-pending').textContent = countPen + ' lancamentos';
			    document.getElementById('c-ret-pending').textContent = 'Retencao: ' + fmtBRL(sumRetPen);

			    document.getElementById('c-val-rejected').textContent = fmtBRL(sumRep);
			    document.getElementById('c-cnt-rejected').textContent = countRep + ' lancamentos';
			    document.getElementById('c-ret-rejected').textContent = 'Retencao: ' + fmtBRL(sumRetRep);

			    document.getElementById('tab-cnt-all').textContent = countAll;
			    document.getElementById('tab-cnt-approved').textContent = countApr;
			    document.getElementById('tab-cnt-validating').textContent = countVal;
			    document.getElementById('tab-cnt-pending').textContent = countPen;
			    document.getElementById('tab-cnt-rejected').textContent = countRep;
			}

			function renderTable() {
			    var search = document.getElementById('search').value.toLowerCase();
			    var startVal = toDateNum(document.getElementById('search-date-start').value), endVal = toDateNum(document.getElementById('search-date-end').value);
			    var startAprovVal = toDateNum(document.getElementById('search-aprov-start').value), endAprovVal = toDateNum(document.getElementById('search-aprov-end').value);
			    var startNfVal = toDateNum(document.getElementById('search-nf-start').value), endNfVal = toDateNum(document.getElementById('search-nf-end').value);
			    var startPgtoRepVal = toDateNum(document.getElementById('search-pgtorep-start').value), endPgtoRepVal = toDateNum(document.getElementById('search-pgtorep-end').value);

			    var data = rawData.filter(function(r) {
			        var ms = !search || r.cnpj.toLowerCase().indexOf(search)>=0 || r.nome.toLowerCase().indexOf(search)>=0 || r.unidade.toLowerCase().indexOf(search)>=0 || r.nomeUnidade.toLowerCase().indexOf(search)>=0 || (r.categoria && r.categoria.toLowerCase().indexOf(search)>=0) || (r.nf && r.nf.toLowerCase().indexOf(search)>=0) || (r.nfCliente && r.nfCliente.toLowerCase().indexOf(search)>=0) || (r.obsNfCliente && r.obsNfCliente.toLowerCase().indexOf(search)>=0) || (r.grossup && r.grossup.toLowerCase().indexOf(search)>=0) || (r.imposto && r.imposto.toLowerCase().indexOf(search)>=0);
			        var rowDateVal = toDateNum(r.dataPagamento), md = (!startVal || rowDateVal >= startVal) && (!endVal || rowDateVal <= endVal);
			        var rowAprovDateVal = toDateNum(r.dataAprovacao), mda = (!startAprovVal || rowAprovDateVal >= startAprovVal) && (!endAprovVal || rowAprovDateVal <= endAprovVal);
			        var rowNfDateVal = toDateNum(r.dataNfCliente), mdnf = (!startNfVal || rowNfDateVal >= startNfVal) && (!endNfVal || rowNfDateVal <= endNfVal);
			        var rowPgtoRepVal = toDateNum(r.dataPgtoRepasse), mdpgtorep = (!startPgtoRepVal || rowPgtoRepVal >= startPgtoRepVal) && (!endPgtoRepVal || rowPgtoRepVal <= endPgtoRepVal);
			        var mf = currentFilter==='all' || (currentFilter==='approved' && r.status==='Aprovado') || (currentFilter==='validating' && r.status==='Validando') || (currentFilter==='pending' && r.status==='Pendente') || (currentFilter==='rejected' && r.status==='Reprovado');
			        return ms && md && mda && mdnf && mdpgtorep && mf;
			    });
			    var isDateCol = (currentSort.key === 'dataPagamento' || currentSort.key === 'dataAprovacao' || currentSort.key === 'dataNfCliente' || currentSort.key === 'dataPgtoRepasse');
			    data.sort(function(a,b) {
			        if (isDateCol) {
			            var vDa = toDateNum(a[currentSort.key]), vDb = toDateNum(b[currentSort.key]);
			            return currentSort.asc ? (vDa - vDb) : (vDb - vDa);
			        }
			        var va = a[currentSort.key] || '', vb = b[currentSort.key] || '';
			        if (typeof va === 'number') return currentSort.asc ? va - vb : vb - va;
			        return currentSort.asc ? String(va).localeCompare(String(vb)) : String(vb).localeCompare(String(va));
			    });

			    var html = '', sumVal = 0, sumUnit = 0, sumRetencao = 0;
			    for (var i=0; i<data.length; i++) {
			        var r = data[i], st = r.status || 'Pendente', pH = r.percHonorario;
			        sumVal += Number(r.valor) || 0;
			        sumUnit += Number(r.valorUnit) || 0;
			        sumRetencao += Number(r.valorRetencao) || 0;
			
			        var isAprovado = (st === 'Aprovado');
			        var hasNf = (r.nfCliente && r.nfCliente.trim() !== '');
			
			        // Rule 1: NF only enabled if Approved
			        var nfCliHtml = '';
			        if (!isAprovado) {
			            if (hasNf) {
				                nfCliHtml = '<span style=""color:var(--text-muted);font-size:12px;"">' + r.nfCliente + '</span>';
			            } else {
			                nfCliHtml = '<span style=""color:var(--text-dim);font-size:12px;cursor:not-allowed;"" title=""Necessario status Aprovado para inserir NF"">-</span>';
			            }
			        } else {
			            var nfTitle = r.dataNfCliente ? ('Preenchido em: ' + r.dataNfCliente) : '';
			            if (hasNf) {
			                var obsBtnHtml = r.obsNfCliente ? '<button class=""btn-view-obs"" onclick=""abrirModalVerObsNf(\\' + r.id + '\\)"" title=""Ver observacao""><svg width=""13"" height=""13"" viewBox=""0 0 24 24"" fill=""none"" stroke=""currentColor"" stroke-width=""2"" stroke-linecap=""round"" stroke-linejoin=""round""><path d=""M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z""></path></svg></button>' : '';
			                nfCliHtml = '<div class=""nf-cliente-box"" title=""' + nfTitle + '""><span class=""nf-cliente-text"">' + r.nfCliente + '</span><button class=""btn-edit-nf"" onclick=""abrirModalAlterarNf(\\' + r.id + '\\)"" title=""Alterar NF""><svg width=""12"" height=""12"" viewBox=""0 0 24 24"" fill=""none"" stroke=""currentColor"" stroke-width=""2"" stroke-linecap=""round"" stroke-linejoin=""round""><path d=""M17 3a2.828 2.828 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5L17 3z""></path></svg></button>' + obsBtnHtml + '</div>';
			            } else {
			                nfCliHtml = '<input type=""text"" id=""inp-nf-' + r.id + '"" class=""input-nf-cliente"" placeholder=""Inserir NF..."" value="""" onkeydown=""if(event.key===\\'Enter\\') salvarNfInicial(\\' + r.id + '\\', this.value)"" onblur=""salvarNfInicial(\\' + r.id + '\\', this.value)"">';
			            }
			        }
			
			        // Rule 2: Data Pgto Repasse only enabled if NF is filled (and Approved)
			        var dataPgtoRepDisplay = '';
			        if (!isAprovado || !hasNf) {
			            if (r.dataPgtoRepasse) {
			                dataPgtoRepDisplay = '<span style=""color:var(--text-muted);font-size:12px;"">' + r.dataPgtoRepasse + '</span>';
			            } else {
			                dataPgtoRepDisplay = '<span style=""color:var(--text-dim);font-size:12px;cursor:not-allowed;"" title=""Necessario NF preenchida para informar Data de Pgto do Repasse"">-</span>';
			            }
			        } else {
			            if (r.dataPgtoRepasse) {
			                dataPgtoRepDisplay = '<div class=""data-pgto-box""><span style=""color:#38bdf8;font-size:12px;font-weight:700;"">' + r.dataPgtoRepasse + '</span><button class=""btn-edit-nf"" onclick=""abrirModalAlterarDataPgtoRep(\\' + r.id + '\\)"" title=""Alterar Data Pgto""><svg width=""11"" height=""11"" viewBox=""0 0 24 24"" fill=""none"" stroke=""currentColor"" stroke-width=""2"" stroke-linecap=""round"" stroke-linejoin=""round""><path d=""M17 3a2.828 2.828 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5L17 3z""></path></svg></button></div>';
			            } else {
			                dataPgtoRepDisplay = '<input type=""date"" id=""inp-dtpgto-' + r.id + '"" class=""input-data-pgto-cell"" onchange=""salvarDataPgtoRepasseDirect(\\' + r.id + '\\', this.value)"" title=""Definir data do pagamento do repasse"">';
			            }
			        }
			
			        var dataNfDisplay = r.dataNfCliente ? ('<span style=""color:var(--gold);font-size:12px;font-weight:600"">' + r.dataNfCliente + '</span>') : '<span style=""color:var(--text-dim)"">-</span>';
			        var aprovDisplay = r.dataAprovacao ? ('<span style=""color:var(--green);font-size:12px;font-weight:600"">' + r.dataAprovacao + '</span>') : '<span style=""color:var(--text-dim)"">-</span>';
			
			        html += '<tr style=""animation-delay:' + (i*0.03) + 's"">';
			        html += '<td style=""color:var(--text-main);font-weight:600"">' + (r.job||'-') + '</td>';
			        html += '<td style=""color:var(--text-main)"">' + (r.dataCadastro||'-') + '</td>';
			        html += '<td><span class=""nome"">' + r.nome + '</span></td>';
			        html += '<td><span style=""color:var(--gold);font-weight:600;font-size:10px;text-transform:uppercase;"">' + (r.bandeira||'-') + '</span></td>';
			        html += '<td><span class=""cnpj"">' + r.cnpj + '</span></td>';
			        html += '<td><span style=""color:var(--gold);font-weight:600;font-size:10px;text-transform:uppercase;"">' + (r.categoria||'-') + '</span></td>';
			        html += '<td class=""valor num"">' + fmtBRL(r.valor) + '</td>';
			        html += '<td style=""color:var(--text-main)"">' + (r.nf||'-') + '</td>';
			        html += '<td style=""text-align:center;"">' + nfCliHtml + '</td>';
			        html += '<td class=""num"">' + dataNfDisplay + '</td>';
			        html += '<td class=""num"" style=""color:var(--text-main);font-weight:600"">' + (r.dataPagamento||'-') + '</td>';
			        html += '<td><span class=""unidade-code"">' + (r.unidade||'') + '</span></td>';
			        html += '<td style=""color:var(--text-main);font-size:11px"">' + (r.nomeUnidade||'') + '</td>';
			        html += '<td style=""color:var(--text-main);text-align:center;font-weight:600;cursor:help;"" onmouseenter=""showTooltip(event, \\'Grossup\\', \\'O contrato de JOB veio com a clausula de Grossup.\\')"" onmousemove=""moveTooltip(event)"" onmouseleave=""hideTooltip()"">' + (r.grossup||'-') + '</td>';
			        html += '<td style=""color:var(--text-main);text-align:center;font-weight:600;cursor:help;"" onmouseenter=""showTooltip(event, \\'Imposto Franq.\\', \\'Descontar o Grossup do franqueado.\\')"" onmousemove=""moveTooltip(event)"" onmouseleave=""hideTooltip()"">' + (r.imposto||'-') + '</td>';
			        html += '<td class=""num"" style=""color:var(--text-main);font-weight:600"">' + (r.retencao ? String(r.retencao).replace('.', ',')+'%' : '0,00%') + '</td>';
			        html += '<td class=""num"" style=""color:var(--text-main)"">' + (r.valorRetencao ? fmtBRL(r.valorRetencao) : '-') + '</td>';
			        html += '<td class=""num"" style=""color:var(--text-main);font-weight:600;"">' + (pH ? String(pH).replace('.', ',')+'%' : '0,00%') + '</td>';
			        html += '<td class=""num"" style=""color:var(--text-main)"">' + (r.valorUnit ? fmtBRL(r.valorUnit) : '-') + '</td>';
			        html += '<td class=""num"">' + aprovDisplay + '</td>';
			        html += '<td class=""num"">' + dataPgtoRepDisplay + '</td>';
			        html += '<td class=""num""><div class=""status-btn-group"">';
			        html += '<div class=""status-btn ' + (st==='Pendente'?'active-p':'') + '"" title=""Pendente"" onclick=""setStatus(\\'' + r.id + '\\',\\'Pendente\\')"">P</div>';
			        html += '<div class=""status-btn ' + (st==='Validando'?'active-v':'') + '"" title=""Validando"" onclick=""setStatus(\\'' + r.id + '\\',\\'Validando\\')"">V</div>';
			        html += '<div class=""status-btn ' + (st==='Aprovado'?'active-a':'') + '"" title=""Aprovado"" onclick=""setStatus(\\'' + r.id + '\\',\\'Aprovado\\')"">A</div>';
			        html += '<div class=""status-btn ' + (st==='Reprovado'?'active-r':'') + '"" title=""Reprovado"" onclick=""setStatus(\\'' + r.id + '\\',\\'Reprovado\\')"">R</div>';
			        if ((st==='Reprovado' || st==='Validando') && r.motivo) html += '<span class=""icon-eye"" title=""Ver motivo / observacao"" onclick=""lerMotivo(\\'' + r.id + '\\')""><svg width=""14"" height=""14"" viewBox=""0 0 24 24"" fill=""none"" stroke=""currentColor"" stroke-width=""2"" stroke-linecap=""round"" stroke-linejoin=""round""><path d=""M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z""></path><circle cx=""12"" cy=""12"" r=""3""></circle></svg></span>';
			        html += '</div></td></tr>';
			    }
			    document.getElementById('tbody').innerHTML = html;
			
			    var foot = '<tr><td colspan=""6"">TOTAL</td><td class=""valor num"">' + fmtBRL(sumVal) + '</td><td colspan=""9""></td><td class=""valor num"">' + fmtBRL(sumRetencao) + '</td><td></td><td class=""valor num"">' + fmtBRL(sumUnit) + '</td><td colspan=""3""></td></tr>';
			    document.getElementById('tfoot').innerHTML = foot;
			    document.getElementById('visible-count').innerHTML = data.length + ' de ' + rawData.length + ' exibidos';
			    updateCards(data);
			}
			loadSaved();
			renderTable();
			</script>"""

# Replace in painel_def
updated_painel = painel_def[:js_start] + new_js_code + painel_def[js_end+len('</script>'):]

# Update full TMDL in OneDrive and Downloads
for p in [r'C:\Users\cristhofer.maciel.GRUPOSTUDIO\OneDrive\repasse.SemanticModel\definition\tables\medidas_html.tmdl', r'C:\Users\cristhofer.maciel.GRUPOSTUDIO\Downloads\repasse.SemanticModel\definition\tables\medidas_html.tmdl']:
    if os.path.exists(p):
        with open(p, 'r', encoding='utf-8') as f:
            c = f.read()
        p_start = c.find('measure Painel_Repasses =')
        p_end = c.find('\n\tmeasure ', p_start + 1)
        if p_end == -1: p_end = len(c)
        c_new = c[:p_start] + updated_painel + c[p_end:]
        with open(p, 'w', encoding='utf-8') as f:
            f.write(c_new)
        print(f'Updated file: {p}')

# Extract DAX expression for MCP
m = re.search(r'```([\s\S]*?)```', updated_painel)
raw_expr = ''
if m:
    lines = [l.replace('\t\t\t', '') for l in m.group(1).strip().splitlines()]
    raw_expr = '\n'.join(lines)

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

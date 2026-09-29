<script>
			var rawData = [" & vJsonRows & "];
			
			for (var i=0; i<rawData.length; i++) {
			    if (!rawData[i].status || rawData[i].status.trim() === '') rawData[i].status = 'Pendente';
			}
			var currentFilter = 'all';
			var currentSort = {key:'nome', asc:true};
			var hasUnsaved = false, isUnlocked = false, itemSendoAlteradoNf = null, itemSendoObservado = null, statusSendoDefinido = null;
			
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
			    for (var i = 0; i < rawData.length; i++) {
			        var saved = map[String(rawData[i].id)];
			        if (saved !== undefined) {
			            if (typeof saved === 'string') {
			                rawData[i].status = saved;
			            } else if (typeof saved === 'object') {
			                rawData[i].status = saved.status || rawData[i].status || 'Pendente';
			                rawData[i].motivo = saved.motivo || '';
			                if (saved.nfCliente !== undefined) rawData[i].nfCliente = saved.nfCliente;
			                if (saved.obsNfCliente !== undefined) rawData[i].obsNfCliente = saved.obsNfCliente;
			                if (saved.dataAprovacao !== undefined) rawData[i].dataAprovacao = saved.dataAprovacao;
			                if (saved.dataNfCliente !== undefined) rawData[i].dataNfCliente = saved.dataNfCliente;
			                if (saved.dataPgtoRepasse !== undefined) rawData[i].dataPgtoRepasse = saved.dataPgtoRepasse;
			            }
			        } else if (!rawData[i].status || rawData[i].status === '') {
			            rawData[i].status = 'Pendente';
			        }
			    }
			    renderTable();
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
			function closeAllDatePopovers() {
			    ['datePopover', 'dateAprovPopover', 'dateNfPopover', 'datePgtoRepPopover'].forEach(function(id){
			        var el = document.getElementById(id);
			        if (el) el.classList.remove('show');
			    });
			}
			function toggleDatePopover(e) {
			    if (e) e.stopPropagation();
			    var p = document.getElementById('datePopover'), isS = p && p.classList.contains('show');
			    closeAllDatePopovers();
			    if (!isS && p) p.classList.add('show');
			}
			function toggleDateAprovPopover(e) {
			    if (e) e.stopPropagation();
			    var p = document.getElementById('dateAprovPopover'), isS = p && p.classList.contains('show');
			    closeAllDatePopovers();
			    if (!isS && p) p.classList.add('show');
			}
			function toggleDateNfPopover(e) {
			    if (e) e.stopPropagation();
			    var p = document.getElementById('dateNfPopover'), isS = p && p.classList.contains('show');
			    closeAllDatePopovers();
			    if (!isS && p) p.classList.add('show');
			}
			function toggleDatePgtoRepPopover(e) {
			    if (e) e.stopPropagation();
			    var p = document.getElementById('datePgtoRepPopover'), isS = p && p.classList.contains('show');
			    closeAllDatePopovers();
			    if (!isS && p) p.classList.add('show');
			}
			window.addEventListener('click', function(e) {
			    if (!e.target.closest('#datePopoverContainer') && !e.target.closest('#dateAprovPopoverContainer') && !e.target.closest('#dateNfPopoverContainer') && !e.target.closest('#datePgtoRepPopoverContainer')) {
			        closeAllDatePopovers();
			    }
			});
			function onDateChange() { updateDateTriggerLabel(); filterTable(); }
			function onDateAprovChange() { updateDateAprovTriggerLabel(); filterTable(); }
			function onDateNfChange() { updateDateNfTriggerLabel(); filterTable(); }
			function onDatePgtoRepChange() { updateDatePgtoRepTriggerLabel(); filterTable(); }
			
			function updateDateTriggerLabel() {
			    var dtS = document.getElementById('search-date-start').value, dtE = document.getElementById('search-date-end').value, btn = document.getElementById('dateTriggerBtn'), txt = document.getElementById('dateTriggerText');
			    if (dtS || dtE) { btn.classList.add('has-filter'); txt.innerHTML = (dtS ? dtS.split('-')[2] + '/' + dtS.split('-')[1] : '...') + ' até ' + (dtE ? dtE.split('-')[2] + '/' + dtE.split('-')[1] : '...'); }
			    else { btn.classList.remove('has-filter'); txt.innerHTML = 'Data Pgto'; }
			}
			function updateDateAprovTriggerLabel() {
			    var dtS = document.getElementById('search-aprov-start').value, dtE = document.getElementById('search-aprov-end').value, btn = document.getElementById('dateAprovTriggerBtn'), txt = document.getElementById('dateAprovTriggerText');
			    if (dtS || dtE) { btn.classList.add('has-filter'); txt.innerHTML = (dtS ? dtS.split('-')[2] + '/' + dtS.split('-')[1] : '...') + ' até ' + (dtE ? dtE.split('-')[2] + '/' + dtE.split('-')[1] : '...'); }
			    else { btn.classList.remove('has-filter'); txt.innerHTML = 'Data Aprov.'; }
			}
			function updateDateNfTriggerLabel() {
			    var dtS = document.getElementById('search-nf-start').value, dtE = document.getElementById('search-nf-end').value, btn = document.getElementById('dateNfTriggerBtn'), txt = document.getElementById('dateNfTriggerText');
			    if (dtS || dtE) { btn.classList.add('has-filter'); txt.innerHTML = (dtS ? dtS.split('-')[2] + '/' + dtS.split('-')[1] : '...') + ' até ' + (dtE ? dtE.split('-')[2] + '/' + dtE.split('-')[1] : '...'); }
			    else { btn.classList.remove('has-filter'); txt.innerHTML = 'Data NF'; }
			}
			function updateDatePgtoRepTriggerLabel() {
			    var dtS = document.getElementById('search-pgtorep-start').value, dtE = document.getElementById('search-pgtorep-end').value, btn = document.getElementById('datePgtoRepTriggerBtn'), txt = document.getElementById('datePgtoRepTriggerText');
			    if (dtS || dtE) { btn.classList.add('has-filter'); txt.innerHTML = (dtS ? dtS.split('-')[2] + '/' + dtS.split('-')[1] : '...') + ' até ' + (dtE ? dtE.split('-')[2] + '/' + dtE.split('-')[1] : '...'); }
			    else { btn.classList.remove('has-filter'); txt.innerHTML = 'Data Pgto Rep.'; }
			}
			function clearDateFilter() { document.getElementById('search-date-start').value = ''; document.getElementById('search-date-end').value = ''; updateDateTriggerLabel(); filterTable(); }
			function clearDateAprovFilter() { document.getElementById('search-aprov-start').value = ''; document.getElementById('search-aprov-end').value = ''; updateDateAprovTriggerLabel(); filterTable(); }
			function clearDateNfFilter() { document.getElementById('search-nf-start').value = ''; document.getElementById('search-nf-end').value = ''; updateDateNfTriggerLabel(); filterTable(); }
			function clearDatePgtoRepFilter() { document.getElementById('search-pgtorep-start').value = ''; document.getElementById('search-pgtorep-end').value = ''; updateDatePgtoRepTriggerLabel(); filterTable(); }
			
			function setStatus(id, newStatus) {
			    if (!isUnlocked) {
			        showToast('Clique em Desbloquear para editar!');
			        return;
			    }
			    var item = rawData.find(function(r){return r.id===id;});
			    if (!item) return;
			    if (newStatus === 'Reprovado' || newStatus === 'Validando') {
			        itemSendoObservado = item;
			        statusSendoDefinido = newStatus;
			        var modalTitle = (newStatus === 'Reprovado') ? 'Motivo da Reprovação' : 'Observação de Validação';
			        var titleEl = document.getElementById('modal-title');
			        titleEl.textContent = modalTitle;
			        titleEl.style.color = (newStatus === 'Reprovado') ? 'var(--red)' : '#38bdf8';
			        var confirmBtn = document.getElementById('btn-confirm-modal');
			        confirmBtn.textContent = (newStatus === 'Reprovado') ? 'Reprovar' : 'Salvar Validação';
			        confirmBtn.className = 'modal-btn confirm';
			        confirmBtn.style.background = (newStatus === 'Reprovado') ? 'var(--red-dim)' : 'rgba(56,189,248,0.18)';
			        confirmBtn.style.color = (newStatus === 'Reprovado') ? 'var(--red)' : '#38bdf8';
			        confirmBtn.style.borderColor = (newStatus === 'Reprovado') ? 'var(--red)' : '#38bdf8';
			        confirmBtn.style.display = 'inline-block';
			        document.getElementById('motivo-leitura').style.display = 'none';
			        var txtArea = document.getElementById('motivo-texto');
			        txtArea.style.display = 'block';
			        txtArea.placeholder = (newStatus === 'Reprovado') ? 'Digite o motivo para reprovar este repasse...' : 'Digite a observação para validação...';
			        txtArea.value = item.motivo || '';
			        document.getElementById('modal-reprova').classList.add('show');
			        return;
			    }
			    item.status = newStatus;
			    item.motivo = '';
			    if (newStatus === 'Aprovado') {
			        if (!item.dataAprovacao) item.dataAprovacao = getNowFormatted();
			    } else {
			        item.dataAprovacao = '';
			    }
			    renderTable();
			    gravarEstadoSilencioso();
			}
			function lerMotivo(id) {
			    var item = rawData.find(function(r){return r.id===id;});
			    if (!item) return;
			    var titleEl = document.getElementById('modal-title');
			    titleEl.textContent = (item.status === 'Validando') ? 'Observação de Validação' : 'Motivo da Reprovação';
			    titleEl.style.color = (item.status === 'Validando') ? '#38bdf8' : 'var(--red)';
			    document.getElementById('motivo-texto').style.display = 'none';
			    document.getElementById('motivo-leitura').style.display = 'block';
			    document.getElementById('motivo-leitura').textContent = item.motivo || 'Nenhuma observação registrada.';
			    document.getElementById('btn-confirm-modal').style.display = 'none';
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
			    document.getElementById('view-nf-obs').textContent = item.obsNfCliente || 'Sem observação registrada.';
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
			        showToast('Necessário status Aprovado primeiro!');
			        renderTable();
			        return;
			    }
			    if (!item.nfCliente || item.nfCliente.trim() === '') {
			        showToast('Necessário preencher a NF Cliente primeiro!');
			        renderTable();
			        return;
			    }
			    var formatted = val;
			    if (val.indexOf('-') >= 0) {
			        var p = val.split('-');
			        formatted = p[2] + '/' + p[1] + '/' + p[0];
			    }
			    item.dataPgtoRepasse = formatted;
			    renderTable();
			    gravarEstadoSilencioso();
			    showToast('Data de pgto repasse salva!');
			}
			function abrirModalAlterarDataPgtoRep(id) {
			    itemSendoAlteradoPgtoRep = rawData.find(function(r){return r.id===id;});
			    if (!itemSendoAlteradoPgtoRep) return;
			    if (itemSendoAlteradoPgtoRep.status !== 'Aprovado' || !itemSendoAlteradoPgtoRep.nfCliente || itemSendoAlteradoPgtoRep.nfCliente.trim() === '') {
			        showToast('Necessário aprovação e NF preenchida!');
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
			    renderTable();
			    gravarEstadoSilencioso();
			    fecharModalPgtoRep();
			    showToast('Data de pgto repasse salva!');
			}
			function removerDataPgtoRep() {
			    if (!itemSendoAlteradoPgtoRep) return;
			    itemSendoAlteradoPgtoRep.dataPgtoRepasse = '';
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
			
			function getPayload() {
			    var payload = {};
			    for (var i = 0; i < rawData.length; i++) {
			        var r = rawData[i];
			        if (r.status !== 'Pendente' || (r.nfCliente && r.nfCliente.trim() !== '') || (r.obsNfCliente && r.obsNfCliente.trim() !== '') || (r.dataPgtoRepasse && r.dataPgtoRepasse.trim() !== '')) {
			            payload[String(r.id)] = {
			                status: r.status,
			                motivo: r.motivo || '',
			                nfCliente: r.nfCliente || '',
			                obsNfCliente: r.obsNfCliente || '',
			                dataAprovacao: r.dataAprovacao || '',
			                dataNfCliente: r.dataNfCliente || '',
			                dataPgtoRepasse: r.dataPgtoRepasse || ''
			            };
			        }
			    }
			    return payload;
			}

			function getPayload() {
			    var payload = {};
			    for (var i = 0; i < rawData.length; i++) {
			        var r = rawData[i];
			        if (r.status !== 'Pendente' || (r.nfCliente && r.nfCliente.trim() !== '') || (r.obsNfCliente && r.obsNfCliente.trim() !== '') || (r.dataPgtoRepasse && r.dataPgtoRepasse.trim() !== '')) {
			            payload[String(r.id)] = {
			                status: r.status,
			                motivo: r.motivo || '',
			                nfCliente: r.nfCliente || '',
			                obsNfCliente: r.obsNfCliente || '',
			                dataAprovacao: r.dataAprovacao || '',
			                dataNfCliente: r.dataNfCliente || '',
			                dataPgtoRepasse: r.dataPgtoRepasse || ''
			            };
			        }
			    }
			    return payload;
			}

			function gravarEstadoSilencioso() {
			    var payload = getPayload();
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
			    var payload = getPayload();
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
			            var btn = document.getElementById('btn-save');
			            if (btn) { btn.classList.remove('has-changes'); btn.textContent = 'GRAVAR'; }
			            showToast('Estado gravado com sucesso na nuvem!');
			        } else {
			            throw new Error('Falha HTTP ' + resp.status);
			        }
			    })
			    .catch(function(e) {
			        showToast('Gravado no cache local! (Nuvem indisponível)');
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
			    var el = document.createElement('textarea');
			    el.value = tsv;
			    document.body.appendChild(el);
			    el.select();
			    try {
			        document.execCommand('copy');
			        showToast('Tabela copiada! Cole no Excel (Ctrl+V)');
			    } catch(e) {
			        showToast('Erro ao copiar');
			    }
			    document.body.removeChild(el);
			}
			function showToast(msg) {
			    var t = document.getElementById('toast');
			    t.textContent = msg;
			    t.classList.add('show');
			    setTimeout(function(){ t.classList.remove('show'); }, 2500);
			}
			function updateCards(filteredList) {
			    var list = filteredList || rawData;
			    var totalRecebidoFiltered = 0;
			    var totalRepasseFiltered = 0;
			    var totalAprovadosVal = 0;
			    var totalAprovadosComNfVal = 0;
			    var distinctUnidades = {};
			    for (var i=0; i<list.length; i++) {
			        var it = list[i];
			        totalRecebidoFiltered += (it.valor || 0);
			        totalRepasseFiltered += (it.valorUnit || 0);
			        if (it.unidade && it.unidade.trim() !== '') distinctUnidades[it.unidade] = true;
			        if (it.status === 'Aprovado') {
			            totalAprovadosVal += (it.valorUnit || 0);
			            if (it.nfCliente && it.nfCliente.trim() !== '') {
			                totalAprovadosComNfVal += (it.valorUnit || 0);
			            }
			        }
			    }
			    var countUnidadesFiltered = Object.keys(distinctUnidades).length;
			    var faltaAprovarVal = totalRepasseFiltered - totalAprovadosVal;
			    if (faltaAprovarVal < 0) faltaAprovarVal = 0;
			    var faltaNfVal = totalAprovadosVal - totalAprovadosComNfVal;
			    if (faltaNfVal < 0) faltaNfVal = 0;
			    var elRec = document.getElementById('card-total-recebido');
			    if (elRec) elRec.innerHTML = '<span class=""currency"">R$</span>' + fmtBRL(totalRecebidoFiltered).replace('R$ ', '');
			    var elRecSub = document.getElementById('card-total-recebido-sub');
			    if (elRecSub) elRecSub.innerHTML = list.length + ' clientes filtrados';
			    var elRep = document.getElementById('card-total-repasse');
			    if (elRep) elRep.innerHTML = '<span class=""currency"">R$</span>' + fmtBRL(totalRepasseFiltered).replace('R$ ', '');
			    var elRepSub = document.getElementById('card-total-repasse-sub');
			    if (elRepSub) elRepSub.innerHTML = countUnidadesFiltered + ' unidades distintas';
			    var pct = totalRepasseFiltered > 0 ? Math.round((totalAprovadosVal / totalRepasseFiltered) * 100) : 0;
			    var elApp = document.getElementById('approved-count');
			    if (elApp) elApp.innerHTML = '<span class=""currency"">R$</span>' + fmtBRL(totalAprovadosVal).replace('R$ ', '') + ' <span style=""font-size:14px;color:var(--text-muted);font-weight:600;"">(' + pct + '%)</span>';
			    var elAppPct = document.getElementById('approved-pct');
			    if (elAppPct) elAppPct.innerHTML = '<span style=""color:#ffb74d; font-weight:700; font-size:13px;"">Falta ' + fmtBRL(faltaAprovarVal) + ' para aprovar</span>';
			    var card = document.getElementById('card-approved');
			    if (card) {
			        if (pct === 100) card.style.borderColor = 'var(--green)';
			        else if (pct > 0) card.style.borderColor = '#ff9100';
			        else card.style.borderColor = 'var(--border)';
			    }
			    var pctNf = totalAprovadosVal > 0 ? Math.round((totalAprovadosComNfVal / totalAprovadosVal) * 100) : 0;
			    var elNfVal = document.getElementById('card-app-nf-val');
			    if (elNfVal) elNfVal.innerHTML = '<span class=""currency"">R$</span>' + fmtBRL(totalAprovadosComNfVal).replace('R$ ', '') + ' <span style=""font-size:14px;color:var(--text-muted);font-weight:600;"">(' + pctNf + '%)</span>';
			    var elNfSub = document.getElementById('card-app-nf-sub');
			    if (elNfSub) elNfSub.innerHTML = '<span style=""color:#ffb74d; font-weight:700; font-size:13px;"">Falta NF: ' + fmtBRL(faltaNfVal) + '</span>';
			    var cardNf = document.getElementById('card-approved-nf');
			    if (cardNf) {
			        if (pctNf === 100 && totalAprovadosVal > 0) cardNf.style.borderColor = 'var(--green)';
			        else if (pctNf > 0) cardNf.style.borderColor = '#ff9100';
			        else cardNf.style.borderColor = 'var(--border)';
			    }
			}
			function setFilter(btn, f) {
			    currentFilter = f;
			    document.querySelectorAll('.filter-btn').forEach(function(b){b.classList.remove('active');});
			    btn.classList.add('active');
			    renderTable();
			}
			function filterTable() { renderTable(); }
			function sortBy(key) {
			    if (currentSort.key === key) currentSort.asc = !currentSort.asc;
			    else { currentSort.key = key; currentSort.asc = true; }
			    renderTable();
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
			    var isDateCol = (currentSort.key === 'dataPagamento' || currentSort.key === 'dataAprovacao' || currentSort.key === 'dataNfCliente' || currentSort.key === 'dataCadastro' || currentSort.key === 'dataPgtoRepasse');
			    data.sort(function(a,b) {
			        if (isDateCol) {
			            var vDa = toDateNum(a[currentSort.key]), vDb = toDateNum(b[currentSort.key]);
			            if (vDa !== vDb) return currentSort.asc ? (vDa - vDb) : (vDb - vDa);
			        }
			        var va=a[currentSort.key], vb=b[currentSort.key];
			        if (typeof va==='string'){va=va.toLowerCase();vb=vb.toLowerCase();}
			        if (va<vb) return currentSort.asc?-1:1;
			        if (va>vb) return currentSort.asc?1:-1;
			        return 0;
			    });
			    var html = '', sumVal = 0, sumUnit = 0, sumRetencao = 0;
			    for (var i=0; i<data.length; i++) {
			        var r = data[i], st = r.status || 'Pendente', pH = r.percHonorario;
			        sumVal += (r.valor || 0);
			        if (r.valorUnit) sumUnit += r.valorUnit;
			        if (r.valorRetencao) sumRetencao += r.valorRetencao;
			
			        var isAprovado = (st === 'Aprovado');
			        var hasNf = (r.nfCliente && String(r.nfCliente).trim() !== '');
			
			        // Rule 1: NF only enabled if approved
			        var nfCliHtml = '';
			        if (!isAprovado) {
			            if (hasNf) {
			                nfCliHtml = '<span style=""color:var(--text-muted);font-family:Consolas,monospace;font-size:12px;"">' + r.nfCliente + '</span>';
			            } else {
			                nfCliHtml = '<span style=""color:var(--text-dim);font-size:12px;cursor:not-allowed;"" title=""Necessário status Aprovado para preencher a NF"">-</span>';
			            }
			        } else {
			            var nfTitle = r.dataNfCliente ? ('Preenchido em: ' + r.dataNfCliente) : '';
			            if (hasNf) {
			                var obsBtnHtml = r.obsNfCliente ? '<button class=""btn-view-obs"" onclick=""abrirModalVerObsNf(\'' + r.id + '\')"" title=""Ver observação""><svg width=""13"" height=""13"" viewBox=""0 0 24 24"" fill=""none"" stroke=""currentColor"" stroke-width=""2"" stroke-linecap=""round"" stroke-linejoin=""round""><path d=""M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z""></path></svg></button>' : '';
			                nfCliHtml = '<div class=""nf-cliente-box"" title=""' + nfTitle + '""><span class=""nf-cliente-text"">' + r.nfCliente + '</span><button class=""btn-edit-nf"" onclick=""abrirModalAlterarNf(\'' + r.id + '\')"" title=""Alterar NF""><svg width=""12"" height=""12"" viewBox=""0 0 24 24"" fill=""none"" stroke=""currentColor"" stroke-width=""2"" stroke-linecap=""round"" stroke-linejoin=""round""><path d=""M17 3a2.828 2.828 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5L17 3z""></path></svg></button>' + obsBtnHtml + '</div>';
			            } else {
			                nfCliHtml = '<input type=""text"" id=""inp-nf-' + r.id + '"" class=""input-nf-cliente"" placeholder=""Inserir NF..."" value="""" onkeydown=""if(event.key===\'Enter\') salvarNfInicial(\'' + r.id + '\', this.value)"" onblur=""salvarNfInicial(\'' + r.id + '\', this.value)"">';
			            }
			        }
			
			        // Rule 2: Data Pgto Repasse only enabled if NF is filled (and Approved)
			        var dataPgtoRepDisplay = '';
			        if (!isAprovado || !hasNf) {
			            if (r.dataPgtoRepasse) {
			                dataPgtoRepDisplay = '<span style=""color:var(--text-muted);font-size:12px;"">' + r.dataPgtoRepasse + '</span>';
			            } else {
			                dataPgtoRepDisplay = '<span style=""color:var(--text-dim);font-size:12px;cursor:not-allowed;"" title=""Necessário NF preenchida para informar Data de Pgto do Repasse"">-</span>';
			            }
			        } else {
			            if (r.dataPgtoRepasse) {
			                dataPgtoRepDisplay = '<div class=""data-pgto-box""><span style=""color:#38bdf8;font-size:12px;font-weight:700;"">' + r.dataPgtoRepasse + '</span><button class=""btn-edit-nf"" onclick=""abrirModalAlterarDataPgtoRep(\'' + r.id + '\')"" title=""Alterar Data Pgto""><svg width=""11"" height=""11"" viewBox=""0 0 24 24"" fill=""none"" stroke=""currentColor"" stroke-width=""2"" stroke-linecap=""round"" stroke-linejoin=""round""><path d=""M17 3a2.828 2.828 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5L17 3z""></path></svg></button></div>';
			            } else {
			                dataPgtoRepDisplay = '<input type=""date"" id=""inp-dtpgto-' + r.id + '"" class=""input-data-pgto-cell"" onchange=""salvarDataPgtoRepasseDirect(\'' + r.id + '\', this.value)"" title=""Definir data do pagamento do repasse"">';
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
			        html += '<td style=""color:var(--text-main);text-align:center;font-weight:600;cursor:help;"" onmouseenter=""showTooltip(event, \'Grossup\', \'O contrato de JOB veio com a cláusula de Grossup.\')"" onmousemove=""moveTooltip(event)"" onmouseleave=""hideTooltip()"">' + (r.grossup||'-') + '</td>';
			        html += '<td style=""color:var(--text-main);text-align:center;font-weight:600;cursor:help;"" onmouseenter=""showTooltip(event, \'Imposto Franq.\', \'Descontar o Grossup do franqueado.\')"" onmousemove=""moveTooltip(event)"" onmouseleave=""hideTooltip()"">' + (r.imposto||'-') + '</td>';
			        html += '<td class=""num"" style=""color:var(--text-main);font-weight:600"">' + (r.retencao ? String(r.retencao).replace('.', ',')+'%' : '0,00%') + '</td>';
			        html += '<td class=""num"" style=""color:var(--text-main)"">' + (r.valorRetencao ? fmtBRL(r.valorRetencao) : '-') + '</td>';
			        html += '<td class=""num"" style=""color:var(--text-main);font-weight:600;"">' + (pH ? String(pH).replace('.', ',')+'%' : '0,00%') + '</td>';
			        html += '<td class=""num"" style=""color:var(--text-main)"">' + (r.valorUnit ? fmtBRL(r.valorUnit) : '-') + '</td>';
			        html += '<td class=""num"">' + aprovDisplay + '</td>';
			        html += '<td class=""num"">' + dataPgtoRepDisplay + '</td>';
			        html += '<td class=""num""><div class=""status-btn-group"">';
			        html += '<div class=""status-btn ' + (st==='Pendente'?'active-p':'') + '"" title=""Pendente"" onclick=""setStatus(\'' + r.id + '\',\'Pendente\')"">P</div>';
			        html += '<div class=""status-btn ' + (st==='Validando'?'active-v':'') + '"" title=""Validando"" onclick=""setStatus(\'' + r.id + '\',\'Validando\')"">V</div>';
			        html += '<div class=""status-btn ' + (st==='Aprovado'?'active-a':'') + '"" title=""Aprovado"" onclick=""setStatus(\'' + r.id + '\',\'Aprovado\')"">A</div>';
			        html += '<div class=""status-btn ' + (st==='Reprovado'?'active-r':'') + '"" title=""Reprovado"" onclick=""setStatus(\'' + r.id + '\',\'Reprovado\')"">R</div>';
			        if ((st==='Reprovado' || st==='Validando') && r.motivo) html += '<span class=""icon-eye"" title=""Ver motivo / observação"" onclick=""lerMotivo(\'' + r.id + '\')""><svg width=""14"" height=""14"" viewBox=""0 0 24 24"" fill=""none"" stroke=""currentColor"" stroke-width=""2"" stroke-linecap=""round"" stroke-linejoin=""round""><path d=""M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z""></path><circle cx=""12"" cy=""12"" r=""3""></circle></svg></span>';
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
			</script>"
			
			RETURN _css & _body & _js
			
			```
		lineageTag: f5ff111c-f3d9-461a-81fb-597f48addb01

	column col
		lineageTag: 5af7799e-1e35-4aac-b64d-749884b212e9
		isNameInferred
		sourceColumn: [col]

	partition medidas_html = calculated
		source = ROW("col", 1)


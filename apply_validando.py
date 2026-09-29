import json

# Read current file
with open('Painel_Repasses_dax.txt', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update CSS: add .status-btn.active-v and refine .icon-eye
css_old = ".status-btn.active-p{background:rgba(255,145,0,0.15);border-color:#ff9100;color:#ff9100;}\n.status-btn.active-a{background:var(--green-dim);border-color:var(--green);color:var(--green);}\n.status-btn.active-r{background:var(--red-dim);border-color:var(--red);color:var(--red);}\n.btn-lock{padding:6px 14px;border-radius:8px;border:1px solid var(--border);background:transparent;color:var(--text-muted);font-size:14px;font-weight:700;cursor:pointer;transition:all 0.2s;margin-left:12px;}\n.btn-lock:hover{border-color:var(--gold);color:var(--gold);}\n.btn-lock.unlocked{color:var(--green);border-color:var(--green);}\n.icon-eye{cursor:pointer;opacity:0.6;transition:opacity 0.2s;margin-left:6px;font-size:17px;}\n.icon-eye:hover{opacity:1;transform:scale(1.1);}"

css_new = """.status-btn.active-p{background:rgba(255,145,0,0.15);border-color:#ff9100;color:#ff9100;}
.status-btn.active-v{background:rgba(56,189,248,0.18);border-color:#38bdf8;color:#38bdf8;}
.status-btn.active-a{background:var(--green-dim);border-color:var(--green);color:var(--green);}
.status-btn.active-r{background:var(--red-dim);border-color:var(--red);color:var(--red);}
.btn-lock{padding:6px 14px;border-radius:8px;border:1px solid var(--border);background:transparent;color:var(--text-muted);font-size:14px;font-weight:700;cursor:pointer;transition:all 0.2s;margin-left:12px;}
.btn-lock:hover{border-color:var(--gold);color:var(--gold);}\n.btn-lock.unlocked{color:var(--green);border-color:var(--green);}
.icon-eye{cursor:pointer;opacity:0.8;transition:all 0.2s;margin-left:4px;color:var(--gold-bright);display:inline-flex;align-items:center;padding:2px;border-radius:4px;}
.icon-eye:hover{opacity:1;transform:scale(1.2);color:#fff;background:rgba(255,215,0,0.15);}"""

assert css_old in content, "Could not find css_old"
content = content.replace(css_old, css_new, 1)

# 2. Update Filter Buttons: Add Validando
btn_old = """        <button class='filter-btn active' onclick='setFilter(this,""all"")'>Todos</button>
        <button class='filter-btn' onclick='setFilter(this,""approved"")'>Aprovados</button>
        <button class='filter-btn' onclick='setFilter(this,""pending"")'>Pendentes</button>
        <button class='filter-btn' onclick='setFilter(this,""rejected"")'>Reprovados</button>"""

btn_new = """        <button class='filter-btn active' onclick='setFilter(this,""all"")'>Todos</button>
        <button class='filter-btn' onclick='setFilter(this,""approved"")'>Aprovados</button>
        <button class='filter-btn' onclick='setFilter(this,""validating"")'>Validando</button>
        <button class='filter-btn' onclick='setFilter(this,""pending"")'>Pendentes</button>
        <button class='filter-btn' onclick='setFilter(this,""rejected"")'>Reprovados</button>"""

assert btn_old in content, "Could not find btn_old"
content = content.replace(btn_old, btn_new, 1)

# 3. Update Modal HTML
modal_old = """<div class='modal-overlay' id='modal-reprova'>
    <div class='modal'>
        <div class='modal-title' id='modal-title'>Motivo da Reprovacao</div>
        <div id='motivo-leitura' style='display:none; font-size: 16px; color:var(--text-main); margin-bottom:16px; background:var(--bg-dark); padding:12px; border-radius:8px; border:1px solid var(--border); min-height:80px;'></div>
        <textarea id='motivo-texto' placeholder='Digite o motivo para reprovar este repasse...'></textarea>
        <div class='modal-actions'>
            <button class='modal-btn cancel' onclick='fecharModal()'>Fechar</button>
            <button class='modal-btn confirm' id='btn-confirm-modal' onclick='confirmarReprova()'>Reprovar</button>
        </div>
    </div>
</div>"""

modal_new = """<div class='modal-overlay' id='modal-reprova'>
    <div class='modal'>
        <div class='modal-title' id='modal-title'>Motivo da Reprovação</div>
        <div id='motivo-leitura' style='display:none; font-size: 14px; color:var(--text-main); margin-bottom:16px; background:var(--bg-dark); padding:12px; border-radius:8px; border:1px solid var(--border); min-height:80px; max-height:160px; overflow-y:auto; word-break:break-word;'></div>
        <textarea id='motivo-texto' placeholder='Digite a observação...'></textarea>
        <div class='modal-actions'>
            <button class='modal-btn cancel' onclick='fecharModal()'>Fechar</button>
            <button class='modal-btn confirm' id='btn-confirm-modal' onclick='confirmarObservacaoStatus()'>Confirmar</button>
        </div>
    </div>
</div>"""

assert modal_old in content, "Could not find modal_old"
content = content.replace(modal_old, modal_new, 1)

# 4. Update JS variables & setStatus / lerMotivo / fecharModal / confirmarReprova
js_old = """var currentFilter = 'all';
var currentSort = {key:'nome', asc:true};
var hasUnsaved = false, isUnlocked = false, itemSendoAlteradoNf = null, itemSendoReprovado = null;"""

js_new = """var currentFilter = 'all';
var currentSort = {key:'nome', asc:true};
var hasUnsaved = false, isUnlocked = false, itemSendoAlteradoNf = null, itemSendoObservado = null, statusSendoDefinido = null;"""

assert js_old in content, "Could not find js_old"
content = content.replace(js_old, js_new, 1)

fn_old = """function setStatus(id, newStatus) {
    if (!isUnlocked) { showToast('Clique em Desbloquear para editar!'); return; }
    var items = rawData.filter(function(r){return r.id===id;});
    if (items.length === 0) return;
    if (newStatus === 'Reprovado') {
        itemSendoReprovado = items[0];
        document.getElementById('modal-title').textContent = 'Motivo da Reprovacao';
        document.getElementById('motivo-leitura').style.display = 'none';
        document.getElementById('motivo-texto').style.display = 'block';
        document.getElementById('motivo-texto').value = itemSendoReprovado.motivo || '';
        document.getElementById('btn-confirm-modal').style.display = 'inline-block';
        document.getElementById('modal-reprova').classList.add('show');
        return;
    }
    items.forEach(function(item) {
        item.status = newStatus; item.motivo = '';
        if (newStatus === 'Aprovado') { if (!item.dataAprovacao) item.dataAprovacao = getNowFormatted(); }
        else { item.dataAprovacao = ''; }
    });
    markUnsaved();
}
function lerMotivo(id) {
    var item = rawData.find(function(r){return r.id===id;});
    if (!item) return;
    document.getElementById('modal-title').textContent = 'Motivo Registrado';
    document.getElementById('motivo-texto').style.display = 'none';
    document.getElementById('motivo-leitura').style.display = 'block';
    document.getElementById('motivo-leitura').textContent = item.motivo || 'Nenhum motivo registrado.';
    document.getElementById('btn-confirm-modal').style.display = 'none';
    document.getElementById('modal-reprova').classList.add('show');
}
function fecharModal() { document.getElementById('modal-reprova').classList.remove('show'); itemSendoReprovado = null; }
function confirmarReprova() {
    if (itemSendoReprovado) {
        var items = rawData.filter(function(r){return r.id===itemSendoReprovado.id;});
        var m = document.getElementById('motivo-texto').value;
        items.forEach(function(item) { item.status = 'Reprovado'; item.motivo = m; item.dataAprovacao = ''; });
        markUnsaved();
    }
    fecharModal();
}"""

fn_new = """function setStatus(id, newStatus) {
    if (!isUnlocked) { showToast('Clique em Desbloquear para editar!'); return; }
    var items = rawData.filter(function(r){return r.id===id;});
    if (items.length === 0) return;
    if (newStatus === 'Reprovado' || newStatus === 'Validando') {
        itemSendoObservado = items[0];
        statusSendoDefinido = newStatus;
        var isRep = (newStatus === 'Reprovado');
        document.getElementById('modal-title').textContent = isRep ? 'Motivo da Reprovação' : 'Observação de Validação';
        document.getElementById('modal-title').style.color = isRep ? 'var(--red)' : '#38bdf8';
        document.getElementById('motivo-leitura').style.display = 'none';
        document.getElementById('motivo-texto').style.display = 'block';
        document.getElementById('motivo-texto').placeholder = isRep ? 'Digite o motivo para reprovar este repasse...' : 'Digite a observação para colocar em validação...';
        document.getElementById('motivo-texto').value = itemSendoObservado.motivo || '';
        document.getElementById('btn-confirm-modal').textContent = isRep ? 'Reprovar' : 'Colocar em Validação';
        document.getElementById('btn-confirm-modal').style.background = isRep ? 'var(--red-dim)' : 'rgba(56,189,248,0.15)';
        document.getElementById('btn-confirm-modal').style.color = isRep ? 'var(--red)' : '#38bdf8';
        document.getElementById('btn-confirm-modal').style.borderColor = isRep ? 'var(--red)' : '#38bdf8';
        document.getElementById('btn-confirm-modal').style.display = 'inline-block';
        document.getElementById('modal-reprova').classList.add('show');
        setTimeout(function(){ document.getElementById('motivo-texto').focus(); }, 100);
        return;
    }
    items.forEach(function(item) {
        item.status = newStatus; item.motivo = '';
        if (newStatus === 'Aprovado') { if (!item.dataAprovacao) item.dataAprovacao = getNowFormatted(); }
        else { item.dataAprovacao = ''; }
    });
    markUnsaved();
}
function lerMotivo(id) {
    var item = rawData.find(function(r){return r.id===id;});
    if (!item) return;
    var isRep = (item.status === 'Reprovado');
    document.getElementById('modal-title').textContent = isRep ? 'Motivo da Reprovação' : 'Observação de Validação';
    document.getElementById('modal-title').style.color = isRep ? 'var(--red)' : '#38bdf8';
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
        var items = rawData.filter(function(r){return r.id===itemSendoObservado.id;});
        var m = document.getElementById('motivo-texto').value;
        items.forEach(function(item) {
            item.status = statusSendoDefinido;
            item.motivo = m;
            item.dataAprovacao = '';
        });
        markUnsaved();
    }
    fecharModal();
}"""

assert fn_old in content, "Could not find fn_old"
content = content.replace(fn_old, fn_new, 1)

# 5. Update copyToExcel filter
copy_old = "var mf = currentFilter==='all' || (currentFilter==='approved' && r.status==='Aprovado') || (currentFilter==='pending' && r.status==='Pendente') || (currentFilter==='rejected' && r.status==='Reprovado');"
copy_new = "var mf = currentFilter==='all' || (currentFilter==='approved' && r.status==='Aprovado') || (currentFilter==='validating' && r.status==='Validando') || (currentFilter==='pending' && r.status==='Pendente') || (currentFilter==='rejected' && r.status==='Reprovado');"

assert copy_old in content, "Could not find copy_old"
content = content.replace(copy_old, copy_new, 2) # used in copyToExcel and renderTable

# 6. Update row rendering for status buttons and eye icon
row_old = """        html+='<td class=""num""><div class=""status-btn-group"">';
        html+='<div class=""status-btn '+(st==='Pendente'?'active-p':'')+'"" title=""Pendente"" onclick=""setStatus(\\''+r.id+'\\',\\'Pendente\\')"">P</div>';
        html+='<div class=""status-btn '+(st==='Aprovado'?'active-a':'')+'"" title=""Aprovado"" onclick=""setStatus(\\''+r.id+'\\',\\'Aprovado\\')"">A</div>';
        html+='<div class=""status-btn '+(st==='Reprovado'?'active-r':'')+'"" title=""Reprovado"" onclick=""setStatus(\\''+r.id+'\\',\\'Reprovado\\')"">R</div>';
        if (st==='Reprovado' && r.motivo) html+='<span class=""icon-eye"" title=""Ver motivo"" onclick=""lerMotivo(\\''+r.id+'\\')"">Ver</span>';
        html+='</div></td></tr>';"""

row_new = """        html+='<td class=""num""><div class=""status-btn-group"">';
        html+='<div class=""status-btn '+(st==='Pendente'?'active-p':'')+'"" title=""Pendente"" onclick=""setStatus(\\''+r.id+'\\',\\'Pendente\\')"">P</div>';
        html+='<div class=""status-btn '+(st==='Validando'?'active-v':'')+'"" title=""Validando"" onclick=""setStatus(\\''+r.id+'\\',\\'Validando\\')"">V</div>';
        html+='<div class=""status-btn '+(st==='Aprovado'?'active-a':'')+'"" title=""Aprovado"" onclick=""setStatus(\\''+r.id+'\\',\\'Aprovado\\')"">A</div>';
        html+='<div class=""status-btn '+(st==='Reprovado'?'active-r':'')+'"" title=""Reprovado"" onclick=""setStatus(\\''+r.id+'\\',\\'Reprovado\\')"">R</div>';
        if ((st==='Reprovado' || st==='Validando') && r.motivo) html+='<span class=""icon-eye"" title=""Ver motivo / observação"" onclick=""lerMotivo(\\''+r.id+'\\')""><svg width=""14"" height=""14"" viewBox=""0 0 24 24"" fill=""none"" stroke=""currentColor"" stroke-width=""2"" stroke-linecap=""round"" stroke-linejoin=""round""><path d=""M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z""></path><circle cx=""12"" cy=""12"" r=""3""></circle></svg></span>';
        html+='</div></td></tr>';"""

assert row_old in content, "Could not find row_old"
content = content.replace(row_old, row_new, 1)

# Write back
with open('Painel_Repasses_dax.txt', 'w', encoding='utf-8') as f:
    f.write(content)

print("Painel_Repasses_dax.txt successfully updated! Length:", len(content))

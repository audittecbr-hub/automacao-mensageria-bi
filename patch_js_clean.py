import re

file_path = r'C:\Users\cristhofer.maciel.GRUPOSTUDIO\Desktop\HTML_Detalhamento_Aprovados_Corrigido.dax'
with open(file_path, 'r', encoding='utf8') as f:
    dax = f.read()

# Let's completely overwrite the JS functions block to be safe.
# Find where the bad block starts
start_idx = dax.find('function toggleDropdown(id) {')

# Find where it ends
end_idx = dax.find('function popularProdutos() {')

if start_idx != -1 and end_idx != -1:
    old_js = dax[start_idx:end_idx]
    
    clean_js = '''function toggleDropdown(id) {
    var m = document.getElementById(id);
    if(m.classList.contains('show')) m.classList.remove('show'); else { document.querySelectorAll('.dropdown-menu').forEach(el=>el.classList.remove('show')); m.classList.add('show'); }
}
function toggleAll(tipo, source) {
    var cbs = document.querySelectorAll('.mes-' + tipo + '-cb');
    cbs.forEach(cb => cb.checked = source.checked);
    atualizarMesBtnText(tipo);
}
function atualizarMesBtnText(tipo) {
    var cbs = document.querySelectorAll('.mes-' + tipo + '-cb');
    var checked = document.querySelectorAll('.mes-' + tipo + '-cb:checked');
    var btnText = 'TODOS';
    if(checked.length === 0) btnText = 'NENHUM';
    else if(checked.length < cbs.length) btnText = checked.length + ' MESES';
    document.getElementById(tipo + 'BtnText').innerText = btnText;
    var allCb = document.getElementById('selectAll' + (tipo === 'rt' ? 'Rt' : 'Mov'));
    if(allCb) allCb.checked = (checked.length === cbs.length);
}
document.addEventListener('click', function(e) {
    if (!e.target.closest('.dropdown-container')) {
        document.querySelectorAll('.dropdown-menu').forEach(el=>el.classList.remove('show'));
    }
});
'''
    dax = dax.replace(old_js, clean_js)

with open(file_path, 'w', encoding='utf8') as f:
    f.write(dax)

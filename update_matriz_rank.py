with open('matriz_current.dax', 'r', encoding='utf-8') as f:
    dax = f.read()

# 1. Update header label from "Pontuação por Ranking" to "Ranking das Regionais"
dax = dax.replace("<th>Pontuação por Ranking</th>", "<th>Ranking das Regionais</th>")
dax = dax.replace("<th>Pontuao por Ranking</th>", "<th>Ranking das Regionais</th>")

# 2. Update initial placeholders from '0 pts' to 'R$ 0,00'
dax = dax.replace("0 pts", "R$ 0,00")

# 3. Update legend line if needed
dax = dax.replace("Legenda de Pontuação:", "Detalhamento das Formas:")
dax = dax.replace("Legenda de Pontuao:", "Detalhamento das Formas:")
dax = dax.replace(" = <b style='color:var(--accent);'>4</b>", "")
dax = dax.replace(" = <b style='color:var(--accent);'>3</b>", "")
dax = dax.replace(" = <b style='color:var(--accent);'>2</b>", "")
dax = dax.replace(" = <b style='color:var(--accent);'>1</b>", "")

# 4. Update the ranking logic in JS
old_js_rank = """        /* CALCULAR PONTUAÇÃO E ORDENAÇÃO SEGURO SEM AFETAR A LEGENDA */
        var ptsSul = tSul * 2;
        var ptsSP = tSP * 2;
        var ptsSD = tSD * 2;
        var ptsNN = tNN * 2;

        var ranks = [
            { id: 'sul', pts: ptsSul },
            { id: 'sp', pts: ptsSP },
            { id: 'sd', pts: ptsSD },
            { id: 'nn', pts: ptsNN }
        ];
        ranks.sort(function(a, b) { return b.pts - a.pts; });
        
        for(var i=0; i<ranks.length; i++){
            var r = ranks[i];
            var elBadge = document.getElementById('badge-' + r.id);
            var elPts = document.getElementById('pts-' + r.id);
            if(elBadge) elBadge.innerText = (i+1) + 'º';
            if(elPts) elPts.innerText = r.pts.toLocaleString('pt-BR', {minimumFractionDigits:2, maximumFractionDigits:2}) + ' pts';
        }"""

new_js_rank = """        /* CALCULAR RANKING POR TOTAL DE HONORÁRIOS APROVADOS */
        var ranks = [
            { id: 'sul', val: tSul },
            { id: 'sp', val: tSP },
            { id: 'sd', val: tSD },
            { id: 'nn', val: tNN }
        ];
        ranks.sort(function(a, b) { return b.val - a.val; });
        
        for(var i=0; i<ranks.length; i++){
            var r = ranks[i];
            var elBadge = document.getElementById('badge-' + r.id);
            var elPts = document.getElementById('pts-' + r.id);
            if(elBadge) elBadge.innerText = (i+1) + 'º';
            if(elPts) elPts.innerText = formatarMilhoes(r.val);
        }"""

if old_js_rank in dax:
    dax = dax.replace(old_js_rank, new_js_rank)
    print("Replaced exact old_js_rank block!")
else:
    print("Exact block not found, searching via regex/substring...")
    import re
    # Let's find "CALCULAR PONTUA" block
    start_pos = dax.find("/* CALCULAR PONTUA")
    end_pos = dax.find("var table = document.querySelector('.tabela');")
    if start_pos != -1 and end_pos != -1:
        dax = dax[:start_pos] + new_js_rank + "\n\n        " + dax[end_pos:]
        print("Replaced using position slicing!")

with open('matriz_updated.dax', 'w', encoding='utf-8') as f:
    f.write(dax)

print("Saved matriz_updated.dax successfully")

const fs = require('fs');

const template = fs.readFileSync('HTML_Detalhamento_Encontrados_current.dax', 'utf8');

let apnegDax = template;

apnegDax = apnegDax.replace("DETALHAMENTO <span>HONORÁRIOS ENCONTRADOS</span>", "DETALHAMENTO <span>HONORÁRIOS APROVADOS EM NEGOCIAÇÃO</span>");
apnegDax = apnegDax.replace("var tipoFixo = 'Encontrado';", "var tipoFixo = 'Aprov. Negociação';");
apnegDax = apnegDax.replace("<option value='encontrado'>Encontrado</option>", "<option value='aprov. negociação'>Aprov. Negociação</option>");

const filterEncontrados = `vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_ENCONTRADO] > 0 && 
            vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] >= DATE(2026, 6, 1) && 
            vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] <= DATE(2026, 12, 31)`;

const filterApneg = `SEARCH("NEGOCI", vw_powerbi_relatorio_aprovacao[AREA_ANTERIOR], 1, 0) > 0 &&
            (
                SEARCH("AJU", vw_powerbi_relatorio_aprovacao[AREA_ATUAL], 1, 0) > 0 ||
                SEARCH("COMP", vw_powerbi_relatorio_aprovacao[AREA_ATUAL], 1, 0) > 0 ||
                SEARCH("ENTR", vw_powerbi_relatorio_aprovacao[AREA_ATUAL], 1, 0) > 0 ||
                SEARCH("IMPL", vw_powerbi_relatorio_aprovacao[AREA_ATUAL], 1, 0) > 0 ||
                SEARCH("RETIF", vw_powerbi_relatorio_aprovacao[AREA_ATUAL], 1, 0) > 0
            ) &&
            (vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_HONORARIOS_INICIAIS] + 
             vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_COMPENSACAO] + 
             vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_RESTITUICAO] + 
             vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_AJUIZAMENTO]) > 0 && 
            vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] >= DATE(2026, 6, 1) && 
            vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] <= DATE(2026, 12, 31)`;

apnegDax = apnegDax.replace(filterEncontrados, filterApneg);

const valEncontrados = `FORMAT(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_ENCONTRADO], "0.00")`;
const valApneg = `FORMAT((vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_HONORARIOS_INICIAIS] + vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_COMPENSACAO] + vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_RESTITUICAO] + vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_AJUIZAMENTO]), "0.00")`;

apnegDax = apnegDax.replace(valEncontrados, valApneg);

fs.writeFileSync('HTML_Detalhamento_Aprovados_Negociacao.dax', apnegDax, 'utf8');
console.log('Saved HTML_Detalhamento_Aprovados_Negociacao.dax successfully');

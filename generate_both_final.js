const fs = require('fs');

// 1. Build HTML_Detalhamento_Aprovados
const template = fs.readFileSync('HTML_Detalhamento_Encontrados_current.dax', 'utf8');

let aprovadosDax = template;
aprovadosDax = aprovadosDax.replace("DETALHAMENTO <span>HONORÁRIOS ENCONTRADOS</span>", "DETALHAMENTO <span>HONORÁRIOS APROVADOS</span>");
aprovadosDax = aprovadosDax.replace("var tipoFixo = 'Encontrado';", "var tipoFixo = 'Aprovado';");
aprovadosDax = aprovadosDax.replace("<option value='encontrado'>Encontrado</option>", "<option value='aprovado'>Aprovado</option>");

const filterEncontrados = `vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_ENCONTRADO] > 0 && 
            vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] >= DATE(2026, 6, 1) && 
            vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] <= DATE(2026, 12, 31)`;

const filterAprovados = `(COALESCE(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_HONORARIOS_INICIAIS], 0) + 
             COALESCE(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_COMPENSACAO], 0) + 
             COALESCE(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_RESTITUICAO], 0) + 
             COALESCE(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_AJUIZAMENTO], 0)) > 0 && 
            vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] >= DATE(2026, 6, 1) && 
            vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] <= DATE(2026, 12, 31)`;

aprovadosDax = aprovadosDax.replace(filterEncontrados, filterAprovados);

const valEncontrados = `FORMAT(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_ENCONTRADO], "0.00")`;
const valAprovados = `FORMAT((COALESCE(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_HONORARIOS_INICIAIS], 0) + COALESCE(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_COMPENSACAO], 0) + COALESCE(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_RESTITUICAO], 0) + COALESCE(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_AJUIZAMENTO], 0)), "0.00")`;

aprovadosDax = aprovadosDax.replace(valEncontrados, valAprovados);
fs.writeFileSync('HTML_Detalhamento_Aprovados_final.dax', aprovadosDax, 'utf8');

// 2. Build HTML_Detalhamento_Aprovados_Negociacao
let apnegDax = template;
apnegDax = apnegDax.replace("DETALHAMENTO <span>HONORÁRIOS ENCONTRADOS</span>", "DETALHAMENTO <span>HONORÁRIOS APROVADOS EM NEGOCIAÇÃO</span>");
apnegDax = apnegDax.replace("var tipoFixo = 'Encontrado';", "var tipoFixo = 'Aprov. Negociação';");
apnegDax = apnegDax.replace("<option value='encontrado'>Encontrado</option>", "<option value='aprov. negociação'>Aprov. Negociação</option>");

const filterApneg = `SEARCH("NEGOCI", vw_powerbi_relatorio_aprovacao[AREA_ANTERIOR], 1, 0) > 0 &&
            (
                SEARCH("AJU", vw_powerbi_relatorio_aprovacao[AREA_ATUAL], 1, 0) > 0 ||
                SEARCH("COMP", vw_powerbi_relatorio_aprovacao[AREA_ATUAL], 1, 0) > 0 ||
                SEARCH("ENTR", vw_powerbi_relatorio_aprovacao[AREA_ATUAL], 1, 0) > 0 ||
                SEARCH("IMPL", vw_powerbi_relatorio_aprovacao[AREA_ATUAL], 1, 0) > 0 ||
                SEARCH("RETIF", vw_powerbi_relatorio_aprovacao[AREA_ATUAL], 1, 0) > 0
            ) &&
            (COALESCE(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_HONORARIOS_INICIAIS], 0) + 
             COALESCE(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_COMPENSACAO], 0) + 
             COALESCE(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_RESTITUICAO], 0) + 
             COALESCE(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_AJUIZAMENTO], 0)) > 0 && 
            vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] >= DATE(2026, 6, 1) && 
            vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] <= DATE(2026, 12, 31)`;

apnegDax = apnegDax.replace(filterEncontrados, filterApneg);
apnegDax = apnegDax.replace(valEncontrados, valAprovados);
fs.writeFileSync('HTML_Detalhamento_Aprovados_Negociacao_final.dax', apnegDax, 'utf8');

console.log('Saved both final detail DAX files successfully');

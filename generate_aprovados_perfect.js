import fs from 'fs';

// Read HTML_Detalhamento_Encontrados_current.dax as baseline
const template = fs.readFileSync('HTML_Detalhamento_Encontrados_current.dax', 'utf8');

// Replace Encontrados with Aprovados
let aprovadosDax = template;

aprovadosDax = aprovadosDax.replace("DETALHAMENTO <span>HONORÁRIOS ENCONTRADOS</span>", "DETALHAMENTO <span>HONORÁRIOS APROVADOS</span>");
aprovadosDax = aprovadosDax.replace("var tipoFixo = 'Encontrado';", "var tipoFixo = 'Aprovado';");
aprovadosDax = aprovadosDax.replace("<option value='encontrado'>Encontrado</option>", "<option value='aprovado'>Aprovado</option>");

// Filter logic for Aprovados
const filterEncontrados = `vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_ENCONTRADO] > 0 && 
            vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] >= DATE(2026, 6, 1) && 
            vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] <= DATE(2026, 12, 31)`;

const filterAprovados = `(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_HONORARIOS_INICIAIS] + 
             vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_COMPENSACAO] + 
             vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_RESTITUICAO] + 
             vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_AJUIZAMENTO]) > 0 && 
            vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] >= DATE(2026, 6, 1) && 
            vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] <= DATE(2026, 12, 31)`;

aprovadosDax = aprovadosDax.replace(filterEncontrados, filterAprovados);

const valEncontrados = `FORMAT(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_ENCONTRADO], "0.00")`;
const valAprovados = `FORMAT((vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_HONORARIOS_INICIAIS] + vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_COMPENSACAO] + vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_RESTITUICAO] + vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_AJUIZAMENTO]), "0.00")`;

aprovadosDax = aprovadosDax.replace(valEncontrados, valAprovados);

fs.writeFileSync('HTML_Detalhamento_Aprovados_perfect.dax', aprovadosDax, 'utf8');
console.log('Saved HTML_Detalhamento_Aprovados_perfect.dax successfully');

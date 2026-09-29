import json

# Read current expression from step 407 output
with open(r'C:\Users\cristhofer.maciel.GRUPOSTUDIO\.gemini\antigravity-ide\brain\b00fb22d-3e1a-40ec-91dd-e3e86e8dd8ce\.system_generated\steps\407\output.txt', 'r', encoding='utf-8') as f:
    data = json.load(f)

expr = data['results'][0]['data']['expression']
print('Original length:', len(expr))

# 1. Update curPercHonorario to prioritize percFromTable
old_perc = '''        VAR percFromJob = CALCULATE(MAX('vw_powerbi_job_repasse'[PERC_HONORARIOS_JOB]), FILTER('vw_powerbi_job_repasse', 'vw_powerbi_job_repasse'[JOB] = [JOB_VAL]))
        VAR percFromFranq = CALCULATE(MAX('vw_powerbi_job_repasse'[PERC_HONORARIOS_FRANQUEADO]), FILTER('vw_powerbi_job_repasse', 'vw_powerbi_job_repasse'[JOB] = [JOB_VAL]))
        VAR percFromFranq2 = CALCULATE(MAX('vw_powerbi_job_repasse'[PERC_FRANQUEADO]), FILTER('vw_powerbi_job_repasse', 'vw_powerbi_job_repasse'[JOB] = [JOB_VAL]))
        VAR percFromTable = CALCULATE(MAX('HonorariosPorJob'[honorario]), FILTER('HonorariosPorJob', 'HonorariosPorJob'[numero_contrato] = [JOB_VAL]))
        VAR curPercHonorario = IF(
            isBloqueado, 
            0, 
            COALESCE(
                IF(percFromFranq > 0, percFromFranq, BLANK()),
                IF(percFromFranq2 > 0, percFromFranq2, BLANK()),
                IF(percFromJob > 0, percFromJob, BLANK()), 
                IF(percFromTable > 0, percFromTable, BLANK()), 
                0
            )
        )'''

new_perc = '''        VAR percFromTable = CALCULATE(MAX('HonorariosPorJob'[honorario]), FILTER('HonorariosPorJob', 'HonorariosPorJob'[numero_contrato] = [JOB_VAL]))
        VAR percFromFranq = CALCULATE(MAX('vw_powerbi_job_repasse'[PERC_HONORARIOS_FRANQUEADO]), FILTER('vw_powerbi_job_repasse', 'vw_powerbi_job_repasse'[JOB] = [JOB_VAL]))
        VAR percFromFranq2 = CALCULATE(MAX('vw_powerbi_job_repasse'[PERC_FRANQUEADO]), FILTER('vw_powerbi_job_repasse', 'vw_powerbi_job_repasse'[JOB] = [JOB_VAL]))
        VAR percFromJob = CALCULATE(MAX('vw_powerbi_job_repasse'[PERC_HONORARIOS_JOB]), FILTER('vw_powerbi_job_repasse', 'vw_powerbi_job_repasse'[JOB] = [JOB_VAL]))
        VAR curPercHonorario = IF(
            isBloqueado, 
            0, 
            COALESCE(
                IF(percFromTable > 0, percFromTable, BLANK()),
                IF(percFromFranq > 0, percFromFranq, BLANK()),
                IF(percFromFranq2 > 0, percFromFranq2, BLANK()),
                IF(percFromJob > 0, percFromJob, BLANK()), 
                0
            )
        )'''

assert old_perc in expr, "old_perc not found"
expr = expr.replace(old_perc, new_perc)
print('Replaced curPercHonorario successfully!')

# 2. Update key generation functions
old_keys_code = '''function getCompositeKey(r) {
    if (!r) return '';
    var j = (r.job || '').trim();
    var n = (r.nf || '').trim();
    var b = (r.bandeira || '').trim();
    var c = (r.cnpj || '').trim();
    return (j + '___' + n + '___' + b + '___' + c).toLowerCase();
}'''

new_keys_code = '''function isValidKey(k) {
    if (!k) return false;
    var cleaned = k.replace(/[_]/g, '').trim();
    return cleaned.length > 0;
}

function getCompositeKey(r) {
    if (!r) return '';
    var j = (r.job || '').trim();
    var n = (r.nf || '').trim();
    var b = (r.bandeira || '').trim();
    var c = (r.cnpj || '').trim();
    var str = (j + '___' + n + '___' + b + '___' + c).toLowerCase();
    return isValidKey(str) ? str : '';
}

function getJobCnpjKey(r) {
    if (!r) return '';
    var j = (r.job || '').trim();
    var c = (r.cnpj || '').trim();
    if (!j && !c) return '';
    return ('jc___' + j + '___' + c).toLowerCase();
}'''

assert old_keys_code in expr, "old_keys_code not found"
expr = expr.replace(old_keys_code, new_keys_code)
print('Replaced keys functions successfully!')

# 3. Update applySavedMap
old_apply_code = '''function applySavedMap(map) {
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
}'''

new_apply_code = '''function applySavedMap(map) {
    if (!map) return;
    for (var k in map) {
        savedGlobalMap[k] = map[k];
    }
    for (var i = 0; i < rawData.length; i++) {
        var r = rawData[i];
        var idKey = String(r.id);
        var compKey = getCompositeKey(r);
        var jobCnpjKey = getJobCnpjKey(r);
        
        var saved = savedGlobalMap[idKey] || 
                    (compKey ? savedGlobalMap[compKey] : null) || 
                    (jobCnpjKey ? savedGlobalMap[jobCnpjKey] : null);
        
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
            if (idKey && idKey !== 'undefined' && idKey !== '') savedGlobalMap[idKey] = saved;
            if (compKey) savedGlobalMap[compKey] = saved;
            if (jobCnpjKey) savedGlobalMap[jobCnpjKey] = saved;
        } else if (!r.status || r.status === '') {
            r.status = 'Pendente';
        }
    }
    renderTable();
}'''

assert old_apply_code in expr, "old_apply_code not found"
expr = expr.replace(old_apply_code, new_apply_code)
print('Replaced applySavedMap successfully!')

# 4. Update updateItemInGlobalMap
old_update_code = '''function updateItemInGlobalMap(r) {
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
}'''

new_update_code = '''function updateItemInGlobalMap(r) {
    if (!r) return;
    var idKey = String(r.id);
    var compKey = getCompositeKey(r);
    var jobCnpjKey = getJobCnpjKey(r);
    
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
        if (idKey && idKey !== 'undefined' && idKey !== '') savedGlobalMap[idKey] = entry;
        if (compKey) savedGlobalMap[compKey] = entry;
        if (jobCnpjKey) savedGlobalMap[jobCnpjKey] = entry;
    } else {
        if (idKey) delete savedGlobalMap[idKey];
        if (compKey) delete savedGlobalMap[compKey];
        if (jobCnpjKey) delete savedGlobalMap[jobCnpjKey];
    }
}'''

assert old_update_code in expr, "old_update_code not found"
expr = expr.replace(old_update_code, new_update_code)
print('Replaced updateItemInGlobalMap successfully!')

# Write updated expression to file
out_file = r'c:\Users\cristhofer.maciel.GRUPOSTUDIO\.gemini\antigravity\scratch\automacao-mensageria-bi\updated_painel_repasses_expr.txt'
with open(out_file, 'w', encoding='utf-8') as f:
    f.write(expr)

print('Updated expression written to:', out_file)
print('New length:', len(expr))

css = """<style>
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif; }
  body, html { width: 100%; height: 100%; background-color: #070B14; color: #E2E8F0; overflow: hidden; }
  
  .onboarding-container {
    display: flex;
    flex-direction: column;
    height: 100vh;
    padding: 14px 16px;
    background: radial-gradient(circle at 50% 0%, #111A2E 0%, #070B14 100%);
    gap: 12px;
  }

  /* Controls Bar */
  .controls-bar {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: space-between;
    background: rgba(15, 23, 42, 0.85);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 10px;
    padding: 10px 16px;
    gap: 12px;
  }
  .search-group {
    display: flex;
    align-items: center;
    gap: 8px;
    flex: 1;
    max-width: 420px;
  }
  .global-search {
    width: 100%;
    background: #0B1120;
    border: 1px solid rgba(255, 255, 255, 0.14);
    border-radius: 6px;
    padding: 8px 14px;
    font-size: 13px;
    color: #F8FAFC;
    outline: none;
    transition: all 0.2s;
  }
  .global-search:focus {
    border-color: #38BDF8;
    box-shadow: 0 0 0 2px rgba(56, 189, 248, 0.2);
  }
  .controls-right {
    display: flex;
    align-items: center;
    gap: 10px;
  }
  .btn-copiar {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(16, 185, 129, 0.15);
    color: #34D399;
    border: 1px solid rgba(16, 185, 129, 0.35);
    padding: 7px 14px;
    border-radius: 6px;
    font-size: 12px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s;
    white-space: nowrap;
  }
  .btn-copiar:hover {
    background: rgba(16, 185, 129, 0.25);
    border-color: #10B981;
    color: #6EE7B7;
    box-shadow: 0 0 10px rgba(16, 185, 129, 0.25);
  }
  .btn-reset {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.12);
    color: #CBD5E1;
    padding: 7px 14px;
    border-radius: 6px;
    font-size: 12px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s;
  }
  .btn-reset:hover {
    background: rgba(239, 68, 68, 0.15);
    color: #FCA5A5;
    border-color: rgba(239, 68, 68, 0.3);
  }
  .counter-badge {
    font-size: 13px;
    color: #94A3B8;
  }
  .counter-badge span {
    font-weight: 700;
    color: #38BDF8;
  }

  /* Table Wrapper */
  .table-wrapper {
    flex: 1;
    overflow: auto;
    background: rgba(11, 17, 32, 0.6);
    border: 1px solid rgba(255, 255, 255, 0.07);
    border-radius: 10px;
    box-shadow: inset 0 2px 10px rgba(0,0,0,0.3);
  }
  .table-wrapper::-webkit-scrollbar {
    width: 6px;
    height: 6px;
  }
  .table-wrapper::-webkit-scrollbar-track {
    background: #070B14;
  }
  .table-wrapper::-webkit-scrollbar-thumb {
    background: #1E293B;
    border-radius: 4px;
  }
  .table-wrapper::-webkit-scrollbar-thumb:hover {
    background: #334155;
  }

  /* Table */
  table.exec-table {
    width: 100%;
    border-collapse: separate;
    border-spacing: 0;
    font-size: 13px;
    text-align: left;
    white-space: nowrap;
  }
  table.exec-table th {
    position: sticky;
    top: 0;
    background: #0F172A;
    color: #CBD5E1;
    padding: 9px 12px;
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.6px;
    border-bottom: 2px solid rgba(56, 189, 248, 0.35);
    z-index: 20;
    overflow: visible;
  }
  .th-header-cell {
    position: relative;
    display: flex;
    flex-direction: column;
    gap: 5px;
  }
  .th-title {
    display: flex;
    align-items: center;
    justify-content: space-between;
    cursor: pointer;
    user-select: none;
    font-size: 12px;
  }
  .th-title:hover {
    color: #38BDF8;
  }
  .th-search {
    width: 100%;
    background: #070B14;
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 4px;
    padding: 4px 8px;
    font-size: 11px;
    color: #F1F5F9;
    outline: none;
    font-weight: normal;
    text-transform: none;
  }
  .th-search:focus {
    border-color: #38BDF8;
    background: #0B1120;
  }

  /* Filter Buttons & Dropdowns */
  .th-filter-btn {
    width: 100%;
    background: #070B14;
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 4px;
    padding: 4px 8px;
    font-size: 11px;
    color: #F1F5F9;
    display: flex;
    align-items: center;
    justify-content: space-between;
    cursor: pointer;
    text-align: left;
    transition: all 0.2s;
    gap: 4px;
    font-weight: normal;
    text-transform: none;
  }
  .th-filter-btn:hover, .th-filter-btn.active {
    border-color: #38BDF8;
    background: #0B1120;
    color: #38BDF8;
  }
  .th-filter-btn .btn-txt {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 95px;
  }
  .th-filter-btn .arrow {
    font-size: 9px;
    opacity: 0.7;
    flex-shrink: 0;
  }

  .th-dropdown-menu {
    display: none;
    position: absolute;
    top: 100%;
    left: 0;
    min-width: 160px;
    background: #0F172A;
    border: 1px solid rgba(56, 189, 248, 0.4);
    border-radius: 6px;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.7);
    padding: 6px;
    z-index: 1000;
    margin-top: 3px;
    backdrop-filter: blur(12px);
  }
  .th-dropdown-menu.show {
    display: block;
  }
  .th-dropdown-item {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 5px 8px;
    font-size: 12px;
    color: #E2E8F0;
    cursor: pointer;
    border-radius: 4px;
    user-select: none;
    text-transform: none;
    font-weight: 500;
  }
  .th-dropdown-item:hover {
    background: rgba(56, 189, 248, 0.15);
    color: #38BDF8;
  }
  .th-dropdown-item input[type='checkbox'] {
    accent-color: #38BDF8;
    cursor: pointer;
    width: 14px;
    height: 14px;
  }
  .th-dropdown-divider {
    height: 1px;
    background: rgba(255, 255, 255, 0.1);
    margin: 4px 0;
  }

  /* Date Popover */
  .date-filter-popover {
    display: none;
    position: absolute;
    top: 100%;
    left: 0;
    min-width: 185px;
    background: #0F172A;
    border: 1px solid rgba(56, 189, 248, 0.4);
    border-radius: 6px;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.7);
    padding: 10px;
    z-index: 1000;
    margin-top: 3px;
  }
  .date-filter-popover.show {
    display: flex;
    flex-direction: column;
    gap: 6px;
  }
  .df-field {
    display: flex;
    flex-direction: column;
    gap: 2px;
  }
  .df-field label {
    font-size: 10px;
    text-transform: uppercase;
    color: #94A3B8;
    font-weight: 700;
    letter-spacing: 0.3px;
  }
  .df-field input[type='date'] {
    background: #070B14;
    border: 1px solid rgba(255, 255, 255, 0.15);
    border-radius: 4px;
    color: #F8FAFC;
    padding: 4px 6px;
    font-size: 12px;
    outline: none;
    color-scheme: dark;
  }
  .df-field input[type='date']:focus {
    border-color: #38BDF8;
  }
  .df-actions {
    display: flex;
    justify-content: flex-end;
    gap: 6px;
    margin-top: 4px;
  }
  .df-btn {
    background: rgba(255, 255, 255, 0.08);
    border: 1px solid rgba(255, 255, 255, 0.1);
    color: #CBD5E1;
    font-size: 11px;
    padding: 4px 8px;
    border-radius: 4px;
    cursor: pointer;
  }
  .df-btn:hover {
    background: rgba(239, 68, 68, 0.2);
    color: #FCA5A5;
    border-color: rgba(239, 68, 68, 0.4);
  }
  
  table.exec-table td {
    padding: 9px 12px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    color: #E2E8F0;
    vertical-align: middle;
    font-size: 13px;
  }
  table.exec-table tbody tr {
    transition: background 0.15s ease;
  }
  table.exec-table tbody tr:nth-child(even) {
    background: rgba(255, 255, 255, 0.02);
  }
  table.exec-table tbody tr:hover {
    background: rgba(56, 189, 248, 0.08) !important;
  }

  /* Badges & Cell Styles */
  .badge-job {
    display: inline-block;
    padding: 4px 8px;
    border-radius: 5px;
    background: rgba(2, 132, 199, 0.22);
    color: #38BDF8;
    font-weight: 700;
    font-size: 12px;
    border: 1px solid rgba(56, 189, 248, 0.35);
    letter-spacing: 0.3px;
  }
  .font-bold { font-weight: 600; color: #FFFFFF; }
  .font-mono { font-family: 'Consolas', 'Courier New', monospace; font-size: 12px; }
  .badge-pill {
    display: inline-block;
    padding: 3px 8px;
    border-radius: 12px;
    background: rgba(148, 163, 184, 0.15);
    color: #CBD5E1;
    font-weight: 600;
    font-size: 12px;
  }
  
  .badge {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    padding: 4px 9px;
    border-radius: 4px;
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.3px;
  }
  .b-green { background: rgba(16, 185, 129, 0.18); color: #34D399; border: 1px solid rgba(16, 185, 129, 0.35); }
  .b-red { background: rgba(239, 68, 68, 0.18); color: #F87171; border: 1px solid rgba(239, 68, 68, 0.35); }
  .b-blue { background: rgba(56, 189, 248, 0.18); color: #38BDF8; border: 1px solid rgba(56, 189, 248, 0.35); }
  .b-gray { background: rgba(148, 163, 184, 0.12); color: #94A3B8; border: 1px solid rgba(148, 163, 184, 0.25); }
  .b-complete { background: linear-gradient(135deg, rgba(16,185,129,0.25) 0%, rgba(5,150,105,0.35) 100%); color: #6EE7B7; border: 1px solid #10B981; box-shadow: 0 0 8px rgba(16,185,129,0.2); }
  .b-progress { background: rgba(245, 158, 11, 0.18); color: #FBBF24; border: 1px solid rgba(245, 158, 11, 0.35); }
</style>"""

header_html = """<div class='onboarding-container'>
  <!-- CONTROLS BAR -->
  <div class='controls-bar'>
    <div class='search-group'>
      <input type='text' id='globalSearch' class='global-search' placeholder='🔍 Busca rápida em todas as colunas...' oninput='window.applyFilters()'>
    </div>
    <div class='controls-right'>
      <button id='btnCopiar' class='btn-copiar' onclick='window.copiarTabela()' title='Copia todos os dados filtrados em formato de tabela para colar no Excel'>📋 Copiar p/ Excel</button>
      <button class='btn-reset' onclick='window.resetFilters()'>Limpar Filtros</button>
      <div class='counter-badge'>Exibindo <span id='visibleCount'>0</span> de <span id='totalCount'>0</span> registros</div>
    </div>
  </div>

  <!-- TABLE WRAPPER -->
  <div class='table-wrapper' id='tableWrapper' onscroll='window.handleScroll()'>
    <table class='exec-table' id='onboardingTable'>
      <thead>
        <tr>
          <!-- 0: JOB -->
          <th>
            <div class='th-header-cell'>
              <div class='th-title' onclick='window.sortTable(0)'>JOB <span>↕</span></div>
              <input type='text' class='th-search' placeholder='Filtrar...' data-col='0' oninput='window.applyFilters()'>
            </div>
          </th>
          <!-- 1: EMPRESA -->
          <th>
            <div class='th-header-cell'>
              <div class='th-title' onclick='window.sortTable(1)'>EMPRESA <span>↕</span></div>
              <input type='text' class='th-search' placeholder='Filtrar...' data-col='1' oninput='window.applyFilters()'>
            </div>
          </th>
          <!-- 2: GRUPO -->
          <th>
            <div class='th-header-cell'>
              <div class='th-title' onclick='window.sortTable(2)'>GRUPO <span>↕</span></div>
              <input type='text' class='th-search' placeholder='Filtrar...' data-col='2' oninput='window.applyFilters()'>
            </div>
          </th>
          <!-- 3: CONSULTOR -->
          <th>
            <div class='th-header-cell'>
              <div class='th-title' onclick='window.sortTable(3)'>CONSULTOR <span>↕</span></div>
              <input type='text' class='th-search' placeholder='Filtrar...' data-col='3' oninput='window.applyFilters()'>
            </div>
          </th>
          <!-- 4: UNIDADE -->
          <th>
            <div class='th-header-cell'>
              <div class='th-title' onclick='window.sortTable(4)'>UNIDADE <span>↕</span></div>
              <input type='text' class='th-search' placeholder='Filtrar...' data-col='4' oninput='window.applyFilters()'>
            </div>
          </th>
          <!-- 5: CADASTRO (DATA FILTER) -->
          <th>
            <div class='th-header-cell'>
              <div class='th-title' onclick='window.sortTable(5)'>CADASTRO <span>↕</span></div>
              <button class='th-filter-btn' onclick='window.toggleDropdown(event, "popover_cad")'>
                <span class='btn-txt' id='btn_cad_label'>Período 📅</span>
                <span class='arrow'>▼</span>
              </button>
              <div class='date-filter-popover' id='popover_cad' onclick='event.stopPropagation()'>
                <div class='df-field'>
                  <label>Data Inicial:</label>
                  <input type='date' id='df_from_cad' onchange='window.applyFilters()'>
                </div>
                <div class='df-field'>
                  <label>Data Final:</label>
                  <input type='date' id='df_to_cad' onchange='window.applyFilters()'>
                </div>
                <div class='df-actions'>
                  <button type='button' class='df-btn' onclick='window.clearDateFilter("cad")'>Limpar</button>
                </div>
              </div>
            </div>
          </th>
          <!-- 6: CNPJ -->
          <th>
            <div class='th-header-cell'>
              <div class='th-title' onclick='window.sortTable(6)'>CNPJ <span>↕</span></div>
              <input type='text' class='th-search' placeholder='Filtrar...' data-col='6' oninput='window.applyFilters()'>
            </div>
          </th>
          <!-- 7: PROCURACAO (MULTI-SELECT) -->
          <th>
            <div class='th-header-cell'>
              <div class='th-title' onclick='window.sortTable(7)'>PROCURAÇÃO <span>↕</span></div>
              <button class='th-filter-btn' onclick='window.toggleDropdown(event, "dropdown_proc")'>
                <span class='btn-txt' id='btn_proc_label'>Todos</span>
                <span class='arrow'>▼</span>
              </button>
              <div class='th-dropdown-menu' id='dropdown_proc' onclick='event.stopPropagation()'>
                <label class='th-dropdown-item'>
                  <input type='checkbox' id='all_proc' checked onchange='window.toggleSelectAll("proc", this)'>
                  <strong>(Todos)</strong>
                </label>
                <div class='th-dropdown-divider'></div>
                <label class='th-dropdown-item'>
                  <input type='checkbox' class='chk-proc' value='SIM' checked onchange='window.checkGroupItem("proc")'>
                  SIM
                </label>
                <label class='th-dropdown-item'>
                  <input type='checkbox' class='chk-proc' value='NÃO' checked onchange='window.checkGroupItem("proc")'>
                  NÃO
                </label>
              </div>
            </div>
          </th>
          <!-- 8: ASSESSMENT (MULTI-SELECT) -->
          <th>
            <div class='th-header-cell'>
              <div class='th-title' onclick='window.sortTable(8)'>ASSESSMENT <span>↕</span></div>
              <button class='th-filter-btn' onclick='window.toggleDropdown(event, "dropdown_ass")'>
                <span class='btn-txt' id='btn_ass_label'>Todos</span>
                <span class='arrow'>▼</span>
              </button>
              <div class='th-dropdown-menu' id='dropdown_ass' onclick='event.stopPropagation()'>
                <label class='th-dropdown-item'>
                  <input type='checkbox' id='all_ass' checked onchange='window.toggleSelectAll("ass", this)'>
                  <strong>(Todos)</strong>
                </label>
                <div class='th-dropdown-divider'></div>
                <label class='th-dropdown-item'>
                  <input type='checkbox' class='chk-ass' value='SIM' checked onchange='window.checkGroupItem("ass")'>
                  SIM
                </label>
                <label class='th-dropdown-item'>
                  <input type='checkbox' class='chk-ass' value='NÃO' checked onchange='window.checkGroupItem("ass")'>
                  NÃO
                </label>
              </div>
            </div>
          </th>
          <!-- 9: REUNIÃO TAX -->
          <th>
            <div class='th-header-cell'>
              <div class='th-title' onclick='window.sortTable(9)'>REUNIÃO TAX <span>↕</span></div>
              <input type='text' class='th-search' placeholder='Filtrar...' data-col='9' oninput='window.applyFilters()'>
            </div>
          </th>
          <!-- 10: REUNIÃO CORP -->
          <th>
            <div class='th-header-cell'>
              <div class='th-title' onclick='window.sortTable(10)'>REUNIÃO CORP <span>↕</span></div>
              <input type='text' class='th-search' placeholder='Filtrar...' data-col='10' oninput='window.applyFilters()'>
            </div>
          </th>
          <!-- 11: CHECKLIST (DATA FILTER) -->
          <th>
            <div class='th-header-cell'>
              <div class='th-title' onclick='window.sortTable(11)'>CHECKLIST <span>↕</span></div>
              <button class='th-filter-btn' onclick='window.toggleDropdown(event, "popover_chk")'>
                <span class='btn-txt' id='btn_chk_label'>Período 📅</span>
                <span class='arrow'>▼</span>
              </button>
              <div class='date-filter-popover' id='popover_chk' onclick='event.stopPropagation()'>
                <div class='df-field'>
                  <label>Data Inicial:</label>
                  <input type='date' id='df_from_chk' onchange='window.applyFilters()'>
                </div>
                <div class='df-field'>
                  <label>Data Final:</label>
                  <input type='date' id='df_to_chk' onchange='window.applyFilters()'>
                </div>
                <div class='th-dropdown-divider'></div>
                <label class='th-dropdown-item' style='padding: 2px 0;'>
                  <input type='checkbox' id='chk_only_pending' onchange='window.toggleOnlyPending()'>
                  Apenas Pendentes
                </label>
                <div class='df-actions'>
                  <button type='button' class='df-btn' onclick='window.clearDateFilter("chk")'>Limpar</button>
                </div>
              </div>
            </div>
          </th>
          <!-- 12: FINALIZADOS (MULTI-SELECT) -->
          <th>
            <div class='th-header-cell'>
              <div class='th-title' onclick='window.sortTable(12)'>FINALIZADOS <span>↕</span></div>
              <button class='th-filter-btn' onclick='window.toggleDropdown(event, "dropdown_comp")'>
                <span class='btn-txt' id='btn_comp_label'>Todos</span>
                <span class='arrow'>▼</span>
              </button>
              <div class='th-dropdown-menu' id='dropdown_comp' onclick='event.stopPropagation()'>
                <label class='th-dropdown-item'>
                  <input type='checkbox' id='all_comp' checked onchange='window.toggleSelectAll("comp", this)'>
                  <strong>(Todos)</strong>
                </label>
                <div class='th-dropdown-divider'></div>
                <label class='th-dropdown-item'>
                  <input type='checkbox' class='chk-comp' value='1' checked onchange='window.checkGroupItem("comp")'>
                  ✔ Completo
                </label>
                <label class='th-dropdown-item'>
                  <input type='checkbox' class='chk-comp' value='0' checked onchange='window.checkGroupItem("comp")'>
                  Em Andamento
                </label>
              </div>
            </div>
          </th>
        </tr>
      </thead>
      <tbody id='tableBody'></tbody>
    </table>
  </div>
</div>
"""

js_part1 = """<script>
(function() {
  var rawData = [];
  var filteredData = [];
  var sortCol = -1;
  var sortAsc = true;
  var renderedCount = 0;
  var BATCH_SIZE = 400;

  function decodeDate(offsetStr) {
    if (!offsetStr && offsetStr !== '0') return { fmt: '-', iso: '' };
    var d = new Date(2024, 0, 1 + parseInt(offsetStr, 10));
    var dd = String(d.getDate()).padStart(2, '0');
    var mm = String(d.getMonth() + 1).padStart(2, '0');
    var yyyy = d.getFullYear();
    return {
      fmt: dd + '/' + mm + '/' + yyyy,
      iso: yyyy + '-' + mm + '-' + dd
    };
  }

  function init() {
    var rawText = \""""

js_part2 = """\";
    if (!rawText) return;

    var rows = rawText.split('~');
    rawData = new Array(rows.length);

    for (var i = 0; i < rows.length; i++) {
      var parts = rows[i].split('^');
      var job = parts[0] || '';
      var empresa = parts[1] || '';
      var grupo = parts[2] || '-';
      var consultor = parts[3] || '-';
      var unidade = parts[4] || '-';
      var cadObj = decodeDate(parts[5]);
      var cnpj = parts[6] || '-';
      var flags = parseInt(parts[7] || '0', 10);
      var isProc = (flags & 1) !== 0;
      var isAss = (flags & 2) !== 0;
      var chkObj = decodeDate(parts[8]);
      var hasChk = (chkObj.iso !== '');
      var isCompleto = (isProc && isAss && hasChk);

      rawData[i] = {
        job: job,
        empresa: empresa,
        grupo: grupo,
        consultor: consultor,
        unidade: unidade,
        cadFmt: cadObj.fmt,
        cadIso: cadObj.iso,
        cnpj: cnpj,
        proc: isProc ? 'SIM' : 'NÃO',
        ass: isAss ? 'SIM' : 'NÃO',
        chkFmt: hasChk ? chkObj.fmt : 'Pendente',
        chkIso: chkObj.iso,
        isCompleto: isCompleto ? '1' : '0',
        searchIndex: (job + ' ' + empresa + ' ' + grupo + ' ' + consultor + ' ' + unidade + ' ' + cadObj.fmt + ' ' + cnpj).toLowerCase()
      };
    }

    filteredData = rawData.slice();
    applyFilters();
  }

  function createRowHTML(item) {
    var procBadge = item.proc === 'SIM' ? '<span class=\"badge b-green\">SIM</span>' : '<span class=\"badge b-red\">NÃO</span>';
    var assBadge = item.ass === 'SIM' ? '<span class=\"badge b-green\">SIM</span>' : '<span class=\"badge b-red\">NÃO</span>';
    var chkBadge = item.chkFmt === 'Pendente' ? '<span class=\"badge b-gray\">Pendente</span>' : '<span class=\"badge b-blue\">' + item.chkFmt + '</span>';
    var compBadge = item.isCompleto === '1' ? '<span class=\"badge b-complete\">✔ COMPLETO</span>' : '<span class=\"badge b-progress\">EM ANDAMENTO</span>';

    return '<tr>' +
      '<td><span class=\"badge-job\">' + item.job + '</span></td>' +
      '<td class=\"font-bold\" title=\"' + item.empresa + '\">' + item.empresa + '</td>' +
      '<td>' + item.grupo + '</td>' +
      '<td>' + item.consultor + '</td>' +
      '<td><span class=\"badge-pill\">' + item.unidade + '</span></td>' +
      '<td>' + item.cadFmt + '</td>' +
      '<td class=\"font-mono\">' + item.cnpj + '</td>' +
      '<td>' + procBadge + '</td>' +
      '<td>' + assBadge + '</td>' +
      '<td><span class=\"badge b-gray\">-</span></td>' +
      '<td><span class=\"badge b-gray\">-</span></td>' +
      '<td>' + chkBadge + '</td>' +
      '<td>' + compBadge + '</td>' +
    '</tr>';
  }

  function renderTableBatch(reset) {
    var tbody = document.getElementById('tableBody');
    if (!tbody) return;

    if (reset) {
      tbody.innerHTML = '';
      renderedCount = 0;
    }

    var total = filteredData.length;
    if (renderedCount >= total) return;

    var end = Math.min(renderedCount + BATCH_SIZE, total);
    var htmlChunk = '';
    for (var i = renderedCount; i < end; i++) {
      htmlChunk += createRowHTML(filteredData[i]);
    }

    tbody.insertAdjacentHTML('beforeend', htmlChunk);
    renderedCount = end;
  }

  window.handleScroll = function() {
    var wrapper = document.getElementById('tableWrapper');
    if (!wrapper) return;
    if (wrapper.scrollTop + wrapper.clientHeight >= wrapper.scrollHeight - 300) {
      if (renderedCount < filteredData.length) {
        renderTableBatch(false);
      }
    }
  };

  window.toggleDropdown = function(e, id) {
    e.stopPropagation();
    var target = document.getElementById(id);
    if (!target) return;
    var isShown = target.classList.contains('show');
    
    document.querySelectorAll('.th-dropdown-menu, .date-filter-popover').forEach(function(d) {
      d.classList.remove('show');
    });

    if (!isShown) {
      target.classList.add('show');
    }
  };

  window.clearDateFilter = function(colKey) {
    var f = document.getElementById('df_from_' + colKey);
    var t = document.getElementById('df_to_' + colKey);
    if (f) f.value = '';
    if (t) t.value = '';
    if (colKey === 'chk') {
      var op = document.getElementById('chk_only_pending');
      if (op) op.checked = false;
    }
    window.applyFilters();
  };

  window.toggleOnlyPending = function() {
    var onlyPending = document.getElementById('chk_only_pending') ? document.getElementById('chk_only_pending').checked : false;
    if (onlyPending) {
      var f = document.getElementById('df_from_chk');
      var t = document.getElementById('df_to_chk');
      if (f) f.value = '';
      if (t) t.value = '';
    }
    window.applyFilters();
  };

  window.toggleSelectAll = function(groupName, masterCheckbox) {
    var checkboxes = document.querySelectorAll('.chk-' + groupName);
    checkboxes.forEach(function(cb) {
      cb.checked = masterCheckbox.checked;
    });
    window.applyFilters();
  };

  window.checkGroupItem = function(groupName) {
    var master = document.getElementById('all_' + groupName);
    var checkboxes = Array.from(document.querySelectorAll('.chk-' + groupName));
    var allChecked = checkboxes.every(function(cb) { return cb.checked; });
    if (master) master.checked = allChecked;
    window.applyFilters();
  };

  function updateButtonLabels() {
    var procChecked = Array.from(document.querySelectorAll('.chk-proc:checked')).map(function(c){ return c.value; });
    var btnProc = document.getElementById('btn_proc_label');
    if (btnProc) {
      btnProc.textContent = (procChecked.length === 0 || procChecked.length === 2) ? 'Todos' : procChecked.join(', ');
    }

    var assChecked = Array.from(document.querySelectorAll('.chk-ass:checked')).map(function(c){ return c.value; });
    var btnAss = document.getElementById('btn_ass_label');
    if (btnAss) {
      btnAss.textContent = (assChecked.length === 0 || assChecked.length === 2) ? 'Todos' : assChecked.join(', ');
    }

    var compChecked = Array.from(document.querySelectorAll('.chk-comp:checked')).map(function(c){ return c.value; });
    var btnComp = document.getElementById('btn_comp_label');
    if (btnComp) {
      if (compChecked.length === 0 || compChecked.length === 2) {
        btnComp.textContent = 'Todos';
      } else {
        btnComp.textContent = compChecked[0] === '1' ? 'Completo' : 'Em Andamento';
      }
    }

    var cadFrom = document.getElementById('df_from_cad') ? document.getElementById('df_from_cad').value : '';
    var cadTo = document.getElementById('df_to_cad') ? document.getElementById('df_to_cad').value : '';
    var btnCad = document.getElementById('btn_cad_label');
    if (btnCad) {
      if (cadFrom && cadTo) {
        btnCad.textContent = cadFrom.split('-').reverse().slice(0,2).join('/') + ' a ' + cadTo.split('-').reverse().slice(0,2).join('/');
      } else if (cadFrom) {
        btnCad.textContent = '>= ' + cadFrom.split('-').reverse().join('/');
      } else if (cadTo) {
        btnCad.textContent = '<= ' + cadTo.split('-').reverse().join('/');
      } else {
        btnCad.textContent = 'Período 📅';
      }
    }

    var onlyPendingChk = document.getElementById('chk_only_pending') ? document.getElementById('chk_only_pending').checked : false;
    var chkFrom = document.getElementById('df_from_chk') ? document.getElementById('df_from_chk').value : '';
    var chkTo = document.getElementById('df_to_chk') ? document.getElementById('df_to_chk').value : '';
    var btnChk = document.getElementById('btn_chk_label');
    if (btnChk) {
      if (onlyPendingChk) {
        btnChk.textContent = 'Pendentes';
      } else if (chkFrom && chkTo) {
        btnChk.textContent = chkFrom.split('-').reverse().slice(0,2).join('/') + ' a ' + chkTo.split('-').reverse().slice(0,2).join('/');
      } else if (chkFrom) {
        btnChk.textContent = '>= ' + chkFrom.split('-').reverse().join('/');
      } else if (chkTo) {
        btnChk.textContent = '<= ' + chkTo.split('-').reverse().join('/');
      } else {
        btnChk.textContent = 'Período 📅';
      }
    }
  }

  window.applyFilters = function() {
    var globalVal = (document.getElementById('globalSearch') ? document.getElementById('globalSearch').value : '').toLowerCase().trim();
    
    var colJob = (document.querySelector('.th-search[data-col="0"]') ? document.querySelector('.th-search[data-col="0"]').value : '').toLowerCase().trim();
    var colEmp = (document.querySelector('.th-search[data-col="1"]') ? document.querySelector('.th-search[data-col="1"]').value : '').toLowerCase().trim();
    var colGrp = (document.querySelector('.th-search[data-col="2"]') ? document.querySelector('.th-search[data-col="2"]').value : '').toLowerCase().trim();
    var colCons = (document.querySelector('.th-search[data-col="3"]') ? document.querySelector('.th-search[data-col="3"]').value : '').toLowerCase().trim();
    var colUnid = (document.querySelector('.th-search[data-col="4"]') ? document.querySelector('.th-search[data-col="4"]').value : '').toLowerCase().trim();
    var colCnpj = (document.querySelector('.th-search[data-col="6"]') ? document.querySelector('.th-search[data-col="6"]').value : '').toLowerCase().trim();

    var procChecked = Array.from(document.querySelectorAll('.chk-proc:checked')).map(function(c) { return c.value; });
    var procFiltered = (procChecked.length === 1);

    var assChecked = Array.from(document.querySelectorAll('.chk-ass:checked')).map(function(c) { return c.value; });
    var assFiltered = (assChecked.length === 1);

    var compChecked = Array.from(document.querySelectorAll('.chk-comp:checked')).map(function(c) { return c.value; });
    var compFiltered = (compChecked.length === 1);

    var cadFrom = document.getElementById('df_from_cad') ? document.getElementById('df_from_cad').value : '';
    var cadTo = document.getElementById('df_to_cad') ? document.getElementById('df_to_cad').value : '';

    var onlyPendingChk = document.getElementById('chk_only_pending') ? document.getElementById('chk_only_pending').checked : false;
    var chkFrom = document.getElementById('df_from_chk') ? document.getElementById('df_from_chk').value : '';
    var chkTo = document.getElementById('df_to_chk') ? document.getElementById('df_to_chk').value : '';

    filteredData = rawData.filter(function(item) {
      if (globalVal && item.searchIndex.indexOf(globalVal) === -1) return false;
      if (colJob && item.job.toLowerCase().indexOf(colJob) === -1) return false;
      if (colEmp && item.empresa.toLowerCase().indexOf(colEmp) === -1) return false;
      if (colGrp && item.grupo.toLowerCase().indexOf(colGrp) === -1) return false;
      if (colCons && item.consultor.toLowerCase().indexOf(colCons) === -1) return false;
      if (colUnid && item.unidade.toLowerCase().indexOf(colUnid) === -1) return false;
      if (colCnpj && item.cnpj.indexOf(colCnpj) === -1) return false;

      if (procFiltered && item.proc !== procChecked[0]) return false;
      if (assFiltered && item.ass !== assChecked[0]) return false;
      if (compFiltered && item.isCompleto !== compChecked[0]) return false;

      if (cadFrom && (!item.cadIso || item.cadIso < cadFrom)) return false;
      if (cadTo && (!item.cadIso || item.cadIso > cadTo)) return false;

      if (onlyPendingChk) {
        if (item.chkIso !== '') return false;
      } else {
        if (chkFrom && (!item.chkIso || item.chkIso < chkFrom)) return false;
        if (chkTo && (!item.chkIso || item.chkIso > chkTo)) return false;
      }

      return true;
    });

    if (sortCol >= 0) {
      applySortInternal();
    }

    renderTableBatch(true);
    updateCounter();
    updateButtonLabels();
  };

  function applySortInternal() {
    var key = 'job';
    if (sortCol === 1) key = 'empresa';
    else if (sortCol === 2) key = 'grupo';
    else if (sortCol === 3) key = 'consultor';
    else if (sortCol === 4) key = 'unidade';
    else if (sortCol === 5) key = 'cadIso';
    else if (sortCol === 6) key = 'cnpj';
    else if (sortCol === 7) key = 'proc';
    else if (sortCol === 8) key = 'ass';
    else if (sortCol === 11) key = 'chkIso';
    else if (sortCol === 12) key = 'isCompleto';

    filteredData.sort(function(a, b) {
      var valA = a[key] || '';
      var valB = b[key] || '';
      if (sortCol === 4) {
        var numA = parseInt(valA, 10) || 0;
        var numB = parseInt(valB, 10) || 0;
        return sortAsc ? numA - numB : numB - numA;
      }
      return sortAsc ? valA.localeCompare(valB) : valB.localeCompare(valA);
    });
  }

  window.sortTable = function(colIndex) {
    if (sortCol === colIndex) {
      sortAsc = !sortAsc;
    } else {
      sortCol = colIndex;
      sortAsc = true;
    }
    applySortInternal();
    renderTableBatch(true);
  };

  window.copiarTabela = function() {
    var btn = document.getElementById('btnCopiar');
    var originalHTML = btn.innerHTML;
    btn.innerHTML = '⏳ Copiando...';

    var headerNames = ['JOB', 'EMPRESA', 'GRUPO', 'CONSULTOR', 'UNIDADE', 'CADASTRO', 'CNPJ', 'PROCURAÇÃO', 'ASSESSMENT', 'REUNIÃO TAX', 'REUNIÃO CORP', 'CHECKLIST', 'FINALIZADOS'];
    var textToCopy = headerNames.join('\\t') + '\\n';

    for (var i = 0; i < filteredData.length; i++) {
      var item = filteredData[i];
      var row = [
        item.job,
        item.empresa,
        item.grupo,
        item.consultor,
        item.unidade,
        item.cadFmt,
        item.cnpj,
        item.proc,
        item.ass,
        '-',
        '-',
        item.chkFmt,
        item.isCompleto === '1' ? '✔ COMPLETO' : 'EM ANDAMENTO'
      ];
      textToCopy += row.join('\\t') + '\\n';
    }

    try {
      var textArea = document.createElement('textarea');
      textArea.value = textToCopy;
      textArea.style.position = 'fixed';
      textArea.style.left = '-999999px';
      textArea.style.top = '-999999px';
      document.body.appendChild(textArea);
      textArea.focus();
      textArea.select();
      var successful = document.execCommand('copy');
      document.body.removeChild(textArea);

      if (successful) {
        btn.innerHTML = '✔ Copiado (' + filteredData.length + ' linhas)';
        btn.style.borderColor = '#10B981';
        btn.style.color = '#34D399';
        setTimeout(function() {
          btn.innerHTML = originalHTML;
          btn.style.borderColor = '';
          btn.style.color = '';
        }, 3000);
      } else {
        throw new Error('Falha ao copiar');
      }
    } catch(err) {
      btn.innerHTML = '❌ Erro ao copiar';
      setTimeout(function() { btn.innerHTML = originalHTML; }, 3000);
    }
  };

  window.resetFilters = function() {
    if (document.getElementById('globalSearch')) document.getElementById('globalSearch').value = '';
    document.querySelectorAll('.th-search').forEach(function(inp) { inp.value = ''; });
    document.querySelectorAll('.df-field input[type="date"]').forEach(function(inp) { inp.value = ''; });
    document.querySelectorAll('input[type="checkbox"]').forEach(function(cb) { cb.checked = true; });
    var op = document.getElementById('chk_only_pending');
    if (op) op.checked = false;
    applyFilters();
  };

  function updateCounter() {
    var total = filteredData.length;
    if (document.getElementById('visibleCount')) document.getElementById('visibleCount').textContent = total;
    if (document.getElementById('totalCount')) document.getElementById('totalCount').textContent = rawData.length;
  }

  document.addEventListener('click', function(e) {
    if (!e.target.closest('.th-header-cell')) {
      document.querySelectorAll('.th-dropdown-menu, .date-filter-popover').forEach(function(d) {
        d.classList.remove('show');
      });
    }
  });

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    setTimeout(init, 30);
  }
})();
</script>"""

def to_dax_literal(s):
    return '"' + s.replace('"', '""') + '"'

dax_top = """VAR _Filtered = 
    FILTER(
        'vw_powerbi_empresas_Onboarding',
        'vw_powerbi_empresas_Onboarding'[DATA_CADASTRO] >= DATE(2024, 1, 1)
    )

VAR _TabelaBase = 
    SUMMARIZE(
        _Filtered,
        'vw_powerbi_empresas_Onboarding'[JOB],
        'vw_powerbi_empresas_Onboarding'[EMPRESA],
        'vw_powerbi_empresas_Onboarding'[Grupo],
        'vw_powerbi_empresas_Onboarding'[CONSULTOR],
        'vw_powerbi_empresas_Onboarding'[UNIDADE],
        'vw_powerbi_empresas_Onboarding'[DATA_CADASTRO],
        'vw_powerbi_empresas_Onboarding'[CNPJ],
        'vw_powerbi_empresas_Onboarding'[PROCURACAO],
        'vw_powerbi_empresas_Onboarding'[ASSESSEMENT],
        'vw_powerbi_empresas_Onboarding'[CHECKLIST]
    )

VAR _CombinedData = 
    CONCATENATEX(
        _TabelaBase,
        VAR _p = IF(UPPER(TRIM([PROCURACAO])) = "SIM", 1, 0)
        VAR _a = IF(UPPER(TRIM([ASSESSEMENT])) = "SIM", 2, 0)
        VAR _flags = FORMAT(_p + _a, "0")
        VAR _dtCad = FORMAT(INT([DATA_CADASTRO] - DATE(2024, 1, 1)), "0")
        VAR _dtChk = IF(ISBLANK([CHECKLIST]), "", FORMAT(INT([CHECKLIST] - DATE(2024, 1, 1)), "0"))
        VAR _emp = SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(LEFT([EMPRESA], 24), "^", " "), "~", " "), UNICHAR(34), " "), UNICHAR(92), " ")
        VAR _grp = SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(LEFT(COALESCE([Grupo], ""), 14), "^", " "), "~", " "), UNICHAR(34), " "), UNICHAR(92), " ")
        VAR _cons = SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(LEFT(COALESCE([CONSULTOR], ""), 14), "^", " "), "~", " "), UNICHAR(34), " "), UNICHAR(92), " ")
        VAR _job = SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE([JOB], "^", " "), "~", " "), UNICHAR(34), " "), UNICHAR(92), " ")
        RETURN
        _job & "^" & 
        _emp & "^" & 
        _grp & "^" & 
        _cons & "^" & 
        FORMAT([UNIDADE], "0") & "^" & 
        _dtCad & "^" & 
        COALESCE([CNPJ], "") & "^" & 
        _flags & "^" & 
        _dtChk,
        "~"
    )

"""

dax_css = "VAR _CSS = " + to_dax_literal(css) + "\n\n"
dax_header = "VAR _HeaderHTML = " + to_dax_literal(header_html) + "\n\n"
dax_js1 = "VAR _JSScript1 = " + to_dax_literal(js_part1) + "\n\n"
dax_js2 = "VAR _JSScript2 = " + to_dax_literal(js_part2) + "\n\n"

dax_return = "RETURN\n    _CSS & _HeaderHTML & _JSScript1 & _CombinedData & _JSScript2\n"

full_dax = dax_top + dax_css + dax_header + dax_js1 + dax_js2 + dax_return

with open('HTML_Onboarding_Executivo.dax', 'w', encoding='utf-8') as f:
    f.write(full_dax)

print("Generated HTML_Onboarding_Executivo.dax cleanly!")

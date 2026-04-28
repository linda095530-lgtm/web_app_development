/* ===== Page Renderers ===== */
let flashMsg = null;
function setFlash(msg, type) { flashMsg = { msg, type: type || 'success' }; }

function flashHTML() {
  if (!flashMsg) return '';
  const f = flashMsg; flashMsg = null;
  return `<div class="flash flash-${f.type}"><span>${f.msg}</span><button class="close-btn" onclick="this.parentElement.remove()">✕</button></div>`;
}

function subjectOptions(selectedId) {
  return DB.getSubjects().map(s =>
    `<option value="${s.id}" ${s.id === selectedId ? 'selected' : ''}>${s.name}</option>`
  ).join('');
}

function professorOptions(selectedId) {
  return DB.getProfessors().map(p =>
    `<option value="${p.id}" ${p.id === selectedId ? 'selected' : ''}>${p.name}</option>`
  ).join('');
}

const Pages = {
  // ===== HOME =====
  home() {
    const sc = DB.getSubjects().length, pc = DB.getProfessors().length, ec = DB.getExams().length;
    const recent = DB.getExams().slice(0, 5);
    let recentHTML = '';
    if (recent.length) {
      recentHTML = `<div style="margin-top:2rem"><h3>🕐 最新上傳</h3><div class="card" style="margin-top:1rem"><div class="table-wrap"><table>
        <thead><tr><th>標題</th><th>科目</th><th>教授</th><th>學年度</th><th>類型</th></tr></thead>
        <tbody>${recent.map(e => `<tr style="cursor:pointer" onclick="navigate('#/exams/${e.id}')">
          <td><strong>${esc(e.title)}</strong></td><td><span class="badge badge-primary">${esc(DB.subjectName(e.subject_id))}</span></td>
          <td>${esc(DB.professorName(e.professor_id))}</td><td>${esc(e.year)}-${esc(e.semester)}</td>
          <td><span class="badge badge-secondary">${esc(e.exam_type)}</span></td></tr>`).join('')}
        </tbody></table></div></div></div>`;
    }
    return `${flashHTML()}
      <div class="hero"><h1>📚 考古題收藏系統</h1><p>集中管理、分類明確、搜尋便利的大學考古題資料庫</p>
        <div><a class="btn btn-primary btn-lg" href="#/exams/create">➕ 上傳考古題</a>&nbsp;&nbsp;
        <a class="btn btn-outline btn-lg" href="#/search">🔍 搜尋考古題</a></div></div>
      <div class="stats-grid">
        <div class="card stat-card"><div class="stat-icon">📖</div><div class="stat-number">${sc}</div><div class="stat-label">科目數量</div><a class="btn btn-outline btn-sm" href="#/subjects">查看所有科目 →</a></div>
        <div class="card stat-card"><div class="stat-icon">👤</div><div class="stat-number">${pc}</div><div class="stat-label">教授數量</div><a class="btn btn-outline-success btn-sm" href="#/professors">查看所有教授 →</a></div>
        <div class="card stat-card"><div class="stat-icon">📝</div><div class="stat-number">${ec}</div><div class="stat-label">考古題數量</div><a class="btn btn-outline-warning btn-sm" href="#/exams">查看所有考古題 →</a></div>
      </div>${recentHTML}`;
  },

  // ===== SUBJECTS =====
  subjectList() {
    const items = DB.getSubjects();
    let body;
    if (!items.length) {
      body = `<div class="empty-state"><div class="icon">📦</div><p>還沒有任何科目</p><a class="btn btn-primary" href="#/subjects/create">➕ 新增第一個科目</a></div>`;
    } else {
      body = `<div class="item-grid">${items.map(s => {
        const cnt = DB.getExamsBySubject(s.id).length;
        return `<div class="card item-card" onclick="navigate('#/subjects/${s.id}')"><div class="card-body">
          <h3>📖 ${esc(s.name)}</h3><p>${esc(s.description || '無描述')}</p>
          <span class="badge badge-primary">${cnt} 份考古題</span></div></div>`;
      }).join('')}</div>`;
    }
    return `${flashHTML()}<div class="page-header"><h1>📖 科目列表</h1><a class="btn btn-primary" href="#/subjects/create">➕ 新增科目</a></div>${body}`;
  },

  subjectDetail(id) {
    const s = DB.getSubject(id);
    if (!s) return '<div class="empty-state"><p>找不到此科目</p></div>';
    const exams = DB.getExamsBySubject(id);
    const profs = DB.getProfessorsBySubject(id);
    let examHTML = exams.length ? `<div class="table-wrap"><table><thead><tr><th>標題</th><th>教授</th><th>學年度</th><th>類型</th></tr></thead><tbody>
      ${exams.map(e => `<tr style="cursor:pointer" onclick="navigate('#/exams/${e.id}')"><td><strong>${esc(e.title)}</strong></td><td>${esc(DB.professorName(e.professor_id))}</td><td>${esc(e.year)}-${esc(e.semester)}</td><td><span class="badge badge-secondary">${esc(e.exam_type)}</span></td></tr>`).join('')}
      </tbody></table></div>` : '<p style="color:var(--text-muted)">此科目尚無考古題</p>';
    return `${flashHTML()}<div class="detail-header"><h1>📖 ${esc(s.name)}</h1><div class="detail-meta"><span>📝 ${exams.length} 份考古題</span><span>👤 ${profs.length} 位教授</span></div></div>
      ${s.description ? `<p style="margin-bottom:1rem">${esc(s.description)}</p>` : ''}
      <div class="detail-actions"><a class="btn btn-primary" href="#/subjects/${id}/edit">✏️ 編輯</a><button class="btn btn-danger" onclick="deleteSubject(${id})">🗑️ 刪除</button></div>
      <h3 style="margin-top:2rem">相關考古題</h3>${examHTML}`;
  },

  subjectForm(id) {
    const s = id ? DB.getSubject(id) : null;
    const title = s ? '編輯科目' : '新增科目';
    return `${flashHTML()}<div class="page-header"><h1>${s ? '✏️' : '➕'} ${title}</h1></div>
      <div class="card"><div class="card-body"><form onsubmit="saveSubject(event, ${id || 'null'})">
        <div class="form-group"><label>科目名稱 <span class="required">*</span></label><input class="form-control" id="f-name" value="${esc(s?.name || '')}" placeholder="例如：微積分" required></div>
        <div class="form-group"><label>描述</label><textarea class="form-control" id="f-desc" placeholder="輸入科目描述...">${esc(s?.description || '')}</textarea></div>
        <div class="form-actions"><button class="btn btn-primary" type="submit">✔️ ${s ? '更新' : '新增'}</button><a class="btn btn-secondary" href="#/subjects">✕ 取消</a></div>
      </form></div></div>`;
  },

  // ===== PROFESSORS =====
  professorList() {
    const items = DB.getProfessors();
    let body;
    if (!items.length) {
      body = `<div class="empty-state"><div class="icon">📦</div><p>還沒有任何教授</p><a class="btn btn-primary" href="#/professors/create">➕ 新增第一位教授</a></div>`;
    } else {
      body = `<div class="item-grid">${items.map(p => {
        const cnt = DB.getExamsByProfessor(p.id).length;
        return `<div class="card item-card" onclick="navigate('#/professors/${p.id}')"><div class="card-body">
          <h3>👤 ${esc(p.name)}</h3><p>所屬科目：${esc(DB.subjectName(p.subject_id))}</p>
          <span class="badge badge-success">${cnt} 份考古題</span></div></div>`;
      }).join('')}</div>`;
    }
    return `${flashHTML()}<div class="page-header"><h1>👤 教授列表</h1><a class="btn btn-primary" href="#/professors/create">➕ 新增教授</a></div>${body}`;
  },

  professorDetail(id) {
    const p = DB.getProfessor(id);
    if (!p) return '<div class="empty-state"><p>找不到此教授</p></div>';
    const exams = DB.getExamsByProfessor(id);
    let examHTML = exams.length ? `<div class="table-wrap"><table><thead><tr><th>標題</th><th>科目</th><th>學年度</th><th>類型</th></tr></thead><tbody>
      ${exams.map(e => `<tr style="cursor:pointer" onclick="navigate('#/exams/${e.id}')"><td><strong>${esc(e.title)}</strong></td><td><span class="badge badge-primary">${esc(DB.subjectName(e.subject_id))}</span></td><td>${esc(e.year)}-${esc(e.semester)}</td><td><span class="badge badge-secondary">${esc(e.exam_type)}</span></td></tr>`).join('')}
      </tbody></table></div>` : '<p style="color:var(--text-muted)">此教授尚無考古題</p>';
    return `${flashHTML()}<div class="detail-header"><h1>👤 ${esc(p.name)}</h1><div class="detail-meta"><span>所屬科目：${esc(DB.subjectName(p.subject_id))}</span><span>📝 ${exams.length} 份考古題</span></div></div>
      <div class="detail-actions"><a class="btn btn-primary" href="#/professors/${id}/edit">✏️ 編輯</a><button class="btn btn-danger" onclick="deleteProfessor(${id})">🗑️ 刪除</button></div>
      <h3 style="margin-top:2rem">出過的考古題</h3>${examHTML}`;
  },

  professorForm(id) {
    const p = id ? DB.getProfessor(id) : null;
    const title = p ? '編輯教授' : '新增教授';
    return `${flashHTML()}<div class="page-header"><h1>${p ? '✏️' : '➕'} ${title}</h1></div>
      <div class="card"><div class="card-body"><form onsubmit="saveProfessor(event, ${id || 'null'})">
        <div class="form-group"><label>教授姓名 <span class="required">*</span></label><input class="form-control" id="f-name" value="${esc(p?.name || '')}" placeholder="例如：王大明" required></div>
        <div class="form-group"><label>所屬科目</label><select class="form-control" id="f-subject"><option value="">-- 請選擇科目 --</option>${subjectOptions(p?.subject_id)}</select></div>
        <div class="form-actions"><button class="btn btn-primary" type="submit">✔️ ${p ? '更新' : '新增'}</button><a class="btn btn-secondary" href="#/professors">✕ 取消</a></div>
      </form></div></div>`;
  },

  // ===== EXAMS =====
  examList() {
    const subs = DB.getSubjects(), profs = DB.getProfessors();
    const sid = window._examFilterSubject || '', pid = window._examFilterProf || '', yr = window._examFilterYear || '', tp = window._examFilterType || '';
    const filters = {};
    if (sid) filters.subject_id = parseInt(sid);
    if (pid) filters.professor_id = parseInt(pid);
    if (yr) filters.year = yr;
    if (tp) filters.exam_type = tp;
    const items = DB.getExams(Object.keys(filters).length ? filters : null);
    const years = DB.getYears();
    let body;
    if (!items.length && !Object.keys(filters).length) {
      body = `<div class="empty-state"><div class="icon">📦</div><p>還沒有任何考古題</p><a class="btn btn-primary" href="#/exams/create">➕ 上傳第一份考古題</a></div>`;
    } else {
      body = items.length ? `<div class="card"><div class="table-wrap"><table><thead><tr><th>標題</th><th>科目</th><th>教授</th><th>學年度</th><th>類型</th></tr></thead><tbody>
        ${items.map(e => `<tr style="cursor:pointer" onclick="navigate('#/exams/${e.id}')"><td><strong>${esc(e.title)}</strong></td>
          <td><span class="badge badge-primary">${esc(DB.subjectName(e.subject_id))}</span></td>
          <td>${esc(DB.professorName(e.professor_id))}</td><td>${esc(e.year)}-${esc(e.semester)}</td>
          <td><span class="badge badge-secondary">${esc(e.exam_type)}</span></td></tr>`).join('')}
        </tbody></table></div></div>` : '<div class="empty-state"><p>沒有符合篩選條件的考古題</p></div>';
    }
    return `${flashHTML()}<div class="page-header"><h1>📝 考古題列表</h1><a class="btn btn-primary" href="#/exams/create">➕ 上傳考古題</a></div>
      <div class="card" style="margin-bottom:1.5rem"><div class="card-body"><div class="search-filters">
        <div class="form-group"><label>科目</label><select class="form-control" id="ef-sub" onchange="filterExams()"><option value="">全部</option>${subs.map(s=>`<option value="${s.id}" ${sid==s.id?'selected':''}>${esc(s.name)}</option>`).join('')}</select></div>
        <div class="form-group"><label>教授</label><select class="form-control" id="ef-prof" onchange="filterExams()"><option value="">全部</option>${profs.map(p=>`<option value="${p.id}" ${pid==p.id?'selected':''}>${esc(p.name)}</option>`).join('')}</select></div>
        <div class="form-group"><label>學年度</label><select class="form-control" id="ef-year" onchange="filterExams()"><option value="">全部</option>${years.map(y=>`<option value="${y}" ${yr==y?'selected':''}>${y}</option>`).join('')}</select></div>
        <div class="form-group"><label>考試類型</label><select class="form-control" id="ef-type" onchange="filterExams()"><option value="">全部</option>${['期中考','期末考','小考'].map(t=>`<option value="${t}" ${tp==t?'selected':''}>${t}</option>`).join('')}</select></div>
        <div class="form-group"><button class="btn btn-secondary btn-sm" onclick="clearExamFilters()">清除</button></div>
      </div></div></div>${body}`;
  },

  examDetail(id) {
    const e = DB.getExam(id);
    if (!e) return '<div class="empty-state"><p>找不到此考古題</p></div>';
    return `${flashHTML()}<div class="detail-header"><h1>${esc(e.title)}</h1>
        <div class="detail-meta"><span class="badge badge-primary">${esc(DB.subjectName(e.subject_id))}</span><span>👤 ${esc(DB.professorName(e.professor_id))}</span>
          <span>📅 ${esc(e.year)}-${esc(e.semester)}</span><span class="badge badge-secondary">${esc(e.exam_type)}</span></div></div>
      ${e.content ? `<h3>題目內容</h3><div class="detail-content">${esc(e.content)}</div>` : '<p style="color:var(--text-muted)">尚未填寫題目內容</p>'}
      <div class="detail-meta" style="margin-top:1rem;font-size:.85rem"><span>建立時間：${esc(e.created_at || '')}</span><span>更新時間：${esc(e.updated_at || '')}</span></div>
      <div class="detail-actions"><a class="btn btn-primary" href="#/exams/${id}/edit">✏️ 編輯</a><button class="btn btn-danger" onclick="deleteExam(${id})">🗑️ 刪除</button><a class="btn btn-secondary" href="#/exams">← 返回列表</a></div>`;
  },

  examForm(id) {
    const e = id ? DB.getExam(id) : null;
    const title = e ? '編輯考古題' : '新增考古題';
    return `${flashHTML()}<div class="page-header"><h1>${e ? '✏️' : '➕'} ${title}</h1></div>
      <div class="card"><div class="card-body"><form onsubmit="saveExam(event, ${id || 'null'})">
        <div class="form-group"><label>標題 <span class="required">*</span></label><input class="form-control" id="f-title" value="${esc(e?.title || '')}" placeholder="例如：113-1 微積分期中考" required></div>
        <div class="form-row">
          <div class="form-group"><label>科目 <span class="required">*</span></label><select class="form-control" id="f-subject" required><option value="">-- 請選擇 --</option>${subjectOptions(e?.subject_id)}</select></div>
          <div class="form-group"><label>教授 <span class="required">*</span></label><select class="form-control" id="f-professor" required><option value="">-- 請選擇 --</option>${professorOptions(e?.professor_id)}</select></div>
        </div>
        <div class="form-row">
          <div class="form-group"><label>學年度 <span class="required">*</span></label><input class="form-control" id="f-year" value="${esc(e?.year || '')}" placeholder="例如：113" required></div>
          <div class="form-group"><label>學期 <span class="required">*</span></label><select class="form-control" id="f-semester" required><option value="">-- 請選擇 --</option><option value="1" ${e?.semester==='1'?'selected':''}>上學期 (1)</option><option value="2" ${e?.semester==='2'?'selected':''}>下學期 (2)</option></select></div>
          <div class="form-group"><label>考試類型 <span class="required">*</span></label><select class="form-control" id="f-type" required><option value="">-- 請選擇 --</option><option value="期中考" ${e?.exam_type==='期中考'?'selected':''}>期中考</option><option value="期末考" ${e?.exam_type==='期末考'?'selected':''}>期末考</option><option value="小考" ${e?.exam_type==='小考'?'selected':''}>小考</option></select></div>
        </div>
        <div class="form-group"><label>題目內容</label><textarea class="form-control" id="f-content" placeholder="請輸入考古題內容...">${esc(e?.content || '')}</textarea></div>
        <div class="form-actions"><button class="btn btn-primary" type="submit">✔️ ${e ? '更新' : '新增'}</button><a class="btn btn-secondary" href="#/exams">✕ 取消</a></div>
      </form></div></div>`;
  },

  // ===== SEARCH =====
  searchPage() {
    const kw = window._searchKw || '', sid = window._searchSub || '', pid = window._searchProf || '', yr = window._searchYear || '';
    const subs = DB.getSubjects(), profs = DB.getProfessors(), years = DB.getYears();
    const filters = {};
    if (sid) filters.subject_id = parseInt(sid);
    if (pid) filters.professor_id = parseInt(pid);
    if (yr) filters.year = yr;
    const results = kw ? DB.search(kw, filters) : [];
    let resultHTML;
    if (kw && results.length) {
      resultHTML = `<p style="color:var(--text-muted);margin-bottom:1rem">搜尋「<strong>${esc(kw)}</strong>」，找到 ${results.length} 筆結果</p>
        <div class="card"><div class="table-wrap"><table><thead><tr><th>標題</th><th>科目</th><th>教授</th><th>學年度</th><th>類型</th></tr></thead><tbody>
        ${results.map(e => `<tr style="cursor:pointer" onclick="navigate('#/exams/${e.id}')"><td><strong>${esc(e.title)}</strong></td>
          <td><span class="badge badge-primary">${esc(DB.subjectName(e.subject_id))}</span></td>
          <td>${esc(DB.professorName(e.professor_id))}</td><td>${esc(e.year)}-${esc(e.semester)}</td>
          <td><span class="badge badge-secondary">${esc(e.exam_type)}</span></td></tr>`).join('')}
        </tbody></table></div></div>`;
    } else if (kw) {
      resultHTML = `<div class="empty-state"><div class="icon">😞</div><p>找不到符合「${esc(kw)}」的考古題</p></div>`;
    } else {
      resultHTML = `<div class="empty-state"><div class="icon">🔍</div><p>輸入關鍵字開始搜尋</p></div>`;
    }
    return `<h1 style="margin-bottom:1.5rem">🔍 搜尋考古題</h1>
      <div class="card" style="margin-bottom:1.5rem"><div class="card-body"><div class="search-filters">
        <div class="form-group"><label>關鍵字</label><input class="form-control" id="sf-kw" value="${esc(kw)}" placeholder="輸入關鍵字搜尋..."></div>
        <div class="form-group"><label>科目</label><select class="form-control" id="sf-sub"><option value="">全部</option>${subs.map(s=>`<option value="${s.id}" ${sid==s.id?'selected':''}>${esc(s.name)}</option>`).join('')}</select></div>
        <div class="form-group"><label>教授</label><select class="form-control" id="sf-prof"><option value="">全部</option>${profs.map(p=>`<option value="${p.id}" ${pid==p.id?'selected':''}>${esc(p.name)}</option>`).join('')}</select></div>
        <div class="form-group"><label>學年度</label><select class="form-control" id="sf-year"><option value="">全部</option>${years.map(y=>`<option value="${y}" ${yr==y?'selected':''}>${y}</option>`).join('')}</select></div>
        <div class="form-group"><button class="btn btn-primary btn-sm" onclick="doSearch()">🔍 搜尋</button></div>
      </div></div></div>${resultHTML}`;
  }
};

function esc(str) { 
  if (str == null) return '';
  const d = document.createElement('div'); 
  d.textContent = String(str); 
  return d.innerHTML; 
}

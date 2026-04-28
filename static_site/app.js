/* ===== Router & Actions ===== */
function navigate(hash) { window.location.hash = hash; }

function router() {
  const hash = window.location.hash || '#/';
  const app = document.getElementById('app');
  let html = '';

  if (hash === '#/' || hash === '') html = Pages.home();
  else if (hash === '#/subjects') html = Pages.subjectList();
  else if (hash === '#/subjects/create') html = Pages.subjectForm();
  else if (hash.match(/^#\/subjects\/(\d+)\/edit$/)) html = Pages.subjectForm(parseInt(hash.match(/(\d+)/)[1]));
  else if (hash.match(/^#\/subjects\/(\d+)$/)) html = Pages.subjectDetail(parseInt(hash.match(/(\d+)/)[1]));
  else if (hash === '#/professors') html = Pages.professorList();
  else if (hash === '#/professors/create') html = Pages.professorForm();
  else if (hash.match(/^#\/professors\/(\d+)\/edit$/)) html = Pages.professorForm(parseInt(hash.match(/(\d+)/)[1]));
  else if (hash.match(/^#\/professors\/(\d+)$/)) html = Pages.professorDetail(parseInt(hash.match(/(\d+)/)[1]));
  else if (hash === '#/exams') html = Pages.examList();
  else if (hash === '#/exams/create') html = Pages.examForm();
  else if (hash.match(/^#\/exams\/(\d+)\/edit$/)) html = Pages.examForm(parseInt(hash.match(/(\d+)/)[1]));
  else if (hash.match(/^#\/exams\/(\d+)$/)) html = Pages.examDetail(parseInt(hash.match(/(\d+)/)[1]));
  else if (hash === '#/search') html = Pages.searchPage();
  else html = Pages.home();

  app.innerHTML = `<div class="page-enter">${html}</div>`;
  window.scrollTo(0, 0);
}

/* ===== Form Handlers ===== */
function saveSubject(e, id) {
  e.preventDefault();
  const name = document.getElementById('f-name').value.trim();
  const desc = document.getElementById('f-desc').value.trim();
  if (!name) { alert('科目名稱為必填欄位！'); return; }
  if (id) { DB.updateSubject(id, name, desc); setFlash('科目更新成功！'); navigate('#/subjects/' + id); }
  else { DB.createSubject(name, desc); setFlash('科目新增成功！'); navigate('#/subjects'); }
}

function deleteSubject(id) {
  if (!confirm('確定要刪除此科目嗎？')) return;
  DB.deleteSubject(id);
  setFlash('科目已刪除！');
  navigate('#/subjects');
}

function saveProfessor(e, id) {
  e.preventDefault();
  const name = document.getElementById('f-name').value.trim();
  const sid = document.getElementById('f-subject').value;
  if (!name) { alert('教授姓名為必填欄位！'); return; }
  const subjectId = sid ? parseInt(sid) : null;
  if (id) { DB.updateProfessor(id, name, subjectId); setFlash('教授資訊更新成功！'); navigate('#/professors/' + id); }
  else { DB.createProfessor(name, subjectId); setFlash('教授新增成功！'); navigate('#/professors'); }
}

function deleteProfessor(id) {
  if (!confirm('確定要刪除此教授嗎？')) return;
  DB.deleteProfessor(id);
  setFlash('教授已刪除！');
  navigate('#/professors');
}

function saveExam(e, id) {
  e.preventDefault();
  const data = {
    title: document.getElementById('f-title').value.trim(),
    subject_id: parseInt(document.getElementById('f-subject').value),
    professor_id: parseInt(document.getElementById('f-professor').value),
    year: document.getElementById('f-year').value.trim(),
    semester: document.getElementById('f-semester').value,
    exam_type: document.getElementById('f-type').value,
    content: document.getElementById('f-content').value.trim()
  };
  if (!data.title) { alert('標題為必填欄位！'); return; }
  if (id) { DB.updateExam(id, data); setFlash('考古題更新成功！'); navigate('#/exams/' + id); }
  else { const created = DB.createExam(data); setFlash('考古題新增成功！'); navigate('#/exams'); }
}

function deleteExam(id) {
  if (!confirm('確定要刪除此考古題嗎？')) return;
  DB.deleteExam(id);
  setFlash('考古題已刪除！');
  navigate('#/exams');
}

/* ===== Exam Filters ===== */
function filterExams() {
  window._examFilterSubject = document.getElementById('ef-sub').value;
  window._examFilterProf = document.getElementById('ef-prof').value;
  window._examFilterYear = document.getElementById('ef-year').value;
  window._examFilterType = document.getElementById('ef-type').value;
  router();
}
function clearExamFilters() {
  window._examFilterSubject = ''; window._examFilterProf = ''; window._examFilterYear = ''; window._examFilterType = '';
  router();
}

/* ===== Search ===== */
function doSearch() {
  window._searchKw = document.getElementById('sf-kw').value.trim();
  window._searchSub = document.getElementById('sf-sub').value;
  window._searchProf = document.getElementById('sf-prof').value;
  window._searchYear = document.getElementById('sf-year').value;
  router();
}
function navSearch() {
  const kw = document.getElementById('nav-q').value.trim();
  if (kw) { window._searchKw = kw; navigate('#/search'); }
}

/* ===== Init ===== */
window.addEventListener('hashchange', router);
window.addEventListener('DOMContentLoaded', router);

/* ===== localStorage Database Layer ===== */
const DB = {
  _get(key) {
    return JSON.parse(localStorage.getItem(key) || '[]');
  },
  _set(key, data) {
    localStorage.setItem(key, JSON.stringify(data));
  },
  _nextId(key) {
    const items = this._get(key);
    return items.length ? Math.max(...items.map(i => i.id)) + 1 : 1;
  },
  // --- Subjects ---
  getSubjects() { return this._get('subjects'); },
  getSubject(id) { return this._get('subjects').find(s => s.id === id); },
  createSubject(name, description) {
    const items = this._get('subjects');
    const item = { id: this._nextId('subjects'), name, description, created_at: new Date().toLocaleString('zh-TW') };
    items.push(item);
    this._set('subjects', items);
    return item;
  },
  updateSubject(id, name, description) {
    const items = this._get('subjects');
    const i = items.findIndex(s => s.id === id);
    if (i >= 0) { items[i].name = name; items[i].description = description; }
    this._set('subjects', items);
  },
  deleteSubject(id) {
    this._set('subjects', this._get('subjects').filter(s => s.id !== id));
  },
  // --- Professors ---
  getProfessors() { return this._get('professors'); },
  getProfessor(id) { return this._get('professors').find(p => p.id === id); },
  createProfessor(name, subject_id) {
    const items = this._get('professors');
    const item = { id: this._nextId('professors'), name, subject_id, created_at: new Date().toLocaleString('zh-TW') };
    items.push(item);
    this._set('professors', items);
    return item;
  },
  updateProfessor(id, name, subject_id) {
    const items = this._get('professors');
    const i = items.findIndex(p => p.id === id);
    if (i >= 0) { items[i].name = name; items[i].subject_id = subject_id; }
    this._set('professors', items);
  },
  deleteProfessor(id) {
    this._set('professors', this._get('professors').filter(p => p.id !== id));
  },
  getProfessorsBySubject(sid) {
    return this._get('professors').filter(p => p.subject_id === sid);
  },
  // --- Exams ---
  getExams(filters) {
    let items = this._get('exams');
    if (filters) {
      if (filters.subject_id) items = items.filter(e => e.subject_id === filters.subject_id);
      if (filters.professor_id) items = items.filter(e => e.professor_id === filters.professor_id);
      if (filters.year) items = items.filter(e => e.year === filters.year);
      if (filters.exam_type) items = items.filter(e => e.exam_type === filters.exam_type);
    }
    return items.sort((a, b) => (b.year || '').localeCompare(a.year || '') || b.id - a.id);
  },
  getExam(id) { return this._get('exams').find(e => e.id === id); },
  createExam(data) {
    const items = this._get('exams');
    data.id = this._nextId('exams');
    data.created_at = new Date().toLocaleString('zh-TW');
    data.updated_at = data.created_at;
    items.push(data);
    this._set('exams', items);
    return data;
  },
  updateExam(id, data) {
    const items = this._get('exams');
    const i = items.findIndex(e => e.id === id);
    if (i >= 0) { Object.assign(items[i], data); items[i].updated_at = new Date().toLocaleString('zh-TW'); }
    this._set('exams', items);
  },
  deleteExam(id) {
    this._set('exams', this._get('exams').filter(e => e.id !== id));
  },
  getExamsBySubject(sid) { return this.getExams({ subject_id: sid }); },
  getExamsByProfessor(pid) { return this.getExams({ professor_id: pid }); },
  getYears() {
    const years = [...new Set(this._get('exams').map(e => e.year).filter(Boolean))];
    return years.sort((a, b) => b.localeCompare(a));
  },
  search(keyword, filters) {
    let items = this._get('exams');
    if (keyword) {
      const kw = keyword.toLowerCase();
      items = items.filter(e => (e.title || '').toLowerCase().includes(kw) || (e.content || '').toLowerCase().includes(kw));
    }
    if (filters) {
      if (filters.subject_id) items = items.filter(e => e.subject_id === filters.subject_id);
      if (filters.professor_id) items = items.filter(e => e.professor_id === filters.professor_id);
      if (filters.year) items = items.filter(e => e.year === filters.year);
    }
    return items.sort((a, b) => b.id - a.id);
  },
  // helpers
  subjectName(id) { const s = this.getSubject(id); return s ? s.name : '—'; },
  professorName(id) { const p = this.getProfessor(id); return p ? p.name : '—'; }
};

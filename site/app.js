'use strict';
const $ = (id) => document.getElementById(id);
const state = { term: '', course: '', kind: '', q: '' };
let catalog;
const fileIcon = '<svg class="file-icon" viewBox="0 0 24 28" fill="none" stroke="currentColor" stroke-width="1.3" aria-hidden="true"><path d="M4 1h10l6 6v20H4z"/><path d="M14 1v7h6M8 14h8M8 18h8M8 22h5"/></svg>';
const downloadIcon = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M12 3v12m-5-5 5 5 5-5M4 16v5h16v-5"/></svg>';
const collator = new Intl.Collator('zh-CN', { numeric: true });
const sizeText = (size) => size < 1024 * 1024 ? `${Math.max(1, Math.round(size / 1024))} KB` : `${(size / 1024 / 1024).toFixed(1)} MB`;
function node(tag, className, text) {
  const el = document.createElement(tag);
  if (className) el.className = className;
  if (text !== undefined) el.textContent = text;
  return el;
}
function external(link, href) { link.href = href; link.target = '_blank'; link.rel = 'noopener'; return link; }
function readState() {
  const params = new URLSearchParams(location.search);
  for (const key of Object.keys(state)) state[key] = params.get(key) || '';
  if (!catalog.terms.includes(state.term)) state.term = '';
  if (!['', '试卷', '教材', '笔记'].includes(state.kind)) state.kind = '';
  if (!catalog.files.some(f => f.course === state.course && (!state.term || f.term === state.term))) state.course = '';
}
function saveState() {
  const params = new URLSearchParams();
  for (const [key, value] of Object.entries(state)) if (value) params.set(key, value);
  history.replaceState(null, '', location.pathname + (params.size ? `?${params}` : '') + location.hash);
}
function renderNav() {
  $('terms').replaceChildren();
  for (const term of ['', ...catalog.terms]) {
    const btn = node('button', 'term');
    btn.append(node('span', '', term || '全部学期'));
    btn.append(node('small', '', String(catalog.files.filter(f => !term || f.term === term).length)));
    btn.setAttribute('aria-current', String(state.term === term));
    btn.addEventListener('click', () => { state.term = term; state.course = ''; update(); });
    $('terms').append(btn);
  }
  $('kinds').replaceChildren();
  for (const kind of ['', '试卷', '教材', '笔记']) {
    const btn = node('button', 'kind', kind || '全部');
    btn.setAttribute('aria-pressed', String(state.kind === kind));
    btn.addEventListener('click', () => { state.kind = kind; update(); });
    $('kinds').append(btn);
  }
  const courses = [...new Set(catalog.files.filter(f => !state.term || f.term === state.term).map(f => f.course))].sort(collator.compare);
  $('course').replaceChildren(new Option('全部课程', ''), ...courses.map(c => new Option(c, c)));
  $('course').value = state.course;
}
function openPreview(file) {
  $('preview-title').textContent = file.filename;
  $('preview-open').href = file.preview;
  $('preview-download').href = file.download;
  $('preview-download').download = file.filename;
  $('pdf').src = `${file.preview}#view=FitH`;
  $('preview').showModal();
}
function fileRow(file) {
  const row = node('div', 'file');
  row.innerHTML = fileIcon;
  const info = node('div', 'file-info');
  let title;
  if (file.preview) {
    title = node('button', 'file-title', file.name);
    title.addEventListener('click', () => openPreview(file));
  } else {
    title = external(node('a', 'file-title', file.name), file.source);
  }
  const meta = node('div', 'file-meta');
  for (const value of [file.category === file.kind ? '' : file.category, file.format, sizeText(file.size)].filter(Boolean)) meta.append(node('span', '', value));
  info.append(title, meta);
  const actions = node('div', 'file-actions');
  if (file.preview) {
    const btn = node('button', 'preview-button', '预览');
    btn.setAttribute('aria-label', `预览 ${file.filename}`);
    btn.addEventListener('click', () => openPreview(file));
    actions.append(btn);
  } else {
    actions.append(external(node('a', 'preview-button', '查看'), file.source));
  }
  const download = node('a', 'download');
  download.href = file.download;
  download.download = file.filename;
  if (!file.preview) { download.target = '_blank'; download.rel = 'noopener'; }
  download.setAttribute('aria-label', `下载 ${file.filename}`);
  download.title = '下载';
  download.innerHTML = downloadIcon;
  actions.append(download);
  row.append(info, actions);
  return row;
}
function renderResults() {
  const tokens = state.q.trim().toLocaleLowerCase().split(/\s+/).filter(Boolean);
  const files = catalog.files.filter(f => (!state.term || f.term === state.term) && (!state.course || f.course === state.course) && (!state.kind || f.kind === state.kind) && tokens.every(t => `${f.name} ${f.course} ${f.term} ${f.category} ${f.format}`.toLocaleLowerCase().includes(t)));
  $('result-count').textContent = `${state.term || '全部学期'} · ${files.length} 份资料`;
  $('reset').hidden = !Object.values(state).some(Boolean);
  const groups = new Map();
  for (const file of files) {
    const key = `${file.term}/${file.course}`;
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key).push(file);
  }
  const fragment = document.createDocumentFragment();
  for (const group of groups.values()) {
    const section = node('section', 'course-group');
    const heading = node('div', 'group-heading');
    heading.append(node('h2', '', group[0].course), node('span', '', `${group[0].term} / ${group.length} 份`));
    const columns = node('div', 'course-columns');
    columns.classList.toggle('single-category', Boolean(state.kind));
    for (const kind of state.kind ? [state.kind] : ['试卷', '教材', '笔记']) {
      const column = node('section', 'material-column');
      column.append(node('h3', 'column-heading', kind));
      const items = group.filter(file => file.kind === kind).sort((a, b) => collator.compare(b.name, a.name));
      const list = node('div', 'file-list');
      const periods = kind === '试卷' ? ['期中', '期末', '期次待核'].map(period => ({
        period,
        files: items.filter(file => (['期中', '期末'].includes(file.category) ? file.category : '期次待核') === period),
      })).filter(group => group.files.length) : [];
      if (periods.length > 1) {
        for (const group of periods) {
          const examGroup = node('section', 'exam-group');
          examGroup.append(node('h4', 'exam-heading', group.period));
          for (const file of group.files) examGroup.append(fileRow(file));
          list.append(examGroup);
        }
      } else {
        for (const file of items) list.append(fileRow(file));
      }
      if (!items.length) list.append(node('p', 'column-empty', state.q.trim() ? '暂无匹配资料' : '暂无资料'));
      column.append(list); columns.append(column);
    }
    section.append(heading, columns); fragment.append(section);
  }
  if (!files.length) {
    const empty = node('div', 'empty');
    empty.append(node('h2', '', '没有找到相关资料'), node('p', '', '试试其他关键词，或清除筛选条件。'));
    fragment.append(empty);
  }
  $('results').replaceChildren(fragment);
  $('results').setAttribute('aria-busy', 'false');
}
function update() { renderNav(); renderResults(); saveState(); }
$('search-form').addEventListener('submit', e => e.preventDefault());
$('query').addEventListener('input', e => { if (!catalog) return; state.q = e.target.value; renderResults(); saveState(); });
$('course').addEventListener('change', e => { state.course = e.target.value; renderResults(); saveState(); });
$('reset').addEventListener('click', () => { for (const key of Object.keys(state)) state[key] = ''; $('query').value = ''; update(); });
$('preview-close').addEventListener('click', () => $('preview').close());
$('preview').addEventListener('close', () => $('pdf').removeAttribute('src'));
$('preview').addEventListener('click', e => { if (e.target === $('preview')) { const r = $('preview').getBoundingClientRect(); if (e.clientX < r.left || e.clientX > r.right || e.clientY < r.top || e.clientY > r.bottom) $('preview').close(); } });
document.addEventListener('keydown', e => { if (e.key === '/' && !['INPUT', 'TEXTAREA', 'SELECT'].includes(document.activeElement.tagName) && !$('preview').open) { e.preventDefault(); $('query').focus(); } });
window.addEventListener('popstate', () => { if (!catalog) return; readState(); $('query').value = state.q; renderNav(); renderResults(); });
async function load() {
  try {
    const response = await fetch('catalog.json');
    if (!response.ok) throw new Error('Catalog request failed');
    catalog = await response.json();
    if (!Array.isArray(catalog.files) || !Array.isArray(catalog.terms)) throw new Error('Invalid catalog');
    readState(); $('query').value = state.q;
    $('summary').textContent = `${new Set(catalog.files.map(f => `${f.term}/${f.course}`)).size} 门课程 · ${catalog.files.length} 份资料`;
    update();
  } catch {
    $('result-count').textContent = '资料目录加载失败';
    $('results').setAttribute('aria-busy', 'false');
    const empty = node('div', 'empty');
    empty.append(node('h2', '', '暂时无法加载资料'), node('p', '', '请刷新页面重试，或直接访问 GitHub 仓库。'));
    empty.append(external(node('a', 'preview-button', '打开 GitHub ↗'), 'https://github.com/ch-z-hc/XMU-AM'));
    $('results').replaceChildren(empty);
  }
}
load();

/* =========================================================
   TRACE NEST UI — INFRASTRUCTURE-GRADE CLIENT
   ========================================================= */

const API_BASE = "/tracenest/api";

/* -------------------------------
   STATE
-------------------------------- */
let currentFile = null;
let logLines = [];
let activeLevels = new Set(); // empty = ALL
let searchTerm = "";
let currentPage = 1;

const PAGE_SIZE = 50;

/* -------------------------------
   DOM
-------------------------------- */
const tbody = document.getElementById("log-body");
const paginationEl = document.getElementById("pagination");
const searchInput = document.querySelector(".search-input");
const fileList = document.getElementById("file-list");
const container = document.getElementById("app-container");
const badges = document.querySelectorAll(".badge-filter");

/* -------------------------------
   PARSING CORE (DO NOT BREAK)
-------------------------------- */
function tryParseJSON(line) {
  try {
    const jsonStart = line.indexOf("{");
    if (jsonStart === -1) return null;
    return JSON.parse(line.slice(jsonStart));
  } catch {
    return null;
  }
}

function extractTimestamp(line, obj) {
  return (
    obj?.timestamp ||
    obj?.time ||
    (line.match(/\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2}/) || [])[0] ||
    "—"
  );
}

function extractEnv(line, obj) {
  return (
    obj?.env ||
    obj?.environment ||
    (line.match(/\[(local|dev|prod|production|staging)\]/i) || [])[1] ||
    "local"
  );
}

function extractLevel(line, obj) {
  const lvl = obj?.level || "";
  const l = (lvl || line).toLowerCase();

  if (l.includes("error")) return "error";
  if (l.includes("warn")) return "warning";
  if (l.includes("debug")) return "debug";
  return "info";
}

function extractMessage(line, obj) {
  return obj?.message || obj?.msg || line;
}

/* -------------------------------
   FILTERING
-------------------------------- */
function matchesSearch(line) {
  return !searchTerm || line.toLowerCase().includes(searchTerm);
}

/* -------------------------------
   API
-------------------------------- */
async function fetchFiles() {
  const r = await fetch(`${API_BASE}/logs`);
  return (await r.json()).logs || [];
}

async function fetchLines(file) {
  const r = await fetch(`${API_BASE}/logs/${file}?limit=4000`);
  return (await r.json()).lines || [];
}

/* -------------------------------
   SIDEBAR
-------------------------------- */
async function renderSidebar() {
  fileList.innerHTML = "";
  const files = await fetchFiles();
  if (!files.length) return;

  files.forEach((file, idx) => {
    const div = document.createElement("div");
    div.className = "file-item";
    if (idx === 0) div.classList.add("active");
    div.innerHTML = `<span>${file}</span>`;
    div.onclick = () => selectFile(file, div);
    fileList.appendChild(div);
  });

  selectFile(files[0], fileList.firstChild);
}

async function selectFile(file, el) {
  document.querySelectorAll(".file-item").forEach(f =>
    f.classList.remove("active")
  );
  el.classList.add("active");

  currentFile = file;
  logLines = await fetchLines(file);

  resetState();
  renderTable();
}

/* -------------------------------
   FILTERED DATA
-------------------------------- */
function filteredLines() {
  return logLines.filter(line => {
    const obj = tryParseJSON(line);
    const level = extractLevel(line, obj);

    if (activeLevels.size && !activeLevels.has(level)) return false;
    if (!matchesSearch(line)) return false;

    return true;
  });
}

/* -------------------------------
   TABLE RENDER
-------------------------------- */
function renderTable() {
  tbody.innerHTML = "";

  const data = filteredLines();
  const start = (currentPage - 1) * PAGE_SIZE;
  const page = data.slice(start, start + PAGE_SIZE);

  page.forEach(line => {
    const obj = tryParseJSON(line);

    const level = extractLevel(line, obj);
    const time = extractTimestamp(line, obj);
    const env = extractEnv(line, obj);
    const msg = extractMessage(line, obj);

    const row = document.createElement("tr");
    row.className = "log-row";
    row.innerHTML = `
      <td><span class="text-${level} fw-bold">● ${level}</span></td>
      <td class="text-muted small">${time}</td>
      <td class="text-muted small">${env}</td>
      <td class="log-desc truncate">${msg}</td>
      <td></td>
    `;

    const expand = document.createElement("tr");
    expand.className = "log-expand";
    expand.innerHTML = `
      <td colspan="5">
        <pre class="expanded-content">${
          obj ? JSON.stringify(obj, null, 2) : line
        }</pre>
      </td>
    `;

    row.onclick = () => {
      document.querySelectorAll(".log-expand.active")
        .forEach(e => e !== expand && e.classList.remove("active"));
      expand.classList.toggle("active");
    };

    tbody.appendChild(row);
    tbody.appendChild(expand);
  });

  renderPagination(data.length);
}

/* -------------------------------
   PAGINATION
-------------------------------- */
function renderPagination(total) {
  paginationEl.innerHTML = "";
  const pages = Math.ceil(total / PAGE_SIZE);
  if (pages <= 1) return;

  for (let i = 1; i <= pages; i++) {
    const s = document.createElement("span");
    s.textContent = i;
    s.className = i === currentPage ? "active" : "";
    s.onclick = () => {
      currentPage = i;
      renderTable();
    };
    paginationEl.appendChild(s);
  }
}

/* -------------------------------
   SEARCH
-------------------------------- */
searchInput.oninput = e => {
  searchTerm = e.target.value.toLowerCase();
  currentPage = 1;
  renderTable();
};

/* -------------------------------
   LEVEL FILTERS (WITH ALL)
-------------------------------- */
badges.forEach(badge => {
  badge.onclick = () => {
    const lvl = badge.dataset.level;

    if (lvl === "all") {
      activeLevels.clear();
      badges.forEach(b => (b.style.opacity = "1"));
    } else {
      activeLevels.has(lvl)
        ? activeLevels.delete(lvl)
        : activeLevels.add(lvl);

      document.querySelector('[data-level="all"]').style.opacity = "0.4";
      badge.style.opacity = activeLevels.has(lvl) ? "1" : "0.4";
    }

    currentPage = 1;
    renderTable();
  };
});

/* -------------------------------
   THEME
-------------------------------- */
function setTheme(theme) {
  container.className = `theme-${theme}`;
  localStorage.setItem("tracenest-theme", theme);
}

document.querySelectorAll("[data-theme]").forEach(btn =>
  btn.onclick = () => setTheme(btn.dataset.theme)
);

const savedTheme = localStorage.getItem("tracenest-theme");
if (savedTheme) setTheme(savedTheme);

/* -------------------------------
   RESET
-------------------------------- */
function resetState() {
  activeLevels.clear();
  searchTerm = "";
  currentPage = 1;
  searchInput.value = "";
  badges.forEach(b => (b.style.opacity = "1"));
}

/* -------------------------------
   INIT
-------------------------------- */
renderSidebar();

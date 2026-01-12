/* =========================================================
   TRACE NEST UI — FULL CLIENT LOGIC
   ========================================================= */

/* -------------------------------
   MOCK DATA (PER FILE)
-------------------------------- */
const FILE_LOGS = {
  "laravel.log": [
    {
      level: "error",
      time: "2022-08-25 11:23:07",
      env: "local",
      message: 'Command "composer" is not defined.',
      details: {
        exception: "CommandNotFoundException",
        file: "/app/Console/Kernel.php:42",
        trace_id: "err-001"
      }
    },
    {
      level: "warning",
      time: "2022-08-25 11:21:11",
      env: "local",
      message: "Deprecated config key detected.",
      details: {
        key: "legacy_timeout",
        suggestion: "Use request_timeout",
        trace_id: "warn-002"
      }
    },
    {
      level: "info",
      time: "2022-08-25 11:18:41",
      env: "local",
      message: "User login successful.",
      details: {
        user_id: 42,
        ip: "192.168.1.10",
        trace_id: "info-003"
      }
    },
    {
      level: "debug",
      time: "2022-08-25 11:17:01",
      env: "local",
      message: "Cache key resolved.",
      details: {
        cache_key: "user_profile_42",
        ttl: 3600,
        trace_id: "dbg-004"
      }
    },
    {
      level: "error",
      time: "2022-08-25 11:15:55",
      env: "local",
      message: "Database connection failed.",
      details: {
        database: "postgres",
        host: "db.internal",
        retry: false,
        trace_id: "err-005"
      }
    },
    {
      level: "info",
      time: "2022-08-25 11:14:21",
      env: "local",
      message: "Background job completed.",
      details: {
        job: "email_dispatch",
        duration_ms: 842,
        trace_id: "info-006"
      }
    }
  ],

  "laravel-2022-08-23.log": [],
  "laravel-2022-07-28.log": []
};

/* -------------------------------
   STATE
-------------------------------- */
let currentFile = "laravel.log";
let activeLevels = new Set();
let searchTerm = "";
let currentPage = 1;

const PAGE_SIZE = 5;

/* -------------------------------
   DOM REFERENCES
-------------------------------- */
const tbody = document.querySelector("tbody");
const paginationEl = document.getElementById("pagination");
const searchInput = document.querySelector(".search-input");
const container = document.getElementById("app-container");

/* -------------------------------
   HELPERS
-------------------------------- */
function levelLabel(level) {
  return level.charAt(0).toUpperCase() + level.slice(1);
}

function matchesSearch(log) {
  if (!searchTerm) return true;
  const haystack = (
    log.message +
    " " +
    JSON.stringify(log.details)
  ).toLowerCase();
  return haystack.includes(searchTerm);
}

/* -------------------------------
   FILTERED LOGS
-------------------------------- */
function getFilteredLogs() {
  const logs = FILE_LOGS[currentFile] || [];

  return logs.filter(log => {
    if (activeLevels.size && !activeLevels.has(log.level)) return false;
    if (!matchesSearch(log)) return false;
    return true;
  });
}

/* -------------------------------
   RENDER TABLE
-------------------------------- */
function renderTable() {
  tbody.innerHTML = "";

  const filtered = getFilteredLogs();
  const start = (currentPage - 1) * PAGE_SIZE;
  const pageLogs = filtered.slice(start, start + PAGE_SIZE);

  pageLogs.forEach(log => {
    const row = document.createElement("tr");
    row.className = "log-row";
    row.innerHTML = `
      <td><span class="text-${log.level} fw-bold">● ${levelLabel(log.level)}</span></td>
      <td class="text-muted small">${log.time}</td>
      <td class="text-muted small">${log.env}</td>
      <td class="log-desc truncate">${log.message}</td>
      <td class="text-muted text-end small"></td>
    `;

    const expandRow = document.createElement("tr");
    expandRow.className = "log-expand";
    expandRow.innerHTML = `
      <td colspan="5">
        <pre class="expanded-content">${JSON.stringify(log.details, null, 2)}</pre>
      </td>
    `;

    row.addEventListener("click", () => {
      // collapse others
      document.querySelectorAll(".log-expand.active").forEach(el => {
        if (el !== expandRow) el.classList.remove("active");
      });
      expandRow.classList.toggle("active");
    });

    tbody.appendChild(row);
    tbody.appendChild(expandRow);
  });

  renderPagination(filtered.length);
}

/* -------------------------------
   PAGINATION
-------------------------------- */
function renderPagination(totalCount) {
  paginationEl.innerHTML = "";
  const totalPages = Math.ceil(totalCount / PAGE_SIZE);

  if (totalPages <= 1) return;

  for (let i = 1; i <= totalPages; i++) {
    const btn = document.createElement("span");
    btn.textContent = i;
    btn.className = i === currentPage ? "active" : "";
    btn.addEventListener("click", () => {
      currentPage = i;
      renderTable();
    });
    paginationEl.appendChild(btn);
  }
}

/* -------------------------------
   SEARCH
-------------------------------- */
searchInput.addEventListener("input", e => {
  searchTerm = e.target.value.toLowerCase();
  currentPage = 1;
  renderTable();
});

/* -------------------------------
   LEVEL FILTERS
-------------------------------- */
document.querySelectorAll(".badge-filter").forEach(badge => {
  badge.addEventListener("click", () => {
    const level = badge.dataset.level;

    if (activeLevels.has(level)) {
      activeLevels.delete(level);
      badge.style.opacity = "0.4";
    } else {
      activeLevels.add(level);
      badge.style.opacity = "1";
    }

    currentPage = 1;
    renderTable();
  });
});

/* -------------------------------
   SIDEBAR FILE SWITCH
-------------------------------- */
document.querySelectorAll(".file-item").forEach(item => {
  item.addEventListener("click", () => {
    document.querySelectorAll(".file-item").forEach(i =>
      i.classList.remove("active")
    );
    item.classList.add("active");

    currentFile = item.querySelector("span").innerText.trim();

    // reset state
    activeLevels.clear();
    searchTerm = "";
    currentPage = 1;
    searchInput.value = "";

    document.querySelectorAll(".badge-filter").forEach(b =>
      (b.style.opacity = "1")
    );

    renderTable();
  });
});

/* -------------------------------
   THEME HANDLING
-------------------------------- */
document.querySelectorAll("[data-theme]").forEach(btn => {
  btn.addEventListener("click", () => {
    setTheme(btn.dataset.theme);
  });
});

function setTheme(theme) {
  container.className = "";
  container.classList.add(`theme-${theme}`);
  localStorage.setItem("tracenest-theme", theme);
}

const savedTheme = localStorage.getItem("tracenest-theme");
if (savedTheme) {
  setTheme(savedTheme);
}

/* -------------------------------
   INIT
-------------------------------- */
renderTable();

/* =========================================================
   TRACE NEST UI — V2
   ========================================================= */

   const API_BASE = "/tracenest/api";

   /* -------------------------------
      STATE
   -------------------------------- */
   let currentFile = null;
   let rawLinesCache = [];
   let parsedLogsCache = [];
   let logLines = []; // Sorted & ready
   
   let activeLevels = new Set(); // empty = ALL
   let searchTerm = "";
   let currentPage = 1;
   let selectedLogId = null;
   
   const PAGE_SIZE = 100;
   
   /* -------------------------------
      DOM ELEMENTS
   -------------------------------- */
   const tbody = document.getElementById("log-body");
   const paginationEl = document.getElementById("pagination");
   const searchInput = document.querySelector(".search-input");
   const fileList = document.getElementById("file-list");
   const container = document.getElementById("app-container");
   const badges = document.querySelectorAll(".level-filters .badge-filter");
   
   const detailsPanel = document.getElementById("detailsPanel");
   const detailsContent = document.getElementById("detailsContent");
   const closeDetailsBtn = document.getElementById("closeDetailsBtn");
   const copyDetailsBtn = document.getElementById("copyDetailsBtn");
   
   const autoRefreshToggle = document.getElementById("autoRefreshToggle");
   const manualRefreshBtn = document.getElementById("manualRefreshBtn");
   const refreshStatus = document.getElementById("refresh-status");
   
   /* -------------------------------
      UTILS
   -------------------------------- */
   function generateId() {
     return 'log_' + Math.random().toString(36).substring(2, 11);
   }
   
   function escapeHtml(unsafe) {
       if (typeof unsafe !== 'string') return unsafe;
       return unsafe
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
   }
   
   function timeAgo(dateString) {
     if (!dateString || dateString === "—") return "—";
     const date = new Date(dateString);
     if (isNaN(date.valueOf())) return dateString;
     
     const seconds = Math.floor((new Date() - date) / 1000);
     if (seconds < 30) return "just now";
     
     let interval = Math.floor(seconds / 31536000);
     if (interval >= 1) return interval + "y ago";
     interval = Math.floor(seconds / 2592000);
     if (interval >= 1) return interval + "mo ago";
     interval = Math.floor(seconds / 86400);
     if (interval >= 1) return interval + "d ago";
     interval = Math.floor(seconds / 3600);
     if (interval >= 1) return interval + "h ago";
     interval = Math.floor(seconds / 60);
     if (interval >= 1) return interval + "m ago";
     return Math.max(0, Math.floor(seconds)) + "s ago";
   }
   
   /* -------------------------------
      PARSING (FORMATTER FIRST)
   -------------------------------- */
   function parseLine(line) {
     const id = generateId();
     // Structured TraceNest log
     try {
       const start = line.indexOf("{");
       if (start !== -1) {
         const obj = JSON.parse(line.slice(start));
         if (obj.schema === "tracenest.v1") {
           return {
             _id: id,
             structured: true,
             level: (obj.level || "INFO").toLowerCase(),
             timestamp: obj.timestamp || obj.ts || "—",
             env: obj.env || "local",
             logger: obj.logger || obj.module || "—",
             message: obj.message || obj.msg || "",
             trace_id: obj.trace_id || null,
             raw: obj,
           };
         }
       }
     } catch {
       // fall through
     }
   
     // Fallback: plain text
     const lower = line.toLowerCase();
     let level = "info";
     if (lower.includes("error") || lower.includes("exception") || lower.includes("traceback")) level = "error";
     else if (lower.includes("warn")) level = "warning";
     else if (lower.includes("debug")) level = "debug";
     else if (lower.includes("success")) level = "success";
   
     return {
       _id: id,
       structured: false,
       level,
       timestamp: "—",
       env: "local",
       logger: "—",
       message: line,
       trace_id: null,
       raw: line,
     };
   }
   
   /* -------------------------------
      FILTERING
   -------------------------------- */
   function matchesSearch(entry) {
     if (!searchTerm) return true;
     // search message, logger, trace_id
     if (entry.message.toLowerCase().includes(searchTerm)) return true;
     if (entry.logger && entry.logger.toLowerCase().includes(searchTerm)) return true;
     if (entry.trace_id && entry.trace_id.toLowerCase().includes(searchTerm)) return true;
     return false;
   }
   
   function filteredEntries() {
     return logLines.filter(entry => {
         if (activeLevels.size && !activeLevels.has(entry.level)) return false;
         if (!matchesSearch(entry)) return false;
         return true;
     });
   }
   
   /* -------------------------------
      API & UPDATES
   -------------------------------- */
   async function fetchFiles() {
     const r = await fetch(`${API_BASE}/logs`);
     return (await r.json()).logs || [];
   }
   
   async function fetchLines(file) {
     const r = await fetch(`${API_BASE}/logs/${file}?limit=5000`);
     return (await r.json()).lines || [];
   }
   
   async function updateLogs(file) {
       const lines = await fetchLines(file);
       if (lines.length !== rawLinesCache.length) {
           // We have new lines or the file was truncated/rotated
           if (lines.length < rawLinesCache.length || lines[0] !== rawLinesCache[0]) {
               // Complete reload (file rotated or cleared)
               rawLinesCache = lines;
               parsedLogsCache = lines.map(parseLine);
           } else {
               // Append new lines
               const newLines = lines.slice(rawLinesCache.length);
               const newParsed = newLines.map(parseLine);
               rawLinesCache = lines;
               parsedLogsCache = [...parsedLogsCache, ...newParsed];
           }
           
           logLines = [...parsedLogsCache].reverse();
           
           // If we are on page 1, auto-render to show new logs.
           // Else just update data, let user keep reading.
           if (currentPage === 1) {
               renderTable();
           }
       }
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
       div.innerHTML = `<span><i class="bi bi-file-text text-muted me-2"></i>${file}</span>`;
       div.onclick = () => selectFile(file, div);
       fileList.appendChild(div);
     });
   
     selectFile(files[0], fileList.firstChild);
   }
   
   async function selectFile(file, el) {
     document.querySelectorAll(".file-item").forEach(f => f.classList.remove("active"));
     el.classList.add("active");
   
     currentFile = file;
     rawLinesCache = [];
     parsedLogsCache = [];
     logLines = [];
     
     closeDetails();
     resetState();
     
     // Full load
     tbody.innerHTML = '<tr><td colspan="4" class="text-center text-muted p-4"><div class="spinner-border spinner-border-sm me-2"></div> Loading logs...</td></tr>';
     await updateLogs(file);
     renderTable();
   }
   
   /* -------------------------------
      TABLE RENDER
   -------------------------------- */
   function getBadgeClass(level) {
       switch(level) {
           case 'trace': return 'badge-trace';
           case 'debug': return 'badge-debug';
           case 'info': return 'badge-info';
           case 'success': return 'badge-success';
           case 'warning': return 'badge-warning';
           case 'error': return 'badge-error';
           case 'fatal': return 'badge-fatal';
           default: return 'badge-info';
       }
   }
   
   function renderTable() {
     tbody.innerHTML = "";
     const data = filteredEntries();
     const start = (currentPage - 1) * PAGE_SIZE;
     const page = data.slice(start, start + PAGE_SIZE);
   
     if (page.length === 0) {
         tbody.innerHTML = '<tr><td colspan="4" class="text-center text-muted p-5">No logs match the current filters.</td></tr>';
         renderPagination(data.length);
         return;
     }
   
     // Use document fragment for performance
     const frag = document.createDocumentFragment();
   
     page.forEach(entry => {
       const row = document.createElement("tr");
       if (entry._id === selectedLogId) row.classList.add("selected");
       
       const displayTime = entry.timestamp === "—" ? "—" : timeAgo(entry.timestamp);
       const titleTime = entry.timestamp === "—" ? "" : new Date(entry.timestamp).toLocaleString();
       
       const badgeCls = getBadgeClass(entry.level);
       const shortLevel = entry.level.length > 5 ? entry.level.substring(0,4) : entry.level;
       
       row.innerHTML = `
         <td class="log-time" title="${titleTime}">${displayTime}</td>
         <td><span class="badge-soft ${badgeCls}">${shortLevel}</span></td>
         <td class="log-logger" title="${escapeHtml(entry.logger)}">${escapeHtml(entry.logger)}</td>
         <td class="log-msg text-break-word">${escapeHtml(entry.message)}</td>
       `;
   
       row.onclick = () => openDetails(entry, row);
       frag.appendChild(row);
     });
   
     tbody.appendChild(frag);
     renderPagination(data.length);
   }
   
   /* -------------------------------
      DETAILS PANEL
   -------------------------------- */
   let currentRawJson = "";
   
   function openDetails(entry, rowEl) {
       selectedLogId = entry._id;
       document.querySelectorAll('#log-body tr').forEach(r => r.classList.remove('selected'));
       if (rowEl) rowEl.classList.add('selected');
       
       detailsPanel.classList.add('open');
       currentRawJson = JSON.stringify(entry.raw, null, 2);
       
       let html = `<div class="p-3">`;
       
       // GENERAL
       html += `
         <div class="detail-section">
             <div class="detail-section-title">General</div>
             <div class="kv-pair"><div class="kv-key">Level</div><div class="kv-val"><span class="badge-soft ${getBadgeClass(entry.level)}">${entry.level}</span></div></div>
             <div class="kv-pair"><div class="kv-key">Timestamp</div><div class="kv-val">${entry.timestamp !== "—" ? new Date(entry.timestamp).toLocaleString() : "—"}</div></div>
             <div class="kv-pair"><div class="kv-key">Environment</div><div class="kv-val">${escapeHtml(entry.env)}</div></div>
             <div class="kv-pair"><div class="kv-key">Logger</div><div class="kv-val">${escapeHtml(entry.logger)}</div></div>
             <div class="kv-pair mt-2"><div class="kv-key">Message</div><div class="kv-val fw-bold">${escapeHtml(entry.message)}</div></div>
         </div>
       `;
       
       // CONTEXT
       if (entry.structured && (entry.trace_id || entry.raw.request_id || entry.raw.client || entry.raw.host)) {
           html += `<div class="detail-section"><div class="detail-section-title">Context</div>`;
           if (entry.trace_id) html += `<div class="kv-pair"><div class="kv-key">Trace ID</div><div class="kv-val">${escapeHtml(entry.trace_id)}</div></div>`;
           if (entry.raw.request_id) html += `<div class="kv-pair"><div class="kv-key">Request ID</div><div class="kv-val">${escapeHtml(entry.raw.request_id)}</div></div>`;
           if (entry.raw.client) html += `<div class="kv-pair"><div class="kv-key">Client</div><div class="kv-val">${escapeHtml(entry.raw.client)}</div></div>`;
           if (entry.raw.duration_ms) html += `<div class="kv-pair"><div class="kv-key">Duration</div><div class="kv-val">${entry.raw.duration_ms} ms</div></div>`;
           html += `</div>`;
       }
       
       // EXCEPTION
       if (entry.structured && (entry.raw.exception || entry.raw.traceback || entry.raw.exc_info)) {
           const excText = entry.raw.exception || entry.raw.traceback || entry.raw.exc_info;
           html += `
             <div class="detail-section">
                 <div class="detail-section-title text-danger">Exception</div>
                 <div class="json-block text-danger border-danger" style="background: rgba(239, 68, 68, 0.05);">${escapeHtml(typeof excText === 'string' ? excText : JSON.stringify(excText, null, 2))}</div>
             </div>
           `;
       }
   
       // JSON PAYLOAD
       html += `
         <div class="detail-section">
             <div class="detail-section-title">Raw Payload</div>
             <div class="json-block">${escapeHtml(currentRawJson)}</div>
         </div>
       `;
       
       html += `</div>`;
       detailsContent.innerHTML = html;
   }
   
   function closeDetails() {
       selectedLogId = null;
       detailsPanel.classList.remove('open');
       document.querySelectorAll('#log-body tr').forEach(r => r.classList.remove('selected'));
   }
   
   closeDetailsBtn.onclick = closeDetails;
   
   copyDetailsBtn.onclick = () => {
       if (currentRawJson) {
           navigator.clipboard.writeText(currentRawJson);
           copyDetailsBtn.innerHTML = `<i class="bi bi-check2 text-success"></i>`;
           setTimeout(() => { copyDetailsBtn.innerHTML = `<i class="bi bi-clipboard"></i>`; }, 2000);
       }
   };
   
   /* -------------------------------
      PAGINATION
   -------------------------------- */
   function renderPagination(total) {
     paginationEl.innerHTML = "";
     const pages = Math.ceil(total / PAGE_SIZE);
     if (pages <= 1) return;
   
     // Simple pagination sliding window
     let startPage = Math.max(1, currentPage - 2);
     let endPage = Math.min(pages, startPage + 4);
     if (endPage - startPage < 4) {
         startPage = Math.max(1, endPage - 4);
     }
   
     if (startPage > 1) {
         const s = document.createElement("span");
         s.innerHTML = "&laquo;";
         s.onclick = () => { currentPage = 1; renderTable(); document.getElementById('table-scroll-area').scrollTop = 0; };
         paginationEl.appendChild(s);
     }
   
     for (let i = startPage; i <= endPage; i++) {
       const s = document.createElement("span");
       s.textContent = i;
       s.className = i === currentPage ? "active shadow-sm" : "";
       s.onclick = () => {
         currentPage = i;
         renderTable();
         document.getElementById('table-scroll-area').scrollTop = 0; // scroll to top
       };
       paginationEl.appendChild(s);
     }
     
     if (endPage < pages) {
         const s = document.createElement("span");
         s.innerHTML = "&raquo;";
         s.onclick = () => { currentPage = pages; renderTable(); document.getElementById('table-scroll-area').scrollTop = 0; };
         paginationEl.appendChild(s);
     }
   }
   
   /* -------------------------------
      SEARCH
   -------------------------------- */
   let searchTimeout;
   searchInput.oninput = e => {
       clearTimeout(searchTimeout);
       searchTimeout = setTimeout(() => {
           searchTerm = e.target.value.toLowerCase();
           currentPage = 1;
           renderTable();
       }, 300); // debounce
   };
   
   /* -------------------------------
      LEVEL FILTERS
   -------------------------------- */
   badges.forEach(badge => {
     badge.onclick = () => {
       const lvl = badge.dataset.level;
   
       if (lvl === "all") {
         activeLevels.clear();
         badges.forEach(b => b.classList.remove('active'));
         badge.classList.add('active');
       } else {
         if (activeLevels.has(lvl)) {
             activeLevels.delete(lvl);
             badge.classList.remove('active');
         } else {
             activeLevels.add(lvl);
             badge.classList.add('active');
         }
         
         document.querySelector('[data-level="all"]').classList.remove('active');
         if (activeLevels.size === 0) {
             document.querySelector('[data-level="all"]').classList.add('active');
         }
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
     
     // Update dropdown active state
     document.querySelectorAll(".theme-menu .dropdown-item").forEach(btn => {
         if(btn.dataset.theme === theme) btn.classList.add('active');
         else btn.classList.remove('active');
     });
   }
   
   document.querySelectorAll("[data-theme]").forEach(btn =>
     btn.onclick = () => setTheme(btn.dataset.theme)
   );
   
   const savedTheme = localStorage.getItem("tracenest-theme") || "dark-blue";
   setTheme(savedTheme);
   
   /* -------------------------------
      RESET
   -------------------------------- */
   function resetState() {
     activeLevels.clear();
     searchTerm = "";
     currentPage = 1;
     searchInput.value = "";
     badges.forEach(b => b.classList.remove('active'));
     document.querySelector('[data-level="all"]').classList.add('active');
   }
   
   /* -------------------------------
      INIT & AUTO-REFRESH
   -------------------------------- */
   renderSidebar();
   
   // Background polling
   setInterval(async () => {
     if (autoRefreshToggle.checked && currentFile) {
       await updateLogs(currentFile);
     }
   }, 3000);
   
   // UI Update for toggle
   autoRefreshToggle.onchange = (e) => {
       if (e.target.checked) {
           refreshStatus.className = 'status-indicator live small fw-medium';
           refreshStatus.innerHTML = '<span class="dot"></span> Live';
       } else {
           refreshStatus.className = 'status-indicator paused small fw-medium';
           refreshStatus.innerHTML = '<span class="dot"></span> Paused';
       }
   };
   
   manualRefreshBtn.onclick = async () => {
       if (currentFile) {
           manualRefreshBtn.disabled = true;
           manualRefreshBtn.innerHTML = `<span class="spinner-border spinner-border-sm"></span>`;
           await updateLogs(currentFile);
           setTimeout(() => {
               manualRefreshBtn.disabled = false;
               manualRefreshBtn.innerHTML = `<i class="bi bi-arrow-clockwise fs-6"></i>`;
           }, 500);
       }
   };
   
   /* -------------------------------
      CHANGELOG MODAL & VERSION CHECK
   -------------------------------- */
   const changelogModal = document.getElementById('changelogModal');
   if (changelogModal) {
     changelogModal.addEventListener('show.bs.modal', async () => {
       const sidebar = document.getElementById('changelog-sidebar');
       const content = document.getElementById('changelog-content');
       const pypiInfo = document.getElementById('pypi-version-info');
       
       // 1. Check PyPI Version
       try {
           const pypiRes = await fetch('https://pypi.org/pypi/tracenest/json');
           const pypiData = await pypiRes.json();
           const pypiVer = pypiData.info.version;
           const localVer = document.getElementById('current-version-display').innerText;
           
           if (pypiVer !== localVer) {
               pypiInfo.innerHTML = `<span class="text-warning"><i class="bi bi-cloud-arrow-down-fill me-1"></i> Update Available (PyPI: v${pypiVer})</span>`;
               document.getElementById('update-badge').classList.remove('d-none');
           } else {
               pypiInfo.innerHTML = `<span class="text-success"><i class="bi bi-check-circle-fill me-1"></i> Up to date (v${pypiVer})</span>`;
           }
       } catch (err) {
           pypiInfo.innerHTML = `<span class="text-muted"><i class="bi bi-dash-circle me-1"></i> PyPI check skipped</span>`;
       }
       
       // 2. Fetch Changelogs
       try {
         const res = await fetch('/tracenest/api/changelogs');
         if (!res.ok) throw new Error("Not found");
         const data = await res.json();
         
         if (!data.versions || data.versions.length === 0) {
           sidebar.innerHTML = '<div class="p-3 text-muted small">No versions found.</div>';
           return;
         }
         
         let html = '<div class="list-group list-group-flush bg-transparent rounded-0">';
         data.versions.forEach(v => {
           html += `<button class="list-group-item list-group-item-action border-0 py-3 fw-medium rounded-0" style="background: transparent;" onclick="loadChangelog('${v}')"><i class="bi bi-tag me-2 opacity-50"></i>${v}</button>`;
         });
         html += '</div>';
         sidebar.innerHTML = html;
         
         // Load the first one by default
         loadChangelog(data.versions[0]);
       } catch (err) {
         sidebar.innerHTML = '<div class="p-3 text-danger small">Failed to load.</div>';
       }
     });
   }
   
   window.loadChangelog = async (version) => {
     const content = document.getElementById('changelog-content');
     content.innerHTML = '<div class="text-muted h-100 d-flex flex-column align-items-center justify-content-center"><div class="spinner-border spinner-border-sm mb-2" role="status"></div>Loading...</div>';
     
     // Update active state
     document.querySelectorAll('#changelog-sidebar .list-group-item').forEach(btn => {
       if (btn.textContent.includes(version)) {
         btn.classList.add('bg-active', 'text-accent');
         btn.style.background = 'var(--active)';
       } else {
         btn.classList.remove('bg-active', 'text-accent');
         btn.style.background = 'transparent';
       }
     });
     
     try {
       const res = await fetch(`/tracenest/api/changelogs/${version}`);
       if (!res.ok) throw new Error();
       const data = await res.json();
       content.innerHTML = marked.parse(data.content || "No release notes provided.");
     } catch (err) {
       content.innerHTML = '<div class="text-danger h-100 d-flex align-items-center justify-content-center"><i class="bi bi-exclamation-triangle me-2"></i> Failed to load version notes.</div>';
     }
   };

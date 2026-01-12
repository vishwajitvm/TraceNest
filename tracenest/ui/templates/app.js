/* Expand / Collapse rows */
document.querySelectorAll('[data-expand]').forEach(row => {
  row.addEventListener('click', () => {
    const expandRow = row.nextElementSibling;

    document.querySelectorAll('.log-expand.active').forEach(el => {
      if (el !== expandRow) el.classList.remove('active');
    });

    expandRow.classList.toggle('active');
  });
});

/* Theme switching */
const container = document.getElementById('app-container');

document.querySelectorAll('[data-theme]').forEach(btn => {
  btn.addEventListener('click', () => {
    const theme = btn.dataset.theme;
    setTheme(theme);
  });
});

function setTheme(theme) {
  container.className = '';
  container.classList.add(`theme-${theme}`);
  localStorage.setItem('tracenest-theme', theme);
}

const savedTheme = localStorage.getItem('tracenest-theme');
if (savedTheme) {
  setTheme(savedTheme);
}

// From https://albertoroura.com/building-a-theme-switcher-for-bootstrap/

function setTheme (mode = 'auto') {
    const userMode = localStorage.getItem('bs-theme');
    const sysMode = window.matchMedia('(prefers-color-scheme: light)').matches;
    const useSystem = mode === 'system' || (!userMode && mode === 'auto');
    const modeChosen = useSystem ? 'system' : mode === 'dark' || mode === 'light' ? mode : userMode;
  
    if (useSystem) {
      localStorage.removeItem('bs-theme');
    } else {
      localStorage.setItem('bs-theme', modeChosen);
    }
  
    document.documentElement.setAttribute('data-bs-theme', useSystem ? (sysMode ? 'light' : 'dark') : modeChosen);
    document.querySelectorAll('.mode-switch .btn').forEach(e => e.classList.remove('text-body'));
    document.getElementById(modeChosen).classList.add('text-body');
}

setTheme();
document.querySelectorAll('.mode-switch .btn').forEach(e => e.addEventListener('click', () => setTheme(e.id)));
window.matchMedia('(prefers-color-scheme: light)').addEventListener('change', () => setTheme());
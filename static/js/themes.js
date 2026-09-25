import {state,setState} from './state.js';

const presets = {
  midnight: {
    bg: '#040711',
    bgDeep: '#020409',
    surface: 'rgba(8, 15, 30, 0.72)',
    surfaceAlt: 'rgba(14, 25, 48, 0.82)',
    surfaceElevated: 'rgba(20, 36, 68, 0.88)',
    accent: '#60a5fa',
    accentStrong: '#3b82f6',
    accentGlow: 'rgba(96, 165, 250, 0.35)',
    borderGlass: 'rgba(147, 197, 253, 0.18)',
    borderGlow: 'rgba(96, 165, 250, 0.4)',
    aurora1: 'rgba(37, 99, 235, 0.32)',
    aurora2: 'rgba(79, 70, 229, 0.24)',
    aurora3: 'rgba(56, 189, 248, 0.20)'
  },
  arctic: {
    bg: '#030a12',
    bgDeep: '#01050a',
    surface: 'rgba(7, 22, 38, 0.74)',
    surfaceAlt: 'rgba(12, 34, 58, 0.84)',
    surfaceElevated: 'rgba(18, 48, 80, 0.90)',
    accent: '#38bdf8',
    accentStrong: '#0ea5e9',
    accentGlow: 'rgba(56, 189, 248, 0.40)',
    borderGlass: 'rgba(186, 230, 253, 0.22)',
    borderGlow: 'rgba(56, 189, 248, 0.45)',
    aurora1: 'rgba(14, 165, 233, 0.36)',
    aurora2: 'rgba(56, 189, 248, 0.26)',
    aurora3: 'rgba(224, 242, 254, 0.22)'
  },
  obsidian: {
    bg: '#000000',
    bgDeep: '#000000',
    surface: 'rgba(12, 12, 16, 0.85)',
    surfaceAlt: 'rgba(20, 20, 26, 0.90)',
    surfaceElevated: 'rgba(28, 28, 36, 0.95)',
    accent: '#f8fafc',
    accentStrong: '#e2e8f0',
    accentGlow: 'rgba(255, 255, 255, 0.22)',
    borderGlass: 'rgba(255, 255, 255, 0.18)',
    borderGlow: 'rgba(255, 255, 255, 0.35)',
    aurora1: 'rgba(255, 255, 255, 0.12)',
    aurora2: 'rgba(148, 163, 184, 0.12)',
    aurora3: 'rgba(71, 85, 105, 0.16)'
  },
  nebula: {
    bg: '#070311',
    bgDeep: '#030108',
    surface: 'rgba(18, 10, 34, 0.75)',
    surfaceAlt: 'rgba(28, 16, 52, 0.85)',
    surfaceElevated: 'rgba(42, 24, 76, 0.90)',
    accent: '#c084fc',
    accentStrong: '#a855f7',
    accentGlow: 'rgba(192, 132, 252, 0.38)',
    borderGlass: 'rgba(233, 213, 255, 0.20)',
    borderGlow: 'rgba(192, 132, 252, 0.45)',
    aurora1: 'rgba(168, 85, 247, 0.34)',
    aurora2: 'rgba(236, 72, 153, 0.22)',
    aurora3: 'rgba(129, 140, 248, 0.24)'
  },
  // Legacy / fallback presets
  ocean: { bg: '#040d16', surface: 'rgba(8, 26, 42, 0.75)', accent: '#38bdf8' },
  emerald: { bg: '#03100a', surface: 'rgba(6, 32, 20, 0.75)', accent: '#34d399' },
  violet: { bg: '#0a0614', surface: 'rgba(22, 14, 40, 0.75)', accent: '#c084fc' },
  monochrome: { bg: '#0a0a0c', surface: 'rgba(18, 18, 22, 0.85)', accent: '#f1f1f1' },
  custom: { bg: '#040711', surface: 'rgba(8, 15, 30, 0.75)', accent: '#60a5fa' }
};

export function applyTheme(name, custom) {
  const t = custom || presets[name] || presets.midnight;
  const root = document.documentElement;
  root.style.setProperty('--bg', t.bg || '#040711');
  root.style.setProperty('--bg-deep', t.bgDeep || t.bg || '#020409');
  root.style.setProperty('--surface', t.surface || 'rgba(8, 15, 30, 0.72)');
  root.style.setProperty('--surface-alt', t.surfaceAlt || t.surface);
  root.style.setProperty('--surface-elevated', t.surfaceElevated || t.surfaceAlt || t.surface);
  root.style.setProperty('--accent', t.accent || '#60a5fa');
  root.style.setProperty('--accent-strong', t.accentStrong || t.accent);
  root.style.setProperty('--accent-glow', t.accentGlow || 'rgba(96, 165, 250, 0.3)');
  root.style.setProperty('--border-glass', t.borderGlass || 'rgba(255, 255, 255, 0.16)');
  root.style.setProperty('--border-glow', t.borderGlow || t.accentGlow);
  root.style.setProperty('--aurora-1', t.aurora1 || 'rgba(37, 99, 235, 0.25)');
  root.style.setProperty('--aurora-2', t.aurora2 || 'rgba(79, 70, 229, 0.20)');
  root.style.setProperty('--aurora-3', t.aurora3 || 'rgba(56, 189, 248, 0.18)');
  root.setAttribute('data-theme', name);
  localStorage.setItem('astra-theme', name);
  setState({theme: name});
}

export function initThemes() {
  const select = document.querySelector('#theme-select');
  if (select) {
    select.value = state.theme || 'midnight';
    select.onchange = () => applyTheme(select.value);
  }
  const accentColor = document.querySelector('#accent-color');
  if (accentColor) {
    accentColor.oninput = e => applyTheme('custom', {...presets.custom, accent: e.target.value});
  }
  const motionToggle = document.querySelector('#motion-toggle');
  if (motionToggle) {
    motionToggle.onchange = e => {
      document.body.classList.toggle('reduce-motion', e.target.checked);
      localStorage.setItem('astra-reduce-motion', e.target.checked ? '1' : '0');
    };
    motionToggle.checked = localStorage.getItem('astra-reduce-motion') === '1';
    document.body.classList.toggle('reduce-motion', motionToggle.checked);
  }
  applyTheme(state.theme || 'midnight');
}

export function exportTheme() {
  const css = getComputedStyle(document.documentElement);
  const blob = new Blob([JSON.stringify({
    bg: css.getPropertyValue('--bg').trim(),
    surface: css.getPropertyValue('--surface').trim(),
    accent: css.getPropertyValue('--accent').trim()
  }, null, 2)], {type: 'application/json'});
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'astra-theme.json';
  a.click();
}

/* Progressive enhancement only: every page is complete without JavaScript.
   Without it, tab lists act as a table of contents and all panels show. */
(() => {
  'use strict';

  document.querySelectorAll('[data-year]').forEach((element) => {
    element.textContent = String(new Date().getFullYear());
  });

  // Follow the browser's colour scheme until the visitor picks one; then remember it.
  // The saved choice is applied by an inline script in <head>, before first paint.
  const toggle = document.querySelector('.theme-toggle');
  if (toggle) {
    const root = document.documentElement;
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)');
    const current = () => root.dataset.theme || (prefersDark.matches ? 'dark' : 'light');
    const render = () => {
      const next = current() === 'dark' ? 'light' : 'dark';
      toggle.querySelector('.theme-label').textContent = next === 'dark' ? 'Dark' : 'Light';
      toggle.setAttribute('aria-label', `Switch to ${next} theme`);
      document.querySelectorAll('meta[name="theme-color"]').forEach((meta) => {
        meta.content = current() === 'dark' ? '#131312' : '#f5f2ea';
      });
    };

    toggle.addEventListener('click', () => {
      root.dataset.theme = current() === 'dark' ? 'light' : 'dark';
      try {
        localStorage.setItem('theme', root.dataset.theme);
      } catch (error) {
        // Storage can be blocked; the switch still works for this page view.
      }
      render();
    });
    prefersDark.addEventListener('change', render);
    toggle.hidden = false;
    render();
  }

  const groups = [...document.querySelectorAll('[data-tabs]')].map((group) => {
    const tabs = [...group.querySelectorAll('[data-tab]')];
    const panels = tabs.map((tab) => document.getElementById(tab.hash.slice(1)));
    const list = group.querySelector('.tab-list');
    list.setAttribute('role', 'tablist');

    tabs.forEach((tab, index) => {
      const panel = panels[index];
      tab.id = `tab-${panel.id}`;
      tab.setAttribute('role', 'tab');
      tab.setAttribute('aria-controls', panel.id);
      panel.setAttribute('role', 'tabpanel');
      panel.setAttribute('aria-labelledby', tab.id);
    });

    const select = (index, { focus = false, remember = false } = {}) => {
      tabs.forEach((tab, i) => {
        const selected = i === index;
        tab.setAttribute('aria-selected', String(selected));
        tab.tabIndex = selected ? 0 : -1;
        panels[i].hidden = !selected;
      });
      if (focus) tabs[index].focus();
      // Keep the selected tab shareable without making the page jump.
      if (remember) history.replaceState(null, '', `#${panels[index].id}`);
    };

    tabs.forEach((tab, index) => {
      tab.addEventListener('click', (event) => {
        event.preventDefault();
        select(index, { remember: true });
      });
      tab.addEventListener('keydown', (event) => {
        const step = { ArrowRight: 1, ArrowDown: 1, ArrowLeft: -1, ArrowUp: -1 }[event.key];
        let next;
        if (step) next = (index + step + tabs.length) % tabs.length;
        else if (event.key === 'Home') next = 0;
        else if (event.key === 'End') next = tabs.length - 1;
        else return;
        event.preventDefault();
        select(next, { focus: true, remember: true });
      });
    });

    select(0);
    document.documentElement.classList.add('js-tabs');
    return { panels, select };
  });

  // A link such as research.html#ref-8 opens the panel that holds the target.
  const showTarget = () => {
    const id = decodeURIComponent(window.location.hash.slice(1));
    const target = id && document.getElementById(id);
    if (!target) return;
    groups.forEach(({ panels, select }) => {
      const index = panels.findIndex((panel) => panel.contains(target));
      if (index < 0) return;
      select(index);
      if (target !== panels[index]) target.scrollIntoView({ block: 'center' });
    });
  };

  showTarget();
  window.addEventListener('hashchange', showTarget);
})();

/* Core content and navigation also work without JavaScript. */
(() => {
  'use strict';

  const toggle = document.querySelector('.nav-toggle');
  const navigation = document.querySelector('#site-navigation');

  if (toggle && navigation) {
    const setOpen = (open) => {
      toggle.setAttribute('aria-expanded', String(open));
      navigation.classList.toggle('is-open', open);
      toggle.textContent = open ? 'Close' : 'Menu';
    };

    toggle.addEventListener('click', () => {
      setOpen(toggle.getAttribute('aria-expanded') !== 'true');
    });
    navigation.addEventListener('click', (event) => {
      if (event.target.closest('a')) setOpen(false);
    });
    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape' && toggle.getAttribute('aria-expanded') === 'true') {
        setOpen(false);
        toggle.focus();
      }
    });
    window.matchMedia('(min-width: 701px)').addEventListener('change', () => setOpen(false));
  }

  // Apply enhanced navigation only after its controls are attached.
  document.documentElement.classList.add('js');
  document.querySelectorAll('[data-year]').forEach((element) => {
    element.textContent = String(new Date().getFullYear());
  });

  if (navigation && !navigation.querySelector('[aria-current="page"]')) {
    const route = window.location.pathname.split('/').pop() || 'index.html';
    navigation.querySelectorAll('a').forEach((link) => {
      if (link.getAttribute('href') === route) link.setAttribute('aria-current', 'page');
    });
  }

  if (!('IntersectionObserver' in window) || window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.08 });

  document.querySelectorAll('[data-reveal]').forEach((element) => {
    // Never hide content already in view, including fragment destinations.
    if (element.getBoundingClientRect().top < window.innerHeight) return;
    element.classList.add('reveal-ready');
    observer.observe(element);
  });
})();

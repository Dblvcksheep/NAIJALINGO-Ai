document.addEventListener('DOMContentLoaded', () => {
  const toggle = document.querySelector('.mobile-toggle');
  const overlay = document.querySelector('.nav-overlay');
  const body = document.body;

  const setNavOpen = (isOpen) => {
    body.classList.toggle('nav-open', isOpen);
    if (overlay) {
      overlay.classList.toggle('visible', isOpen);
    }
  };

  if (toggle) {
    toggle.addEventListener('click', () => {
      setNavOpen(!body.classList.contains('nav-open'));
    });
  }

  if (overlay) {
    overlay.addEventListener('click', () => setNavOpen(false));
  }

  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') {
      setNavOpen(false);
    }
  });

  document.querySelectorAll('.sidebar a').forEach((link) => {
    link.addEventListener('click', () => setNavOpen(false));
  });
});

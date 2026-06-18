/* ============================================================
   SYTFIX — MAIN JS
   Navigation · Scroll Animations · Lindy Score Gauge
   ============================================================ */

(function () {
  'use strict';

  /* ── NAV HAMBURGER ── */
  const hamburger = document.getElementById('hamburger');
  const drawer    = document.getElementById('nav-drawer');

  if (hamburger && drawer) {
    hamburger.addEventListener('click', function () {
      const open = drawer.classList.toggle('is-open');
      hamburger.classList.toggle('is-open', open);
      hamburger.setAttribute('aria-expanded', String(open));
      document.body.style.overflow = open ? 'hidden' : '';
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && drawer.classList.contains('is-open')) {
        drawer.classList.remove('is-open');
        hamburger.classList.remove('is-open');
        hamburger.setAttribute('aria-expanded', 'false');
        document.body.style.overflow = '';
        hamburger.focus();
      }
    });

    drawer.querySelectorAll('.nav__drawer-link').forEach(function (link) {
      link.addEventListener('click', function () {
        drawer.classList.remove('is-open');
        hamburger.classList.remove('is-open');
        hamburger.setAttribute('aria-expanded', 'false');
        document.body.style.overflow = '';
      });
    });
  }

  /* ── ACTIVE NAV LINK ── */
  (function setActiveNav() {
    const path     = window.location.pathname.split('/').pop() || 'index.html';
    const navLinks = document.querySelectorAll('.nav__link, .nav__drawer-link');
    navLinks.forEach(function (link) {
      const href = (link.getAttribute('href') || '').split('/').pop();
      if (href === path || (path === '' && href === 'index.html')) {
        link.classList.add('active');
      }
    });
  })();

  /* ── SCROLL REVEAL ── */
  (function initReveal() {
    const items = document.querySelectorAll('.js-reveal');
    if (!items.length) return;

    if (!window.IntersectionObserver) {
      items.forEach(function (el) { el.classList.add('is-visible'); });
      return;
    }

    const observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });

    items.forEach(function (el) { observer.observe(el); });
  })();

  /* ── LINDY SCORE GAUGE ANIMATION ── */
  (function initGauge() {
    const beforeProgress = document.getElementById('gauge-before-progress');
    const afterProgress  = document.getElementById('gauge-after-progress');
    const beforeScoreEl  = document.getElementById('gauge-before-score');
    const afterScoreEl   = document.getElementById('gauge-after-score');
    const dimFills       = document.querySelectorAll('.gauge-dim__fill');

    if (!beforeProgress) return;

    const CIRCUMFERENCE = 471;
    const BEFORE_SCORE  = 47;
    const AFTER_SCORE   = 84;

    function scoreToOffset(score) {
      return CIRCUMFERENCE - (score / 100) * CIRCUMFERENCE;
    }

    function animateCount(el, target, duration) {
      if (!el) return;
      const start = performance.now();
      function step(now) {
        const elapsed  = now - start;
        const progress = Math.min(elapsed / duration, 1);
        const eased    = 1 - Math.pow(1 - progress, 3);
        el.textContent = Math.round(eased * target);
        if (progress < 1) requestAnimationFrame(step);
      }
      requestAnimationFrame(step);
    }

    const dimPercents = [38, 55, 42, 61, 29, 33, 58];

    let gaugeObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;

        setTimeout(function () {
          if (beforeProgress) {
            beforeProgress.style.strokeDashoffset = scoreToOffset(BEFORE_SCORE);
          }
          animateCount(beforeScoreEl, BEFORE_SCORE, 1200);
        }, 200);

        setTimeout(function () {
          if (afterProgress) {
            afterProgress.style.strokeDashoffset = scoreToOffset(AFTER_SCORE);
          }
          animateCount(afterScoreEl, AFTER_SCORE, 1000);
        }, 800);

        dimFills.forEach(function (fill, i) {
          setTimeout(function () {
            fill.style.width = (dimPercents[i] || 50) + '%';
          }, 400 + i * 80);
        });

        gaugeObserver.disconnect();
      });
    }, { threshold: 0.3 });

    const gaugeCard = document.querySelector('.gauge-card');
    if (gaugeCard) gaugeObserver.observe(gaugeCard);
  })();

  /* ── NAV SHADOW ON SCROLL ── */
  (function navShadow() {
    const nav = document.querySelector('.nav');
    if (!nav) return;
    window.addEventListener('scroll', function () {
      nav.style.boxShadow = window.scrollY > 8
        ? '0 2px 16px rgba(0,0,0,.08)'
        : '';
    }, { passive: true });
  })();

  /* ── SMOOTH ANCHOR SCROLL ── */
  document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
    anchor.addEventListener('click', function (e) {
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        e.preventDefault();
        const navH = parseInt(getComputedStyle(document.documentElement)
          .getPropertyValue('--nav-h')) || 72;
        const top  = target.getBoundingClientRect().top + window.scrollY - navH - 24;
        window.scrollTo({ top: top, behavior: 'smooth' });
      }
    });
  });

  /* ── CONTACT FORM (if on contact page) ── */
  const contactForm = document.getElementById('contact-form');
  if (contactForm) {
    contactForm.addEventListener('submit', function (e) {
      e.preventDefault();

      const btn     = contactForm.querySelector('button[type="submit"]');
      const success = document.getElementById('form-success');

      if (btn) {
        btn.disabled    = true;
        btn.textContent = 'Sending…';
      }

      setTimeout(function () {
        if (btn) {
          btn.disabled    = false;
          btn.textContent = 'Send Message';
        }
        if (success) success.classList.add('is-visible');
        contactForm.reset();

        setTimeout(function () {
          if (success) success.classList.remove('is-visible');
        }, 6000);
      }, 900);
    });
  }

})();

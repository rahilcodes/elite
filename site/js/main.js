/* Elite Architecture — shared behaviour (vanilla JS, no dependencies) */
(function () {
  'use strict';

  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* Mobile menu -------------------------------------------------------- */
  var burger = document.querySelector('.burger');
  var menu = document.getElementById('mobile-menu');

  if (burger && menu) {
    var closeBtn = menu.querySelector('.mobile-menu__close');
    var desktop = window.matchMedia('(min-width: 901px)');

    var focusables = function () {
      return menu.querySelectorAll('a[href], button:not([disabled])');
    };

    var openMenu = function () {
      menu.hidden = false;
      burger.setAttribute('aria-expanded', 'true');
      document.body.classList.add('menu-open');
      closeBtn.focus();
    };

    var closeMenu = function (returnFocus) {
      if (menu.hidden) return;
      menu.hidden = true;
      burger.setAttribute('aria-expanded', 'false');
      document.body.classList.remove('menu-open');
      if (returnFocus) burger.focus();
    };

    burger.addEventListener('click', openMenu);
    closeBtn.addEventListener('click', function () { closeMenu(true); });

    menu.addEventListener('click', function (e) {
      if (e.target.closest('a')) closeMenu(false);
    });

    menu.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') { closeMenu(true); return; }
      if (e.key !== 'Tab') return;
      var items = focusables();
      var first = items[0];
      var last = items[items.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    });

    desktop.addEventListener('change', function () { closeMenu(false); });
  }

  /* Scroll reveal ------------------------------------------------------ */
  var revealEls = document.querySelectorAll('[data-reveal]');

  if (revealEls.length && !reduceMotion && 'IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        var el = entry.target;
        el.classList.add('reveal-in');
        io.unobserve(el);
        // Hand the element back to its own hover transitions once revealed
        setTimeout(function () { el.classList.remove('reveal-init', 'reveal-ready', 'reveal-in'); }, 1000);
      });
    }, { threshold: 0.1 });

    revealEls.forEach(function (el) {
      // Only animate what starts below the fold, so nothing visible flashes
      if (el.getBoundingClientRect().top > window.innerHeight) {
        el.classList.add('reveal-init');
        // Force a style flush so the transition class applies from the hidden state
        void el.offsetWidth;
        el.classList.add('reveal-ready');
        io.observe(el);
      }
    });
  }

  /* Footer year -------------------------------------------------------- */
  var year = document.querySelector('[data-year]');
  if (year) year.textContent = new Date().getFullYear();
})();

/* Accordion (FAQ) ------------------------------------------------------ */
(function () {
  'use strict';
  document.querySelectorAll('[data-accordion]').forEach(function (acc) {
    var triggers = Array.prototype.slice.call(acc.querySelectorAll('.accordion__trigger'));

    triggers.forEach(function (btn, i) {
      btn.addEventListener('click', function () {
        var open = btn.getAttribute('aria-expanded') === 'true';
        btn.setAttribute('aria-expanded', String(!open));
        document.getElementById(btn.getAttribute('aria-controls')).hidden = open;
      });

      btn.addEventListener('keydown', function (e) {
        var next = null;
        if (e.key === 'ArrowDown') next = triggers[(i + 1) % triggers.length];
        else if (e.key === 'ArrowUp') next = triggers[(i - 1 + triggers.length) % triggers.length];
        else if (e.key === 'Home') next = triggers[0];
        else if (e.key === 'End') next = triggers[triggers.length - 1];
        if (next) { e.preventDefault(); next.focus(); }
      });
    });
  });
})();

/* Project filter ------------------------------------------------------- */
(function () {
  'use strict';
  var grid = document.querySelector('[data-filter-grid]');
  if (!grid) return;

  var buttons = document.querySelectorAll('.filter-btn');
  var status = document.querySelector('[data-filter-status]');
  var cards = grid.querySelectorAll('[data-category]');

  buttons.forEach(function (btn) {
    btn.addEventListener('click', function () {
      var filter = btn.getAttribute('data-filter');
      var shown = 0;

      buttons.forEach(function (b) { b.setAttribute('aria-pressed', String(b === btn)); });

      cards.forEach(function (card) {
        var match = filter === 'all' || card.getAttribute('data-category') === filter;
        card.hidden = !match;
        if (match) {
          shown++;
          card.classList.remove('reveal-init', 'reveal-ready', 'reveal-in');
        }
      });

      if (status) status.textContent = shown + (shown === 1 ? ' project' : ' projects') + ' shown';
    });
  });
})();

/* Contact form --------------------------------------------------------- */
(function () {
  'use strict';
  var form = document.getElementById('contact-form');
  if (!form) return;

  var success = document.getElementById('form-success');
  var successLink = document.getElementById('form-success-link');
  var resetBtn = document.getElementById('form-reset');
  var fields = ['name', 'email', 'phone', 'type', 'message'].map(function (n) { return form.elements[n]; });

  var rules = {
    name: function (v) { return v.length >= 2 ? '' : 'Please enter your name.'; },
    email: function (v) { return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v) ? '' : 'Please enter a valid email address.'; },
    phone: function (v) { return v === '' || /^[+()\d][\d\s()-]{5,}$/.test(v) ? '' : 'Please enter a valid phone number, or leave this empty.'; },
    type: function (v) { return v ? '' : 'Please choose a project type.'; },
    message: function (v) { return v.length >= 10 ? '' : 'Please tell us a little about your project (at least 10 characters).'; }
  };

  var validate = function (field) {
    var msg = rules[field.name](field.value.trim());
    var err = document.getElementById(field.id + '-err');
    err.textContent = msg;
    if (msg) field.setAttribute('aria-invalid', 'true');
    else field.removeAttribute('aria-invalid');
    return !msg;
  };

  fields.forEach(function (field) {
    field.addEventListener('blur', function () { if (field.value.trim() || field.hasAttribute('aria-invalid')) validate(field); });
    field.addEventListener('input', function () { if (field.hasAttribute('aria-invalid')) validate(field); });
  });

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var firstInvalid = null;
    fields.forEach(function (field) {
      if (!validate(field) && !firstInvalid) firstInvalid = field;
    });
    if (firstInvalid) { firstInvalid.focus(); return; }

    var v = function (n) { return form.elements[n].value.trim(); };
    var text = 'Hello Elite Architecture, I would like to discuss a project.\n\n' +
      'Name: ' + v('name') + '\n' +
      'Email: ' + v('email') + '\n' +
      (v('phone') ? 'Phone: ' + v('phone') + '\n' : '') +
      'Project type: ' + v('type') + '\n\n' + v('message');
    var url = 'https://wa.me/' + form.getAttribute('data-whatsapp') + '?text=' + encodeURIComponent(text);

    successLink.href = url;
    window.open(url, '_blank', 'noopener');

    form.hidden = true;
    success.hidden = false;
    success.focus();
  });

  resetBtn.addEventListener('click', function () {
    form.reset();
    success.hidden = true;
    form.hidden = false;
    fields[0].focus();
  });
})();

/* Gallery lightbox ----------------------------------------------------- */
(function () {
  'use strict';
  var links = Array.prototype.slice.call(document.querySelectorAll('[data-lightbox]'));
  if (!links.length || !('HTMLDialogElement' in window)) return; // falls back to opening the image

  var index = 0;
  var opener = null;
  var dialog = document.createElement('dialog');
  dialog.className = 'lightbox on-dark';
  dialog.setAttribute('aria-label', 'Image viewer');
  dialog.innerHTML =
    '<div class="lightbox__bar"><span class="lightbox__count" aria-live="polite"></span>' +
    '<button class="lightbox__btn" type="button" data-close>Close</button></div>' +
    '<div class="lightbox__stage"><img alt=""></div>' +
    '<div class="lightbox__nav"><button class="lightbox__btn" type="button" data-prev>\u2190 Previous</button>' +
    '<button class="lightbox__btn" type="button" data-next>Next \u2192</button></div>';
  document.body.appendChild(dialog);

  var img = dialog.querySelector('img');
  var count = dialog.querySelector('.lightbox__count');

  var show = function (i) {
    index = (i + links.length) % links.length;
    var thumb = links[index].querySelector('img');
    img.src = links[index].href;
    img.alt = thumb ? thumb.alt : '';
    count.textContent = (index + 1) + ' / ' + links.length;
  };

  links.forEach(function (link, i) {
    link.addEventListener('click', function (e) {
      e.preventDefault();
      opener = link;
      show(i);
      dialog.showModal();
      document.body.classList.add('menu-open');
    });
  });

  dialog.querySelector('[data-close]').addEventListener('click', function () { dialog.close(); });
  dialog.querySelector('[data-prev]').addEventListener('click', function () { show(index - 1); });
  dialog.querySelector('[data-next]').addEventListener('click', function () { show(index + 1); });
  dialog.querySelector('.lightbox__stage').addEventListener('click', function (e) {
    if (e.target !== img) dialog.close();
  });
  dialog.addEventListener('keydown', function (e) {
    if (e.key === 'ArrowLeft') show(index - 1);
    else if (e.key === 'ArrowRight') show(index + 1);
  });
  dialog.addEventListener('close', function () {
    document.body.classList.remove('menu-open');
    img.removeAttribute('src');
    if (opener) opener.focus();
  });
})();

/* Floating contact ----------------------------------------------------- */
(function () {
  'use strict';
  var fab = document.querySelector('[data-fab]');
  if (fab) {
    var toggle = fab.querySelector('.contact-fab__toggle');
    var menu = fab.querySelector('.contact-fab__menu');
    var setOpen = function (open) {
      menu.hidden = !open;
      toggle.setAttribute('aria-expanded', String(open));
    };
    toggle.addEventListener('click', function () { setOpen(menu.hidden); });
    document.addEventListener('click', function (e) { if (!fab.contains(e.target)) setOpen(false); });
    fab.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && !menu.hidden) { setOpen(false); toggle.focus(); }
    });
    menu.addEventListener('click', function (e) { if (e.target.closest('a')) setOpen(false); });
  }

  // Mobile bar: slides in once the visitor starts scrolling, so the hero stays clean
  var bar = document.querySelector('[data-contact-bar]');
  if (bar) {
    var ticking = false;
    var update = function () {
      bar.classList.toggle('is-visible', window.scrollY > 160);
      ticking = false;
    };
    window.addEventListener('scroll', function () {
      if (!ticking) { ticking = true; window.requestAnimationFrame(update); }
    }, { passive: true });
    update();
  }
})();

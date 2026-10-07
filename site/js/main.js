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
        var match = filter === 'all' || card.getAttribute('data-category') === filter ||
          (filter === 'featured' && card.hasAttribute('data-featured'));
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

  // Clean-up runs directly on close; the dialog's own 'close' event only covers the Esc key
  var shut = function () {
    if (dialog.open) dialog.close();
    document.body.classList.remove('menu-open');
    img.removeAttribute('src');
    if (opener) { opener.focus(); opener = null; }
  };
  dialog.querySelector('[data-close]').addEventListener('click', shut);
  dialog.querySelector('[data-prev]').addEventListener('click', function () { show(index - 1); });
  dialog.querySelector('[data-next]').addEventListener('click', function () { show(index + 1); });
  dialog.querySelector('.lightbox__stage').addEventListener('click', function (e) {
    if (e.target !== img) shut();
  });
  dialog.addEventListener('keydown', function (e) {
    if (e.key === 'ArrowLeft') show(index - 1);
    else if (e.key === 'ArrowRight') show(index + 1);
  });
  dialog.addEventListener('close', shut);
  dialog.addEventListener('cancel', function () { setTimeout(shut, 0); });
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

/* ======================================================================
   Film & motion upgrade
   ====================================================================== */
(function () {
  'use strict';

  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var finePointer = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
  var saveData = navigator.connection && navigator.connection.saveData;
  var root = document.documentElement;

  /* Header height + scroll progress ----------------------------------- */
  var header = document.querySelector('.site-header');
  if (header) {
    var bar = document.createElement('span');
    bar.className = 'scroll-progress';
    bar.setAttribute('aria-hidden', 'true');
    header.appendChild(bar);
    var setHdr = function () { root.style.setProperty('--hdr', header.offsetHeight + 'px'); };
    setHdr();
    window.addEventListener('resize', setHdr);
  }

  /* One scroll loop for everything that follows the scroll position ----- */
  var rail = document.querySelector('.features__rail');
  var features = rail ? Array.prototype.slice.call(document.querySelectorAll('.features .feature')) : [];
  var heroMedia = document.querySelector('.filmhero__media');
  var ticking = false;
  var onScroll = function () {
    var max = document.documentElement.scrollHeight - window.innerHeight;
    root.style.setProperty('--scroll', max > 0 ? (window.scrollY / max).toFixed(4) : 0);
    if (heroMedia && !reduce && window.scrollY < window.innerHeight) {
      heroMedia.style.transform = 'translate3d(0,' + (window.scrollY * 0.18).toFixed(1) + 'px,0)';
    }
    if (rail) {
      var box = rail.parentNode.getBoundingClientRect();
      var p = (window.innerHeight * 0.55 - box.top) / box.height;
      rail.style.setProperty('--rail', Math.max(0, Math.min(1, p)).toFixed(4));
      features.forEach(function (f) {
        f.classList.toggle('is-reached', f.getBoundingClientRect().top < window.innerHeight * 0.55);
      });
    }
    var waiting = document.querySelectorAll('.wipe-init:not(.wipe-in), .reveal-init:not(.reveal-in)');
    for (var w = 0; w < waiting.length; w++) {
      var el = waiting[w];
      if (el.getBoundingClientRect().top < window.innerHeight * 0.92) {
        el.classList.add(el.classList.contains('wipe-init') ? 'wipe-in' : 'reveal-in');
      }
    }
    ticking = false;
  };
  window.addEventListener('scroll', function () {
    if (!ticking) { ticking = true; window.requestAnimationFrame(onScroll); }
  }, { passive: true });
  window.addEventListener('load', function () { setTimeout(onScroll, 300); });
  onScroll();

  /* Intro curtain (home, first page of a visit) ------------------------- */
  var intro = document.querySelector('.intro');
  var introDelay = 0;
  if (intro && root.classList.contains('has-intro')) {
    introDelay = 1500;
    setTimeout(function () {
      intro.classList.add('is-leaving');
      root.classList.remove('has-intro');
      setTimeout(function () { intro.remove(); }, 1000);
    }, 1750);
  } else if (intro) {
    intro.remove();
  }

  /* Headlines: word-by-word reveal -------------------------------------- */
  if (!reduce) {
    var splitNode = function (node, state) {
      Array.prototype.slice.call(node.childNodes).forEach(function (child) {
        if (child.nodeType === 3) {
          var frag = document.createDocumentFragment();
          child.textContent.split(/(\s+)/).forEach(function (part) {
            if (!part) return;
            if (/^\s+$/.test(part)) { frag.appendChild(document.createTextNode(' ')); return; }
            var outer = document.createElement('span');
            outer.className = 'split-word';
            var inner = document.createElement('span');
            inner.style.setProperty('--i', state.i++);
            inner.textContent = part;
            outer.appendChild(inner);
            frag.appendChild(outer);
          });
          node.replaceChild(frag, child);
        } else if (child.nodeType === 1) {
          splitNode(child, state);
        }
      });
    };
    document.querySelectorAll('main h1').forEach(function (h) {
      h.setAttribute('aria-label', h.textContent.replace(/\s+/g, ' ').trim());
      splitNode(h, { i: 0 });
      h.style.setProperty('--split-delay', (introDelay + 150) + 'ms');
      setTimeout(function () { h.classList.add('split-in'); }, 40);
    });
  }

  /* Images: wipe open as they scroll into view --------------------------- */
  if (!reduce && 'IntersectionObserver' in window) {
    var wipeIO = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        var el = entry.target;
        el.classList.add('wipe-in');
        wipeIO.unobserve(el);
        setTimeout(function () { el.classList.remove('wipe-init', 'wipe-ready', 'wipe-in'); }, 1700);
      });
    }, { threshold: 0.15 });
    document.querySelectorAll('.project-card__media, .media, .film-card__media').forEach(function (el) {
      if (el.closest('.reel') || el.getBoundingClientRect().top <= window.innerHeight) return;
      el.classList.add('wipe-init');
      void el.offsetWidth;
      el.classList.add('wipe-ready');
      wipeIO.observe(el);
    });

    /* Numbers count up */
    var countIO = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        countIO.unobserve(entry.target);
        var node = entry.target.firstChild;
        if (!node || node.nodeType !== 3) return;
        var raw = node.textContent.trim();
        var target = parseFloat(raw);
        if (isNaN(target)) return;
        var decimals = (raw.split('.')[1] || '').length;
        var pad = /^0\d/.test(raw) ? raw.length : 0;
        var t0 = null;
        var step = function (t) {
          if (t0 === null) t0 = t;
          var k = Math.min(1, (t - t0) / 1400);
          var eased = 1 - Math.pow(1 - k, 3);
          var val = (target * eased).toFixed(decimals);
          if (pad) while (val.length < pad) val = '0' + val;
          node.textContent = val;
          if (k < 1) window.requestAnimationFrame(step);
          else node.textContent = raw;
        };
        window.requestAnimationFrame(step);
      });
    }, { threshold: 0.6 });
    document.querySelectorAll('.stat__num, .filmhero__stat').forEach(function (el) { countIO.observe(el); });

    /* Footer elevation draws itself */
    var footer = document.querySelector('.site-footer');
    if (footer) {
      footer.querySelectorAll('.footer-elevation path, .footer-elevation circle').forEach(function (p) { p.setAttribute('pathLength', '1'); });
      if (footer.getBoundingClientRect().top > window.innerHeight) {
        footer.classList.add('draw-init');
        var drawIO = new IntersectionObserver(function (entries) {
          if (!entries[0].isIntersecting) return;
          footer.classList.add('draw-in');
          footer.classList.remove('draw-init');
          drawIO.disconnect();
        }, { threshold: 0.12 });
        drawIO.observe(footer);
      }
    }
  }

  /* Hero slideshow: the client's featured renders, cross-fading with a slow zoom */
  var show = document.querySelector('.hero-show');
  if (show) {
    var slides = Array.prototype.slice.call(show.querySelectorAll('.hero-slide'));
    var dots = Array.prototype.slice.call(show.querySelectorAll('.hero-dot'));
    var nums = show.querySelectorAll('[data-slide-num]');
    var link = show.querySelector('[data-slide-link]');
    var meta = show.querySelector('[data-slide-meta]');
    var interval = parseInt(show.getAttribute('data-interval'), 10) || 6500;
    var cur = 0, timer = null, paused = false;
    show.style.setProperty('--slide-ms', interval + 'ms');
    show.style.setProperty('--zoom-ms', (interval + 1600) + 'ms');

    var caption = function (i) {
      var img = slides[i];
      nums.forEach(function (n) { n.textContent = ('0' + (i + 1)).slice(-2); });
      link.textContent = img.getAttribute('data-title');
      link.href = img.getAttribute('data-href');
      meta.textContent = img.getAttribute('data-meta');
    };
    var queue = function () {
      clearTimeout(timer);
      if (reduce || paused || document.hidden) return;
      timer = setTimeout(function () { go(cur + 1); }, interval);
    };
    var go = function (i) {
      cur = (i + slides.length) % slides.length;
      slides.forEach(function (sl, k) { sl.classList.toggle('is-active', k === cur); });
      dots.forEach(function (d, k) {
        d.classList.toggle('is-active', k === cur);
        d.setAttribute('aria-selected', String(k === cur));
      });
      caption(cur);
      queue();
    };
    caption(0);
    queue();

    show.querySelector('[data-slide-prev]').addEventListener('click', function () { go(cur - 1); });
    show.querySelector('[data-slide-next]').addEventListener('click', function () { go(cur + 1); });
    dots.forEach(function (d) { d.addEventListener('click', function () { go(parseInt(d.getAttribute('data-slide-to'), 10)); }); });
    show.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowLeft') go(cur - 1);
      else if (e.key === 'ArrowRight') go(cur + 1);
    });
    var pause = function (on) { paused = on; show.classList.toggle('is-paused', on); queue(); };
    show.querySelector('.filmhero__aside').addEventListener('mouseenter', function () { pause(true); });
    show.querySelector('.filmhero__aside').addEventListener('mouseleave', function () { pause(false); });
    document.addEventListener('visibilitychange', function () { if (!document.hidden) queue(); else clearTimeout(timer); });
    var tx = null;
    show.addEventListener('touchstart', function (e) { tx = e.touches[0].clientX; }, { passive: true });
    show.addEventListener('touchend', function (e) {
      if (tx === null) return;
      var dx = e.changedTouches[0].clientX - tx;
      tx = null;
      if (Math.abs(dx) > 48) go(dx < 0 ? cur + 1 : cur - 1);
    }, { passive: true });
  }

  /* Film cards: silent moving preview on hover / focus --------------------- */
  var cards = Array.prototype.slice.call(document.querySelectorAll('[data-film]'));
  var addLoop = function (card) {
    var media = card.querySelector('.film-card__media');
    var img = new Image();
    img.className = 'film-card__loop';
    img.alt = '';
    img.onload = function () { if (card.matches(':hover, :focus') || card.hasAttribute('data-autoloop')) card.classList.add('is-previewing'); };
    img.src = card.getAttribute('data-loop');
    media.appendChild(img);
    return img;
  };
  if (finePointer && !reduce && !saveData) {
    cards.forEach(function (card) {
      if (!card.getAttribute('data-loop') || !card.querySelector('.film-card__media') || card.hasAttribute('data-autoloop')) return;
      var img = null;
      var timer = null;
      var start = function () {
        timer = setTimeout(function () {
          if (!img) img = addLoop(card);
          else if (img.complete) card.classList.add('is-previewing');
        }, 140);
      };
      var stop = function () { clearTimeout(timer); card.classList.remove('is-previewing'); };
      card.addEventListener('mouseenter', start);
      card.addEventListener('mouseleave', stop);
      card.addEventListener('focus', start);
      card.addEventListener('blur', stop);
    });
  }

  /* Featured film on the Films page starts moving when it scrolls into view */
  var auto = document.querySelector('[data-autoloop]');
  if (auto && !reduce && !saveData && 'IntersectionObserver' in window) {
    var autoIO = new IntersectionObserver(function (entries) {
      if (!entries[0].isIntersecting) return;
      autoIO.disconnect();
      addLoop(auto);
    }, { threshold: 0.35 });
    autoIO.observe(auto);
  }

  /* Film reel: drag to scroll + arrow buttons ------------------------------ */
  document.querySelectorAll('.reel__track').forEach(function (track) {
    var down = false, moved = false, startX = 0, startLeft = 0;
    track.addEventListener('mousedown', function (e) { down = true; moved = false; startX = e.pageX; startLeft = track.scrollLeft; });
    window.addEventListener('mousemove', function (e) {
      if (!down) return;
      var dx = e.pageX - startX;
      if (Math.abs(dx) > 6) { moved = true; track.classList.add('is-dragging'); }
      if (moved) track.scrollLeft = startLeft - dx;
    });
    window.addEventListener('mouseup', function () {
      if (!down) return;
      down = false;
      setTimeout(function () { track.classList.remove('is-dragging'); }, 0);
    });
    track.addEventListener('click', function (e) { if (moved) { e.preventDefault(); e.stopPropagation(); moved = false; } }, true);
    var section = track.closest('section');
    var step = function (dir) {
      var card = track.querySelector('.film-card');
      var w = card ? card.getBoundingClientRect().width + 20 : 400;
      track.scrollBy({ left: dir * w * (window.innerWidth > 900 ? 2 : 1), behavior: reduce ? 'auto' : 'smooth' });
    };
    if (section) {
      var prev = section.querySelector('[data-reel-prev]');
      var next = section.querySelector('[data-reel-next]');
      if (prev) prev.addEventListener('click', function () { step(-1); });
      if (next) next.addEventListener('click', function () { step(1); });
    }
  });

  /* Cinema player: full films stream from Google Drive on demand ---------- */
  if (cards.length && 'HTMLDialogElement' in window) {
    var films = [];
    var seen = {};
    cards.forEach(function (c) {
      var id = c.getAttribute('data-film');
      if (seen[id]) return;
      seen[id] = true;
      films.push({ id: id, title: c.getAttribute('data-title'), poster: c.getAttribute('data-poster'), href: c.getAttribute('href') });
    });
    var current = 0;
    var opener = null;
    var dlg = document.createElement('dialog');
    dlg.className = 'cinema';
    dlg.setAttribute('aria-label', 'Film player');
    dlg.innerHTML =
      '<div class="cinema__bar"><div class="cinema__title"><span></span><b></b></div>' +
      '<button class="cinema__btn" type="button" data-close>Close</button></div>' +
      '<div class="cinema__stage"><div class="cinema__frame"></div></div>' +
      '<div class="cinema__foot"><a target="_blank" rel="noopener">Having trouble? Open the film in Google Drive</a>' +
      '<div class="cinema__nav"><button class="cinema__btn" type="button" data-prev>← Previous film</button>' +
      '<button class="cinema__btn" type="button" data-next>Next film →</button></div></div>';
    document.body.appendChild(dlg);
    var frame = dlg.querySelector('.cinema__frame');
    var titleEl = dlg.querySelector('.cinema__title b');
    var countEl = dlg.querySelector('.cinema__title span');
    var fallback = dlg.querySelector('.cinema__foot a');

    var show = function (i) {
      current = (i + films.length) % films.length;
      var f = films[current];
      titleEl.textContent = f.title;
      countEl.textContent = ('0' + (current + 1)).slice(-2) + ' / ' + ('0' + films.length).slice(-2);
      fallback.href = f.href;
      frame.style.backgroundImage = f.poster ? 'url("' + f.poster + '")' : '';
      frame.innerHTML = '';
      var iframe = document.createElement('iframe');
      iframe.src = 'https://drive.google.com/file/d/' + f.id + '/preview';
      iframe.title = f.title + ' — walkthrough film';
      iframe.allow = 'autoplay; fullscreen; picture-in-picture';
      iframe.setAttribute('allowfullscreen', '');
      frame.appendChild(iframe);
    };

    cards.forEach(function (c) {
      c.addEventListener('click', function (e) {
        e.preventDefault();
        opener = c;
        var id = c.getAttribute('data-film');
        var idx = 0;
        films.forEach(function (f, k) { if (f.id === id) idx = k; });
        show(idx);
        dlg.showModal();
        document.body.classList.add('menu-open');
      });
    });
    // Clean-up runs directly on close so the film always stops and the page unlocks
    var shutPlayer = function () {
      if (dlg.open) dlg.close();
      frame.innerHTML = '';
      document.body.classList.remove('menu-open');
      if (opener) { opener.focus(); opener = null; }
    };
    dlg.querySelector('[data-close]').addEventListener('click', shutPlayer);
    dlg.querySelector('[data-prev]').addEventListener('click', function () { show(current - 1); });
    dlg.querySelector('[data-next]').addEventListener('click', function () { show(current + 1); });
    dlg.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowLeft') show(current - 1);
      else if (e.key === 'ArrowRight') show(current + 1);
    });
    dlg.addEventListener('click', function (e) { if (e.target === dlg || e.target.classList.contains('cinema__stage')) shutPlayer(); });
    dlg.addEventListener('close', shutPlayer);
    dlg.addEventListener('cancel', function () { setTimeout(shutPlayer, 0); });
  }

  /* Films page filter ------------------------------------------------------ */
  var fgrid = document.querySelector('[data-film-grid]');
  if (fgrid) {
    var fbtns = document.querySelectorAll('[data-film-filter]');
    var fstatus = document.querySelector('[data-film-status]');
    fbtns.forEach(function (btn) {
      btn.addEventListener('click', function () {
        var want = btn.getAttribute('data-film-filter');
        var n = 0;
        fbtns.forEach(function (b) { b.setAttribute('aria-pressed', String(b === btn)); });
        fgrid.querySelectorAll('[data-category]').forEach(function (card) {
          var ok = want === 'all' || card.getAttribute('data-category') === want;
          card.hidden = !ok;
          if (ok) { n++; card.classList.remove('reveal-init', 'reveal-ready', 'reveal-in'); }
        });
        if (fstatus) fstatus.textContent = n + (n === 1 ? ' film' : ' films') + ' shown';
      });
    });
  }

  /* Custom cursor on films and projects (desktop only) ---------------------- */
  if (finePointer && !reduce) {
    var cursor = document.createElement('div');
    cursor.className = 'cursor';
    cursor.setAttribute('aria-hidden', 'true');
    document.body.appendChild(cursor);
    var label = '';
    document.addEventListener('mousemove', function (e) {
      cursor.style.setProperty('--cx', e.clientX + 'px');
      cursor.style.setProperty('--cy', e.clientY + 'px');
      var t = e.target.closest ? e.target.closest('[data-cursor]') : null;
      var want = t ? t.getAttribute('data-cursor') : '';
      if (want !== label) {
        label = want;
        if (want) cursor.textContent = want;
        cursor.classList.toggle('is-on', !!want);
      }
    }, { passive: true });
    document.addEventListener('mouseleave', function () { cursor.classList.remove('is-on'); label = ''; });
    document.addEventListener('mousedown', function () { cursor.classList.remove('is-on'); label = ''; });
  }
})();

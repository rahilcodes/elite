import io
def patch(p, pairs):
    s = io.open(p, encoding='utf-8').read()
    for a, b in pairs:
        assert s.count(a) == 1, (s.count(a), a[:70])
        s = s.replace(a, b)
    io.open(p, 'w', encoding='utf-8', newline='\n').write(s)

# 1. hero loop on every screen size, phone gets the portrait version
patch('site/js/main.js', [
 ("  if (hero && !reduce && !saveData && window.matchMedia('(min-width: 828px)').matches) {",
  "  if (hero && !reduce && !saveData) {"),
 ("      loop.src = hero.getAttribute('data-loop');",
  "      var phone = window.matchMedia('(max-width: 827px)').matches && hero.getAttribute('data-loop-mobile');\n"
  "      loop.src = phone || hero.getAttribute('data-loop');"),
 # featured filter on the projects page
 ("        var match = filter === 'all' || card.getAttribute('data-category') === filter;",
  "        var match = filter === 'all' || card.getAttribute('data-category') === filter ||\n"
  "          (filter === 'featured' && card.hasAttribute('data-featured'));"),
])
patch('build/home-main.html', [
 ('data-loop="assets/films/hero-loop.webp">', 'data-loop="assets/films/hero-loop.webp" data-loop-mobile="assets/films/hero-loop-mobile.webp">'),
])
patch('site/css/styles.css', [
 (".filmhero__poster { animation: kenburns 22s ease-in-out infinite alternate;", ".filmhero__poster { animation: kenburns 12s ease-in-out infinite alternate;"),
 ("@media (min-width: 828px) { .filmhero__aside { padding-bottom: 68px; } }",
  "@media (min-width: 828px) { .filmhero__aside { padding-bottom: 68px; } }\n"
  "@media (max-width: 827px) { .filmhero.is-playing .filmhero__poster { opacity: 0; } }"),
 (".project-card h3 { margin-bottom: 6px; transition: color var(--t-fast); }",
  ".project-card h3 { margin-bottom: 6px; transition: color var(--t-fast); }\n"
  ".project-card__flag { display: inline-flex; align-items: center; gap: 8px; margin-bottom: 10px; font-size: var(--fs-tag); letter-spacing: var(--ls-eyebrow); text-transform: uppercase; color: var(--bronze-deep); }\n"
  ".project-card__flag::before { content: \"\"; width: 14px; height: 1px; background: var(--bronze); }"),
])

# 2. featured projects: six on the home page, featured first (and a Featured filter) on the projects page
patch('build/build.py', [
 ("def project_card(p, root='', heading='h2'):\n    return '''        <a class=\"project-card\" href=\"%sprojects/%s.html\" data-category=\"%s\" data-cursor=\"View\" data-reveal>\n          <div class=\"project-card__media\">%s</div>\n          <div class=\"project-card__meta\">\n            <div>\n              <%s class=\"h3\">%s</%s>",
  "# The client's highlighted work, in the order it is shown on the home page\nHOME_FEATURED = ['cummings-lodge-multipurpose-building', 'demerara-estates-residence-1', 'peters-hall-residence-3',\n                 'floral-park-residence', 'demerara-estates-residence-2', 'earls-court-apartments']\n\n\ndef by_slug(slug):\n    return next(p for p in PROJECTS if p['slug'] == slug)\n\n\ndef projects_featured_first():\n    lead = [by_slug(s) for s in HOME_FEATURED]\n    rest_featured = [p for p in PROJECTS if p['featured'] and p not in lead]\n    others = [p for p in PROJECTS if not p['featured']]\n    return lead + rest_featured + others\n\n\ndef project_card(p, root='', heading='h2'):\n    return '''        <a class=\"project-card\" href=\"%sprojects/%s.html\" data-category=\"%s\"%s data-cursor=\"View\" data-reveal>\n          <div class=\"project-card__media\">%s</div>\n          <div class=\"project-card__meta\">\n            <div>%s\n              <%s class=\"h3\">%s</%s>"),
 ("        </a>''' % (root, p['slug'], p['cat'].lower(), pimg(p, 1, p['title'] + ' — 3D view', root=root),\n                  heading, e(p['title']), heading, e(p['place']), p['cat'])",
  "        </a>''' % (root, p['slug'], p['cat'].lower(), ' data-featured' if p['featured'] else '',\n                  pimg(p, 1, p['title'] + ' — 3D view', root=root),\n                  '\n              <span class=\"project-card__flag\">Featured</span>' if p['featured'] else '',\n                  heading, e(p['title']), heading, e(p['place']), p['cat'])"),
 ("    cards = '\n'.join(project_card(p, heading='h3') for p in PROJECTS[:3])",
  "    cards = '\n'.join(project_card(by_slug(s), heading='h3') for s in HOME_FEATURED)"),
 ("        <button class=\"filter-btn\" type=\"button\" data-filter=\"all\" aria-pressed=\"true\">All <span>%d</span></button>\n        <button class=\"filter-btn\" type=\"button\" data-filter=\"residential\"",
  "        <button class=\"filter-btn\" type=\"button\" data-filter=\"all\" aria-pressed=\"true\">All <span>%d</span></button>\n        <button class=\"filter-btn\" type=\"button\" data-filter=\"featured\" aria-pressed=\"false\">Featured <span>%d</span></button>\n        <button class=\"filter-btn\" type=\"button\" data-filter=\"residential\""),
 ("''' % (len(PROJECTS), count('Residential'), count('Commercial'), count('Institutional'),\n       '\n'.join(project_card(p) for p in PROJECTS))",
  "''' % (len(PROJECTS), sum(1 for p in PROJECTS if p['featured']), count('Residential'), count('Commercial'), count('Institutional'),\n       '\n'.join(project_card(p) for p in projects_featured_first()))"),
])
print('ok')

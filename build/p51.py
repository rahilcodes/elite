import io, re
p = 'build/build.py'
s = io.open(p, encoding='utf-8').read()

def rep(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:60])
    s = s.replace(a, b)

rep(r"""def project_card(p, root='', heading='h2'):
    return '''        <a class="project-card" href="%sprojects/%s.html" data-category="%s" data-cursor="View" data-reveal>
          <div class="project-card__media">%s</div>
          <div class="project-card__meta">
            <div>
              <%s class="h3">%s</%s>""",
r"""# The client's highlighted work, in the order it is shown on the home page
HOME_FEATURED = ['cummings-lodge-multipurpose-building', 'demerara-estates-residence-1', 'peters-hall-residence-3',
                 'floral-park-residence', 'demerara-estates-residence-2', 'earls-court-apartments']


def by_slug(slug):
    return next(p for p in PROJECTS if p['slug'] == slug)


def projects_featured_first():
    lead = [by_slug(s) for s in HOME_FEATURED]
    rest_featured = [p for p in PROJECTS if p['featured'] and p not in lead]
    others = [p for p in PROJECTS if not p['featured']]
    return lead + rest_featured + others


def project_card(p, root='', heading='h2'):
    return '''        <a class="project-card" href="%sprojects/%s.html" data-category="%s"%s data-cursor="View" data-reveal>
          <div class="project-card__media">%s</div>
          <div class="project-card__meta">
            <div>%s
              <%s class="h3">%s</%s>""")

rep(r"""        </a>''' % (root, p['slug'], p['cat'].lower(), pimg(p, 1, p['title'] + ' — 3D view', root=root),
                  heading, e(p['title']), heading, e(p['place']), p['cat'])""",
r"""        </a>''' % (root, p['slug'], p['cat'].lower(), ' data-featured' if p['featured'] else '',
                  pimg(p, 1, p['title'] + ' — 3D view', root=root),
                  '\n              <span class="project-card__flag">Featured</span>' if p['featured'] else '',
                  heading, e(p['title']), heading, e(p['place']), p['cat'])""")

rep(r"""    cards = '\n'.join(project_card(p, heading='h3') for p in PROJECTS[:3])""",
    r"""    cards = '\n'.join(project_card(by_slug(s), heading='h3') for s in HOME_FEATURED)""")

rep(r"""        <button class="filter-btn" type="button" data-filter="all" aria-pressed="true">All <span>%d</span></button>
        <button class="filter-btn" type="button" data-filter="residential\"""",
    r"""        <button class="filter-btn" type="button" data-filter="all" aria-pressed="true">All <span>%d</span></button>
        <button class="filter-btn" type="button" data-filter="featured" aria-pressed="false">Featured <span>%d</span></button>
        <button class="filter-btn" type="button" data-filter="residential\"""")

rep(r"""''' % (len(PROJECTS), count('Residential'), count('Commercial'), count('Institutional'),
       '\n'.join(project_card(p) for p in PROJECTS))""",
    r"""''' % (len(PROJECTS), sum(1 for p in PROJECTS if p['featured']), count('Residential'), count('Commercial'), count('Institutional'),
       '\n'.join(project_card(p) for p in projects_featured_first()))""")
io.open(p, 'w', encoding='utf-8', newline='\n').write(s)
print('ok')

"""Generates the static pages in site/ so the shared header, footer and <head>
stay identical on every page. Run from the project root:  python build/build.py
The output is plain HTML; nothing here is needed at runtime."""
import io, json, os
from html import escape as e

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'site')
SITE = 'https://elitearchitecturegy.com/'
# Changes whenever the stylesheet or script changes, so browsers never show a stale copy
import hashlib
VERSION = hashlib.md5(b''.join(open(os.path.join(OUT, f), 'rb').read() for f in ('css/styles.css', 'js/main.js'))).hexdigest()[:8]
PHONE = '+592-618-9518'
TEL = 'tel:+5926189518'
WA = 'https://wa.me/5926189518'
MAPS = 'https://www.google.com/maps/search/?api=1&amp;query=6.8221819%2C-58.1375138&amp;query_place_id=ChIJ03RHaZnvr40RdVLlgewALBc'
MAP_EMBED = 'https://maps.google.com/maps?q=Elite%20Architecture%2C%205th%20%26%20Earl%27s%20Ave%2C%20Subryanville%2C%20Georgetown%2C%20Guyana&amp;ll=6.8221819,-58.1375138&amp;z=16&amp;output=embed'
EMAIL = 'info@elitearchitecturegy.com'
STREET = "262 5th &amp; Earl's Avenue"
AREA = 'Subryanville, Georgetown, Guyana'

NAV = [('services.html', 'Services'), ('projects.html', 'Projects'), ('about.html', 'About'),
       ('team.html', 'Team'), ('faq.html', 'FAQ'), ('contact.html', 'Contact')]
FOOTER_EXTRA = [('careers.html', 'Careers')]

SIZES_CARD = '(min-width: 1040px) 30vw, (min-width: 700px) 45vw, 92vw'
SIZES_SPLIT = '(min-width: 900px) 45vw, 92vw'
SIZES_FULL = '(min-width: 1500px) 1380px, 94vw'


def u(pid, w, h=None, q=75):
    s = 'https://images.unsplash.com/photo-%s?auto=format&amp;fit=crop&amp;w=%d' % (pid, w)
    if h:
        s += '&amp;h=%d' % h
    return s + '&amp;q=%d' % q


def img(pid, alt, ratio=(4, 3), sizes=SIZES_CARD, widths=(480, 800, 1200), lazy=True):
    rw, rh = ratio
    hh = lambda w: round(w * rh / rw)
    mid = widths[1]
    srcset = ', '.join('%s %dw' % (u(pid, w, hh(w)), w) for w in widths)
    extra = ' loading="lazy"' if lazy else ' fetchpriority="high"'
    return '<img src="%s" srcset="%s" sizes="%s" width="%d" height="%d" alt="%s"%s decoding="async">' % (
        u(pid, mid, hh(mid)), srcset, sizes, mid, hh(mid), e(alt), extra)


def business_ld():
    return {
        "@context": "https://schema.org",
        "@type": ["LocalBusiness", "ProfessionalService"],
        "@id": SITE + "#business",
        "name": "Elite Architecture",
        "slogan": "Vision Evolved. Spaces Revolved.",
        "description": "Architecture and construction consultancy in Georgetown, Guyana, with 18+ years of experience.",
        "url": SITE,
        "telephone": PHONE,
        "image": SITE + "assets/logo-dark.png",
        "logo": SITE + "assets/logo-dark.png",
        "email": EMAIL,
        "address": {"@type": "PostalAddress", "streetAddress": "262 5th & Earl's Avenue, Subryanville",
                    "addressLocality": "Georgetown", "addressCountry": "GY"},
        "geo": {"@type": "GeoCoordinates", "latitude": 6.8221819, "longitude": -58.1375138},
        "openingHoursSpecification": [
            {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
             "opens": "09:00", "closes": "22:00"},
            {"@type": "OpeningHoursSpecification", "dayOfWeek": "Saturday", "opens": "11:00", "closes": "20:00"}],
        "founder": {"@type": "Person", "name": "Vickram Paul", "jobTitle": "CEO & Principal Architect"},
        "areaServed": {"@type": "Country", "name": "Guyana"},
        "contactPoint": {"@type": "ContactPoint", "telephone": PHONE, "email": EMAIL, "contactType": "customer service",
                         "areaServed": "GY", "availableLanguage": "English"},
        "knowsAbout": ["Architecture", "Building design", "3D concept design", "Construction drawings",
                       "As-built drawings", "Schematic design", "Landscape design", "Civil engineering consultancy"],
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Architecture services", "itemListElement": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": s['title']}} for s in SERVICES]},
    }


def crumbs_ld(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + (h if h != 'index.html' else '')}
        for i, (h, n) in enumerate(items)]}


def breadcrumb(items, root=''):
    """items: [(href-from-site-root, label)], last one is the current page."""
    out = ['<nav aria-label="Breadcrumb"><ol class="breadcrumb">']
    for i, (h, n) in enumerate(items):
        if i == len(items) - 1:
            out.append('<li aria-current="page">%s</li>' % e(n))
        else:
            out.append('<li><a href="%s%s">%s</a></li>' % (root, h, e(n)))
    out.append('</ol></nav>')
    return ''.join(out)


def page_hero(crumbs, eyebrow, h1, lead, root=''):
    return '''  <section class="page-hero" aria-labelledby="page-title">
    <div class="container page-hero__inner">
      %s
      <p class="eyebrow">%s</p>
      <h1 id="page-title">%s</h1>
      <p class="lead">%s</p>
    </div>
  </section>
''' % (breadcrumb(crumbs, root), eyebrow, h1, lead)


def cta(root='', eyebrow='Start a project', title="Ready to start? Let's talk about your project.",
        text='Book a first consultation — no drawings required. Just bring your ideas.'):
    bg = '1518005020951-eccb494ad742'
    return '''  <section class="cta-band on-dark" aria-labelledby="cta-title">
    <img class="cta-band__bg" src="%s" srcset="%s 800w, %s 1600w, %s 2400w" sizes="100vw" width="1600" height="1067" alt="" loading="lazy" decoding="async">
    <div class="cta-band__inner" data-reveal>
      <div class="cta-band__copy">
        <p class="eyebrow">%s</p>
        <h2 id="cta-title">%s</h2>
        <p>%s</p>
      </div>
      <div class="cta-band__actions">
        <a class="btn btn--light" href="%scontact.html">Book a Consultation <span aria-hidden="true">→</span></a>
        <a class="cta-band__phone" href="%s">Or call %s</a>
      </div>
    </div>
  </section>
''' % (u(bg, 1600, q=60), u(bg, 800, q=60), u(bg, 1600, q=60), u(bg, 2400, q=60), eyebrow, title, text, root, TEL, PHONE)


def nav_links(active, root):
    return '\n'.join('      <a href="%s%s"%s>%s</a>' % (root, h, ' aria-current="page"' if h == active else '', n)
                     for h, n in NAV)


def page(path, title, desc, main, active=None, og_image=None, ld=(), base=None, noindex=False):
    depth = path.count('/')
    root = '' if base else '../' * depth
    canonical = SITE + ('' if path == 'index.html' else path)
    og_image = og_image or u('1600585154340-be6161a56a0c', 1200, 630, 80)
    ld_html = '\n'.join('<script type="application/ld+json">%s</script>' % json.dumps(x, ensure_ascii=False)
                        for x in ld)
    footer_a = lambda h, n: '        <a href="%s%s"%s>%s</a>' % (root, h, ' aria-current="page"' if h == active else '', n)
    html = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{base}<title>{title}</title>
<meta name="description" content="{desc}">
{robots}<link rel="canonical" href="{canonical}">
<meta name="theme-color" content="#F5F2EC">

<meta property="og:type" content="website">
<meta property="og:site_name" content="Elite Architecture">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{og_image}">
<meta property="og:locale" content="en_GY">
<meta name="twitter:card" content="summary_large_image">

<link rel="icon" href="{root}assets/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{root}assets/apple-touch-icon.png">
<link rel="manifest" href="{root}site.webmanifest">

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preconnect" href="https://images.unsplash.com">
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;1,300;1,400&amp;family=Jost:wght@300;400;500&amp;display=swap" rel="stylesheet">
<link rel="stylesheet" href="{root}css/styles.css?v={ver}">

{ld}
</head>
<body>
<a class="skip-link" href="{self}#main">Skip to content</a>

<header class="site-header">
  <div class="site-header__inner">
    <a class="site-logo" href="{root}index.html" aria-label="Elite Architecture — home"><img src="{root}assets/logo-dark.png" alt="Elite Architecture" width="720" height="139"></a>
    <nav class="site-nav" aria-label="Primary">
{nav}
    </nav>
    <div class="site-header__actions">
      <a class="site-header__phone" href="{tel}">{phone}</a>
      <a class="btn btn--primary btn--sm" href="{root}contact.html">Book a Consultation</a>
    </div>
    <button class="burger" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="mobile-menu">
      <span></span><span></span>
    </button>
  </div>
</header>

<div class="mobile-menu" id="mobile-menu" role="dialog" aria-modal="true" aria-label="Menu" hidden>
  <div class="mobile-menu__top">
    <img src="{root}assets/logo-dark.png" alt="Elite Architecture" width="720" height="139">
    <button class="mobile-menu__close" type="button">Close</button>
  </div>
  <nav class="mobile-menu__nav" aria-label="Mobile">
{nav}
  </nav>
  <a class="btn btn--primary btn--block" href="{root}contact.html">Book a Consultation</a>
  <a class="mobile-menu__phone" href="{tel}">{phone} · Georgetown, Guyana</a>
</div>

<main id="main">
{main}</main>

<footer class="site-footer">
  <div class="footer-elevation" aria-hidden="true">
    <svg viewBox="0 0 1400 170" preserveAspectRatio="xMidYMax slice" fill="none" stroke="currentColor" stroke-width="1" vector-effect="non-scaling-stroke">
      <path d="M0 150H1400"/>
      <path d="M60 150V95l70-40 70 40v55M118 150v-35h24v35M76 108h26v20H76zM158 108h26v20h-26z"/>
      <circle cx="240" cy="108" r="22"/><path d="M240 130v20"/>
      <path d="M285 70h250M300 70v80M520 70v80M300 110h220M320 80h60v22h-60zM400 80h100v22H400zM320 120h40v30M360 120v30M380 120h120v22H380z"/>
      <circle cx="562" cy="118" r="16"/><path d="M562 134v16"/>
      <path d="M600 150V30h160v120M600 54h160M600 78h160M600 102h160M600 126h160M640 30v120M680 30v120M720 30v120"/>
      <path d="M820 150V50h80v100M840 50V30h40v20M860 30V4M820 70h80M820 90h80M820 110h80M820 130h80"/>
      <path d="M950 105l50-25h200l50 25M960 105v45M1240 105v45M960 105h280M1000 105v45M1040 105v45M1080 105v45M1120 105v45M1160 105v45M1200 105v45"/>
      <circle cx="1285" cy="112" r="20"/><path d="M1285 132v18"/>
      <path d="M1320 150v-40l35-22 35 22v40M1345 150v-24h20v24"/>
      <g class="footer-elevation__dim"><path d="M300 164h220M300 159v10M520 159v10M600 164h160M600 159v10M760 159v10M960 164h280M960 159v10M1240 159v10"/></g>
    </svg>
  </div>
  <div class="container">
    <div class="footer-sheet">
      <div class="footer-cell footer-cell--brand">
        <img class="site-footer__logo" src="{root}assets/logo-dark.png" alt="Elite Architecture" width="720" height="139" loading="lazy">
        <p class="site-footer__about">Architecture &amp; construction consultancy in Georgetown, Guyana. Elevating luxury living through cutting-edge architecture.</p>
      </div>
      <nav class="footer-cell" aria-label="Footer">
        <p class="footer-cell__label"><span>01</span>Explore</p>
{f1}
      </nav>
      <nav class="footer-cell" aria-label="Footer — studio">
        <p class="footer-cell__label"><span>02</span>Studio</p>
{f2}
      </nav>
      <address class="footer-cell footer-cell--contact">
        <p class="footer-cell__label"><span>03</span>Contact</p>
        <a href="{tel}">{phone}</a>
        <a href="{wa}" target="_blank" rel="noopener">WhatsApp us</a>
        <a href="mailto:{email}">{email}</a>
        <span>{street}<br>{area}</span>
      </address>
    </div>
    <dl class="footer-titleblock">
      <div><dt>Site</dt><dd>6.8222° N<br>58.1375° W</dd></div>
      <div><dt>Hours</dt><dd>Mon–Fri 9am–10pm<br>Sat 11am–8pm</dd></div>
      <div><dt>Scale</dt><dd class="footer-scale"><span class="footer-scale__bar" aria-hidden="true"></span><span>1:1 with<br>your vision</span></dd></div>
      <div class="footer-titleblock__north"><dt>Drawn by</dt><dd>Vickram Paul<br>18+ years</dd>
        <svg viewBox="0 0 40 40" width="40" height="40" fill="none" stroke="currentColor" stroke-width="1" aria-hidden="true"><circle cx="20" cy="20" r="15"/><path d="M20 8l6 20-6-5-6 5z"/><path d="M20 2v4"/></svg>
      </div>
    </dl>
    <div class="site-footer__bottom">
      <span>© <span data-year>2026</span> Elite Architecture. All rights reserved.</span>
      <span>Designed &amp; developed by <a href="https://creativals.com" target="_blank" rel="noopener">Creativals.com</a></span>
      <a class="site-footer__top" href="{self}#main">Back to top <span aria-hidden="true">↑</span></a>
    </div>
  </div>
</footer>

<div class="contact-fab" data-fab>
  <div class="contact-fab__menu" id="fab-menu" hidden>
    <a href="{wa}" target="_blank" rel="noopener"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 20l1.4-4.2A8 8 0 1 1 8.6 19z"/><path d="M9 10.5h6M9 13.5h4"/></svg>WhatsApp</a>
    <a href="{tel}"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a1 1 0 0 1-1 1A15 15 0 0 1 4 5a1 1 0 0 1 1-1z"/></svg>Call {phone}</a>
    <a href="mailto:{email}"><svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="5" width="18" height="14"/><path d="M3 6l9 7 9-7"/></svg>Email us</a>
    <a href="{root}contact.html"><svg viewBox="0 0 24 24" aria-hidden="true"><rect x="4" y="5" width="16" height="15"/><path d="M4 10h16M9 3v4M15 3v4"/></svg>Book a consultation</a>
  </div>
  <button class="contact-fab__toggle" type="button" aria-expanded="false" aria-controls="fab-menu">
    <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 20l1.4-4.2A8 8 0 1 1 8.6 19z"/><path d="M9 10.5h6M9 13.5h4"/></svg>
    <span>Contact us</span>
  </button>
</div>

<nav class="contact-bar" aria-label="Quick contact" data-contact-bar>
  <a href="{tel}"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a1 1 0 0 1-1 1A15 15 0 0 1 4 5a1 1 0 0 1 1-1z"/></svg>Call</a>
  <a href="{wa}" target="_blank" rel="noopener"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 20l1.4-4.2A8 8 0 1 1 8.6 19z"/><path d="M9 10.5h6M9 13.5h4"/></svg>WhatsApp</a>
  <a class="contact-bar__primary" href="{root}contact.html">Book <span aria-hidden="true">→</span></a>
</nav>

<script src="{root}js/main.js?v={ver}" defer></script>
</body>
</html>
'''.format(base='<base href="/">\n' if base else '', title=e(title), desc=e(desc), canonical=canonical,
           robots='<meta name="robots" content="noindex">\n' if noindex else '',
           og_image=og_image, root=root, ld=ld_html, nav=nav_links(active, root), tel=TEL, phone=PHONE, wa=WA,
           main=main, self=path if base else '', ver=VERSION, email=EMAIL, street=STREET, area=AREA,
           f1='\n'.join(footer_a(h, n) for h, n in NAV[:3]), f2='\n'.join(footer_a(h, n) for h, n in NAV[3:] + FOOTER_EXTRA))
    full = os.path.join(OUT, path.replace('/', os.sep))
    os.makedirs(os.path.dirname(full), exist_ok=True)
    io.open(full, 'w', encoding='utf-8', newline='\n').write(html)
    print('wrote', path)


# ---------------------------------------------------------------------------
# Content
# ---------------------------------------------------------------------------
ICONS = {
    'building': '<svg viewBox="0 0 24 24" stroke-linecap="round" aria-hidden="true"><rect x="4" y="9" width="16" height="12"/><path d="M2 10 12 3l10 7"/></svg>',
    'cube': '<svg viewBox="0 0 24 24" stroke-linejoin="round" aria-hidden="true"><path d="M12 3 20 7.5v9L12 21l-8-4.5v-9z"/><path d="M12 12v9M12 12 4 7.5M12 12l8-4.5"/></svg>',
    'grid': '<svg viewBox="0 0 24 24" stroke-linecap="round" aria-hidden="true"><rect x="3" y="3" width="18" height="18"/><path d="M3 12h18M12 3v18"/></svg>',
    'pencil': '<svg viewBox="0 0 24 24" stroke-linecap="round" aria-hidden="true"><path d="M3 17 17 3l4 4L7 21H3z"/><path d="M14 6l4 4"/></svg>',
    'sheet': '<svg viewBox="0 0 24 24" stroke-linecap="round" aria-hidden="true"><rect x="5" y="3" width="14" height="18"/><path d="M9 8h6M9 12h6M9 16h4"/></svg>',
    'leaf': '<svg viewBox="0 0 24 24" stroke-linecap="round" aria-hidden="true"><path d="M4 20c0-8 5-13 14-14-1 9-6 14-14 14z"/><path d="M4 20 14 10"/></svg>',
    'structure': '<svg viewBox="0 0 24 24" stroke-linecap="round" aria-hidden="true"><path d="M3 20h18M5 20V9l7-5 7 5v11"/><path d="M9 20v-6h6v6"/></svg>',
}

SERVICES = [
    dict(slug='building-designs', title='Building Designs', icon='building', img='1600596542815-ffad4c1539a9',
         alt='Modern home exterior with clean lines and large windows',
         short='Homes and commercial spaces designed around the way you actually live and work.',
         long='Every building starts with how you want to live or work in it. We design homes, offices and public buildings that fit your plot, your budget and Guyana\'s climate — with layouts that make sense on day one and still work years from now.',
         benefits=['A design shaped around your routine, family or business', 'Natural light and cross-ventilation planned in from the start',
                   'Layouts that respect your budget and your plot', 'One team carrying the design through to construction drawings'],
         steps=['Consultation and site visit', 'Brief, budget and concept options', 'Design development with your feedback', 'Final design, ready for drawings and approval']),
    dict(slug='3d-concept-designs', title='3D Concept Designs', icon='cube', img='1613490493576-7fde63acd811',
         alt='Rendered view of a contemporary villa',
         short='Walk through your building on screen before a single block is laid.',
         long='Plans can be hard to read. A 3D concept shows you exactly what you are getting — the shape of the building, the materials, the light in each room — so you can make changes while they are still free.',
         benefits=['See your building from every angle before you commit', 'Compare finishes, colours and roof forms side by side',
                   'Catch layout problems before they reach site', 'Images you can share with family, partners or lenders'],
         steps=['We model your approved layout', 'Materials and finishes are applied', 'You review exterior and interior views', 'Revisions, then final images']),
    dict(slug='schematic-designs', title='Schematic Designs', icon='grid', img='1503387762-592deb58ef4e',
         alt='Architect sketching a floor plan at a desk',
         short='Early layouts that settle the big decisions — space, flow and budget — first.',
         long='Schematic design is where the big questions are answered: how many rooms, how they connect, where the building sits on the land and roughly what it will cost. Getting this stage right saves time and money at every stage after it.',
         benefits=['Clear floor plans and site layout early on', 'Options to compare before you settle on one direction',
                   'An early sense of cost before detailed work begins', 'A firm base for 3D concepts and construction drawings'],
         steps=['Brief and site information gathered', 'Layout options sketched', 'Preferred option refined with you', 'Schematic set signed off']),
    dict(slug='construction-drawings', title='Construction Drawings', icon='pencil', img='1541888946425-d81bb19240f5',
         alt='Building under construction with scaffolding',
         short='Clear, complete drawings your builder can price accurately and follow with confidence.',
         long='Good drawings protect you. Our construction sets give your contractor everything needed to price the job properly and build it as designed — plans, sections, elevations, details and schedules, coordinated and clearly labelled.',
         benefits=['Accurate contractor pricing with fewer surprises', 'Fewer questions and delays on site',
                   'Drawings prepared for the approval process', 'Details that protect the quality of the finished build'],
         steps=['Approved design is developed in detail', 'Structure and services coordinated', 'Full drawing set prepared and checked', 'Issued for approval, pricing and construction']),
    dict(slug='as-built-drawings', title='As-Built Drawings', icon='sheet', img='1497366811353-6870744d04b2',
         alt='Completed modern office interior',
         short='An accurate record of what was built — for approvals, renovations and resale.',
         long='If your building has no drawings, or the drawings no longer match what stands on site, we measure and document it as it is today. As-built drawings are often needed for approvals, financing, insurance, renovation or sale.',
         benefits=['A reliable record of your property as it stands', 'Supports applications, valuations and sales',
                   'A sound starting point for extensions and renovations', 'Digital files you can keep and reuse'],
         steps=['Site visit and measured survey', 'Existing building drawn up', 'Drawings checked against site', 'Final set issued in print and digital']),
    dict(slug='landscape-designs', title='Landscape Designs', icon='leaf', img='1558904541-efa843a96f01',
         alt='Landscaped garden with planting and pathway',
         short="Gardens, yards and outdoor rooms that make the most of Guyana's climate.",
         long='Outdoor space is living space. We plan yards, gardens, driveways and outdoor rooms that handle heavy rain and strong sun, stay easy to maintain, and make the building feel finished.',
         benefits=['Shade, drainage and planting suited to local conditions', 'Outdoor areas that extend how you use your home',
                   'Driveways, paths and parking planned with the building', 'A more complete, more valuable property'],
         steps=['Site walk and wish list', 'Layout of hard and soft landscaping', 'Planting and material selection', 'Landscape plan ready for installation']),
    dict(slug='civil-engineering-consultancy', title='Civil Engineering Consultancy', icon='structure', img='1504307651254-35680f356dfd',
         alt='Engineer reviewing work on a construction site',
         short='Structural and site engineering advice so your design is as sound as it is beautiful.',
         long='A beautiful design still has to stand up, drain properly and sit safely on its ground. Our engineering consultancy works alongside the design team so structure, foundations and site works are considered from the beginning.',
         benefits=['Foundations and structure suited to your site', 'Drainage and site levels planned early',
                   'Engineering input that avoids costly redesign', 'Design and engineering advice from one team'],
         steps=['Review of site and design', 'Engineering advice and options', 'Coordination with the drawings', 'Support through approval and construction']),
]

# Real client projects, migrated from the previous website. Photos live in
# site/assets/projects/<slug>/NN-{480,800,1600}.webp (originals: client-originals/projects/).
PROJECTS = json.load(io.open(os.path.join(ROOT, 'build', 'projects.json'), encoding='utf-8'))
LEADS = {
    'Residential': 'A residential design for %s, developed and visualised in 3D by Elite Architecture.',
    'Commercial': 'A commercial design for %s, developed and visualised in 3D by Elite Architecture.',
    'Institutional': 'An institutional design for %s, developed and visualised in 3D by Elite Architecture.',
}


def pimg(p, n, alt, sizes=SIZES_CARD, root='', lazy=True):
    base = '%sassets/projects/%s/%02d' % (root, p['slug'], n)
    extra = ' loading="lazy"' if lazy else ' fetchpriority="high"'
    return ('<img src="%s-800.webp" srcset="%s-480.webp 480w, %s-800.webp 800w, %s-1600.webp 1600w" sizes="%s" '
            'width="800" height="450" alt="%s"%s decoding="async">') % (base, base, base, base, sizes, e(alt), extra)


# Client logos migrated from the previous website: (file slug, client name, width, height)
CLIENTS = [
    ('nirva', 'Nirva Super Convenience', 150, 95),
    ('steves-jewellery', "Steve's Jewellery", 150, 95),
    ('rose-ramdehol', 'Rose Ramdehol', 150, 95),
    ('guygas', 'GuyGas', 150, 95),
    ('raj-jewellery', 'Raj Jewellery', 150, 95),
    ('bm-soat-auto-spares', 'BM Soat Auto Spares', 150, 95),
    ('gr-engineering', 'GR Engineering Co.', 150, 95),
    ('action-invest-caribbean', 'Action Invest Caribbean Inc.', 150, 95),
    ('techlify', 'Techlify', 150, 95),
    ('impressions', 'Impressions', 150, 95),
    ('bm-soat-auto-sales', 'B.M. Soat Auto Sales', 150, 95),
    ('method4-engineering', 'Method4 Engineering', 150, 95),
    ('belco-eximport', 'Belco Eximport', 150, 95),
    ('jop-sp', 'JOP SP', 150, 95),
    ('giftland-mall', 'Giftland Mall', 150, 95),
    ('the-beauty-box', 'The Beauty Box + Health', 150, 95),
    ('bernies-pharmacy', "Bernie's Pharmacy", 150, 95),
    ('fairfield-rice', 'Fairfield Rice Inc.', 150, 95),
    ('massy-finance', 'Massy Finance Remittances', 300, 144),
    ('regency-suites-hotel', 'Regency Suites Hotel', 150, 95),
]


FAQS = [
    ('Why choose Elite Architecture?',
     'Because you get experience, creativity and care in one team. We have more than eighteen years of work behind us, we use current design technology, and we measure ourselves by whether you are satisfied. Our clients rate us 4.9 out of 5 on Google.'),
    ('What services do you offer?',
     'Building designs, 3D concept designs, schematic designs, construction drawings, as-built drawings, landscape designs and civil engineering consultancy. We can take a project from the first concept to a complete drawing set, or help with a single stage.'),
    ('What does an architect actually do for me?',
     'We turn your ideas, budget and plot into a building that can be approved, priced and built. That covers the design itself, 3D views so you can see it, the drawings your contractor builds from, and engineering advice to make sure it is sound. You deal with one team from the first conversation to the finished build.'),
    ('How do I start a project with Elite Architecture?',
     'Call or WhatsApp us on +592-618-9518, or send the form on our contact page. We arrange a first consultation to talk through what you want to build, where, and your budget. You do not need drawings or a finished plan — just your ideas.'),
    ('What should I bring to the first consultation?',
     'Anything you have: the location and size of your land, a transport or lease document if available, photos of the site, pictures of buildings you like, a rough room list and an idea of budget. If you have none of these yet, we can still begin.'),
    ('How long does the design process take?',
     'It depends on the size of the project and how quickly decisions are made. A house design typically moves from first sketches to a full construction set over a number of weeks; larger commercial or institutional buildings take longer. We give you a timeline for your project after the first consultation.'),
    ('Are you affordable to hire?',
     'Yes. Our prices are competitive and we shape our service to suit your budget without lowering the quality of the design. Fees depend on the type and size of the building and the services you need, so after we understand your project we give you a clear quotation before any work begins.'),
    ('Do you help with building approvals?',
     'Yes. We prepare drawings to the standard required for submission to the relevant authorities, such as the Central Housing and Planning Authority and your local council, and we can guide you through what is needed at each step.'),
    ('Can I see my building before it is built?',
     'Yes. Our 3D concept designs show the exterior and interior of your building with materials and colours applied. It is the easiest way to be sure about the design, and changes at this stage cost far less than changes on site.'),
    ('Do you design both homes and commercial buildings?',
     'We do. Our work includes residences, offices, hospitality venues and institutional buildings such as schools. The same team handles design, drawings and engineering consultancy across all of them.'),
    ('I already have a building but no drawings. Can you help?',
     'Yes. We measure the existing building and produce as-built drawings that record it accurately. These are useful for approvals, bank financing, insurance, renovations, extensions and resale.'),
    ('Do you work outside Georgetown?',
     'Yes. We are based in Georgetown and take on projects around Guyana. Tell us where your site is and we will let you know how we can help.'),
]

TEAM = [
    dict(name='Vickram Paul', role='CEO &amp; Principal Architect', img='vickram-paul',
         bio='Vickram founded and leads Elite Architecture, and sets the design direction for every project. '
             'He works by the studio motto — Vision Evolved. Spaces Revolved. — and is known by clients for being dependable, '
             'easy to talk to and hands-on, including regular visits to projects under construction.'),
    dict(name='Raza Jan', role='Architect', img='raza-jan',
         bio='Raza designs spaces that balance how a building looks with how it works. His eye for detail and his creative '
             'approach shape layouts that are practical to build and a pleasure to use.'),
    dict(name='Johanan Dolphin', role='Civil Engineer — Consultant', img='johanan-dolphin',
         bio='Johanan looks after the structure behind the design. He plans and checks each project for safety, efficiency and '
             'long life, so that what is drawn can be built soundly.'),
]


def service_card(s, i, root='', link=True):
    inner = '''<div class="service-card__top">%s<span class="service-card__num">%02d</span></div>
          <h3>%s</h3>
          <p>%s</p>''' % (ICONS[s['icon']], i, s['title'], s['short'])
    if link:
        return '        <a class="service-card" href="%s#%s" data-reveal>\n          %s\n        </a>' % (root, s['slug'], inner)
    return '        <div class="service-card" data-reveal>\n          %s\n        </div>' % inner


def info_card(num, title, text):
    return '''        <div class="service-card" data-reveal>
          <div class="service-card__top"><span class="service-card__num">%s</span></div>
          <h3>%s</h3>
          <p>%s</p>
        </div>''' % (num, title, text)


def project_card(p, root='', heading='h2'):
    return '''        <a class="project-card" href="%sprojects/%s.html" data-category="%s" data-reveal>
          <div class="project-card__media">%s</div>
          <div class="project-card__meta">
            <div>
              <%s class="h3">%s</%s>
              <p class="project-card__place">%s</p>
            </div>
            <span class="tag">%s</span>
          </div>
        </a>''' % (root, p['slug'], p['cat'].lower(), pimg(p, 1, p['title'] + ' — 3D view', root=root),
                  heading, e(p['title']), heading, e(p['place']), p['cat'])


def team_card(t, heading='h2', root=''):
    base = '%sassets/team/%s' % (root, t['img'])
    media = ('<div class="media media--1x1"><img src="%s-640.webp" srcset="%s-320.webp 320w, %s-640.webp 640w" sizes="%s" '
             'width="640" height="640" alt="%s, %s" loading="lazy" decoding="async"></div>') % (
        base, base, base, SIZES_CARD, e(t['name']), t['role'].replace('&amp;', 'and'))
    return '''        <article class="team-card" data-reveal>
          %s
          <div class="team-card__body">
            <%s class="h3">%s</%s>
            <p class="label">%s</p>
            <p class="body-sm">%s</p>
          </div>
        </article>''' % (media, heading, e(t['name']), heading, t['role'], t['bio'])


def build_home():
    main = io.open(os.path.join(ROOT, 'build', 'home-main.html'), encoding='utf-8').read()
    cards = '\n'.join(project_card(p, heading='h3') for p in PROJECTS[:3])
    a = main.index('<div class="grid-projects">')
    b = main.index('</div>\n    </div>\n  </section>', a)
    main = main[:a] + '<div class="grid-projects">\n' + cards + '\n      ' + main[b:]
    logos = '\n'.join(
        '        <li class="client-logo"><img src="assets/clients/%s.png" width="%d" height="%d" alt="%s" loading="lazy" decoding="async"></li>'
        % (slug, w, h, e(name)) for slug, name, w, h in CLIENTS)
    clients = '''  <!-- Clients -->
  <section id="clients" class="section section--sand" aria-labelledby="clients-title">
    <div class="container">
      <div class="section-head section-head--tight" data-reveal>
        <div>
          <p class="eyebrow">Our clients</p>
          <h2 id="clients-title">Trusted by businesses across Guyana.</h2>
        </div>
        <p class="section-head__aside">We value long relationships. These are some of the companies and people we have been proud to design for.</p>
      </div>
      <ul class="client-grid" data-reveal>
%s
      </ul>
    </div>
  </section>

''' % logos
    marker = '  <!-- Testimonials -->'
    assert marker in main
    main = main.replace(marker, clients + marker, 1)
    main = main.replace('<p class="stat__num">42<span>+</span></p>', '<p class="stat__num">100<span>+</span></p>')
    main = main.replace('Led by Vickram, Elite', 'Led by Vickram Paul, Elite')
    page('index.html',
         'Elite Architecture | Architects in Georgetown, Guyana',
         'Georgetown architecture and construction consultancy with 18+ years of experience. Building designs, 3D concepts and construction drawings. Call +592-618-9518.',
         main, ld=[business_ld()])


def build_about():
    crumbs = [('index.html', 'Home'), ('about.html', 'About')]
    why = [('I', 'One team, start to finish', 'Design, engineering consultancy and drawings from one team — no hand-offs.'),
           ('II', 'Service clients talk about', 'Customer service our clients call unmatched — 4.9 stars on Google.'),
           ('III', 'Designed for Guyana', "Designs built for Guyana's climate, materials and approval process."),
           ('IV', 'Plain language, no surprises', 'We explain each stage clearly and keep you informed from concept through construction.')]
    main = page_hero(crumbs, 'About the studio',
                     'Eighteen years of turning ideas into <em>buildings</em>.',
                     'Elite Architecture is an architecture and construction consultancy based in Georgetown, Guyana. We design homes, workplaces and public buildings — and stay with our clients until they are built.')
    main += '''
  <section class="section section--after-hero" aria-labelledby="story-title">
    <div class="container grid-split">
      <div class="media media--4x3" data-reveal>%s</div>
      <div class="prose" data-reveal>
        <p class="eyebrow">Our story</p>
        <h2 id="story-title">Vision evolved. Spaces revolved.</h2>
        <p>We design for better living. To us a home is more than a structure: it reflects the people who live in it, and it should make everyday life easier and more enjoyable.</p>
        <p>Led by Vickram Paul, the studio has spent more than eighteen years shaping homes, apartment buildings, offices, warehouses and schools across Guyana. Our work rests on three things — professional concept development, quality architectural design and construction consultancy.</p>
        <p>Every building tells a story. Ours is to make sure it is yours, built well, with the best materials and resources available.</p>
      </div>
    </div>
  </section>

  <section class="section section--sand" aria-labelledby="mission-title">
    <div class="container">
      <div class="section-head section-head--tight" data-reveal>
        <div>
          <p class="eyebrow">What drives us</p>
          <h2 id="mission-title">Our mission is a building you are proud of.</h2>
        </div>
        <p class="section-head__aside">A legacy of quality, innovation and client satisfaction guides every project, whatever its size.</p>
      </div>
      <div class="grid-cards">
%s
%s
%s
      </div>
    </div>
  </section>

  <section class="section section--dark on-dark about-block" aria-labelledby="why-title">
    <div class="container grid-split" data-reveal>
      <div>
        <p class="eyebrow">Why families and businesses choose us</p>
        <h2 id="why-title">18+ years of experience, and a team that listens.</h2>
        <ol class="numbered-list">
%s
        </ol>
      </div>
      <div class="stats">
        <div class="stat"><p class="stat__num">18<span>+</span></p><p class="stat__label">Years of experience</p></div>
        <div class="stat"><p class="stat__num">100<span>+</span></p><p class="stat__label">Happy clients</p></div>
        <div class="stat"><p class="stat__num">4.9<span class="star" aria-hidden="true">★</span></p><p class="stat__label">Google rating</p></div>
        <div class="stat"><p class="stat__num">6<span>+</span></p><p class="stat__label">Experienced staff</p></div>
      </div>
    </div>
  </section>

  <section class="section section--sand" aria-labelledby="reviews-title">
    <div class="container">
      <div class="section-head section-head--tight" data-reveal>
        <div>
          <p class="eyebrow">What clients say</p>
          <h2 id="reviews-title">In our clients' words</h2>
        </div>
        <a class="link-arrow" href="https://www.google.com/search?q=Elite+Architecture+Georgetown+Guyana" target="_blank" rel="noopener">Read all Google reviews →<span class="visually-hidden"> (opens in a new tab)</span></a>
      </div>
      <div class="grid-projects">
        <figure class="quote-card quote-card--ivory" data-reveal>
          <span class="stars" role="img" aria-label="5 out of 5 stars">★★★★★</span>
          <blockquote class="quote-card__sm">“Their customer service is unmatched in the industry.”</blockquote>
          <figcaption class="quote-card__author"><span class="avatar" aria-hidden="true">SR</span><div><p class="label">Susan Rodrigues</p><p class="caption">Google review</p></div></figcaption>
        </figure>
        <figure class="quote-card quote-card--ivory" data-reveal>
          <span class="stars" role="img" aria-label="5 out of 5 stars">★★★★★</span>
          <blockquote class="quote-card__sm">“Vickram is very dependable, easy to communicate with, and is always willing to put in extra effort.”</blockquote>
          <figcaption class="quote-card__author"><span class="avatar" aria-hidden="true">JK</span><div><p class="label">Joshua Kissoon</p><p class="caption">Google review</p></div></figcaption>
        </figure>
        <figure class="quote-card quote-card--ivory" data-reveal>
          <span class="stars" role="img" aria-label="5 out of 5 stars">★★★★★</span>
          <blockquote class="quote-card__sm">“The team displayed a high level of professionalism.”</blockquote>
          <figcaption class="quote-card__author"><span class="avatar" aria-hidden="true">NP</span><div><p class="label">Nome Persaud</p><p class="caption">Google review</p></div></figcaption>
        </figure>
      </div>
    </div>
  </section>

  <section class="section" aria-labelledby="team-title">
    <div class="container">
      <div class="section-head" data-reveal>
        <div>
          <p class="eyebrow">The people</p>
          <h2 id="team-title">Meet the team behind the drawings</h2>
        </div>
        <a class="link-arrow" href="team.html">Meet the full team →</a>
      </div>
      <div class="grid-projects">
%s
      </div>
    </div>
  </section>
''' % (img('1503387762-592deb58ef4e', 'Architectural plans being drawn by hand', (4, 3), SIZES_SPLIT, lazy=False),
       info_card('Mission', 'On time, on budget, beyond expectations', 'To deliver projects that arrive on schedule, respect the budget and use sustainable building practices that reduce our impact on the environment.'),
       info_card('Vision', 'Buildings that give back', 'A future where every building combines innovation, sustainability and human connection, and adds something good to the community around it.'),
       info_card('Process', 'Open and collaborative', 'A transparent design process built on your input. We listen, communicate openly and turn what you have in mind into drawings you can build from.'),
       '\n'.join('          <li><span class="numbered-list__num" aria-hidden="true">%s</span><p><strong>%s</strong>%s</p></li>' % w for w in why),
       '\n'.join(team_card(t, 'h3') for t in TEAM[:3]))
    main += cta()
    page('about.html', 'About Elite Architecture | 18+ Years of Design in Guyana',
         'Meet Elite Architecture: a Georgetown architecture and construction consultancy led by Vickram Paul, with 18+ years of experience and a 4.9 Google rating.',
         main, active='about.html', ld=[business_ld(), crumbs_ld(crumbs)])


def build_services():
    crumbs = [('index.html', 'Home'), ('services.html', 'Services')]
    main = page_hero(crumbs, 'What we do',
                     'Seven services. One team. <em>Start to finish</em>.',
                     'From the first sketch to the final drawing set, everything your project needs is handled in-house — so nothing is lost between design, engineering and construction.')
    main += '''
  <section class="section section--after-hero section--sand" aria-labelledby="overview-title">
    <div class="container">
      <div class="section-head section-head--tight" data-reveal>
        <div>
          <p class="eyebrow">Overview</p>
          <h2 id="overview-title">Choose where you need us.</h2>
        </div>
        <p class="section-head__aside">Take one service or the full journey. Select a card to read more.</p>
      </div>
      <div class="grid-cards">
%s
        <a class="prompt-card on-dark" href="contact.html" data-reveal>
          <h3>Not sure which service you need?</h3>
          <span>Book a consultation →</span>
        </a>
      </div>
    </div>
  </section>

  <section class="section" aria-label="Services in detail">
    <div class="container">
''' % '\n'.join(service_card(s, i + 1) for i, s in enumerate(SERVICES))
    for i, s in enumerate(SERVICES):
        main += '''      <article class="feature%s" id="%s" aria-labelledby="%s-title">
        <div class="feature__media media media--4x3" data-reveal>%s</div>
        <div data-reveal>
          <p class="eyebrow">Service %02d</p>
          <h2 id="%s-title">%s</h2>
          <p class="lead">%s</p>
          <div class="feature__cols">
            <div>
              <h3>What you gain</h3>
              <ul class="dash-list">
%s
              </ul>
            </div>
            <div>
              <h3>How it works</h3>
              <ol class="steps">
%s
              </ol>
            </div>
          </div>
          <a class="btn btn--outline" href="contact.html">Discuss %s <span aria-hidden="true">→</span></a>
        </div>
      </article>
''' % (' feature--flip' if i % 2 else '', s['slug'], s['slug'], img(s['img'], s['alt'], (4, 3), SIZES_SPLIT),
       i + 1, s['slug'], s['title'], s['long'],
       '\n'.join('                <li>%s</li>' % b for b in s['benefits']),
       '\n'.join('                <li>%s</li>' % b for b in s['steps']),
       s['title'].lower().replace('3d', '3D'))
    main += '    </div>\n  </section>\n'
    main += '''
  <section class="section section--sand" aria-labelledby="included-title">
    <div class="container">
      <div class="section-head section-head--tight" data-reveal>
        <div>
          <p class="eyebrow">With every service</p>
          <h2 id="included-title">What you can count on.</h2>
        </div>
        <p class="section-head__aside">Whichever service you choose, the same standards come with it.</p>
      </div>
      <div class="grid-cards">
%s
      </div>
    </div>
  </section>
''' % '\n'.join(info_card('%02d' % (i + 1), t, d) for i, (t, d) in enumerate([
        ('Attention to detail', 'Every drawing is checked so that small mistakes do not become expensive ones on site.'),
        ('Expert team', 'Architects and a civil engineer working on your project together.'),
        ('Customer focused', 'Your needs, your routine and your budget lead the design.'),
        ('Timely delivery', 'Clear timelines, agreed at the start and kept.'),
        ('Transparent process', 'You always know what stage we are at and what comes next.'),
        ('Affordable excellence', 'Competitive pricing without cutting the quality of the work.'),
        ('Estimates on request', "Engineer's estimates are available to help you plan your budget."),
        ('Built to last', 'Sustainable practices and sound engineering behind every design.')]))
    main += cta(title='Have a project in mind? Start with a conversation.')
    ld = [business_ld(), crumbs_ld(crumbs)]
    page('services.html', 'Architecture Services in Guyana | Elite Architecture',
         'Building designs, 3D concepts, construction and as-built drawings, landscape design and civil engineering consultancy in Georgetown, Guyana.',
         main, active='services.html', ld=ld, og_image=u(SERVICES[0]['img'], 1200, 630, 80))


def build_projects():
    crumbs = [('index.html', 'Home'), ('projects.html', 'Projects')]
    main = page_hero(crumbs, 'Portfolio',
                     'Work that people live, learn and <em>do business</em> in.',
                     '%d residential, commercial and institutional designs from around Guyana. Filter by type, or open a project to see every view.' % len(PROJECTS))
    count = lambda c: sum(1 for p in PROJECTS if p['cat'] == c)
    main += '''
  <section class="section section--after-hero" aria-label="Projects">
    <div class="container">
      <div class="filter-bar" role="group" aria-label="Filter projects by type">
        <button class="filter-btn" type="button" data-filter="all" aria-pressed="true">All <span>%d</span></button>
        <button class="filter-btn" type="button" data-filter="residential" aria-pressed="false">Residential <span>%d</span></button>
        <button class="filter-btn" type="button" data-filter="commercial" aria-pressed="false">Commercial <span>%d</span></button>
        <button class="filter-btn" type="button" data-filter="institutional" aria-pressed="false">Institutional <span>%d</span></button>
      </div>
      <p class="visually-hidden" role="status" aria-live="polite" data-filter-status></p>
      <div class="grid-projects" data-filter-grid>
%s
      </div>
    </div>
  </section>
''' % (len(PROJECTS), count('Residential'), count('Commercial'), count('Institutional'),
       '\n'.join(project_card(p) for p in PROJECTS))
    main += cta(title='Your project could be next. Let\'s talk.')
    page('projects.html', 'Projects & Portfolio | Elite Architecture, Guyana',
         'Residential, commercial and institutional projects by Elite Architecture, including Tuschen Secondary School and Belco Shipping Office.',
         main, active='projects.html', ld=[crumbs_ld(crumbs)],
         og_image=SITE + 'assets/projects/%s/cover.jpg' % PROJECTS[0]['slug'])


def build_project(i):
    p = PROJECTS[i]
    nxt = PROJECTS[(i + 1) % len(PROJECTS)]
    prv = PROJECTS[(i - 1) % len(PROJECTS)]
    path = 'projects/%s.html' % p['slug']
    crumbs = [('index.html', 'Home'), ('projects.html', 'Projects'), (path, p['title'])]
    lead = LEADS[p['cat']] % e(p['place'])
    main = page_hero(crumbs, p['cat'] + ' project', e(p['title']), lead, root='../')
    gallery = '\n'.join(
        '        <a class="media media--16x9 gallery__item" href="../assets/projects/%s/%02d-1600.webp" data-lightbox aria-label="View image %d of %d larger">%s</a>'
        % (p['slug'], n, n, p['count'], pimg(p, n, '%s — view %d' % (p['title'], n), '(min-width: 900px) 46vw, 92vw', '../'))
        for n in range(2, p['count'] + 1))
    main += '''
  <section class="section section--after-hero" aria-label="Project overview">
    <div class="container stack">
      <a class="media media--16x9 gallery__item" href="../assets/projects/%s/01-1600.webp" data-lightbox aria-label="View image 1 of %d larger">%s</a>
      <dl class="meta-grid" data-reveal>
        <div><dt>Location</dt><dd>%s</dd></div>
        <div><dt>Type</dt><dd>%s</dd></div>
        <div><dt>Scope</dt><dd>Design &amp; 3D visualisation</dd></div>
        <div><dt>Designed by</dt><dd>Elite Architecture</dd></div>
      </dl>
    </div>
  </section>

  <section class="section section--sand" aria-labelledby="gallery-title">
    <div class="container">
      <div class="section-head section-head--tight" data-reveal>
        <div>
          <p class="eyebrow">Gallery</p>
          <h2 id="gallery-title">Every view of the design</h2>
        </div>
        <p class="section-head__aside">%d images. Select any image to see it larger.</p>
      </div>
      <div class="gallery">
%s
      </div>
    </div>
  </section>

  <section class="section" aria-label="More projects">
    <div class="container">
      <div class="project-next" data-reveal>
        <div>
          <p class="eyebrow eyebrow--gap">Next project</p>
          <a class="project-next__title" href="%s.html">%s</a>
        </div>
        <div class="btn-row">
          <a class="link-arrow" href="%s.html">← Previous</a>
          <a class="link-arrow" href="../projects.html">All projects →</a>
        </div>
      </div>
    </div>
  </section>
''' % (p['slug'], p['count'], pimg(p, 1, p['title'] + ' — main view', SIZES_FULL, '../', lazy=False),
       e(p['place']), p['cat'], p['count'], gallery, nxt['slug'], e(nxt['title']), prv['slug'])
    main += cta('../', title='Planning something similar? Let\'s talk.')
    page(path, '%s | Elite Architecture' % p['title'],
         '%s: %s design in %s by Elite Architecture, Georgetown, Guyana. View the 3D images.' % (p['title'], p['cat'].lower(), p['place']),
         main, active='projects.html', ld=[crumbs_ld(crumbs)],
         og_image=SITE + 'assets/projects/%s/cover.jpg' % p['slug'])


def build_team():
    crumbs = [('index.html', 'Home'), ('team.html', 'Our Team')]
    main = page_hero(crumbs, 'Our team',
                     'Design is not just seen. It is <em>experienced</em>.',
                     'Meet the architects and engineer behind Elite Architecture. Whoever you speak to, you are speaking to someone who knows your project.')
    main += '''
  <section class="section section--after-hero" aria-label="Team members">
    <div class="container">
      <div class="grid-projects">
%s
      </div>
    </div>
  </section>

  <section class="section section--sand" aria-labelledby="work-title">
    <div class="container">
      <div class="section-head section-head--tight" data-reveal>
        <div>
          <p class="eyebrow">How we work</p>
          <h2 id="work-title">What you can expect from us.</h2>
        </div>
        <p class="section-head__aside">The same standards apply to every client and every project.</p>
      </div>
      <div class="grid-cards">
%s
%s
%s
%s
      </div>
    </div>
  </section>
''' % ('\n'.join(team_card(t) for t in TEAM),
       info_card('01', 'We listen first', 'Every project begins with your ideas, your routine and your budget — not ours.'),
       info_card('02', 'We explain clearly', 'Plans, costs and next steps are set out in plain language at every stage.'),
       info_card('03', 'We stay in touch', 'You get regular updates and quick answers, from the first call to completion.'),
       info_card('04', 'We see it through', 'Our involvement continues from concept through construction.'))
    main += '''
  <section class="section" aria-labelledby="join-title">
    <div class="container">
      <div class="project-next" data-reveal>
        <div>
          <p class="eyebrow eyebrow--gap">Careers</p>
          <h2 id="join-title">Want to join the team?</h2>
        </div>
        <a class="link-arrow" href="careers.html">See open roles →</a>
      </div>
    </div>
  </section>
'''
    main += cta(eyebrow='Work with us', title='Meet the team in person. Book a consultation.')
    page('team.html', 'Our Team | Elite Architecture, Georgetown',
         'Meet the Elite Architecture team: Vickram Paul, CEO and Principal Architect, architect Raza Jan and civil engineer Johanan Dolphin.',
         main, active='team.html', ld=[crumbs_ld(crumbs)])


def build_faq():
    crumbs = [('index.html', 'Home'), ('faq.html', 'FAQ')]
    main = page_hero(crumbs, 'Questions &amp; answers',
                     'Everything you wanted to ask <em>before</em> you build.',
                     'Straight answers to the questions we hear most. If yours is not here, call or message us — we are happy to help.')
    items = []
    for i, (q, a) in enumerate(FAQS):
        items.append('''          <div class="accordion__item">
            <h2 class="h3"><button class="accordion__trigger" type="button" aria-expanded="%s" aria-controls="faq-panel-%d" id="faq-trigger-%d">%s<span class="accordion__icon" aria-hidden="true"></span></button></h2>
            <div class="accordion__panel" id="faq-panel-%d" role="region" aria-labelledby="faq-trigger-%d"%s>
              <p>%s</p>
            </div>
          </div>''' % ('true' if i == 0 else 'false', i, i, e(q), i, i, '' if i == 0 else ' hidden', e(a)))
    main += '''
  <section class="section section--after-hero" aria-label="Frequently asked questions">
    <div class="container faq-layout">
      <div class="accordion" data-accordion>
%s
      </div>
      <aside class="faq-aside" aria-labelledby="faq-aside-title" data-reveal>
        <p class="eyebrow">Still have a question?</p>
        <h2 id="faq-aside-title" class="h3">Talk to the team directly.</h2>
        <p class="body-sm">Call or WhatsApp %s and we will answer it for you.</p>
        <a class="btn btn--primary" href="contact.html">Contact us <span aria-hidden="true">→</span></a>
        <a class="link-arrow" href="%s" target="_blank" rel="noopener">Message on WhatsApp →<span class="visually-hidden"> (opens in a new tab)</span></a>
      </aside>
    </div>
  </section>
''' % ('\n'.join(items), PHONE, WA)
    main += cta()
    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQS]}
    page('faq.html', 'FAQ | Working With an Architect in Guyana | Elite Architecture',
         'Answers to common questions about hiring an architect in Guyana: process, timelines, costs, approvals, 3D designs and as-built drawings.',
         main, active='faq.html', ld=[faq_ld, crumbs_ld(crumbs)])


def build_contact():
    crumbs = [('index.html', 'Home'), ('contact.html', 'Contact')]
    main = page_hero(crumbs, 'Contact',
                     "Let's talk about your <em>project</em>.",
                     'Book a first consultation — no drawings required. Send us a few details and we will get back to you, or call and speak to the team now.')
    main += '''
  <section class="section section--after-hero" aria-label="Contact form and details">
    <div class="container grid-split grid-split--top">
      <div>
        <p class="eyebrow eyebrow--gap">Send a message</p>
        <h2 id="form-title" class="form-heading">Tell us what you want to build.</h2>
        <form class="form" id="contact-form" novalidate aria-labelledby="form-title" data-whatsapp="5926189518">
          <div class="field">
            <label for="f-name">Full name</label>
            <input id="f-name" name="name" type="text" autocomplete="name" required aria-describedby="f-name-err">
            <p class="field__error" id="f-name-err" aria-live="polite"></p>
          </div>
          <div class="field">
            <label for="f-email">Email</label>
            <input id="f-email" name="email" type="email" autocomplete="email" inputmode="email" required aria-describedby="f-email-err">
            <p class="field__error" id="f-email-err" aria-live="polite"></p>
          </div>
          <div class="field">
            <label for="f-phone">Phone <span>(optional)</span></label>
            <input id="f-phone" name="phone" type="tel" autocomplete="tel" inputmode="tel" aria-describedby="f-phone-err">
            <p class="field__error" id="f-phone-err" aria-live="polite"></p>
          </div>
          <div class="field">
            <label for="f-type">Project type</label>
            <select id="f-type" name="type" required aria-describedby="f-type-err">
              <option value="">Select one</option>
              <option>Residential</option>
              <option>Commercial</option>
              <option>Institutional</option>
              <option>Landscape</option>
              <option>Engineering consultancy</option>
              <option>Not sure yet</option>
            </select>
            <p class="field__error" id="f-type-err" aria-live="polite"></p>
          </div>
          <div class="field field--full">
            <label for="f-message">Message</label>
            <textarea id="f-message" name="message" rows="6" required aria-describedby="f-message-err"></textarea>
            <p class="field__error" id="f-message-err" aria-live="polite"></p>
          </div>
          <div class="field field--full form__actions">
            <button class="btn btn--primary" type="submit">Send message <span aria-hidden="true">→</span></button>
            <p class="form__note">Your message opens in WhatsApp, ready to send to our team. Prefer email? Write to <a href="mailto:%s">%s</a>.</p>
          </div>
        </form>
        <div class="form-success" id="form-success" role="status" tabindex="-1" hidden>
          <p class="eyebrow">Thank you</p>
          <h3>Your message is ready to send.</h3>
          <p class="body-sm">We have opened WhatsApp with your details filled in — press send there and our team will reply as soon as possible. If WhatsApp did not open, use the button below or call %s.</p>
          <div class="btn-row">
            <a class="btn btn--primary" id="form-success-link" href="%s" target="_blank" rel="noopener">Open WhatsApp <span aria-hidden="true">→</span></a>
            <button class="btn btn--outline" type="button" id="form-reset">Write another message</button>
          </div>
        </div>
      </div>
      <div data-reveal>
        <p class="eyebrow eyebrow--gap">Reach us directly</p>
        <h2 class="form-heading">Studio details</h2>
        <dl class="info-list">
          <div><dt>Phone</dt><dd><a href="%s">%s</a></dd></div>
          <div><dt>WhatsApp</dt><dd><a href="%s" target="_blank" rel="noopener">Message us on WhatsApp<span class="visually-hidden"> (opens in a new tab)</span></a></dd></div>
          <div><dt>Email</dt><dd><a href="mailto:%s">%s</a></dd></div>
          <div><dt>Address</dt><dd><address class="plain-address">%s<br>%s</address></dd></div>
          <div><dt>Hours</dt><dd><div class="hours"><span>Monday – Friday</span><span>9:00 am – 10:00 pm</span><span>Saturday</span><span>11:00 am – 8:00 pm</span><span>Sunday</span><span>Closed</span></div></dd></div>
        </dl>
      </div>
    </div>
  </section>

  <section class="section section--sand" aria-labelledby="map-title">
    <div class="container">
      <div class="section-head section-head--tight" data-reveal>
        <div>
          <p class="eyebrow">Find us</p>
          <h2 id="map-title">Based in Subryanville, working across Guyana.</h2>
        </div>
        <a class="link-arrow" href="%s" target="_blank" rel="noopener">Open in Google Maps →<span class="visually-hidden"> (opens in a new tab)</span></a>
      </div>
      <div class="map-frame" data-reveal>
        <iframe src="%s" title="Map showing Elite Architecture at 5th and Earl's Avenue, Subryanville, Georgetown" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
        <div class="map-placeholder__card map-frame__card">
          <span class="map-placeholder__pin" aria-hidden="true"></span>
          <h3>Elite Architecture</h3>
          <p class="body-sm">%s<br>%s</p>
        </div>
      </div>
    </div>
  </section>
''' % (EMAIL, EMAIL, PHONE, WA, TEL, PHONE, WA, EMAIL, EMAIL, STREET, AREA, MAPS, MAP_EMBED, STREET, AREA)
    page('contact.html', 'Contact Elite Architecture | Book a Consultation in Georgetown',
         "Contact Elite Architecture at 5th & Earl's Avenue, Subryanville, Georgetown. Call or WhatsApp +592-618-9518 or email info@elitearchitecturegy.com.",
         main, active='contact.html', ld=[business_ld(), crumbs_ld(crumbs)])


def build_careers():
    crumbs = [('index.html', 'Home'), ('careers.html', 'Careers')]
    roles = [('Head Contractor', 'Full time / Part time', 'Lead and oversee large-scale projects from start to finish. A role for a strategic, detail-minded builder who can manage people and programme.'),
             ('Civil Engineer', 'Full time', 'Design and check the structure behind our buildings. We are looking for an engineer who brings precision and fresh thinking to every drawing.'),
             ('Field Inspector', 'Part time', 'Check quality and compliance on site across a range of projects. Suited to someone who cares about construction standards and notices the details.'),
             ('Assistant', 'Full time / Part time', 'Support day-to-day operations and keep our projects well coordinated. An important role at the centre of the team.')]
    cards = '\n'.join('''        <article class="service-card role-card" data-reveal>
          <div class="service-card__top"><span class="tag">%s</span><span class="service-card__num">%02d</span></div>
          <h2 class="h3">%s</h2>
          <p>%s</p>
          <a class="link-arrow" href="mailto:%s?subject=%s">Apply by email →</a>
        </article>''' % (t, i + 1, n, d, EMAIL, ('Application: ' + n).replace(' ', '%20')) for i, (n, t, d) in enumerate(roles))
    main = page_hero(crumbs, 'Careers',
                     "Let's build the future of design <em>together</em>.",
                     'We are a growing studio, and we are always glad to hear from people who want to do careful, ambitious work. If that is you, take a look at the roles below.')
    main += '''
  <section class="section section--after-hero" aria-labelledby="roles-title">
    <div class="container">
      <div class="section-head section-head--tight" data-reveal>
        <div>
          <p class="eyebrow">Open roles</p>
          <h2 id="roles-title" class="h2">Where you could fit in.</h2>
        </div>
        <p class="section-head__aside">To apply, email us your CV and a short note about the role you are interested in.</p>
      </div>
      <div class="grid-cards">
%s
      </div>
    </div>
  </section>
''' % cards
    main = main.replace('<h2 id="roles-title" class="h2">Where you could fit in.</h2>', '<p id="roles-title" class="h2">Where you could fit in.</p>')
    main += cta(eyebrow='Not hiring for your role?', title='Introduce yourself anyway. We keep every CV on file.',
                text='Send your details to %s and tell us what you do best.' % EMAIL)
    page('careers.html', 'Careers | Join Elite Architecture in Georgetown, Guyana',
         'Open roles at Elite Architecture in Georgetown, Guyana: head contractor, civil engineer, field inspector and assistant. Apply by email.',
         main, active='careers.html', ld=[crumbs_ld(crumbs)])


def build_404():
    main = '''  <section class="error-page" aria-labelledby="page-title">
    <div class="container">
      <p class="error-page__code" aria-hidden="true">404</p>
      <h1 id="page-title">This page is off the plan.</h1>
      <p class="lead">The page you are looking for has moved or never existed. Head back home, or take a look at our recent work.</p>
      <div class="btn-row">
        <a class="btn btn--primary" href="index.html">Back to home <span aria-hidden="true">→</span></a>
        <a class="btn btn--outline" href="projects.html">See our projects</a>
      </div>
    </div>
  </section>
'''
    page('404.html', 'Page Not Found | Elite Architecture',
         'The page you are looking for could not be found. Return to the Elite Architecture home page or browse our projects.',
         main, base=True, noindex=True)


def build_seo_files():
    urls = ['', 'about.html', 'services.html', 'projects.html', 'team.html', 'faq.html', 'contact.html', 'careers.html'] + \
           ['projects/%s.html' % p['slug'] for p in PROJECTS]
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    xml += ''.join('  <url><loc>%s%s</loc></url>\n' % (SITE, x) for x in urls) + '</urlset>\n'
    io.open(os.path.join(OUT, 'sitemap.xml'), 'w', encoding='utf-8', newline='\n').write(xml)
    io.open(os.path.join(OUT, 'robots.txt'), 'w', encoding='utf-8', newline='\n').write(
        'User-agent: *\nAllow: /\n\nSitemap: %ssitemap.xml\n' % SITE)


if __name__ == '__main__':
    build_home()
    build_about()
    build_services()
    build_projects()
    for i in range(len(PROJECTS)):
        build_project(i)
    build_team()
    build_faq()
    build_contact()
    build_careers()
    build_404()
    build_seo_files()

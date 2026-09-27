# Elite Architecture — Design System

Source of truth: `design/elite-architecture-demos/demo-4/` ("Luxury Minimal, Client-Friendly").
Every value below was read from that file's markup and is implemented as CSS custom properties in
`site/css/styles.css`. Pages are built only from these tokens and components — no one-off styles.

**Character:** ivory ground, light Cormorant serif at large sizes, small wide-tracked Jost labels,
bronze accent, hairline rules, square corners, no shadows.

---

## 1. Color

| Token | Value | Use |
|---|---|---|
| `--ivory` | `#F5F2EC` | Page background, cards on sand, light button |
| `--sand` | `#ECE7DE` | Alternate section background, quote card |
| `--stone` | `#E6E1D8` | Image placeholder ground (shows while photos load) |
| `--ink` | `#1C1B19` | Headings, dark sections, primary button, section rule |
| `--text-body` | `#5C574F` | Paragraphs |
| `--text-muted` | `#6B665E` | Captions, locations, footer text |
| `--bronze` | `#A8764A` | Accent: italic display words, icons, stars, rules, hover borders |
| `--bronze-deep` | `#8A5D36` | Accent for **small text** and hover fills on light surfaces |
| `--bronze-light` | `#D6B08A` | Accent on dark surfaces |
| `--on-dark` | `#F5F2EC` | Text on ink |
| `--on-dark-strong` / `-body` / `-muted` | ivory at 92% / 78% / 70% | Text hierarchy on ink |

Lines: `--line` (ink 14%), `--line-soft` (8%), `--line-mid` (20%), `--line-strong` (30%),
`--line-on-dark` (ivory 16%). Section headers use a solid 1px `--ink` rule.

**Hover states:** links → `--bronze-deep`; primary button ink → `--bronze-deep`; outline button
border + text → `--bronze-deep`; light button ivory → `--bronze-light`; links on dark → `--bronze-light`.

**Contrast note (the one color deviation from the design):** the design's bronze `#A8764A` on ivory
is 3.5:1 — fine for large display text, below WCAG AA (4.5:1) for 12–13px labels. Small bronze text
and hover fills therefore use `--bronze-deep` (5.1:1 on ivory, 4.6:1 on sand). Large italic accents,
icons, stars and rules keep the original `#A8764A`.

## 2. Typography

| Family | Token | Weights | Use |
|---|---|---|---|
| Cormorant Garamond | `--font-display` | 300, 400, 500, italic 300/400 | Headings, stats, quotes |
| Jost | `--font-body` | 300, 400, 500 | Body, labels, buttons, nav |

| Style | Size | Weight | Line height | Tracking |
|---|---|---|---|---|
| h1 | `clamp(44px, 5.6vw, 84px)` | 300 | 1 | -0.01em |
| h2 | `clamp(36px, 4.2vw, 60px)` | 300 | 1.02 | -0.01em |
| h2 (dark about block) | `clamp(36px, 4vw, 58px)` | 300 | 1.05 | 0 |
| h2 (CTA band) | `clamp(40px, 5.2vw, 80px)` | 300 | 1 | 0 |
| h3 | 28px (30px / 300 in prompt card) | 400 | 1.1 | 0 |
| h4 | 22px | 400 | 1.2 | 0 |
| h5 | 16px Jost | 500 | 1.4 | 0 |
| h6 | 12px Jost uppercase | 400 | 1.4 | 0.18em |
| Stat number | `clamp(48px, 5vw, 80px)` | 300 | 1 | 0 |
| Stat number XL | `clamp(64px, 7vw, 110px)` | 300 | 1 | 0 |
| Quote | `clamp(24px, 2.3vw, 34px)` italic | 300 | 1.3 | 0 |
| Lead | `clamp(16px, 1.25vw, 18px)` | 400 | 1.7 | 0 |
| Body | 16px (1.75 on dark) | 400 | 1.7 | 0 |
| Body small (cards) | 15px | 400 | 1.65 | 0 |
| Small / caption | 14px / 13px | 400 | normal | 0–0.06em |
| Eyebrow | 12px uppercase | 400 | normal | 0.22em |
| Label / nav | 12px uppercase | 400 | normal | 0.18em |
| Button | 13px (12px small) uppercase | 400 | normal | 0.16em |
| Tag | 11px uppercase | 400 | normal | 0.16em |

Accent words inside h1/h2 use `<em>`: italic, `--bronze`. h4–h6 do not appear in the design; they
extend the scale downward for inner pages.

## 3. Spacing & layout

| Token | Value | Use |
|---|---|---|
| `--container` | 1380px | Content max-width |
| `--gutter` | `clamp(20px, 4vw, 56px)` | Horizontal page padding |
| `--section-y` | `clamp(64px, 8vw, 130px)` | Standard section padding |
| `--section-y-dark` | `clamp(72px, 9vw, 140px)` | Dark section padding |
| `--section-y-cta` | `clamp(88px, 11vw, 170px)` | CTA band padding |
| `--head-gap` | `clamp(32px, 4vw, 56px)` | Section header → content |
| `--gap-tight` | 12px | Card grids, image collage, button rows |
| `--gap-cards` | `clamp(24px, 3vw, 40px)` | Project grid |
| `--gap-split` | `clamp(40px, 6vw, 96px)` | Two-column text/media splits |
| `--card-pad` | 32px 28px | Service cards |
| `--card-pad-lg` | `clamp(28px, 3.5vw, 48px)` | Quote / review cards |

Small steps in use: 6, 10, 12, 14, 16, 18, 20, 24, 28, 32, 36, 40, 48px.

**Grids** are intrinsic (`repeat(auto-fit, minmax(min(100%, N), 1fr))`), so columns collapse by
available width rather than fixed breakpoints:

| Class | Min column | Gap | Columns at 1440 / 768 / 390 |
|---|---|---|---|
| `.grid-cards` | 280px | 12px | 4 / 2 / 1 |
| `.grid-projects` | 300px | 24–40px | 3 / 2 / 1 |
| `.grid-split` | 380px | 40–96px | 2 / 1 / 1 |
| `.grid-duo` | 320px | 12px | 2 / 2 / 1 |
| `.hero__grid` | 360px | 32–80px | 2 / 2 / 1 |

Hard breakpoints: **1023px** desktop nav ↔ hamburger (the design used 900px with four links; six
links need the extra room), 1279px hides the header phone number, 1100px re-flows the footer.

### Height-aware scaling
Display type and section spacing use `min(vw, vh)` inside their clamps (the vh value is the vw value
x 1.6), so on 16:10 and taller windows everything is exactly the design size, and on shorter windows
(a 16:9 laptop with browser toolbars) type and spacing shrink in proportion to the screen height.
From 900px wide, the home hero also caps its image collage to the height left under the header so the
whole hero fits in one screen.

### Mobile hero (up to 827px wide)
The home hero is composed as one screen: rating badge, a three-line headline (`clamp(28px, min(9.2vw, 6vh), 56px)`),
lead, full-width buttons, then the collage as a three-tile strip (photo, photo, 18+ tile) that stretches to fill the
height left under the header. The three hero points are hidden at this size. On short phones (under 660px tall) the
secondary button is hidden so the primary action and the image strip both stay on screen.

## 4. Components

### Buttons — `.btn`
Square corners, uppercase, 0.16em tracking, 1px border, 0.3s ease transitions, min-height 44px.

| Variant | Rest | Hover | Padding |
|---|---|---|---|
| `.btn--primary` | ink fill, ivory text | bronze-deep fill | 18px 30px |
| `.btn--outline` | transparent, 30% ink border | bronze-deep border + text | 18px 30px |
| `.btn--outline-solid` | transparent, ink border | ink fill, ivory text | 16px 24px |
| `.btn--light` (on dark) | ivory fill, ink text | bronze-light fill | 18px 30px |
| `.btn--sm` (header) | — | — | 13px 22px, 12px text |

Focus: 2px `--bronze-deep` outline, 3px offset (`--bronze-light` on dark). Active: 1px press.
`.link-arrow`: uppercase 12px text link with a 1px bronze underline and trailing →.

### Section header — `.section-head`
Eyebrow (bronze, 0.22em) → h2, optional aside paragraph (max 400px) or link on the right, aligned to
the baseline; 28px below sits a 1px ink rule. `.section-head--center` is the centered, rule-less variant.

### Cards
- **Service card** `.service-card` — ivory on sand, 8% ink border, 28px line icon (1.2 stroke, bronze)
  top-left, two-digit number top-right, h3, 15px description. Hover: bronze border, lifts 3px.
- **Prompt card** `.prompt-card` — ink fill closing a card grid; 30px light h3 + uppercase action.
  Hover: bronze-deep fill.
- **Project card** `.project-card` — 4:3 image, hairline rule, h3 + location left, bordered `.tag`
  right. Hover: image scales to 1.03 over 1.1s, title turns bronze-deep.
- **Quote card** `.quote-card` — sand fill, stars, italic serif quote, rule, 48px round avatar + name.
- **Reviews card** `.reviews-card` — hairline border, "G" monogram tile, XL score, outline button.
- **Stat** `.stat` (bordered, on dark) and `.stat-tile` (ink fill, used in image collages).
- **Rating badge** `.rating-badge` — inline hairline box: stars + "4.9 on Google · 42 reviews".
- **Numbered list** `.numbered-list` — roman numerals in bronze-light, hairline rules (dark sections).

### Header — `.site-header`
Sticky, 90% ivory with 14px backdrop blur, 1px bottom hairline, 16px vertical padding (≈79px tall).
Logo left (34–46px high), uppercase nav centered (12px, 0.18em, 20–32px gap) with six links —
Services, Projects, About, Team, FAQ, Contact — each its own page; phone + small primary button right. Hover: bronze-deep. **Active page:** bronze-deep text + 1px bronze underline
(`aria-current="page"`).

### Mobile menu — `.mobile-menu` (≤ 1023px)
Two-line hamburger (28px / 20px, 1px strokes). Opens a full-screen ivory overlay: logo + "Close"
text button, large serif links (`clamp(36px, 9vw, 56px)`, weight 300) separated by hairlines,
full-width primary button pinned to the bottom, phone line beneath.

### CTA band — `.cta-band`
Ink ground, full-bleed photo at 35% opacity, copy left (max 720px), light button + serif phone link right.

### Footer — `.site-footer`
Ivory; logo (52px) + short description, uppercase link lists, contact column; hairline rule;
12px legal row.

### Inner-page components (extensions, built from the same tokens)
| Component | Class | Notes |
|---|---|---|
| Page hero | `.page-hero` | Breadcrumb, eyebrow, h1 at `clamp(40px, 5vw, 72px)`, lead, ink rule beneath |
| Breadcrumb | `.breadcrumb` | 12px uppercase labels separated by "/" |
| Media frame | `.media--4x3 / --3x4 / --16x9` | Fixed-ratio photo frame on `--stone` |
| Service feature | `.feature` | Sticky 4:3 photo + eyebrow, h2, lead, "What you gain" dash list, "How it works" numbered steps, outline button; alternates sides |
| Dash list / steps | `.dash-list`, `.steps` | Bronze rule or two-digit number markers (from the hero points and card numbers) |
| Filter bar | `.filter-btn` | Tag-styled toggle buttons; active = ink fill |
| Project meta | `.meta-grid` | Label + 22px serif value over hairlines |
| Next project | `.project-next` | Ink rule, h2-scale serif link |
| Team card | `.team-card` | 1:1 portrait (the client's photos are square), h3, bronze role label, 15px bio |
| Small quote card | `.quote-card--ivory` | Quote card on sand sections, 22–26px italic quote, initials avatar |
| Role card | `.role-card` | Service card with a tag (hours), title, description and email link |
| Live map | `.map-frame` | Lazy Google map, slightly desaturated, with the ivory address card overlaid |
| Accordion | `.accordion` | Hairline rows, serif question, 1px plus/minus icon |
| Info list / hours | `.info-list` | Label column + value, hairline rows |
| Map placeholder | `.map-placeholder` | Stone ground with hairline grid, ivory card with pin and Maps link |
| Initials avatar | `.avatar` | 48px round ink disc with serif initials |
| 404 | `.error-page` | Oversized bronze numerals, h1 at h2 scale |

### Footer (redesigned) — `.site-footer`
Drawn like an architectural sheet, using only system tokens: a line-drawn street elevation (1px ink strokes at 50%,
bronze dimension ticks) sits on the footer's top edge; below it a bordered sheet of four cells on a faint 28px drawing
grid (brand, 01 Explore, 02 Studio, 03 Contact); then a title block (Site coordinates, Hours, Scale bar, Drawn by +
north arrow); then the legal row with the Creativals.com credit and Back to top. Under 1024px the sheet becomes
brand / two link cells side by side / contact, and the title block becomes 2 x 2.

### Floating contact
- **Desktop (828px and up):** `.contact-fab`, a bronze-deep button fixed bottom-right that opens a small ivory menu:
  WhatsApp, Call, Email, Book a consultation. Closes on Escape, outside click or selection.
- **Mobile:** `.contact-bar`, a fixed bottom bar (Call / WhatsApp / Book) that slides in after 160px of scroll so the
  hero stays clean, and hides while the menu overlay is open.

### Form fields (extension — not in the home design; used from the Contact page onward)
Built from the same parts: uppercase 12px label (0.18em) above the field; field is transparent with
a 1px 30%-ink border, square corners, 16px Jost text, 16px 18px padding, min-height 52px.
Hover: ink border. Focus: bronze-deep border + focus ring. Error: `#9B2C1F` border and 13px message.
Success state: sand panel with serif heading.

## 5. Imagery

| Context | Aspect ratio | Treatment |
|---|---|---|
| Hero collage — tall | 3:4 | `object-fit: cover`, no radius |
| Hero collage — square | 1:1 | same |
| Project / service card | 4:3 | hover scale 1.03, 1.1s |
| CTA background | full-bleed | 35% opacity over ink + scrim |
| Avatar | 1:1, 48px | fully round — the only radius in the system |

Corners are square everywhere else. No shadows, no borders on photos. Photos sit on `--stone` while
loading. Style: warm, natural-light architecture and interiors. All current photos are Unsplash
placeholders served with `srcset`; ratios are fixed in CSS so real photos drop in without layout changes.

## 6. Motion

| Pattern | Spec |
|---|---|
| Easing | `cubic-bezier(.2, .7, .2, 1)` |
| Hero entrance | fade + 24px rise, 1s |
| Scroll reveal (`data-reveal`) | fade + 28px rise, 0.9s, fires once at 10% visibility; only applied to elements that start below the fold |
| Hover transitions | 0.3s ease (color, border, background) |
| Menu overlay | 0.3s fade |

`prefers-reduced-motion: reduce` disables reveals, the hero entrance, hover transforms and smooth scrolling.

## 7. Where the build departs from or extends the design

| Item | Change | Why |
|---|---|---|
| Small bronze text, hover fills | `#A8764A` → `#8A5D36` | WCAG AA contrast |
| CTA band | Added a subtle dark gradient scrim over the photo | Guarantees AA for text over any photo |
| Tap targets | Nav, footer links and the CTA phone link get 44px hit areas | Requirement; visual position unchanged |
| Primary button | Gains a 1px ink border | Makes it exactly the same height as the outline button beside it |
| Footer | Second link column (Our Team, FAQ, Contact) + WhatsApp link; 2-column layout under 1100px | Site has more pages than the one-page demo |
| Header nav | Six page links instead of four in-page anchors; "Reviews" removed from the nav (the section stays on Home) | Every menu item opens its own page |
| Mobile menu | Six links, slightly tighter row padding; focus trap, Esc to close | Extra pages; keyboard accessibility |
| Reviewer avatar | Stock portrait replaced by an initials disc | A stock face should not represent a real named reviewer |
| Project tags | Education / Hospitality → Institutional / Commercial | Match the portfolio filter categories |
| Service cards | Now links to their service sections | Multi-page site |
| Header / CTA buttons | Point to `contact.html` instead of `#contact` / `tel:` | Multi-page site; the phone link remains beside it |
| Active nav state, skip link, focus rings | Added | Not specified in the design; required |

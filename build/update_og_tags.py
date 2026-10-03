import glob
import re

og_banner_url = "https://rahilcodes.github.io/elite/assets/og-banner.jpg"

files = glob.glob("site/**/*.html", recursive=True) + glob.glob("site/*.html")
files = sorted(list(set(files)))

updated = 0
for filepath in files:
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Update or insert og:image
    if '<meta property="og:image"' in content:
        content = re.sub(
            r'<meta property="og:image" content="[^"]*">',
            f'<meta property="og:image" content="{og_banner_url}">\n<meta property="og:image:secure_url" content="{og_banner_url}">\n<meta property="og:image:type" content="image/jpeg">\n<meta property="og:image:width" content="1200">\n<meta property="og:image:height" content="630">',
            content
        )
    else:
        og_tags = f'<meta property="og:image" content="{og_banner_url}">\n<meta property="og:image:secure_url" content="{og_banner_url}">\n<meta property="og:image:type" content="image/jpeg">\n<meta property="og:image:width" content="1200">\n<meta property="og:image:height" content="630">\n'
        content = content.replace("</head>", og_tags + "</head>")

    # Update or insert twitter:image
    if '<meta name="twitter:image"' in content:
        content = re.sub(
            r'<meta name="twitter:image" content="[^"]*">',
            f'<meta name="twitter:image" content="{og_banner_url}">',
            content
        )
    elif '<meta name="twitter:card"' in content:
        content = content.replace(
            '<meta name="twitter:card" content="summary_large_image">',
            f'<meta name="twitter:card" content="summary_large_image">\n<meta name="twitter:image" content="{og_banner_url}">'
        )
    else:
        tw_tags = f'<meta name="twitter:card" content="summary_large_image">\n<meta name="twitter:image" content="{og_banner_url}">\n'
        content = content.replace("</head>", tw_tags + "</head>")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    updated += 1

print(f"Successfully updated OG & Twitter banner meta tags in {updated} HTML files.")

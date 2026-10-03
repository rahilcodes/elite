import glob
import re

og_banner_url = "https://rahilcodes.github.io/elite/assets/og-banner.jpg"

files = glob.glob("site/**/*.html", recursive=True) + glob.glob("site/*.html") + ["index.html"]
files = sorted(list(set(files)))

for filepath in files:
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Clean up any existing og:image tags
    content = re.sub(r'<meta property="og:image[^"]*" content="[^"]*">\n?', '', content)
    content = re.sub(r'<meta name="twitter:image" content="[^"]*">\n?', '', content)
    content = re.sub(r'<meta name="twitter:card" content="[^"]*">\n?', '', content)

    og_tags = f'''<meta property="og:image" content="{og_banner_url}">
<meta property="og:image:secure_url" content="{og_banner_url}">
<meta property="og:image:type" content="image/jpeg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{og_banner_url}">
'''

    content = content.replace("</head>", og_tags + "</head>")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

print(f"Cleaned and updated OG & Twitter banner meta tags in {len(files)} files.")

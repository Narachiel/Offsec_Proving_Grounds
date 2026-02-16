from pathlib import Path
import re

# Lightweight spelling/grammar pass without external packages.
# Rules applied:
# - Fix common concatenation artifacts created earlier (e.g., 'can geta' -> 'can get a')
# - Replace repeated letters from OCR-like errors (e.g., 'lccal' -> 'local') using a small map
# - Normalize punctuation spacing and remove double spaces
# - Do not touch fenced code blocks or inline code or URLs

ROOT = Path.cwd()
MDs = list(ROOT.rglob('*.md'))

concat_fixes = {
    r'cangeta': 'can get a',
    r'uploadreverseshell': 'upload reverse shell',
    r'uploadreverseshellafter': 'upload reverse shell after',
    r'uploadreverseshellaftercheck': 'upload reverse shell after check',
    r'uploadreverseshellafterCheck': 'upload reverse shell after check',
    r'getget': 'get',
    r'getgeta': 'get a',
    r'geta': 'get a',
    r'gett': 'get',
}

ocr_fixes = {
    'lccal': 'local',
    'llocal': 'local',
    'obtaian': 'obtain',
}

url_re = re.compile(r'https?://[^\s`\)]+')
inline_code_re = re.compile(r'`[^`]*`')
code_fence_re = re.compile(r'(```[\s\S]*?```)', re.MULTILINE)

updated = []
for md in MDs:
    try:
        text = md.read_text(encoding='utf-8')
    except Exception:
        continue
    parts = re.split(code_fence_re, text)
    changed = False
    for i in range(0, len(parts), 2):
        part = parts[i]
        # protect inline code and URLs
        codes = inline_code_re.findall(part)
        urls = url_re.findall(part)
        placeholders = []
        for idx, code in enumerate(codes):
            ph = f'__CODE_{idx}__'
            placeholders.append((ph, code))
            part = part.replace(code, ph)
        for idx, url in enumerate(urls, start=len(placeholders)):
            ph = f'__URL_{idx}__'
            placeholders.append((ph, url))
            part = part.replace(url, ph)
        # apply concat fixes
        for pat, rep in concat_fixes.items():
            new = re.sub(pat, rep, part, flags=re.IGNORECASE)
            if new != part:
                part = new
                changed = True
        # apply ocr fixes
        for pat, rep in ocr_fixes.items():
            if pat in part:
                part = part.replace(pat, rep)
                changed = True
        # punctuation spacing
        part = re.sub(r'\s+,', ',', part)
        part = re.sub(r'\s+\.', '.', part)
        part = re.sub(r'\s+:', ':', part)
        part = re.sub(r'\s+;', ';', part)
        part = re.sub(r'\s{2,}', ' ', part)
        # restore placeholders
        for ph, orig in placeholders:
            part = part.replace(ph, orig)
        parts[i] = part
    new_text = ''.join(parts)
    if new_text != text:
        md.write_text(new_text, encoding='utf-8')
        updated.append(str(md))

print('Spell/grammar pass updated files:')
for p in updated:
    print(p)
print('Done')

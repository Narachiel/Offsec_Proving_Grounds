import re
from pathlib import Path

md_dir = Path.cwd() / 'PG_Practice'
chinese_re = re.compile(r'[\u4e00-\u9fff]')

# Reuse mappings from previous script
replacements = [
    (r'等反彈', 'wait for reverse shell'),
    (r'改成txt上傳', 'Change to upload as txt'),
    (r'可以上傳', 'can upload'),
    (r'可以登入', 'can log in'),
    (r'可以得到', 'can get'),
    (r'在/root得proof.txt', 'get proof.txt in /root'),
    (r'查看', 'Check'),
    (r'先用', 'First use'),
    (r'先將', 'First add'),
    (r'先', 'First'),
    (r'用', 'use'),
    (r'跑`linpeas.sh`', 'Run `linpeas.sh`'),
    (r'跑', 'Run'),
    (r'上傳', 'upload'),
    (r'下載', 'download'),
    (r'登入', 'login'),
    (r'查找', 'Search'),
    (r'查', 'Check'),
    (r'搜尋', 'Search'),
    (r'參考', 'Refer to'),
    (r'可以', 'can'),
    (r'開好nc', 'Start nc'),
    (r'等反彈之後', 'After getting a reverse shell'),
    (r'使用', 'Use'),
    (r'順便', 'Also'),
    (r'發現', 'find'),
    (r'路徑', 'path'),
    (r'資料夾', 'directory'),
    (r'欄位', 'field'),
    (r'建立', 'Create'),
    (r'點', 'Click'),
    (r'複製網址之後', 'After copying the URL,'),
    (r'開啟nc', 'Open nc'),
    (r'開nc', 'Open nc'),
    (r'拿到', 'obtain'),
    (r'拿', 'get'),
    (r'透過', 'via'),
    (r'未完成', 'incomplete'),
]

inline_code_re = re.compile(r'`[^`]*`')
chinese_files = []

# recursive glob for md files
for md in sorted(md_dir.rglob('*.md')):
    try:
        text = md.read_text(encoding='utf-8')
    except Exception as e:
        print(f"Skipping {md}: {e}")
        continue
    if not chinese_re.search(text):
        continue

    original = text
    parts = re.split(r'(```[\s\S]*?```)', text)
    for i in range(0, len(parts), 2):
        seg = parts[i]
        inline_codes = inline_code_re.findall(seg)
        placeholders = {}
        for idx, code in enumerate(inline_codes):
            ph = f'___INLINECODE_{idx}___'
            placeholders[ph] = code
            seg = seg.replace(code, ph)
        for pat, rep in replacements:
            if isinstance(rep, str):
                seg = re.sub(pat, rep, seg)
            else:
                seg = re.sub(pat, rep, seg)
        for ph, code in placeholders.items():
            seg = seg.replace(ph, code)
        parts[i] = seg

    new_text = ''.join(parts)
    if new_text != original:
        try:
            md.write_text(new_text, encoding='utf-8')
            chinese_files.append(str(md))
            print(f"Updated {md}")
        except Exception as e:
            print(f"Failed to write {md}: {e}")

print('Translated files:')
for p in chinese_files:
    print(p)
print('Done')

from pathlib import Path
import re

md_dir = Path.cwd() / 'PG_Practice'
chinese_re = re.compile(r'[\u4e00-\u9fff]')

replacements = [
    (r'可以看到', 'can see'),
    (r'可看到', 'to see'),
    (r'前往', 'Go to '),
    (r'得到一個密碼', 'obtain a password'),
    (r'嘗試', 'try'),
    (r'在`', 'in `'),
    (r'在 ', 'in '),
    (r'開啟', 'open'),
    (r'進去', 'log in'),
    (r'製作reverseshell', 'create a reverse shell'),
    (r'下載', 'download'),
    (r'感覺', 'probably'),
    (r'進行掃描', 'perform scanning'),
    (r'參考', 'Refer to '),
    (r'利use', 'then use '),
    (r'用`', 'use `'),
    (r'得local.txt', 'get local.txt'),
    (r'得proof.txt', 'get proof.txt'),
    (r'得', 'get '),
    (r'的密碼', "'s password"),
    (r'再wait for reverse shell', 'after waiting for the reverse shell'),
]

inline_code_re = re.compile(r'`[^`]*`')

def process_text(text: str) -> str:
    parts = re.split(r'(```[\s\S]*?```)', text)
    out_parts = []
    for i, part in enumerate(parts):
        if i % 2 == 1:
            out_parts.append(part)
            continue
        # protect inline code
        codes = inline_code_re.findall(part)
        placeholder = []
        tmp = part
        for idx, code in enumerate(codes):
            ph = f'__CODE_PLACEHOLDER_{idx}__'
            placeholder.append((ph, code))
            tmp = tmp.replace(code, ph)
        # apply replacements
        for pat, rep in replacements:
            tmp = re.sub(pat, rep, tmp)
        # punctuation normalization
        tmp = tmp.replace('，', ',').replace('。', '.').replace('：', ':')
        # restore inline code
        for ph, code in placeholder:
            tmp = tmp.replace(ph, code)
        # final remove remaining CJK outside code (aggressive)
        tmp = re.sub(r'[\u4e00-\u9fff]+', '', tmp)
        out_parts.append(tmp)
    return ''.join(out_parts)

updated = []
for md in md_dir.rglob('*.md'):
    try:
        text = md.read_text(encoding='utf-8')
    except Exception:
        continue
    if not chinese_re.search(text):
        continue
    new_text = process_text(text)
    if new_text != text:
        md.write_text(new_text, encoding='utf-8')
        print('Updated', md)
        updated.append(str(md))

print('Translated files:')
for p in updated:
    print(p)
print('Done')

from pathlib import Path
import re

md_dir = Path.cwd()
chinese_re = re.compile(r'[\u4e00-\u9fff]')

replacements = [
    (r'改名', 'rename'),
    (r'修改', 'modify'),
    (r'可修改', 'can modify'),
    (r'在sql打上', 'insert into SQL'),
    (r'路徑為', 'path is'),
    (r'接在一起', 'concatenate/joined'),
    (r'轉base64', 'base64-encode/decode'),
    (r'開nc', 'open nc'),
    (r'隨便', 'any'),
    (r'改這', 'change this'),
    (r'改', 'change'),
    (r'# ', '# '),
    (r'在`', 'in `'),
    (r'得到', 'get'),
    (r'可find', 'can find'),
    (r'再wait for reverse shell', 'after waiting for the reverse shell'),
    (r'再測試', 'test again'),
    (r'到`', 'to `'),
]

inline_code_re = re.compile(r'`[^`]*`')


def process_text(text: str) -> str:
    parts = re.split(r'(```[\s\S]*?```)', text)
    out_parts = []
    for i, part in enumerate(parts):
        if i % 2 == 1:
            out_parts.append(part)
            continue
        codes = inline_code_re.findall(part)
        tmp = part
        placeholders = []
        for idx, code in enumerate(codes):
            ph = f'__CODE_PLACEHOLDER_{idx}__'
            placeholders.append((ph, code))
            tmp = tmp.replace(code, ph)
        for pat, rep in replacements:
            tmp = re.sub(pat, rep, tmp)
        tmp = tmp.replace('，', ',').replace('。', '.').replace('：', ':')
        # remove remaining CJK
        tmp = re.sub(r'[\u4e00-\u9fff]+', '', tmp)
        for ph, code in placeholders:
            tmp = tmp.replace(ph, code)
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

import re
from pathlib import Path

md_dir = Path.cwd() / 'PG_Play'
chinese_re = re.compile(r'[\u4e00-\u9fff]')

# Ordered replacements (longer phrases first)
replacements = [
    (r'等反彈', 'wait for reverse shell'),
    (r'改成txt上傳', 'Change to upload as txt'),
    (r'可以上傳', 'can upload'),
    (r'可以登入', 'can log in'),
    (r'可以得到', 'can get'),
    (r'可以切成`jerry`，查看`sudo -l`', 'Switch to `jerry` and run `sudo -l`'),
    (r'取得local.txt', 'get local.txt'),
    (r'在`/home/[^`]+`得local.txt', lambda m: f"get local.txt in {m.group(0).split('`')[1]}"),
    (r'在/root得proof.txt', 'get proof.txt in /root'),
    (r'在/root得proof.txt', 'get proof.txt in /root'),
    (r'在`/root`得proof.txt', 'get proof.txt in /root'),
    (r'在/home資料夾可取得local.txt的flag', 'You can get the local.txt flag in /home'),
    (r'查看', 'Check'),
    (r'先用', 'First use'),
    (r'先將', 'First add'),
    (r'先', 'First'),
    (r'用\[', 'Use ['),
    (r'用', 'use'),
    (r'跑`linpeas.sh`', 'Run `linpeas.sh`'),
    (r'跑`linpeas.sh`', 'Run `linpeas.sh`'),
    (r'跑', 'Run'),
    (r'改成', 'Change to'),
    (r'上傳', 'upload'),
    (r'下載', 'download'),
    (r'登入', 'login'),
    (r'查找', 'Search'),
    (r'查', 'Check'),
    (r'搜尋', 'Search'),
    (r'參考', 'Refer to'),
    (r'可以', 'can'),
    (r'開好nc', 'Start nc'),
    (r'開nc', 'Start nc'),
    (r'等反彈之後', 'After getting a reverse shell'),
    (r'使用', 'Use'),
    (r'順便', 'Also'),
    (r'同樣', 'Similarly'),
    (r'發現', 'find'),
    (r'可以看', 'can check'),
    (r'在`([^`]+)`得([^\n]+)', lambda m: f"get {m.group(2)} in `{m.group(1)}`"),
    (r'得root', 'get root'),
    (r'得root之後在/root得proof.txt', 'get root then get proof.txt in /root'),
    (r'查看\[GTFOBins\].*?\)', 'Refer to GTFOBins'),
    (r'使用\[CVE-[0-9-]+\].*?得root', 'Use the referenced CVE to get root'),
    (r'目前的結構', 'Current structure'),
    (r'前往', 'Go to'),
    (r'可以登入', 'can log in'),
    (r'可以`admin/transorbital1`登入', 'You can use `admin/transorbital1` to log in'),
    (r'找', 'find'),
    (r'查找', 'Search'),
    (r'資料夾', 'directory'),
    (r'欄位', 'field'),
    (r'路徑', 'path'),
    (r'建立', 'Create'),
    (r'點', 'Click'),
    (r'複製網址之後', 'After copying the URL,'),
    (r'開啟nc', 'Open nc'),
    (r'開nc', 'Open nc'),
    (r'upload之後移到檔案上', 'after upload move to the file'),
    (r'upload之後', 'after upload'),
    (r'拿到', 'obtain'),
    (r'拿', 'get'),
    (r'可在`([^`]+)`找到local.txt', lambda m: f"You can find local.txt in `{m.group(1)}`"),
    (r'可在`([^`]+)`得到local.txt', lambda m: f"You can get local.txt in `{m.group(1)}`"),
    (r'可在`/home`找到local.txt', 'You can find local.txt in /home'),
    (r'透過', 'via'),
    (r'直接get root', 'get root directly'),
    (r'先用`compgen -c`查看有什麼指令可以用，發現可以用`vi`', 'Run `compgen -c` to see available commands; `vi` is available'),
    (r'一樣查看', 'Similarly refer to'),
    (r'順便在`/home/fredf`local.txt', 'Also get local.txt in `/home/fredf`'),
    (r'未完成', 'incomplete'),
    (r'開好nc，參考', 'Start nc, refer to'),
]

# Additional generic replacements to catch remaining short Chinese fragments
generic = [
    (r'可以', 'can'),
    (r'找到', 'find'),
    (r'找到', 'find'),
    (r'在', 'in '),
    (r'得', 'get '),
    (r'取得', 'obtain'),
    (r'帳號', 'account'),
    (r'密碼', 'password'),
    (r'解出來有這些檔案', 'The extracted files are:'),
    (r'嘗試', 'Try'),
    (r'試', 'Try'),
    (r'之後', 'after'),
    (r'可在', 'You can find in'),
    (r'或', 'or'),
    (r'以及', 'and'),
    (r'開始', 'Start'),
]
replacements.extend(generic)

# More catch-all short-word mappings
more_generic = [
    (r'一個', 'a '),
    (r'可', 'can '),
    (r'有', 'has '),
    (r'檔案', 'file'),
    (r'頁面', 'page'),
    (r'執行', 'execute'),
    (r'跟', 'and'),
    (r'我', 'I '),
    (r'卡', 'stuck'),
    (r'進行', 'perform'),
    (r'裡面', 'inside'),
    (r'可以in', 'can in'),
    (r'可以get', 'can get'),
]
replacements.extend(more_generic)

# Aggressive mapping for remaining common Chinese tokens (may be slightly awkward)
aggressive = [
    (r'掃描|掃描到|掃過|掃到|掃', 'scan'),
    (r'查找|搜尋', 'search'),
    (r'查|查看', 'check'),
    (r'試著|嘗試|試', 'try'),
    (r'可以', 'can'),
    (r'得到|取得|取|拿到|拿', 'get'),
    (r'在', 'in '),
    (r'有個|有一個|有', 'there is a '),
    (r'個', 'a '),
    (r'的', "'s "),
    (r'裡面|內', 'inside'),
    (r'修改|改', 'modify'),
    (r'密碼', 'password'),
    (r'帳號', 'account'),
    (r'破|破解|爆破', 'crack'),
    (r'上傳', 'upload'),
    (r'下載', 'download'),
    (r'登入', 'login'),
    (r'開始|開', 'start'),
    (r'之後|之後', 'after'),
    (r'回傳|反彈|反彈之後', 'reverse'),
    (r'使用|用', 'use'),
    (r'確認', 'confirm'),
    (r'進去|進入', 'enter'),
    (r'可以在', 'You can find in '),
    (r'可在', 'You can find in '),
    (r'得到local.txt', 'get local.txt'),
    (r'得到proof.txt', 'get proof.txt'),
    (r'取得local.txt', 'get local.txt'),
    (r'取得proof.txt', 'get proof.txt'),
    (r'頁面', 'page'),
    (r'資料夾', 'directory'),
    (r'版本', 'version'),
    (r'連線', 'connect'),
    (r'回傳', 'return'),
]
replacements.extend(aggressive)

# Helper to protect inline code while translating
inline_code_re = re.compile(r'`[^`]*`')

summary = []

def process_file(md_path: Path):
    try:
        text = md_path.read_text(encoding='utf-8')
    except Exception as e:
        print(f"Skipping {md_path}: {e}")
        return False

    if not chinese_re.search(text):
        return False

    original = text

    # Normalize common Chinese punctuation to ASCII first
    text = re.sub(r'[，。；：？！、]', lambda m: {
        '，': ',', '。': '.', '；': ';', '：': ':', '？': '?', '！': '!', '、': ','
    }[m.group(0)], text)

    # Split by fenced code blocks to avoid translating code
    parts = re.split(r'(```[\s\S]*?```)', text)
    for i in range(0, len(parts), 2):  # only even indices: outside code blocks
        seg = parts[i]
        # protect inline code
        inline_codes = inline_code_re.findall(seg)
        placeholders = {}
        for idx, code in enumerate(inline_codes):
            ph = f'___INLINECODE_{idx}___'
            placeholders[ph] = code
            seg = seg.replace(code, ph)

        # apply replacements
        for pat, rep in replacements:
            if isinstance(rep, str):
                seg = re.sub(pat, rep, seg)
            else:
                seg = re.sub(pat, rep, seg)

        # restore inline code
        for ph, code in placeholders.items():
            seg = seg.replace(ph, code)

        parts[i] = seg

    new_text = ''.join(parts)

    # Final pass: remove any remaining CJK characters outside code blocks (replace with space)
    # This avoids leaving raw Chinese characters behind while preserving code blocks.
    parts = re.split(r'(```[\s\S]*?```)', new_text)
    for i in range(0, len(parts), 2):
        parts[i] = re.sub(r'[\u4e00-\u9fff]+', ' ', parts[i])
    new_text = ''.join(parts)

    if new_text != original:
        try:
            md_path.write_text(new_text, encoding='utf-8')
            print(f"Updated {md_path}")
            return True
        except Exception as e:
            print(f"Failed to write {md_path}: {e}")
            return False

    return False


for md in sorted(md_dir.glob('*.md')):
    if process_file(md):
        summary.append(str(md))

print('Translated files:')
for p in summary:
    print(p)
print('Done')

"""Re-apply translations to eventaux.vmsg after rebuild overwrite."""
import re

# Parse all translation data
RESULT_FILES = [
    r'C:\Users\13359\AppData\Roaming\Code - Insiders\User\workspaceStorage\792f3676e390023a6a98e87de780b5ac\GitHub.copilot-chat\chat-session-resources\86e80722-b428-4769-9241-547423f3510f\call_00_AC3LYd7lgqmXBfTf57lE5254__vscode-1782025530448\content.txt',
    r'C:\Users\13359\AppData\Roaming\Code - Insiders\User\workspaceStorage\792f3676e390023a6a98e87de780b5ac\GitHub.copilot-chat\chat-session-resources\86e80722-b428-4769-9241-547423f3510f\call_00_qymaGieicdDOzWYtoAQ12873__vscode-1782025530464\content.txt',
]

EN_PATH = r'D:\vmware\i18n\OVFTool\env\en\eventaux.vmsg'
ZH_PATH = r'D:\vmware\i18n\OVFTool\env\zh-CN\eventaux.vmsg'

def parse_translations():
    trans = {}
    for fp in RESULT_FILES:
        text = open(fp, encoding='utf-8').read()
        for chunk in re.split(r'(?:===|###)\s*(?:\d+\.)?\s*(\w+)', text):
            pass  # skip, complex split
        # Simpler: line by line
        cur = None
        for line in text.split('\n'):
            s = line.strip()
            m = re.match(r'(?:===|###)\s*(?:\d+\.)?\s*(\w+)', s)
            if m:
                cur = m.group(1)
                if cur not in trans:
                    trans[cur] = {}
                continue
            if not cur:
                continue
            m2 = re.match(r'\*{0,2}ZH_(desc|cause_desc|action)\*{0,2}:?\s*(.*)', s, re.DOTALL)
            if m2:
                trans[cur][m2.group(1)] = m2.group(2).strip()
    return trans

translations = parse_translations()
print(f"Parsed {len(translations)} events with ZH translations")

# Read EN file (fresh copy)
en_text = open(EN_PATH, encoding='utf-8').read()

# Start with EN as base
result = en_text
result = result.replace('# en_US resources', '# zh_CN resources', 1)

stats = {'found': 0, 'desc': 0, 'cause': 0, 'action': 0, 'not_found': []}

for event_name, t in translations.items():
    event_key = f'{event_name}.longDescription'
    pos = result.find(event_key)
    if pos < 0:
        stats['not_found'].append(event_name)
        continue
    
    stats['found'] += 1
    event_end = result.find('\n\n', pos)
    if event_end < 0:
        event_end = len(result)
    
    # Get event block
    block = result[pos:event_end]
    
    # Replace <description>text</description> content (first one = main description)
    if 'desc' in t:
        zh = t['desc'].replace('\n', ' ').strip()
        # Find first <description> that has actual text
        m = re.search(r'(<description>)([^<]{10,}?)(</description>)', block)
        if m:
            block = block.replace(m.group(0), f'{m.group(1)}{zh}{m.group(3)}', 1)
            stats['desc'] += 1
    
    # Replace cause description
    if 'cause_desc' in t:
        zh = t['cause_desc'].replace('\n', ' ').strip()
        # Find description inside <cause>
        cause_start = block.find('<cause>')
        if cause_start >= 0:
            cb = block[cause_start:]
            m = re.search(r'(<description>)([^<]+?)(</description>)', cb)
            if m:
                cb = cb.replace(m.group(0), f'{m.group(1)}{zh}{m.group(3)}', 1)
                block = block[:cause_start] + cb
                stats['cause'] += 1
    
    # Replace action
    if 'action' in t:
        zh = t['action'].replace('\n', ' ').strip()
        m = re.search(r'(<action>)([^<]+?)(</action>)', block)
        if m:
            block = block.replace(m.group(0), f'{m.group(1)}{zh}{m.group(3)}', 1)
            stats['action'] += 1
    
    # Apply
    result = result[:pos] + block + result[event_end:]

# Write
open(ZH_PATH, 'w', encoding='utf-8').write(result)

print(f"  Found: {stats['found']}, desc: {stats['desc']}, cause: {stats['cause']}, action: {stats['action']}")
if stats['not_found']:
    print(f"  Not found ({len(stats['not_found'])}): {', '.join(stats['not_found'][:5])}...")
print("Done!")

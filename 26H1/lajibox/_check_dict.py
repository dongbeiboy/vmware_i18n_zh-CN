"""检查翻译库中有多少可用 JA→ZH 翻译对"""
import csv

ja_zh = {}
with open('key_en_ja_cn_fixed.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        if len(row) >= 4 and row[2] and row[3]:
            ja = row[2].strip()
            zh = row[3].strip()
            if ja and zh and ja != zh:
                ja_zh[ja] = zh

print(f"共 {len(ja_zh)} 条 JA→ZH 翻译对")

# DLL 中出现的日语词汇
dll_terms = [
    '設定', '接続', '切断', 'キャンセル', 'ヘルプ', '名前',
    '仮想マシン', 'パスワード', 'アイコン', '表示', '非表示',
    'スマート カード', '挿入', '取り出し', '変更',
    '作成', '開く', '削除', '追加', '停止', '開始',
    'ダウンロード', 'メッセージ', 'ドライブ', 'ファイル',
    'ディスク', 'パワーオン', 'ライブラリ', 'ホーム',
    'ディレクトリ', 'マッピング', 'ボリューム',
    'エクスプローラー', 'トランザクション', 'ロールバック',
    'ムービー', 'キャプチャ', 'ログ', '消去',
    '設定の解除', '反映', '強制', '参照',
    'コメント', 'ディスクから削除', '名前の変更',
    '新規', 'マシン', 'ドライブ', 'マップ',
    '読取り専用', 'モード', 'デバイス', '問題',
    'VMDB', 'ビューア', '新規ディレクトリ',
    'ルール', '無視', 'VNC',
]

# 统计有多少在库里
found_count = 0
for term in dll_terms:
    matches = [(ja, zh) for ja, zh in ja_zh.items() if term in ja]
    if matches:
        found_count += 1
        ex_ja, ex_zh = matches[0]
        print(f"  ✅ {term:20s} → {ex_zh[:40]}")
    else:
        print(f"  ❌ {term:20s} → 未找到")

print(f"\n覆盖: {found_count}/{len(dll_terms)} 词汇")

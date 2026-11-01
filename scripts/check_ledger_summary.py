import json
import sys

if sys.stdout:
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

with open('published_ledger.json', 'r', encoding='utf-8') as f:
    ledger = json.load(f)

print(f"Total en ledger: {len(ledger)}")
print("\nÚltimos 10 videos publicados:")
for item in ledger[-10:]:
    print(f"- [{item.get('id')}] {item.get('title')} ({item.get('timestamp')})")

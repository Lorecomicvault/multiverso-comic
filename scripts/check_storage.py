import json
import subprocess

cmd = ['gh', 'api', 'repos/Lorecomicvault/multiverso-comic/actions/artifacts', '--paginate']
out = subprocess.check_output(cmd, encoding='utf-8')
data = json.loads(out)
artifacts = data.get('artifacts', [])
total_bytes = sum(a['size_in_bytes'] for a in artifacts)

print(f"Total artefactos encontrados: {len(artifacts)}")
print(f"Espacio total ocupado: {total_bytes / (1024*1024):.2f} MB ({total_bytes / (1024*1024*1024):.3f} GB)")
print("-" * 75)
for a in artifacts:
    mb = a['size_in_bytes'] / (1024 * 1024)
    print(f"ID: {a['id']} | {a['name']:<40} | {mb:>6.2f} MB | {a['created_at'][:10]}")

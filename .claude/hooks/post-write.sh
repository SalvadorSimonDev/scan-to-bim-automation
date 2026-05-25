#!/usr/bin/env bash
# Log de archivos generados
input=$(cat)
fp=$(echo "$input" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('file_path',''))" 2>/dev/null)
name=$(basename "$fp")
ts=$(date '+%Y-%m-%d %H:%M:%S')
echo "$ts | WRITE | $name" >> .claude/build.log 2>/dev/null
exit 0

#!/usr/bin/env bash
# Guard: Transaction sin RollBack en scripts Python
input=$(cat)
fp=$(echo "$input" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('file_path',''))" 2>/dev/null)
ct=$(echo "$input" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('content',''))" 2>/dev/null)

if [[ "$fp" == *.py ]] && echo "$ct" | grep -q "Transaction" && ! echo "$ct" | grep -q "RollBack"; then
    echo "[BIM-GUARD] Transaction sin RollBack detectada. Añade RollBack en el bloque except."
    exit 2
fi
exit 0

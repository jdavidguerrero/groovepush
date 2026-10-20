#!/bin/bash
# Rebuild one panel board from placement to DRC (same order as the Brain's build_pcb_a.sh).
#   bash hardware/boards/tools/build.sh pcb-f
set -euo pipefail
cd "$(dirname "$0")"
B=$1
KPY=/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/Current/bin/python3
KC=/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli
run() { "$KPY" "$@" 2>&1 | grep -v -e "assert" -e "leak" -e "^$" | tail -2; }
"$KPY" - "$B" <<'PY' 2>/dev/null
import sys, pcbnew
p = f"../{sys.argv[1]}/{sys.argv[1]}.kicad_pcb"
b = pcbnew.LoadBoard(p)
for t in list(b.GetTracks()): b.Delete(t)
for z in list(b.Zones()): b.Delete(z)
for g in list(b.Groups()): b.Delete(g)
pcbnew.SaveBoard(p, b)
PY
run "place_${B//-/_}.py"
run sync_from_netlist.py "$B"
run sync_fp_fields.py "$B"
run trim_silk_outside.py "$B"
run add_gnd_escapes.py "$B"
for pass in 1 2; do
  rm -f "../$B/$B.ses" "../$B/${B}_best.ses"
  run route_board.py "$B" 60 || echo "Freerouting pass $pass gave no result"
done
run finish_routing.py "$B"
run clean_vias.py "$B"
run add_gnd_pours.py "$B"
run sync_fp_fields.py "$B"
"$KC" pcb drc --schematic-parity --severity-all -o "/tmp/$B-drc.rpt" "../$B/$B.kicad_pcb" >/dev/null 2>&1 || true
grep -E "Found" "/tmp/$B-drc.rpt"
grep -E "^\[" "/tmp/$B-drc.rpt" | sed -E 's/\]:.*/]/' | sort | uniq -c | sort -rn

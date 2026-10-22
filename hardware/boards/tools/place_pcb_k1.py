"""Place PCB-K1 (front row + edit block, 15 keys, MCP23017 @0x21/@0x22) from the panel table.

L-shaped board: a front strip (SHIFT, transport, navigation) and the edit block left of the
NeoTrellis M4. Choc V2 on F.Cu; LEDs (4.93 mm behind each key centre), caps, MCPs and JSTs on B.Cu.
U1 sits between METRO and BANK_L, U2 above UNDO (each next to the keys it reads). J1 (to PCB-A) and J2 (to
PCB-K2) face the back edge of the edit block. Right edge stops at x 229.5 to clear fader F1's body.
"""
import boardlib as bl

LED_OFFSET = 4.93
path, b = bl.load("pcb-k1")
print("refreshed", bl.refresh_lib_footprints(b), "library footprints")
P = bl.panel()
bl.jlc_rules(b)

ORDER = ["QUANTIZE", "DUPLICATE", "DELETE", "UNDO", "NEW", "SHIFT", "PLAY", "STOP", "RECORD", "LOOP",
         "METRO", "BANK_L", "BANK_R", "OCT_DN", "OCT_UP"]  # SW1..15, D1..15, C10..24
for i, k in enumerate(ORDER):
    x, y = float(P[k]["x_mm"]), float(P[k]["y_mm"])
    bl.place(b, f"SW{i+1}", x, y)
    bl.place(b, f"D{i+1}", x, y + LED_OFFSET, back=True)
    side = -1 if k == "METRO" else 1   # METRO's cap would sit on U1
    bl.place(b, f"C{10+i}", x + 7.5 * side, y + LED_OFFSET, rot=90, back=True)

# MCPs by locality: U1 (SSOP-28) serves transport + navigation from the 10.5 mm gap between
# METRO and BANK_L; U2 (SOIC-28W) serves the edit block, SHIFT and PCB-K2 from above UNDO.
bl.place(b, "U1", 149.25, 24.0, rot=0, back=True)   # @0x21
bl.place(b, "C1", 149.25, 31.0, rot=0, back=True)
bl.place(b, "U2", 34.0, 89.5, rot=90, back=True)    # @0x22
bl.place(b, "C2", 44.0, 89.5, rot=90, back=True)
TOP = 103.0
for ref, x in (("J2", 35.0), ("J1", 52.5)):  # J2 key pins right above U2 GPA1–5
    for rot in (0, 180):
        bl.place(b, ref, x, TOP - 3.3, rot=rot, back=True)
        if bl.jst_opening(b, ref)[1] > 0.9:
            break
    assert bl.jst_opening(b, ref)[1] > 0.9, f"{ref} must open to the back"
bl.place(b, "C3", 61.5, 96.0, rot=90, back=True)
bl.place(b, "R1", 44.5, 95.0, rot=0, back=True)
bl.place(b, "H1", 45.75, 24.0)
bl.place(b, "H2", 34.0, 41.0)

bl.hide_refs(b, [f"D{i+1}" for i in range(15)] + [f"C{10+i}" for i in range(15)] +
             ["C1", "C2", "C3", "R1", "H1", "H2", "J1", "J2", "U1", "U2"])
bl.outline_poly(b, [(22, 12), (229.5, 12), (229.5, 35.5), (64, 35.5), (64, TOP), (22, TOP)])
bl.save(b, path)
print("PCB-K1 placed")

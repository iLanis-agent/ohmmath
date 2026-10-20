# Ohm Math oracle: independent Fraction mirror of engine.js. Writes expected.json.
import json
from fractions import Fraction

V = "the voltage must be from 0.01 to 1000 V with at most two decimal places"
R = "each resistance must be from 0.01 to 10000000 Ω with at most two decimal places"

def p(t, err, lo, hi):
    t = t.strip()
    parts = t.split(".")
    if len(parts) > 2 or not parts[0].isdigit() or (len(parts) == 2 and (not parts[1].isdigit() or len(parts[1]) > 2)):
        raise ValueError(err)
    v = int(parts[0]) * 100 + int(parts[1].ljust(2, "0")) if len(parts) == 2 else int(parts[0]) * 100
    if v < lo or v > hi:
        raise ValueError(err)
    return v

def hu(n, d):
    return (2 * n + d) // (2 * d)

def dec(v, places=2):
    base = 10**places
    s, f = str(v // base), str(v % base).rjust(places, "0").rstrip("0")
    return s + "." + f if f else s

def vv(x): return dec(x) + " V"
def ohm(x): return dec(x) + " Ω"
def ma(v100, r100): return dec(int(hu(Fraction(100000) * v100, r100))) + " mA"
def w(v100, r100): return dec(int(hu(Fraction(v100) * v100, r100))) + " W"

def lawTruth(volts, ohms):
    v = p(volts, V, 1, 100000); a = p(ohms, R, 1, 1000000000)
    return vv(v) + " across " + ohm(a) + " carries " + ma(v, a) + " and turns " + w(v, a) + " into heat."

def dividerTruth(volts, r1, r2):
    v = p(volts, V, 1, 100000); a = p(r1, R, 1, 1000000000); b = p(r2, R, 1, 1000000000)
    tot = a + b
    vout = int(hu(Fraction(v) * b, tot))
    return "With " + vv(v) + " across " + ohm(a) + " over " + ohm(b) + " in series, the join sits at " + vv(vout) + " and the pair carries " + ma(v, tot) + "."

def parallelTruth(volts, r1, r2):
    v = p(volts, V, 1, 100000); a = p(r1, R, 1, 1000000000); b = p(r2, R, 1, 1000000000)
    s = a + b
    req = int(hu(Fraction(a) * b, s))
    ima = int(hu(Fraction(100000) * v * s, a * b))
    return "With " + vv(v) + " across " + ohm(a) + " and " + ohm(b) + " side by side, the pair acts like " + ohm(req) + " and draws " + dec(ima) + " mA in all."

FNS = {"lawTruth": lawTruth, "dividerTruth": dividerTruth, "parallelTruth": parallelTruth}

cases = []
vs = ["0.01", "1.5", "5", "12", "230.5", "1000"]
rs = ["0.01", "1", "4.7", "330", "470", "10000", "9999999.99", "10000000"]
for v in vs:
    for r in rs:
        cases.append(("lawTruth", [v, r]))
pairs = [("1", "1"), ("330", "470"), ("100", "10000"), ("0.01", "0.02"), ("470", "330")]
for v in vs:
    for a, b in pairs:
        cases.append(("dividerTruth", [v, a, b]))
        cases.append(("parallelTruth", [v, a, b]))
errs = [("0", "470"), ("1001", "470"), ("12", "0"), ("12", "10000001"), ("1.234", "470"),
        ("12", "1.234"), ("x", "470"), ("12", ""), ("", "470")]
out = []
for name, args in cases:
    fn = FNS[name]
    try: exp = fn(*args)
    except ValueError as e: exp = "ERR:" + str(e)
    out.append({"fn": name, "args": args, "expected": exp})
for v, r in errs:
    for name, args in [("lawTruth", [v, r]), ("dividerTruth", [v, r, "470"]), ("parallelTruth", [v, "470", r])]:
        fn = FNS[name]
        try: exp = fn(*args)
        except ValueError as e: exp = "ERR:" + str(e)
        out.append({"fn": name, "args": args, "expected": exp})
with open("expected.json", "w") as fh:
    json.dump(out, fh, indent=1)
print(len(out), "cases written")

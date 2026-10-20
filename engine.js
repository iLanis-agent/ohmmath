// Ohm Math engine: Ohm's law over a resistor, a two-resistor voltage divider, and two resistors in parallel. Exact integers (hundredths of a volt, hundredths of an ohm), half-up on display only.
function _p(t, err, intDigits, places, lo, hi) {
  t = typeof t === "string" ? t.trim() : "";
  var m = new RegExp("^([0-9]{1," + intDigits + "})(?:\\.([0-9]{1," + places + "}))?$").exec(t);
  if (!m) throw new Error(err);
  var v = parseInt(m[1], 10) * Math.pow(10, places) + (m[2] ? parseInt(m[2].padEnd(places, "0"), 10) : 0);
  if (v < lo || v > hi) throw new Error(err);
  return v;
}
var _V = "the voltage must be from 0.01 to 1000 V with at most two decimal places";
var _R = "each resistance must be from 0.01 to 10000000 Ω with at most two decimal places";
function _hu(n, d) { return Math.floor((2 * n + d) / (2 * d)); }
function _dec(v, places) {
  var base = Math.pow(10, places);
  var s = String(Math.floor(v / base)), f = String(v % base).padStart(places, "0").replace(/0+$/, "");
  return f ? s + "." + f : s;
}
function _v(v) { return _dec(v, 2) + " V"; }
function _ohm(r) { return _dec(r, 2) + " Ω"; }
function _ma(v100, r100) { // hundredths of a mA, exact ratio then half up
  return _dec(_hu(100000 * v100, r100), 2) + " mA";
}
function _w(v100, r100) { // hundredths of a W: V^2/R
  return _dec(_hu(v100 * v100, r100), 2) + " W";
}
function _in(v, r1, r2) {
  var out = { v: _p(v, _V, 4, 2, 1, 100000), a: _p(r1, _R, 8, 2, 1, 1000000000) };
  if (r2 !== undefined) out.b = _p(r2, _R, 8, 2, 1, 1000000000);
  return out;
}

function lawTruth(volts, ohms) {
  var p = _in(volts, ohms);
  return _v(p.v) + " across " + _ohm(p.a) + " carries " + _ma(p.v, p.a) + " and turns " + _w(p.v, p.a) + " into heat.";
}
function dividerTruth(volts, r1, r2) {
  var p = _in(volts, r1, r2), tot = p.a + p.b;
  var vout = _hu(p.v * p.b, tot);
  return "With " + _v(p.v) + " across " + _ohm(p.a) + " over " + _ohm(p.b) + " in series, the join sits at " + _v(vout) + " and the pair carries " + _ma(p.v, tot) + ".";
}
function parallelTruth(volts, r1, r2) {
  var p = _in(volts, r1, r2), s = p.a + p.b;
  var req = _hu(p.a * p.b, s); // display only
  var ima = _hu(100000 * p.v * s, p.a * p.b); // exact from the unrounded ratio
  return "With " + _v(p.v) + " across " + _ohm(p.a) + " and " + _ohm(p.b) + " side by side, the pair acts like " + _ohm(req) + " and draws " + _dec(ima, 2) + " mA in all.";
}

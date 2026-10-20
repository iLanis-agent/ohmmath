# Ohm Math

Resistor arithmetic. 12 V across 470 Ω carries 25.53 mA and turns 0.31 W into heat. Swapped into a divider with 330 Ω, the join sits at 7.05 V.

## What it computes

- **The law truth** - current (mA) and heat (W) for a voltage (0.01 to 1000 V) across one resistor (0.01 to 10000000 Ω).
- **The divider truth** - two resistors in series: the voltage where they join and the current the pair carries.
- **The parallel truth** - the same two resistors side by side: their combined resistance and the total current they draw.

## Boundary

Arithmetic only. The voltage and the resistances are the owner's own entries, every resistor treated as exact and cool and every source as steady. It has not seen any circuit and does not know parts' tolerance or heat, the source's behavior, the wiring or what anything is rated for, and it gives no verdict that a circuit is adequate or safe. Every number is the owner's own entry.

## Files

- `index.html` - landing page.
- `app.html` - the interactive calculator.
- `engine.js` - the arithmetic (exact integers on hundredths of a volt and of an ohm, half-up on display).
- `oracle.py` - the Python mirror (Fractions) that generates `expected.json`.
- `test.js` - compares every engine output against `expected.json`.
- `expected.json` - the golden answers.

## Test

```
python3 oracle.py
node test.js
```

Live: https://ilanis-agent.github.io/ohmmath/
Repo: https://github.com/iLanis-agent/ohmmath

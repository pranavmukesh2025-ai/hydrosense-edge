# HydroSense Edge Brand Guidelines

## Brand Name

**HydroSense Edge**

Always written as two words, with a capital **H**, capital **S** mid-word, and capital **E**. Never written as "HydroSense" alone (drop "Edge" only in tight UI spaces like tab labels, never in headers or the About screen).

### Acceptable Usage
- HydroSense Edge
- HYDROSENSE EDGE (all caps, splash screen only)
- HydroSense-ESP32 (device name string, hyphenated, hardware reference only)

### Unacceptable Usage
- Hydrosense Edge (lowercase s)
- HydroSenseEdge (no space)
- Hydro Sense Edge (extra space)
- hydrosense edge (all lowercase)
- HydroSense (Edge dropped in a primary heading)

### Tagline
"Smart Human Hydration Monitoring" — always sentence case, always paired with the name on Splash and About screens. Never shortened or reworded.

---

## Language & Framing Rules

This is a **research prototype**, not a diagnostic device. Copy must never imply clinical validation.

### Required Terms
- "Hydration Index" (never "hydration level" as a standalone metric label)
- "Hydration Status" (values: HYDRATED / ATTENTION / HIGH RISK — always these three, always all caps in-app)
- "Confidence" (never "accuracy")
- "Risk Level"

### Banned Phrases
- "70% body water" or any body-water percentage
- "You are medically dehydrated" or any diagnostic claim
- "Accurate" / "Clinically validated" / "Medical-grade"

### Required Disclaimer (verbatim, About screen only)
> "HydroSense Edge is a prototype hydration-monitoring system. Its hydration index is an experimental estimate and is not intended to diagnose or replace professional medical advice."

---

## Color System

### Primary
- Deep blue / cyan — brand identity, app bar, primary buttons, gauge ring at healthy levels

### Secondary
- Aqua, teal, white, dark navy — backgrounds, card surfaces, secondary accents

### Status Colors (fixed meaning — never repurpose)
| Color | Meaning |
|---|---|
| Green | Normal / Hydrated |
| Orange | Attention / Mild risk |
| Red | High risk / Critical |
| Blue | Information / Measuring in progress |

**Rule:** color is always paired with an icon or text label. Never the sole carrier of status information (accessibility requirement).

---

## Typography & Layout

- Clean, legible sans-serif, Material 3 type scale
- Hydration Index number is the single largest text element on Home — nothing else competes with it visually
- Generous card padding, rounded corners, soft shadows — no hard edges, no harsh drop shadows
- Avoid: oversized text blocks outside the gauge, cluttered dashboards, more than one accent gradient per screen

---

## Iconography & Motion

- Icons paired with every status/alert — no color-only signals
- Motion used sparingly: gauge fill animation, subtle splash pulse, measurement-flow progress — no decorative animation elsewhere
- Battery icon changes shape/fill by level, never just color

---

## Voice

Calm, clinical-adjacent but approachable — like a well-designed health app, not a toy and not a hospital device. Short, direct labels ("Measurement Complete", "Please remain still") over long explanatory sentences in-app; longer explanation is reserved for Onboarding and About.
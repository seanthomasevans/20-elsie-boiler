# Combi Boiler vs Tankless + External Components

What's actually different inside the box, and what Sean's build replicates vs what it doesn't.

---

## What's Inside a Combi Boiler

A combi boiler (Navien NCB-E, Rinnai i-Series Combi, Viessmann Vitodens 100-W) is a tankless water heater with the following built in:

1. **Primary heat exchanger** for the heating loop (stainless steel or copper-fin)
2. **Secondary plate heat exchanger** for DHW (flat-plate stainless, separates heating water from potable water)
3. **Diverter valve** that switches between heating mode and DHW priority mode
4. **Circulation pump** (variable-speed, built into the unit)
5. **Expansion vessel** (small, typically 2L, internal or bracket-mounted)
6. **Pressure relief valve** and **pressure gauge** (3 bar / 45 psi typically)
7. **Auto-fill / filling loop** connection (to top up the closed heating circuit)
8. **System controls**: outdoor reset curve, frost protection, anti-cycling logic, DHW priority timer
9. **Flow switch** for DHW detection

The critical architectural difference: a combi runs a **closed heating loop**. The water in the radiator/fan coil circuit is separate from potable water. It recirculates the same treated water. DHW gets heated indirectly through the plate heat exchanger.

---

## What's Inside Sean's Build (Rinnai RXP199iN + External Components)

Sean's system uses a standard tankless water heater with externally assembled components:

| Component | Combi (Internal) | Sean's Build (External) |
|---|---|---|
| Heat exchanger | Dual (primary + plate HX) | Single (one HX does both jobs) |
| Circulation pump | Built-in variable-speed | External cast-iron circ pump |
| Expansion tank | Small internal vessel | External 2-gal Watts or Amtrol |
| Diverter/zone valve | Internal motorized diverter | External Honeywell zone valve |
| DHW temperature control | Internal modulation | External TMV (thermostatic mixing valve) |
| Heating controls | Built-in outdoor reset, frost protection | MCC912 controller + thermostat |
| Loop type | **Closed loop** (treated water) | **Open loop** (potable water) |
| Pressure management | Internal PRV + gauge | External PRV on expansion tank |

---

## The Real Difference: Open Loop vs Closed Loop

This is the thing that matters most for longevity and maintenance.

### Closed loop (combi boiler)
- Same water recirculates through the heating circuit indefinitely
- Water gets dosed with inhibitor chemicals (Fernox F1, Sentinel X100) that prevent corrosion and scale
- Very little dissolved oxygen after initial fill (oxygen is the main driver of corrosion)
- Fan coil internals see almost no fresh mineral content
- **Result**: minimal scaling, minimal corrosion, long component life

### Open loop (Sean's build)
- Fresh potable water flows through the fan coil every cycle
- No chemical treatment possible (it's drinking water)
- Continuous oxygen exposure from fresh water supply
- Fresh minerals deposited with every heating cycle
- **Result**: more maintenance attention needed, but absolutely viable for Toronto's water quality

### Is open loop a problem?

Not really, for this specific situation:

- **Toronto water hardness is moderate** (~120-140 ppm / 7-8 grains). Not soft enough to be corrosive, not hard enough to scale aggressively.
- **Rinnai explicitly supports open-loop hydronic** per Technical Bulletin TB-043. They wouldn't publish that if it killed their heat exchangers.
- **The fan coil is copper or copper-nickel**. Resistant to the oxygen levels in potable water.
- **Flow rate through the fan coil is high** (2-4 GPM), which prevents stagnant scale buildup.
- **No stagnant dead legs** in Sean's design. Water moves when heating calls, sits in pipes when idle (same as any plumbing).

The main maintenance item: **flush the heating loop annually**. Run cold water through until it runs clear. Five minutes with a hose bib. A combi with a closed loop might go 5-10 years between flushes (just top up inhibitor annually).

---

## What the Expansion Tank and Pump Actually Do

### Expansion tank

**Same job in both systems.** When water heats from 60F to 160F, it expands about 3%. In a closed system (combi), this expansion has nowhere to go without a tank. In Sean's open system, the expansion tank prevents pressure spikes that could trigger the T&P relief valve or stress fittings. It also absorbs the "water hammer" from the zone valve opening/closing.

The expansion tank is NOT what makes a combi a combi. It's just pressure management. Sean's external tank does the exact same job.

### Circulation pump

**Same job in both systems.** Moves water through the fan coil when the thermostat calls for heat. A combi has a variable-speed pump that modulates flow. Sean's external pump is likely fixed-speed (Taco 007e or Grundfos UP15-42), which is fine for a single zone. A variable-speed option (Taco VR1816) would save a few watts but isn't necessary for one fan coil.

The pump is NOT what makes a combi a combi either. It's just circulation.

---

## What Actually Makes a Combi a Combi

The two things Sean's build can't replicate:

### 1. The plate heat exchanger (DHW isolation)

A combi heats the primary loop to 160-180F, then passes that heat through a flat-plate heat exchanger to make DHW at 120F. The heating water and drinking water never mix. This means:

- Heating loop can run inhibitor chemicals
- Heating loop water stays oxygen-depleted
- DHW gets heated on-demand without the unit needing to switch output temperatures

**Sean's workaround**: the TMV. The Rinnai fires at 140-160F for heating. When you open a tap, the TMV blends the hot output with cold to deliver 120F. This works perfectly. The tradeoff is that during simultaneous DHW + heating calls, the Rinnai is serving both from one heat exchanger at one temperature. The RXP199iN at 199K BTU has more than enough capacity for this (Sean's heating load is ~30K BTU, leaving 169K BTU for DHW).

### 2. The diverter valve (DHW priority)

Combis automatically pause heating and divert all capacity to DHW when someone opens a tap. This guarantees instant, full-capacity hot water. Once the tap closes, heating resumes.

**Sean's workaround**: the zone valve stays open during DHW calls (the Rinnai modulates internally based on flow demand). With 199K BTU of capacity, there's no scenario where DHW and heating compete. The unit can deliver both simultaneously without anyone noticing. True DHW priority switching isn't needed at this capacity-to-load ratio.

---

## Strengths of Sean's Approach

1. **Cost**: $2,100 secondhand RXP199iN + ~$400 in external components vs $4,000-6,000 for a new combi
2. **Repairability**: every external component is individually replaceable. Pump dies? Swap it in 20 minutes with SharkBite fittings. Combi pump dies? Call a tech, order a proprietary part, wait.
3. **Capacity**: 199K BTU is overkill for this unit. A combi at this price point would be 100-150K BTU.
4. **Simplicity of controls**: thermostat calls zone valve, zone valve opens, pump runs, water flows. No proprietary control board to fail.
5. **Parts availability**: SharkBite, Taco, Honeywell, Watts are all Home Depot/Lowes stock. Combi-specific parts are specialty order.
6. **The model exists**: Sean has a 3D installation model showing every fitting, run, and component. Most combi installs don't get this level of planning.

## Weaknesses of Sean's Approach

1. **Annual flush recommended**: fresh potable water through the heating loop means mineral deposits over time. Flush annually.
2. **More external components to install**: pump, expansion tank, zone valve, TMV, check valve all need to be plumbed in. A combi is mostly "hang on wall, connect four pipes."
3. **No inhibitor protection**: can't dose the heating loop with corrosion inhibitor since it's potable water.
4. **Slightly less efficient in heating-only mode**: a combi's closed loop retains heat between cycles. Sean's open loop loses some heat to the cold water sitting in pipes. Marginal difference with good insulation.
5. **No outdoor reset**: a combi adjusts heating water temperature based on outdoor temp (warmer days = lower water temp = less energy). Sean's system fires at a fixed setpoint. Could be addressed with the MCC912 controller if desired.

---

## Bottom Line

Sean is building a combi boiler from parts. The expansion tank and pump are not "what makes it a combi." They're standard hydronic components that both systems need. What makes a combi a combi is the dual heat exchanger and the diverter valve, both of which Sean's system replaces with simpler, equally effective external alternatives (TMV and zone valve).

The open-loop tradeoff is real but manageable. Flush annually, keep an eye on the fan coil, and this system will run for 15-20 years. The Rinnai's heat exchanger warranty is 12 years (residential use). The external components are all commodity parts replaceable in minutes.

It's a combi boiler with the guts on the outside. Same result, more visibility, lower cost, easier to fix.

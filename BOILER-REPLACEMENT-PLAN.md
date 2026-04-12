# Boiler Replacement Plan - Unit 217, 20 Elsie Lane

## Your Situation

Unit 217, 20 Elsie Lane, Junction, Toronto. Failed Enbridge rental unit. Natural gas forced air with hydronic heating (water-to-air heat exchanger in the plenum, fan coil blows air over hot water coils into ductwork). ~1,000 sq ft stacked townhouse.

---

## THE KEY QUESTION: Combi Boiler vs Standard Tankless?

### Short answer: A standard tankless CAN work. But it's not as simple as "just buy a tankless."

Your system needs two things from one heat source:
1. **Domestic hot water** (showers, taps, dishwasher) at 120F
2. **Hydronic space heating** (140-160F water pumped through the fan coil)

A **combi boiler** does both with built-in controls, diverter valve, and circulation pump. One box, plug and play.

A **standard tankless water heater** just heats water on demand. To make it serve the hydronic loop too, you need to add external components: circulation pump, buffer/expansion tank, zone valve, controls, and a thermostatic mixing valve. It works. It's code-legal in Ontario. Manufacturers (Rinnai, Navien) explicitly support this configuration. But you're building a system from parts instead of installing a single appliance.

### What the code says

- **CSA B149.1** (adopted by TSSA for Ontario): does NOT prohibit using a water heater for combination DHW + space heating
- **CSA/ANSI Z21.10.3 / CSA 4.3**: explicitly includes "combination potable water/space heating applications"
- **Rinnai Technical Bulletin TB-043**: Rinnai tankless water heaters "may be used in combination potable water/space heating (open loop) applications"
- **Navien**: sells the H2Air Kit specifically to integrate NPE-A2 tankless with hydronic air handlers
- The heating loop must be **open loop** (potable water flows through the fan coil and back) OR separated by a plate heat exchanger

**Bottom line: 100% legal in Ontario. Not a code issue.**

### Critical requirements if going standard tankless

1. **Minimum 180,000 BTU input** (your 1,000 sq ft needs 25,000-35,000 BTU for heating + 20,000-40,000 for DHW simultaneously = 70,000+ BTU. You want headroom.)
2. **Must be condensing** (95%+ AFUE, vents with PVC, higher efficiency)
3. **Must reach 140-160F output** (most residential tankless cap at 140F by default, but Rinnai and Navien can go to 185F in commercial mode)
4. **Need external circulation pump** for the heating loop (unless you use Navien NPE with H2Air Kit, which uses the built-in pump)
5. **Need expansion tank** on the heating loop
6. **Need thermostatic mixing valve** on DHW side (unit fires at 140-160F for heating, TMV blends it down to 120F for taps)
7. **Need zone valve + thermostat wiring** for heating calls

### What WON'T work: the Rinnai V65iN

The V65iN was in the original research file. **Do NOT buy it for this application.** It's non-condensing (lower efficiency, needs stainless steel venting not PVC), only 150,000 BTU (too small for simultaneous DHW + heating), max 140F (marginal for hydronic), and only 6.5 GPM. Wrong unit for the job.

---

## THE TWO PATHS

### Path A: Standard Tankless from Home Depot (today)

**Best unit: Rinnai RU199iN** (SENSEI SE+)
- 199,000 BTU, 11 GPM, condensing, indoor
- 96% UEF, ENERGY STAR
- Default max 140F, but can reach 185F via commercial mode (DIP switch #6 + MCC-601 controller)
- 15-year heat exchanger warranty (drops to 8 years if run above 160F)
- [Home Depot Canada](https://www.homedepot.ca/product/rinnai-ru199in-super-high-efficiency-plus-condensing-tankless-water-heater-199-000-btu/1001529291): **~$2,400-2,700 CAD** (pricing varies, check store)
- Also at [Lowe's](https://www.lowes.ca/product/tankless-gas-water-heaters/rinnai-11-gpm199-000-btu-natural-gas-tankless-water-heater-330690840) and [RONA](https://www.rona.ca/en/product/rinnai-11-gpm-199-000-btu-natural-gas-tankless-water-heater-ru199in-330690840)

**Other HD options:**
- Rinnai RSC199iN (with built-in pump + valve kit): **~$3,250 CAD** (out of stock at time of search)
- Rinnai RUR199iN (with built-in recirc pump): **~$4,280 CAD** (out of stock)
- Rinnai RU160iN (160K BTU, smaller): ~$3,299 CAD
- Rheem ECOH200DVELN (199K BTU): ~$2,000-2,500 CAD -- **BUT max 140F with NO commercial mode override, so marginal for hydronic**

**Avoid:** Rinnai V65iN (non-condensing, 150K, too small), Rheem 140F-cap models, anything under 180K BTU

**Total cost with Path A:**
- Unit: ~$2,400-2,700
- External components (pump, valves, expansion tank, TMV, controls, etc.): ~$500-1,000
- Venting (PVC): ~$200-350
- Fittings/pipe/consumables: ~$300-500
- Gas fitter: ~$300-600
- **Total: ~$3,700-5,150**

**Pros:** Available today. Cheapest unit cost. Known brand with parts everywhere.
**Cons:** More DIY plumbing/controls work. Building a system from parts. Not what your neighbors installed, so nobody local has done this exact config in your building.

### Path B: Combi Boiler (purpose-built, what your neighbors did)

**Best options:**

| Unit                | Price         | Where                                                                                           | Notes                                             |
| ------------------- | ------------- | ----------------------------------------------------------------------------------------------- | ------------------------------------------------- |
| Rinnai IP120199C    | **$3,474.64** | [Andrew Sheret](https://www.sheret.com/account/catalog/product/2281493)                         | 120K heating/199K DHW, 96% AFUE, 12yr HX warranty |
| Navien NCB-240/110H | **$4,624.42** | [BPH Sales](https://bphsales.ca/products/navien-combi-boiler-ncb-h)                             | 110K heating, built-in pump + buffer, in stock    |
| Navien NCB-240/130H | **$4,757.30** | [BPH Sales](https://bphsales.ca/products/navien-combi-boiler-ncb-h)                             | 130K heating, built-in pump + buffer, in stock    |
| IBC SFC 199         | **$4,393**    | [American Copper & Brass](https://acandb.com/products/natural-gas-28-3-125btu-boiler_sfc-199-1) | Same as neighbor's unit, in stock                 |

**Total cost with Path B:**
- Unit: ~$3,475-4,757
- Venting (PVC): ~$200-350
- Fittings/pipe/consumables: ~$200-400 (less than Path A because pump/controls are built in)
- Gas fitter: ~$300-600
- **Total: ~$4,175-6,100**

**Pros:** One box, integrated controls, what your neighbors did (proven in your building), simpler install, easier for future techs to service.
**Cons:** Can't buy at Home Depot today. Need to order from trade supply.

### THE VERDICT

The savings from going standard tankless vs combi are **~$500-1,000** once you add external components. The combi is simpler to install and proven in your building. But if you need hot water TODAY, the Rinnai RU199iN from Home Depot gets you there.

**If it were my house:** I'd buy the Rinnai RU199iN from Home Depot today, plumb it for DHW only to get hot water back immediately, then add the heating loop components over the next few days. Or order the Rinnai IP120199C from Sheret (call to check stock, might ship same/next day) and do it right the first time.

---

## COMPREHENSIVE PARTS LIST (DIY Install)

This list covers BOTH paths. Items marked **(combi only)** or **(tankless only)** apply to that path.

### 1. The Unit

| Option | Model | BTU | Price | Where |
|--------|-------|-----|-------|-------|
| Standard tankless | Rinnai RU199iN | 199,000 | ~$2,400-2,700 | Home Depot, Lowe's, RONA |
| Combi boiler | Rinnai IP120199C | 120K/199K | $3,474.64 | Andrew Sheret |
| Combi boiler | Navien NCB-240/110H | 110K/199K | $4,624.42 | BPH Sales |
| Combi boiler | IBC SFC 199 | 125K/199K | $4,393 | American Copper & Brass |

### 2. Venting (condensing unit, PVC)

| Part | Spec | Qty | Price (CAD) |
|------|------|-----|-------------|
| Manufacturer vent adapter kit | Rinnai or Navien specific | 1 | $80-120 |
| 2" or 3" PVC Schedule 40 pipe (intake) | 10 ft lengths | 2-3 | $15-20 ea |
| 2" or 3" PVC Schedule 40 pipe (exhaust) | 10 ft lengths | 2-3 | $15-20 ea |
| PVC 90 degree elbows | 2" or 3" | 4-6 | $3-5 ea |
| PVC 45 degree elbows | 2" or 3" | 2-4 | $3-4 ea |
| PVC couplings | 2" or 3" | 4-6 | $2-3 ea |
| Concentric vent termination kit | Manufacturer-specific or universal | 1 | $60-100 |
| PVC cement (medium body) | Oatey or IPS | 1 can | $12-15 |
| PVC primer (purple) | Oatey | 1 can | $8-10 |
| Wall thimble / escutcheon | For exterior wall penetration | 1 | $15-25 |
| Fire caulk / high-temp sealant | 3M or Hilti firestop | 1 tube | $15-25 |

**Subtotal: ~$200-350**

**Important notes on venting:**
- Two-pipe (separate intake + exhaust) is more common in townhouse installs
- Max vent run: ~60 ft equivalent for 2" pipe, ~150 ft for 3" pipe
- Each 90 degree elbow = 5 ft equivalent. Each 45 degree = 2.5 ft equivalent
- Slope horizontal runs 1/4" per foot back toward unit so condensate drains back
- Do NOT vent a condensing unit into an existing chimney (the cool wet exhaust will destroy masonry)

### 3. Water Connections (DHW side)

| Part | Spec | Qty | Price (CAD) |
|------|------|-----|-------------|
| 3/4" braided stainless flex connectors | 18-24" long, 3/4" FIP x FIP | 2 | $15-25 ea |
| 3/4" brass full-port ball valves | Cold inlet + hot outlet isolation | 2 | $12-18 ea |
| 3/4" brass unions | For serviceability | 2 | $10-15 ea |
| 3/4" dielectric unions or brass nipples | If transitioning copper to unit | 2 | $8-12 ea |
| 3/4" copper tee | Branch off cold supply for heating loop | 1 | $5-8 |
| 3/4" copper pipe Type L or M | Short runs near unit, 10 ft lengths | 2 | $40-60 ea |
| 3/4" copper 90 degree elbows | | 6-8 | $2-4 ea |
| 3/4" copper tees | | 2-4 | $3-5 ea |
| Boiler drain valves (hose bib) | For flushing/servicing | 2 | $8-12 ea |

**Subtotal: ~$200-350**

### 4. Heating Loop Piping

| Part | Spec | Qty | Price (CAD) |
|------|------|-----|-------------|
| 3/4" oxygen-barrier PEX tubing | Uponor hePEX or Viega PureFlow (MUST be O2 barrier) | 50-100 ft | $1.50-2.50/ft |
| 3/4" brass full-port ball valves | Heating supply + return isolation | 2 | $12-18 ea |
| 3/4" spring check valve | Heating return (prevents thermosiphon) | 1 | $10-15 |
| 3/4" PEX crimp rings (copper) | If using crimp method | Bag of 25 | $8-12 |
| 3/4" PEX brass insert fittings | Couplings, tees, elbows, adapters | 10-15 | $4-8 ea |
| OR: 3/4" SharkBite push-fit couplings | Alternative to crimp | 6-8 | $12-18 ea |
| OR: 3/4" SharkBite 90 degree elbows | | 4-6 | $15-20 ea |
| OR: 3/4" SharkBite tees | | 2 | $18-22 ea |
| SharkBite disconnect tool | If using SharkBite | 1 | $3-5 |

**CRITICAL: Use oxygen-barrier PEX for the heating loop. Regular PEX lets oxygen permeate into the loop, causing corrosion of the heat exchanger. This is warranty-voiding. Uponor hePEX (red with stripe) or Viega PureFlow are standard.**

**SharkBite vs crimp:** SharkBite is ~$15-20 per fitting vs ~$5 for crimp, but you don't need the crimp tool ($50-80). SharkBite is code-legal in Ontario for accessible locations. Do NOT bury SharkBite behind drywall.

**Subtotal: ~$200-400**

### 5. Isolation Valves (complete list)

| Location | Type | Qty | Price ea |
|----------|------|-----|----------|
| Cold water inlet to unit | 3/4" brass full-port ball valve | 1 | $12-18 |
| Hot water outlet from unit | 3/4" brass full-port ball valve | 1 | $12-18 |
| Heating supply (to fan coil) | 3/4" brass full-port ball valve | 1 | $12-18 |
| Heating return (from fan coil) | 3/4" brass full-port ball valve | 1 | $12-18 |
| TMV hot inlet | 3/4" ball valve | 1 | $12-18 |
| TMV cold inlet | 3/4" ball valve | 1 | $12-18 |

**Subtotal: ~$70-110**

The red-handle ball valves in your neighbor's photos are standard 3/4" brass full-port ball valves. Brand doesn't matter. Watts, Apollo, Webstone, or Home Depot generic all work.

### 6. Expansion Tanks

| Part | Spec | Price (CAD) |
|------|------|-------------|
| Potable water expansion tank | Amtrol ST-5 or Watts PLT-5 (2 gallon) | $45-65 |
| Heating loop expansion tank | Amtrol Extrol 15 (2 gal) | $50-80 |
| 3/4" brass tee (to mount tanks) | | $5-8 ea |

**The grey tank on the floor in your neighbor's photos = the heating loop expansion tank.** Pre-charge pressure must match your incoming water pressure (Toronto is typically 50-70 PSI, most tanks ship at 40 PSI, adjust with a bicycle pump via the Schrader valve).

**Subtotal: ~$100-155**

### 7. Buffer Tank

**For combi boilers (Navien NCB, IBC SFC):** Built-in buffer. Skip this.

**For standard tankless (Rinnai RU199iN):** Start without one. The water volume in your piping + fan coil is usually enough for a 1,000 sq ft unit. If you get short cycling (unit fires and shuts off rapidly), add a 10-20 gallon buffer tank later. A decommissioned 20-gallon electric tank with the element disconnected works (~$250-350) or a purpose-built Caleffi buffer (~$300-500).

**Subtotal: $0 (start without, add if needed)**

### 8. Circulation Pump (tankless only, combi has it built in)

| Option | Model | Flow | Head | Price (CAD) |
|--------|-------|------|------|-------------|
| Budget | Grundfos UP 15-58 FC (bronze, potable-rated) | 0-10 GPM | 0-19 ft | $200-280 |
| Best value | Taco 007e (ECM variable speed, smart) | 0-12 GPM | 0-16 ft | $250-350 |
| Premium | Grundfos Alpha2 26-99 | 0-16 GPM | 0-19 ft | $350-450 |

Your 1,000 sq ft townhouse with a single fan coil needs ~3-5 GPM at 8-12 ft of head. Install on the return line, pushing water toward the unit.

**Subtotal: $0 (combi) or $200-350 (tankless)**

### 9. Thermostatic Mixing Valve

| Part | Spec | Price (CAD) |
|------|------|-------------|
| 3/4" TMV | Watts LFMMVM1-UT or Caleffi 521 MixCal | $80-130 |
| 3/4" check valves for TMV ports | Watts or Apollo | $10-15 ea (x2) |

The TMV goes on the DHW side. Unit fires at 140-160F for the heating loop. TMV blends cold water in to bring DHW down to a safe 120F at the fixtures.

**Subtotal: ~$100-160**

### 10. Check Valves / Backflow Prevention

| Part | Location | Qty | Price |
|------|----------|-----|-------|
| 3/4" spring check valve | Heating return | 1 | $10-15 |
| 3/4" spring check valve | TMV cold inlet | 1 | $10-15 |
| 3/4" spring check valve | TMV hot inlet | 1 | $10-15 |
| Backflow preventer (dual check) | Cold water supply (Toronto code) | 1 | $30-50 |

**Subtotal: ~$60-95**

### 11. Gas Line Components

The gas fitter handles installation. This is what they'll need (let them buy their own if they prefer):

| Part | Spec | Price (CAD) |
|------|------|-------------|
| CSST flexible gas line (yellow) | 3/4" Gastite or TracPipe, 10-25 ft | $80-150 |
| CSST fittings | Male adapter, tee | $20-40 ea |
| Gas shutoff valve (CSA approved) | 3/4" lever-handle gas ball valve | $20-35 |
| Gas sediment trap (drip leg) | 3/4" x 3" nipple + cap | $8-12 |
| Yellow gas-rated Teflon tape | | $5-10 |
| Gas leak detection solution | Spray bottle | $8-12 |

**IMPORTANT: The Navien NCB-240E / Rinnai RU199iN requires 3/4" gas supply at minimum 7" WC. The gas fitter must verify your meter and supply line can handle 199,000 BTU. If the existing line is 1/2", it may need upsizing.**

**Subtotal: ~$200-400 (often included in gas fitter's quote)**

### 12. Electrical

| Part | Spec | Price (CAD) |
|------|------|-------------|
| Dedicated 120V/15A circuit | From panel to unit location | $150-300 (if new circuit needed) |
| 120V GFCI outlet or GFCI breaker | Near unit | $20-40 |
| 14/2 NMD90 cable (Romex) | If running new circuit, 25-50 ft | $30-50 |
| Single gang box + cover plate | | $5-10 |
| UPS / surge protector (recommended) | Protects control board | $30-60 |

The unit draws ~100-120W and plugs into a standard 120V outlet (comes with a cord). Code requires a dedicated circuit. Ontario ESC: you can do this yourself as homeowner but need ESA inspection.

**Subtotal: ~$80-400**

### 13. Mounting Hardware

| Part | Spec | Price (CAD) |
|------|------|-------------|
| Wall mount bracket | Included with unit | $0 |
| Concrete/masonry anchors | 3/8" x 3" Tapcon screws (if concrete wall) | $12-18 |
| Toggle bolts | If drywall (find studs instead) | $8-15 |
| Unistrut channel 12-24" | If creating a mounting frame | $15-25 |
| P-clamps / pipe clamps | Securing pipes to wall | $2-4 ea (x10-15) |
| Copper pipe hangers / bell hangers | Supporting horizontal copper runs | $2-3 ea (x6-10) |

Unit weighs ~80 lbs filled. Mount to studs or concrete.

**Subtotal: ~$50-100**

### 14. Consumables

| Part | Spec | Price (CAD) |
|------|------|-------------|
| Lead-free solder | 1/2 lb roll, 95/5 tin-antimony or Oatey Safe-Flo | $15-20 |
| Soldering flux (water-soluble, lead-free) | Oatey No. 95 | $8-12 |
| White/pink Teflon tape (for water) | Thread seal | $3-5 |
| Pipe dope / thread sealant | Rectorseal T Plus 2, or Megaloc | $8-12 |
| Emery cloth / sandpaper (120 grit) | Cleaning copper before soldering | $5-8 |
| Flux brush | Small acid brush | $2-3 |
| Fire cloth / heat shield | Protect wall while soldering | $8-12 |

**Subtotal: ~$55-80**

### 15. Pipe Insulation

| Part | Spec | Qty | Price (CAD) |
|------|------|-----|-------------|
| 3/4" foam pipe insulation | Armaflex or generic, 6 ft sticks | 8-12 sticks | $3-5 ea |
| Insulation tape | Self-adhesive foam tape for joints | 1 roll | $5-8 |

Insulate ALL hot water pipes, both DHW and heating loop.

**Subtotal: ~$40-75**

### 16. Condensate Drain (condensing units produce acidic condensate)

| Part | Spec | Price (CAD) |
|------|------|-------------|
| 1/2" or 3/4" PVC drain line | From unit to floor drain | $5-10 |
| PVC fittings | Elbows, couplings for routing | $5-10 |
| Condensate neutralizer kit | Manufacturer kit, or DIY with marble chips in PVC tube | $30-60 |
| Condensate pump (if no floor drain nearby) | Little Giant VCMA-15 or similar | $80-120 |

**Ontario code requires condensate neutralization.** You can't dump acidic condensate straight into the drain. If you have a floor drain nearby (you do, visible in the photos): gravity drain through the neutralizer, no pump needed.

**Subtotal: ~$40-80 (with floor drain) or $120-200 (without)**

### 17. Thermostat / Controls

| Part | Spec | Price (CAD) |
|------|------|-------------|
| Standard 24V thermostat | Honeywell T6 Pro, Ecobee, or Nest (may reuse existing) | $0-300 |
| Thermostat wire (18/2 or 18/5) | From thermostat to unit/zone valve | $15-30 |
| Zone valve / actuator | Honeywell V8043E or Taco 571-2 (normally closed, 2-way) | $80-120 |
| End switch relay (if zone valve needs it) | Signals boiler to fire on heat call | $20-30 |
| MCC-601 commercial controller **(tankless only)** | To unlock 160F+ output on Rinnai | $100-150 |

**How heating calls work:** Thermostat calls for heat --> 24V signal to zone valve --> valve opens --> end switch closes --> signals unit to fire in space heating mode --> pump runs --> hot water flows through fan coil --> blower pushes warm air into ducts.

Combi boilers have thermostat terminals built in and can accept a direct 24V heat call.

**Subtotal: ~$200-500**

### 18. Fan Coil Unit (Hydronic Air Handler)

This is the galvanized metal box in the plenum visible in your neighbor's photos.

**You almost certainly DO NOT need to buy a new one.** The existing fan coil from the previous system should be compatible. Check that it:
- Has correct BTU rating (30,000-50,000 BTU for your space)
- Has 3/4" water connections
- Blower works

If you DO need a new one:
| Part | Spec | Price (CAD) |
|------|------|-------------|
| Hydronic fan coil | First Company AquaTherm 36HX or similar, 2-ton / 40,000+ BTU | $800-1,400 |
| Plenum adapter | Sheet metal transition to existing ductwork | $50-100 |
| Foil tape (NOT fabric duct tape) | Sealing duct connections | $10-15 |
| Mastic / duct sealant | Airtight connections | $10-15 |

**Subtotal: $0 (reusing) or $900-1,600 (new)**

---

## GRAND TOTAL: PARTS

### Path A: Standard Tankless (Rinnai RU199iN from Home Depot)

| Category | Low | High |
|----------|-----|------|
| Tankless unit | $2,400 | $2,700 |
| Venting | $200 | $350 |
| DHW water connections | $200 | $350 |
| Heating loop piping | $200 | $400 |
| Isolation valves | $70 | $110 |
| Expansion tanks | $100 | $155 |
| Circulation pump | $200 | $350 |
| TMV | $100 | $160 |
| Check valves / backflow | $60 | $95 |
| Gas line (fitter may supply) | $0 | $400 |
| Electrical | $80 | $400 |
| Mounting | $50 | $100 |
| Consumables | $55 | $80 |
| Pipe insulation | $40 | $75 |
| Condensate drain | $40 | $80 |
| Controls + MCC-601 | $300 | $650 |
| Fan coil | $0 | $0 |
| **TOTAL (parts)** | **$4,095** | **$6,455** |
| Gas fitter | $300 | $600 |
| **GRAND TOTAL** | **$4,395** | **$7,055** |

### Path B: Combi Boiler (Rinnai IP120199C or Navien NCB)

| Category | Low | High |
|----------|-----|------|
| Combi boiler unit | $3,475 | $4,757 |
| Venting | $200 | $350 |
| DHW water connections | $200 | $350 |
| Heating loop piping | $200 | $400 |
| Isolation valves | $70 | $110 |
| Expansion tanks | $100 | $155 |
| Circulation pump | $0 | $0 |
| TMV | $100 | $160 |
| Check valves / backflow | $60 | $95 |
| Gas line (fitter may supply) | $0 | $400 |
| Electrical | $80 | $400 |
| Mounting | $50 | $100 |
| Consumables | $55 | $80 |
| Pipe insulation | $40 | $75 |
| Condensate drain | $40 | $80 |
| Controls | $100 | $350 |
| Fan coil | $0 | $0 |
| **TOTAL (parts)** | **$4,770** | **$7,862** |
| Gas fitter | $300 | $600 |
| **GRAND TOTAL** | **$5,070** | **$8,462** |

**Realistic middle estimate (reusing fan coil, basic controls):**
- Path A (standard tankless): **~$4,500-5,500**
- Path B (combi boiler): **~$5,000-6,000**

---

## COMPREHENSIVE TOOLS LIST

### Essential Tools (must have)

| Tool | What It's For | Buy Price (CAD) |
|------|---------------|-----------------|
| Copper tube cutter (3/4" and 1/2") | Cutting copper pipe cleanly | $15-30 |
| PEX cutter (ratcheting) | Cutting PEX tubing | $15-25 |
| PEX crimp tool (3/4") | Crimping copper rings onto PEX (skip if using SharkBite) | $50-80 buy / $20-30/day rent |
| PEX crimp gauge (go/no-go) | Verifying crimps | $10-15 |
| MAPP gas torch or propane torch | Soldering copper joints | $30-50 (with cylinder) |
| Adjustable wrenches x2 (10" + 12") | Tightening fittings | $15-25 ea |
| Channel lock pliers x2 (10" + 12") | Gripping pipes and fittings | $15-25 ea |
| Pipe wrenches x2 (12" + 14") | Threaded pipe connections | $20-35 ea |
| Cordless drill / impact driver | Mounting bracket, drilling holes | $100-200 (if you don't own one) |
| Masonry drill bits (3/16", 1/4", 3/8") | Drilling concrete for Tapcons | $10-20 |
| Hole saw kit (2", 3", 4") | Cutting wall penetrations for venting | $25-50 |
| Level (24" torpedo or laser) | Ensuring unit and pipes are level | $10-30 |
| Tape measure | Everything | $10-15 |
| Hacksaw or reciprocating saw | Cutting PVC, removing old pipe | $15-40 |
| Deburring tool / reamer | Removing burrs from cut pipe | $8-15 |
| Bucket and rags | Catching water when cutting into lines | $5-10 |
| Headlamp or work light | Seeing inside plenum/closet | $15-30 |
| Wire strippers / crimpers | Thermostat wiring | $10-15 |
| Multimeter | Testing voltage, thermostat wiring | $20-40 |
| Fire extinguisher (ABC type) | Safety when soldering | $30-50 |
| Safety glasses | Soldering, drilling, cutting | $5-10 |
| Work gloves | Sharp sheet metal, hot pipes | $10-15 |

### Rental-worthy specialty tools

| Tool | What It's For | Rental Cost |
|------|---------------|-------------|
| SDS hammer drill | Drilling through concrete for venting | $30-50/day |
| Core drill | Large hole through masonry for vent termination | $50-80/day |
| PEX expansion tool (Milwaukee ProPEX) | If using Uponor expansion PEX instead of crimp | $40-60/day |

**Tool total if buying from scratch: ~$400-700**
**Tool total if you have basic hand tools + drill: ~$100-200**

---

## STEP-BY-STEP INSTALLATION SEQUENCE

### Phase 0: Planning and Prep (before buying)

1. **Photograph everything.** The existing unit, piping, venting, gas line, electrical, fan coil, ductwork connections. You'll reference these constantly.
2. **Measure the vent run.** From proposed unit location to exterior wall. Count elbows. Calculate total equivalent length. Verify it's within max vent length for your pipe diameter.
3. **Measure the gas line.** From meter to unit location. Note pipe size. Gas fitter needs this. If existing line is 1/2", it may need upsizing to 3/4" for 199K BTU.
4. **Verify electrical.** Is there a 120V outlet near the install location? Is it on a dedicated circuit?
5. **Inspect the existing fan coil.** Model number, BTU rating, pipe connection sizes. Verify compatibility.
6. **Check floor drain location** for condensate drainage.
7. **Read the installation manual** for your chosen unit. Available as PDF on manufacturer's website. Read it cover to cover. It has clearance requirements, venting specs, piping diagrams.
8. **Get permits.** In Toronto you need:
   - Plumbing permit (water connections)
   - Mechanical permit (heating system)
   - Gas permit (gas fitter pulls this)
   - Homeowner CAN pull plumbing and mechanical permits for own residence in Ontario
   - Call 311 or check toronto.ca/building-permits
9. **Schedule the gas fitter.** Tell them you'll have everything installed and ready for gas hookup. Ask what they want to see when they arrive.

### Phase 1: Removal of Old Unit (half day)

**You do all of this:**

1. Turn off gas to existing unit at gas shutoff valve
2. Turn off water supply (isolation valves or main shutoff)
3. Turn off electrical (breaker or unplug)
4. Drain the old tank: garden hose to drain valve, run to floor drain or outside. Open hot water tap upstairs to break vacuum. Takes 30-60 min.
5. Disconnect water lines. Have buckets ready. Cut copper if needed.
6. Disconnect vent pipe from old unit.
7. **Gas line disconnect: if ANY doubt about gas being fully off, LEAVE THIS FOR THE GAS FITTER.** If confident gas valve is shut, disconnect flex connector, cap the gas line with brass cap + pipe dope immediately.
8. Remove old unit. 100+ lbs empty. Get a helper + hand truck.
9. Clean wall, patch holes, identify where new unit mounts.

### Phase 2: Mounting and Venting (half to full day)

**You do all of this:**

1. Mount the bracket using manufacturer's template. Level it. Drill into studs or concrete.
   - Typical clearances: 12" top, 6" sides, 12" bottom (check your manual)
2. Hang unit on bracket. Get a helper -- 80 lbs.
3. Plan vent route. Mark wall penetration. **Key Ontario clearances:**
   - 12" above grade
   - 6" from inside corners
   - 12" below eaves/soffits
   - 3 ft from forced air inlet
   - 4 ft below / 1 ft above any window or door that opens
4. Cut wall penetration with hole saw or core drill
5. Run PVC vent pipes. Dry-fit first, then prime and cement. Support every 4 ft with hangers. Slope horizontal runs 1/4" per foot back toward unit.
6. Install vent termination on exterior. Seal around penetration.
7. Connect vent pipes to unit's vent adapter.

### Phase 3: Water Piping - DHW Side (half day)

**You do all of this:**

1. Install cold water isolation valve on supply line
2. Install expansion tank on cold line (tee off, tank pointing down or horizontal, never upside down)
3. Run cold water supply to unit's cold inlet
4. Install hot water outlet isolation valve
5. Install thermostatic mixing valve:
   - Hot inlet: from unit's hot outlet
   - Cold inlet: branch from cold supply (before unit)
   - Mixed outlet: to house's hot water distribution
6. Install check valves on both TMV inlets
7. Connect mixed outlet to house hot water piping
8. Install boiler drain valves (hose bibs) on cold inlet and hot outlet for flushing
9. Solder all copper joints. Clean, flux, heat, solder. Wipe excess flux.

### Phase 4: Water Piping - Heating Loop (half day)

**You do all of this:**

1. Run supply line from unit's heating supply port to fan coil inlet. Copper near unit, oxygen-barrier PEX for longer runs.
2. Run return line from fan coil outlet back to unit's heating return port.
3. Install isolation ball valves on both supply and return near fan coil
4. Install check valve on return line (prevents thermosiphon)
5. Install heating loop expansion tank on return line near unit
6. **(Standard tankless only):** Install external circulation pump on return line, pushing toward unit. Isolation valves on both sides.
7. Install zone valve on supply line to fan coil. Wire to thermostat circuit.
8. Connect fan coil to existing ductwork. Sheet metal screws + foil tape / mastic. Check airflow direction arrow.

### Phase 5: Condensate Drain

1. Run PVC from unit's condensate port to neutralizer
2. Install condensate neutralizer (manufacturer kit or DIY marble chip tube)
3. Run PVC from neutralizer to floor drain

### Phase 6: Electrical and Controls

1. Install/verify 120V dedicated outlet
2. Wire thermostat to zone valve and/or unit's thermostat terminals
3. **(Standard tankless):** Install MCC-601 controller for 160F+ access
4. Plug in unit

### Phase 7: Fill, Purge, and Pressure Test (CRITICAL)

1. Close all drain valves
2. Open cold water isolation valve slowly. Let system fill. Open hot tap upstairs to bleed air.
3. For heating loop: open fill valve, let water flow through loop, open air bleed valves on fan coil, run until no air bubbles (10-15 min)
4. **Check EVERY SINGLE JOINT for leaks.** Paper towels at each joint. Even a slow drip will show.
5. Pressure test: close all valves, watch pressure gauge. Should hold steady (12-20 PSI for heating loop) for 30+ minutes without dropping. If it drops, you have a leak.
6. Verify expansion tank pressure matches fill pressure
7. Check condensate drain with water pour test

### Phase 8: Gas Connection and Commissioning (GAS FITTER)

**Gas fitter does ALL of this (typically 2-4 hours, $300-600):**

1. Connects gas supply line to unit
2. Installs sediment trap (drip leg)
3. Leak tests all gas connections
4. Pressurizes gas line, verifies no drop
5. Opens gas valve and fires unit
6. Combustion analysis (CO levels, flue gas temp, gas pressure)
7. Adjusts gas pressure if needed
8. Verifies proper venting
9. Runs through unit's setup menu (DHW temp, heating temp, pump speed)
10. Tests DHW operation at multiple fixtures
11. Tests heating operation (thermostat call, fan coil produces warm air)
12. Checks for error codes
13. Fills out TSSA paperwork
14. Briefs you on operation, error codes, maintenance schedule

### Phase 9: Insulation and Cleanup

1. Insulate all hot water pipes (DHW + heating loop)
2. Label all valves with Sharpie or adhesive labels
3. Photograph the completed installation
4. Clean up. Vacuum copper shavings, wipe flux residue.
5. **Register the warranty online within 30 days**

---

## KEY WARNINGS

1. **Do NOT skip the condensate neutralizer.** Inspectors check. Acidic condensate corrodes copper drains.
2. **Do NOT use regular PEX on the heating loop.** Oxygen-barrier PEX only. Regular PEX = heat exchanger corrosion in 2-5 years. Warranty void.
3. **Do NOT vent into an existing chimney.** Condensing exhaust is cool and wet. It'll destroy masonry.
4. **The unit requires minimum flow rate to fire.** If the circ pump is too weak or loop too restrictive, it won't fire for heating.
5. **Air in the heating loop = no heat.** Purge thoroughly. Install auto air vent at highest point.
6. **Freeze protection:** Navien/Rinnai have internal freeze protection for the unit only. Not external pipes. If pipes run through unheated spaces, insulate heavily and consider heat trace cable.
7. **Pull permits.** Toronto building inspectors do random audits. Unpermitted work surfaces at home inspection when selling.
8. **The gas fitter may have opinions about your piping.** Listen. They see dozens of these installs. Good ones will catch problems.
9. **Annual maintenance:** Descale with vinegar flush pump once per year. Budget ~$150-250 for a descaling pump kit (or DIY with a small utility pump + white vinegar).

---

## WHERE TO BUY IN TORONTO

| Store | Best For | Notes |
|-------|----------|-------|
| **Home Depot** | Rinnai RU199iN, basic fittings, PVC, copper, SharkBite, expansion tanks, valves, tools | Can buy the unit today |
| **Lowe's / RONA** | Same Rinnai models, some different tool selection | Check stock |
| **Andrew Sheret** | Rinnai IP120199C combi boiler ($3,474.64) | Trade supply, call 1-888-970-2709 |
| **BPH Sales** | Navien NCB-H combi boilers ($4,378-5,182) | Online, in stock |
| **Marks Supply / Wolseley** | IBC SFC 199, wholesale pricing | Open a trade account with your business license |
| **DigelAir** | IBC boilers, Ontario wholesale | Need trade account |
| **American Copper & Brass** | IBC SFC 199 ($4,393, in stock) | Online, ships to Canada |
| **Home Hardware** | Surprisingly good plumbing parts selection, reasonable prices | |
| **Amazon.ca** | Grundfos/Taco pumps, TMVs, specialty parts | Watch for counterfeit SharkBite |

---

## WHAT YOUR NEIGHBORS INSTALLED (Photo Analysis)

### Install #1: Rinnai Empower (photos 577/579 series)
- Wall-mounted Rinnai Empower combi unit
- Galvanized metal box below = hydronic fan coil / air handler
- Copper + PEX piping with SharkBite push-fit connectors
- Ball valves with red handles
- PVC venting out top
- Label reads "THIS UNIT IS BEING SE... EMPOWER HOME COM..."

### Install #2: IBC SFC 199 (photos 506 series - invoices)
- Atomic Air estimate for Unit 112 at 30 Elsie Lane (Matthew Downey)
- IBC SFC 199 Tankless Combi Boiler - $9,000 + HST = $10,170 installed (Jan 2023)
- Full scope: decommission, install, heating piping, DHW connections, venting, gas calibration, CSA B149.1 compliance
- Previous unit was a Reliance rental

### Install #3: Unknown brand tankless (photos 474/475 series)
- BEFORE: GSW/Rheem PDV (Power Direct Vent) tank-style water heater, ~40-50 gallon
- AFTER: Wall-mounted white tankless (EnergyGuide sticker, possibly Navien or Eternal)
- Grey expansion tank on floor
- Diamond-mesh visible = hydronic heat exchanger coil

---

## ENBRIDGE RENTAL RETURN

- Call the number on your Enbridge bill, schedule curbside pickup ($75-200)
- Or drop off at the Lesmill Rd location (GTA)

---

## Sources

- [Rinnai RU199iN - Home Depot Canada](https://www.homedepot.ca/product/rinnai-ru199in-super-high-efficiency-plus-condensing-tankless-water-heater-199-000-btu/1001529291)
- [Rinnai TB-043: Space Heating Applications](https://media.rinnai.us/salsify_asset/s-b3633f2d-3e82-4f6b-acdb-fb2c7f909b1a/TB-043%20Space%20Heating%20Applications.pdf)
- [Navien H2Air Kit](https://www.navieninc.com/accessories/h2air)
- [Navien NPE-A2 Series](https://www.navieninc.com/series/npe-a2)
- [IBC SFC 199 - American Copper & Brass](https://acandb.com/products/natural-gas-28-3-125btu-boiler_sfc-199-1)
- [Rinnai IP120199C - Andrew Sheret](https://www.sheret.com/account/catalog/product/2281493)
- [Navien NCB-H Series - BPH Sales](https://bphsales.ca/products/navien-combi-boiler-ncb-h)
- [HVAC Ontario - Rinnai Combi Sale](https://www.hvacontario.ca/buy-rinnai-combi-tankless-boiler)
- [Atomic Air - HomeStars Reviews](https://www.homestars.com/companies/2977624-atomic-air)
- [Hoerner Heating - IBC Boilers](https://www.hoerner.ca/brand/ibc-boilers/)
- [Energy Vanguard: Hydronic Furnace + Tankless](https://www.energyvanguard.com/blog/hydronic-furnace-tankless-water-heater-a-great-combo/)
- [Building America: Integrated Heating + Hot Water](https://basc.pnnl.gov/resource-guides/integrated-heating-and-hot-water-tankless-gas-or-electric-water-heating)
- [CSA B214: Hydronic Heating Systems](https://www.csagroup.org/store/product/b214-21/)
- [Rinnai RU199iN at Lowe's Canada](https://www.lowes.ca/product/tankless-gas-water-heaters/rinnai-11-gpm199-000-btu-natural-gas-tankless-water-heater-330690840)
- [Rinnai RU199iN at RONA](https://www.rona.ca/en/product/rinnai-11-gpm-199-000-btu-natural-gas-tankless-water-heater-ru199in-330690840)
- [Navien NCB Combi-Boilers](https://www.navieninc.ca/residential/combi-boilers)

---

*Last updated: 2026-04-11*

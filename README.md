# Forcair

**The open-source robot that cleans your patio while you relax.**

<!-- TODO: replace with generated banner image -->
<!-- ![Forcair Banner](docs/branding/banner.png) -->

Forcair is a low-cost, open-source autonomous robot that removes moss and weeds from paved surfaces using a rotating brush and computer vision.

Built with aluminum extrusion profiles, 3D printed parts, and an ESP32-CAM. Under 1.3 kg. Under 100 EUR.

> Named after a vehicle from [*Jayce and the Wheeled Warriors*](https://en.wikipedia.org/wiki/Jayce_and_the_Wheeled_Warriors) (1985).

![Concept](specs/concept-forcair-v1.jpg)

---

## The Problem

Interlocking pavers and stone patios accumulate **moss and weeds** in their joints. Existing solutions:

| Solution | Cost | Effort | Eco-friendly |
|----------|------|--------|--------------|
| Manual scraping | 0 EUR | Hours on your knees | Yes |
| Pressure washer | 200+ EUR | Heavy, damages joints | Wastes water |
| Chemical herbicide | 10 EUR/year | Easy | **No** |
| Commercial robot mower | 1000+ EUR | N/A on pavers | N/A |
| **Forcair** | **~75 EUR** | **Autonomous** | **Yes** |

## How It Works

```
  1. DETECT            2. NAVIGATE           3. CLEAN
  ESP32-CAM sees      Bump & turn on        Rotating brush
  green moss on       paved surface         scrubs joints
  gray pavers         (Tertill-style)       automatically
  (HSV threshold)     (~30m2 coverage)      (nylon or steel)
```

The robot patrols your patio autonomously. When the camera detects green moss (computer vision, no cloud), it lowers a rotating brush and scrubs the joint clean. Simple, mechanical, effective.

## Specifications

| Parameter | Value |
|-----------|-------|
| Dimensions | 300 x 250 x 100 mm |
| Weight | ~1.3 kg |
| Frame | Aluminum 2020 extrusion profiles |
| Wheels | 4x 80mm (PETG hub + TPU tire), 4WD |
| Brain | ESP32-CAM (camera + WiFi + GPIO) |
| Motor driver | TB6612FNG (dual H-bridge, MOSFET) |
| Brush | Rotary nylon or steel wire, 50mm, on Z-axis |
| Battery | 3S 18650 pack (11.1V), ~1h15 autonomy |
| Navigation | Bump & turn + IR obstacle + cliff sensors |
| Detection | HSV green-on-gray thresholding (inspired by [OWL](https://github.com/geezacoleman/OpenWeedLocator)) |
| Manufacturing | 3D printing (Bambu Lab X1C) + off-the-shelf parts |
| **Total cost** | **~75 EUR** (including shared hardware order) |

## Project Status

| Phase | Status | Description |
|-------|--------|-------------|
| **Phase 0** | **In progress** | Manual brush testing (drill + brush on pavers) |
| Phase 1 | Planned | Wheeled base + ESP32-CAM scout + remote control |
| Phase 1.5 | Planned | Autonomous bump & turn + brush on detected moss |
| Phase 2 | Future | RPi Zero 2W + SLAM + GPS logging + smart navigation |

## Build Your Own

### Bill of Materials (BOM)

| Part | Source | Cost |
|------|--------|------|
| 4x 2020 profiles (300+250mm) | Motedis or similar | ~8 EUR |
| 4x corner brackets + T-nuts | Motedis | ~5 EUR |
| Plywood platform 5mm | Hardware store | ~3 EUR |
| 4x wheels (PETG hub + TPU tire) | 3D printed | ~4 EUR filament |
| 4x 608ZZ bearings | AliExpress | ~3 EUR |
| 4x shaft couplers | AliExpress | ~2 EUR |
| 4x DC motors (traction) | Reclaimed from printers | 0 EUR* |
| Brush motor (12V DC) | Reclaimed or ~5 EUR | 0-5 EUR |
| Nylon brush (drill attachment) | Hardware store | ~5 EUR |
| Steel wire brush (drill attachment) | Hardware store | ~5 EUR |
| ESP32-CAM | AliExpress | ~5 EUR |
| TB6612FNG motor driver | AliExpress | ~3 EUR |
| 2x Sharp GP2Y0A21 IR sensors | AliExpress | ~2 EUR |
| 2x micro-switch bumpers | AliExpress or reclaimed | ~1 EUR |
| 2x TCRT5000 cliff sensors | AliExpress | ~0.50 EUR |
| Piezo buzzer | AliExpress | ~0.30 EUR |
| 3S 18650 battery pack | Reclaimed or ~15 EUR | 0-15 EUR |
| SG90 servo (Z-axis) | AliExpress | ~2 EUR |
| 3D printed parts (~21 pieces) | PETG + TPU filament | ~10 EUR |
| Waterproofing (seals, grommets) | Hardware store | ~3 EUR |
| **TOTAL** | | **~50-75 EUR** |

*Reclaimed DC motors from old inkjet printers work great. Fallback: 4x N20 200RPM motors (~10 EUR on AliExpress).*

### CAD Files

All mechanical parts are parametric, written in [CadQuery](https://cadquery.readthedocs.io/) (Python).
STEP and STL exports are provided for direct slicing.

```
hardware/cad/
├── assembly_chassis.py      # Full assembly visualization
├── wheel_hub.py             # PETG wheel hub (WH-001)
├── wheel_tire.py            # TPU tire (WT-001)
├── motor_mount.py           # Motor cradle for 2020 profile
├── ims_plate.py             # Interchangeable Module Standard plate
├── mod002_brosse.py         # Rotating brush module (MOD-002)
├── esp32_cam_mount.py       # ESP32-CAM bracket with tilt
├── capot_dome.py            # Protective dome (PETG translucent blue)
├── step/                    # STEP exports
└── stl/                     # STL exports (ready to print)
```

### Printing Guide

| Part | Material | Infill | Layer | Time |
|------|----------|--------|-------|------|
| Wheel hubs (x4) | PETG | 100% | 0.2mm | ~1h each |
| Tires (x4) | TPU 95A | 100% | 0.2mm | ~45min each |
| Motor mounts (x4) | PETG | 80% | 0.2mm | ~30min each |
| Dome cover | PETG (translucent blue) | 20% | 0.2mm | ~3h |
| All other parts | PETG | 50% | 0.2mm | varies |
| **Total Phase 1** | | | | **~12-13h** |

## Research & State of the Art

See [`research/state-of-the-art.md`](research/state-of-the-art.md) for a comprehensive literature review covering:

- 12+ similar DIY/open-source projects analyzed
- 24 scientific papers reviewed
- Validation of the rotating brush approach on hard surfaces ([Rask & Kristoffersen 2007](https://doi.org/10.1111/j.1365-3180.2007.00579.x))
- Identified gap: **no published work on autonomous robotic weeding for domestic paved surfaces**

Key references:
- [OpenWeedLocator (OWL)](https://github.com/geezacoleman/OpenWeedLocator) - green-on-brown detection algorithm we adapt to green-on-gray
- [Tertill](https://tertill.com/) (discontinued) - bump & turn navigation validated for small surfaces
- [LIAM-ESP](https://github.com/trycoon/liam-esp) - ESP32 navigation code reference

## Modular Tool System (IMS)

Forcair uses an **Interchangeable Module Standard** (IMS) interface:

```
     ┌──── IMS Plate (100x80mm) ────┐
     │  2x M5 butterfly bolts       │  ← tool-free swap in 30 seconds
     │  2x centering posts (8mm)    │
     │  XT60 connector (12V, 10A)   │
     │  JST-XH 3-pin (PWM signal)  │
     └──────────────────────────────┘
```

| Module | Function | Status |
|--------|----------|--------|
| MOD-002 | Rotating brush (nylon/steel) | Phase 1.5 |
| MOD-001 | Camera scout (GoPro) | Phase 2 |
| MOD-003 | Spray (water or anti-moss) | Future |
| MOD-004 | Leaf blower | Future |

Design your own module! The IMS plate CAD file is in `hardware/cad/ims_plate.py`.

## Architecture

```
Phase 1-1.5 (ESP32-CAM only):

  ┌─────────────┐    WiFi     ┌──────────────┐
  │  ESP32-CAM  │◄───────────►│   Smartphone  │
  │  OV2640 cam │             │  (monitoring) │
  │  HSV detect │             └──────────────┘
  │  GPIO ctrl  │
  └──┬───┬──┬───┘
     │   │  └──── 2x IR Sharp + 2x bumper + 2x cliff + buzzer
     │   └─────── SG90 servo (Z-axis)
     └─────────── TB6612FNG → 4x DC motors + brush motor (MOSFET)
```

## Contributing

Contributions welcome! Here's how you can help:

- **Build one** and share your results (especially with different paver types)
- **Improve the firmware** (ESP32 Arduino or ESP-IDF)
- **Design new modules** for the IMS interface
- **Test different brushes** and document effectiveness vs. joint wear
- **Translate** documentation
- **Report issues** or suggest improvements

## License

- **Hardware** (CAD, mechanical design): [CERN-OHL-S v2](LICENSE-HARDWARE)
- **Software** (firmware, scripts): [MIT](LICENSE-SOFTWARE)
- **Documentation**: [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

## Related Projects

Forcair is part of a family of DIY projects, all named after vehicles from *Jayce and the Wheeled Warriors*:

| Project | Description |
|---------|-------------|
| **Forcair** | Autonomous paver weeding robot (this project) |
| Vrillair | DIY CNC machine |
| Blindair | Modular workshop storage boxes |
| Depistair | Reclaimed parts inventory & shared BOM |

## Acknowledgments

- [OpenWeedLocator](https://github.com/geezacoleman/OpenWeedLocator) for the green-on-brown detection approach
- [Tertill](https://tertill.com/) (Franklin Robotics) for proving bump & turn works
- [LIAM-ESP](https://github.com/trycoon/liam-esp) for ESP32 navigation patterns
- The scientific work of Rask & Kristoffersen (2007) and Cauwer et al. (2014) on non-chemical weed control on hard surfaces

---

*Forcair is a personal open-source project. Not affiliated with any company.*

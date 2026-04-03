# Hackaday.io - Page Projet Forcair (brouillon)

> Ce fichier sert de brouillon pour creer la page projet sur hackaday.io.
> Copier-coller les sections dans le formulaire Hackaday.

## Infos projet

- **Titre** : Forcair - Open-Source Autonomous Paver Weeding Robot
- **URL souhaitee** : hackaday.io/project/XXXXX-forcair
- **Tagline** : A <100 EUR robot that cleans moss from your patio autonomously
- **Statut** : Work in progress

## Tags

`robot`, `esp32`, `esp32-cam`, `weeding`, `3d-printing`, `open-hardware`,
`autonomous`, `opencv`, `cadquery`, `aluminum-extrusion`, `diy`,
`garden-robot`, `paver`, `moss`, `outdoor`, `bump-and-turn`

## Description (Project Details)

### What is Forcair?

Forcair is a small (300x250x100mm, 1.3kg) autonomous robot that patrols
your paver patio and removes moss and weeds from the joints using a
rotating brush. It sees green moss on gray pavers using an ESP32-CAM
(computer vision), navigates with bump & turn (like a Roomba), and costs
under 100 EUR to build.

### Why?

Every spring, moss creeps back between your pavers. You can:
- Spend hours on your knees scraping joints
- Blast with a pressure washer (damages joints, wastes water)
- Spray herbicide (bad for the environment)
- Or let a small robot handle it autonomously

Existing robot mowers work on grass, not pavers. Commercial solutions
don't exist for this niche. So I'm building one.

### How?

- **Frame**: Aluminum 2020 extrusion profiles (Motedis)
- **Wheels**: 4x 80mm, 3D printed (PETG hub + TPU tire)
- **Brain**: ESP32-CAM (camera + WiFi + control, all-in-one)
- **Vision**: HSV green-on-gray detection (inspired by OpenWeedLocator)
- **Navigation**: Bump & turn (IR sensors + bumpers + cliff sensors)
- **Brush**: Rotary nylon or steel wire, on a Z-axis with spring pressure
- **Power**: 3S 18650 battery, ~1h15 autonomy
- **Modular**: Interchangeable tool system (IMS) for future attachments

Everything is open-source: hardware (CERN-OHL-S v2), software (MIT),
CAD files in parametric CadQuery (Python), STL/STEP exports included.

### What makes this different?

I did a full literature review (24 papers, 12+ similar projects). Key finding:
**no one has published an autonomous robotic weeding solution for domestic
paved surfaces**. Agricultural weeding robots exist. Manual paver cleaning
methods are studied. But the intersection is empty.

Forcair fills this gap.

### State of the art

The rotating brush approach is validated by scientific literature:
- Rask & Kristoffersen (2007): brushing is the most effective non-chemical
  method on hard surfaces, 4-6 passes per year are sufficient
- Cauwer et al. (2014): specifically tested on interlocking concrete pavers
- ESP32-CAM can run CNN inference in 7.6ms (Flores et al. 2024)

Full references: see the research/ folder on GitHub.

## Images

1. Concept render (specs/concept-forcair-v1.jpg) - hero image
2. Terrain photos (specs/photos/) - the problem in context
3. Phase 0 results (docs/hackaday/phase-0/) - before/after brush tests

## Composants (Components list sur Hackaday)

Reprendre la BOM du README-community.md.

## Liens

- GitHub : https://github.com/SebE585/forcair
- Licence hardware : CERN-OHL-S v2
- Licence software : MIT

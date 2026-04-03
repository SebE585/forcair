# Forcair - Plateforme Robotique Modulaire d'Exterieur

> Ref : Jayce et les Conquerants de la Lumiere - Forcair (vehicule principal / Armed Force)

Plateforme robotique autonome modulaire pour l'entretien des surfaces pavees.
Base roulante commune + modules outils interchangeables (brosse, camera, spray...).

## Contexte

- Terrain : paves autobloquants (terrasse ~30m2) + dalles carrees (allee piscine)
- Probleme : mousse verte dans les joints, mauvaises herbes
- Robot tondeuse existant : Ecovacs Goat 800 RTK (pelouse OK, pas les paves)
- Fabrication : chassis profiles alu 2020 (Motedis) + pieces imprimees 3D (Bambu Lab X1 Carbon)

## Design

Voir document detaille : `hardware/design-v1.md`

### Image concept

![Concept Forcair](specs/concept-forcair-v1.jpg)

### Deux versions

| | Proto (Phase 1) | Version finale (Phase 2+) |
|---|---|---|
| Plateau | Contreplaque 5mm | PETG noir imprime |
| Capot | PETG simple (gris) | **PETG bleu translucide** (PCB visibles) |
| Carrosserie | Profiles 2020 apparents | Profiles integres, habillage lisse |
| Cout supp. | - | +25 EUR (bobine PETG bleu translucide) |

### Modules outils (interface standard IMS)

| Ref | Module | Usage | Statut |
|-----|--------|-------|--------|
| MOD-001 | Camera Scout | Cartographie, inspection terrain | Phase 1 |
| MOD-002 | Brosse Rotative | Mousse/herbes dans joints | Phase 2 |
| MOD-003 | Spray | Jet d'eau ou anti-mousse | Futur |
| MOD-004 | Souffleur | Feuilles mortes | Futur |

Changement de module : 2 vis papillon M5, sans outil, en 30 secondes.

### Apercu

```
     300 x 250 x 100 mm, ~1.4 kg

     ┌══profiles 2020══════════════════┐
     │  ┌────────────────────────────┐ │
     │  │  [ESP32-CAM] [RPi Zero 2W]│ │  capot PETG
     │  │  [L298N]     [Batterie 3S]│ │  (waterproof)
     │  ├────────────────────────────┤ │
     │  │  [Axe Z]  [IMS interface] │ │
     │  └────────────┬───────────────┘ │
     └═══════════════╪════════════════─┘
    ◯roue            │brosse         roue◯
                  ▓▓▓▓▓▓▓▓ paves
```

- **Cadre** : 4x profiles alu 2020 (Motedis), equerres aux angles
- **Plateau** : contreplaque 5mm (proto) puis inox recup ou PETG
- **Roues** : 4x 80mm, moyeu PETG + pneu TPU + roulement 608ZZ
- **Traction** : 4WD, moteurs DC recup imprimantes
- **Brosse** : moteur Telsa 80 (12.6V DC) + brosse nylon, sur axe Z lineaire
- **Electronique** : ESP32-CAM + RPi Zero 2W + L298N, tout en stock sauf driver (3 EUR)

## Phases

### Phase 0 - Test actionneur (manuel)
- [ ] Acheter 2-3 brosses nylon/laiton perceuse (Brico, ~10 EUR)
- [ ] Tester manuellement sur un coin de terrasse
- [ ] Evaluer si moteur Telsa 80 ou Fellowes convient
- [ ] Valider quel outil nettoie sans abimer les paves

### Phase 1 - Robot scout + vision
- [x] Tester GoPro Hero 3+ → fonctionnelle
- [x] Identifier electronique → ESP32-CAM + RPi Zero 2W en stock
- [ ] Commander quincaillerie (Motedis + AliExpress)
- [ ] Couper profiles et assembler cadre
- [ ] Demonter imprimantes (moteurs DC + tiges lineaires)
- [ ] Imprimer roues (moyeu PETG + pneu TPU)
- [ ] Imprimer supports moteurs (adapter aux moteurs recup)
- [ ] Assembler base roulante 4WD
- [ ] Cabler ESP32-CAM + L298N + moteurs
- [ ] Pipeline vision : detection mousse par seuillage HSV (OpenCV)
- [ ] Telecommande WiFi depuis Mac/smartphone
- [ ] Cartographie zone a traiter (GoPro montee sur robot)

### Phase 2 - Robot nettoyeur
- [ ] Integrer actionneur valide en Phase 0
- [ ] Monter mecanisme Z (tiges lineaires recup + servo)
- [ ] Asservissement : brosse ON uniquement sur zone verte
- [ ] Boucle fermee : verification apres passage (photo avant/apres)

## BOM

| Piece | Source | Cout |
|-------|--------|------|
| 4x profiles 2020 (300+300+250+250mm) | Motedis (coupe dans barres 1m) | Inclus commande partagee |
| 4x equerres + fixations | Motedis | Inclus commande partagee |
| Plateau contreplaque 5mm | Brico | ~3 EUR |
| 4x roues (moyeu PETG + pneu TPU) | Impression 3D Bambu Lab | ~4 EUR filament |
| 4x roulements 608ZZ | AliExpress | Inclus commande partagee |
| 4x coupleurs d'arbre | AliExpress | Inclus commande partagee |
| 4x supports moteurs | Impression 3D PETG | ~2 EUR filament |
| 4x moteurs DC traction | Recup imprimantes | 0 EUR |
| Moteur brosse (12.6V DC) | Recup Telsa 80 | 0 EUR |
| Brosse nylon perceuse | Brico | ~5 EUR |
| Mecanisme Z (tiges + paliers) | Recup imprimantes + impression 3D | ~1 EUR |
| ESP32-CAM | Stock (tiroir) | 0 EUR |
| RPi Zero 2W | Stock (tiroir) | 0 EUR |
| GoPro Hero 3+ | Stock | 0 EUR |
| Motor driver L298N | AliExpress | 3 EUR |
| Batterie 3S (18650 recup ou achat) | Recup Ryobi ou achat | 0-15 EUR |
| Capot PETG | Impression 3D | ~3 EUR filament |
| **Total Forcair seul** | | **~10-25 EUR** |
| **+ quote-part quincaillerie partagee** | Motedis + AliExpress | **~40 EUR** |

## Recherche et etat de l'art

Voir document complet : `research/state-of-the-art.md`

Principaux enseignements :
- Brosse rotative validee par la litterature (Rask & Kristoffersen 2007, Cauwer 2014) comme methode la plus efficace sur surfaces dures
- ESP32-CAM suffit pour detection mousse (algo vert-sur-gris inspire de OpenWeedLocator)
- Navigation type Tertill (bump & turn) suffisante pour 30m2
- Gap dans la litterature : aucun papier sur le desherbage autonome robotise sur paves domestiques

## Photos terrain

Voir `specs/photos/` - 8 photos des paves et joints avec mousse.

## Pieces recup + quincaillerie

Voir inventaire et BOM partages : `../depistair/inventory.md`

## Lien entre projets

```
Depistair (recup) ──fournit pieces──▶ Forcair
Vrillair (CNC) ──usine pieces custom──▶ Forcair (supports, plaques)
Blindair (boites) ──range les pieces──▶ Forcair
```

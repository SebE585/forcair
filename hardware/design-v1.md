# Forcair - Design Chassis v1.1

> Plateforme robotique modulaire d'exterieur pour entretien des paves.
> Version : v1.1 - 2026-04-03 (mise a jour post etat de l'art)
> Version precedente : v1 - 2026-03-29
> Image concept : `../specs/concept-forcair-v1.jpg`
> Etat de l'art : `../research/state-of-the-art.md`

## 0. Architecture modulaire

Forcair est une **plateforme** (base roulante + electronique + vision) sur laquelle
se montent des **modules outils** interchangeables via une interface standard.

```
         PLATEFORME FORCAIR (base commune)
    ┌──────────────────────────────────────────┐
    │  Chassis 2020 + 4WD + ESP32 + RPi + Bat  │
    │  Navigation + Vision + WiFi              │
    └─────────────────────┬────────────────────┘
                          │
                 Interface Module Standard
                 (2x vis papillon M5 + XT60)
                          │
        ┌─────────────────┼─────────────────┐──── ...
        │                 │                 │
   ┌────┴────┐      ┌─────┴─────┐     ┌────┴────┐
   │ MOD-001 │      │  MOD-002  │     │ MOD-003 │
   │ CAMERA  │      │  BROSSE   │     │  SPRAY  │
   │ SCOUT   │      │ ROTATIVE  │     │         │
   │         │      │           │     │ Jet eau │
   │ Carto + │      │ Mousse /  │     │ ou anti │
   │ inspect │      │ herbes    │     │ mousse  │
   │         │      │           │     │         │
   │ Phase 1 │      │ Phase 2   │     │ Futur   │
   └─────────┘      └───────────┘     └─────────┘
```

### Interface Module Standard (IMS)

L'interface entre la plateforme et les modules est le point cle de la modularite.
Elle se situe sur le **chariot Z** (mecanisme montee/descente).

```
     VUE DE FACE - Interface Module Standard

     ┌──────────── chariot Z ────────────┐
     │                                    │
     │  ⊙ vis papillon     vis papillon ⊙ │  ← M5, serrage a la main
     │       M5                  M5       │
     │                                    │
     │       ┌──── plot ────┐             │
     │       │  centrage    │             │  ← 2 plots de centrage (imprimes 3D)
     │       └──────────────┘             │     garantissent l'alignement
     │                                    │
     │    [XT60]        [JST-XH 3p]       │  ← connecteurs : alim + signal
     │    alim 12V      signal PWM        │
     │                                    │
     └────────────────────────────────────┘
               ↕ interchangeable ↕
     ┌────────────────────────────────────┐
     │         MODULE (ex: brosse)        │
     │                                    │
     │  ⊙ trou M5           trou M5 ⊙    │
     │       ┌──── trou ────┐             │
     │       │  centrage    │             │
     │       └──────────────┘             │
     │    [XT60]        [JST-XH 3p]       │
     │                                    │
     │         [outil]                    │
     └────────────────────────────────────┘
```

### Specs interface

| Parametre | Valeur | Notes |
|-----------|--------|-------|
| Fixation mecanique | 2x vis papillon M5 | Serrage/desserrage a la main, pas d'outil |
| Centrage | 2x plots diam 8mm | Imprimes 3D, positionnement reproductible |
| Alimentation | Connecteur XT60 | 12V, 10A max (suffisant pour moteur brosse) |
| Signal | Connecteur JST-XH 3 broches | PWM vitesse + GND + sens rotation |
| Dimensions plaque module | 100 x 80 mm | Standard pour tous les modules |
| Masse max module | 500g | Budget masse restant sur chariot Z |

### Catalogue modules (prevu)

| Ref | Nom | Contenu | Statut |
|-----|-----|---------|--------|
| MOD-001 | Camera Scout | GoPro Hero 3+ sur support orientable | Phase 1 |
| MOD-002 | Brosse Rotative | Moteur Telsa 80 + brosse nylon | Phase 2 |
| MOD-003 | Spray | Pompe 12V + reservoir + buse | Futur |
| MOD-004 | Souffleur | Ventilateur 12V centrifuge | Futur |
| MOD-005 | Balai | Brosse douce large | Futur |

## 1. Contraintes terrain

Donnees extraites des photos (`specs/photos/`) :

| Contrainte | Valeur | Impact design |
|------------|--------|---------------|
| Type paves (terrasse) | Autobloquants, joints ~10mm | Roues > 60mm diam, pas trop fines |
| Type dalles (allee) | Carrees ~30x30cm, joints ~8mm | Surface plus reguliere |
| Mousse | Dans les joints, epaisseur 2-5mm | Brosse doit atteindre le fond du joint |
| Denivele joints | 3-8mm entre paves | Suspension ou roues souples |
| Surface totale | ~30m2 terrasse + ~10m2 allee | Autonomie batterie ~1h min |
| Environnement | Exterieur, humidite, soleil | Electronique protegee |
| Obstacles | Bordures pierre, pieds de table, mur | Detection ou bumper |

## 2. Dimensions generales

```
     VUE DE DESSUS (cotes en mm)

     ←──────── 300 ─────────→

  ↑  ┌─profilé 2020─────────────profilé 2020─┐
  │  │                                        │
  │  │  ┌──────────────────────────────────┐  │
     │  │          ZONE ELECTRONIQUE       │  │
 250 │  │  [ESP32-CAM]       [RPi Zero 2W] │  │
     │  │  [Motor driver]    [Batterie 3S] │  │
  │  │  └──────────────────────────────────┘  │
  │  │                                        │
  │  │  ┌──────────────────────────────────┐  │
  ↓  │  │          ZONE ACTIONNEUR         │  │
     │  │  [Moteur brosse]   [Mecanisme Z] │  │
     │  └──────────────────────────────────┘  │
     └────────────────────────────────────────┘
    ◯roue AR-G                        roue AR-D◯


    ◯roue AV-G                        roue AV-D◯
```

| Parametre | Valeur | Justification |
|-----------|--------|---------------|
| Longueur (X) | 300 mm | Couvre 2-3 paves en largeur |
| Largeur (Y) | 250 mm | Stabilite + place pour electronique |
| Hauteur chassis | ~100 mm | Garde au sol ~30mm + plateau + composants |
| Garde au sol | 30 mm | Passer les irregularites entre paves |
| Poids cible | < 2.5 kg | Moteurs recup DC suffisants |
| Empattement roues | 260 x 210 mm | Stabilite sur surface irreguliere |

## 3. Structure chassis

### 3.1 Cadre en profiles 2020

```
     VUE DE DESSUS - CADRE

     ┌═══════════════════════════════════┐
     ║           traverse AV            ║  ← profilé 250mm
     ╠═══════════════════════════════════╣
     ║                                   ║
     ║  longueur G          longueur D   ║  ← profilés 300mm
     ║                                   ║
     ╠═══════════════════════════════════╣
     ║           traverse AR            ║  ← profilé 250mm
     └═══════════════════════════════════┘

     Assemblage : 4x equerres 20x20 Motedis (1 par angle)
```

**Decoupe dans les barres Motedis 1m :**
- Barre 1 : 300 + 300 + 250 + 100(reste) = 1 barre
- Barre 2 : 250 + reste pour Vrillair

**Fixation equerres :** ecrou marteau M4 + vis M4x8 (kit Motedis)

### 3.2 Plateau

Le plateau se fixe sur les profiles via T-nuts M5.

| Option | Materiau | Epaisseur | Poids | Waterproof | Recommandation |
|--------|----------|-----------|-------|------------|----------------|
| A | Contreplaque | 5mm | ~150g | Non (vernis possible) | **Proto Phase 1** |
| B | **PETG noir imprime** | 2-3mm | ~120g | Oui | **Version finale** (cf image concept) |
| C | Plaque inox Silvercrest | 1-2mm | ~200g | Oui | Alternative (decoupe necessaire) |
| D | Polypropylene alveolaire | 4mm | ~50g | Oui | Trop souple seul |

**Phase 1 : contreplaque 5mm** (280 x 230 mm), perce aux emplacements T-nuts.
**Version finale : PETG noir** imprime en plusieurs pieces, assemblee par clips/vis.

### 3.3 Protection electronique / Carrosserie

> Ref visuelle : `../specs/concept-forcair-v1.jpg`
> Objectif : capot translucide bleu laissant voir les PCB (effet "tech visible").

L'electronique doit etre protegee (usage exterieur, projections d'eau/mousse).

```
     VUE DE COTE - CAPOT

          ┌──capot PETG imprime──┐
          │                      │
     ─────┤   [electronique]     ├─────  plateau
          │                      │
          └──────────────────────┘
```

**Phase 1 (proto) :**
- Capot imprime en PETG gris/naturel
- Fixation par clips sur le plateau (pas de vis = demontage rapide)
- Ouvertures pour ventilation (labyrinthes anti-projection)
- Passage cables etanches vers moteurs (presse-etoupes ou silicone)

**Version finale (cf image concept) :**
- **Capot en PETG bleu translucide** : les PCB vertes (ESP32-CAM, RPi) sont visibles a travers
- Forme arrondie type dome (rayon de courbure ~120mm)
- Bandeau alu visible au milieu (profile 2020 = element esthetique)
- Joint silicone entre capot et plateau pour etancheite
- LED status visible a travers le capot (optionnel)
- **Filament** : PETG bleu translucide (eSUN, Polymaker, ou Bambu Lab) ~25 EUR/bobine

## 4. Roues et traction

### 4.1 Conception roues

```
     VUE EN COUPE ROUE (diam 80mm)

     ┌─────────────────────────┐
     │ ░░░ Pneu TPU 95A ░░░░░ │  8mm epaisseur
     │ ░ ┌─────────────────┐ ░ │
     │ ░ │  Moyeu PETG     │ ░ │
     │ ░ │                 │ ░ │
     │ ░ │    ┌───────┐    │ ░ │
     │ ░ │    │ 608ZZ │    │ ░ │  roulement 8x22x7mm
     │ ░ │    │  ⊕    │    │ ░ │  axe 8mm
     │ ░ │    └───────┘    │ ░ │
     │ ░ │                 │ ░ │
     │ ░ └─────────────────┘ ░ │
     │ ░░░░░░░░░░░░░░░░░░░░░░ │
     └─────────────────────────┘
            ←── 80mm ──→
```

| Piece | Materiau | Impression | Parametres cles |
|-------|----------|------------|-----------------|
| Moyeu | PETG | Bambu Lab, 0.2mm layer | Logement 608ZZ (22mm ext), fixation axe |
| Pneu | TPU 95A | Bambu Lab, 0.2mm layer | Epaisseur 8mm, profil strie pour grip |

**Profil du pneu :** stries transversales pour grip sur paves humides + mousse.

```
     Surface du pneu (deroulee)
     ═══╗  ╔═══╗  ╔═══╗  ╔═══
        ╚══╝   ╚══╝   ╚══╝
     Stries 2mm profondeur, pas 5mm
```

### 4.2 Motorisation traction

**Config : 4WD (4 roues motrices)**

Chaque roue est entrainee par un moteur DC recup.

| Moteur | Source recup | Tension | Usage |
|--------|-------------|---------|-------|
| 2x moteurs DC (chariot) | Canon MG6450 + Epson XP-2150 | 5-12V | Roues AV |
| 2x moteurs DC | Ancienne imprimante (boite recup) | 5-12V | Roues AR |

**Si les moteurs recup sont trop faibles** (couple insuffisant sur paves) :
- Fallback : 4x moteurs N20 12V 200RPM (~10 EUR les 4 sur AliExpress)
- Ou 4x moteurs GA12-N20 avec reducteur metal

### 4.3 Fixation moteurs sur profiles

```
     VUE DE DESSOUS

     ┌══════════════════════════════════┐  profil 2020
     │  ┌──────┐              ┌──────┐ │
     │  │MotAVG│              │MotAVD│ │  supports moteur
     │  │  ◯───┼──axe────────┼───◯  │ │  imprimes 3D
     │  └──┼───┘              └───┼──┘ │  fixes par T-nuts
     │     │                      │    │
     │   roue                   roue   │
     │   AV-G                   AV-D   │
     │                                 │
     │  ┌──────┐              ┌──────┐ │
     │  │MotARG│              │MotARD│ │
     │  │  ◯───┼──axe────────┼───◯  │ │
     │  └──┼───┘              └───┼──┘ │
     │     │                      │    │
     │   roue                   roue   │
     │   AR-G                   AR-D   │
     └══════════════════════════════════┘
```

**Support moteur** : piece imprimee 3D (PETG) en forme de U.
- Se fixe sous le profile 2020 via 2x T-nuts M5
- Collier ou berceau ajuste au diametre du moteur recup
- Conception parametrique (CadQuery) : adaptable a chaque moteur

**Transmission moteur → roue :**
- Coupleur d'arbre rigide (axe moteur → axe 8mm roulement 608)
- Ou impression 3D d'un engrenage si reduction necessaire

## 5. Systeme modulaire (actionneur)

> Tous les outils se montent sur l'Interface Module Standard (IMS) du chariot Z.
> Voir section 0 pour les specs de l'interface.

### 5.1 MOD-002 : Brosse rotative (premier module)

```
     VUE DE FACE - MODULE BROSSE sur IMS

     ══════════ plateau ══════════
           │              │
     ──────┤  chariot Z    ├──────  guides lineaires
     tige  │              │  tige  (recup imprimante)
     lisse │  ┌─── IMS ──┐│  lisse
           │  │⊙M5    M5⊙││
           │  │ [XT60]    ││
           │  └─────┬─────┘│
           │  ======╪====== │  ← decrochage rapide
           │  ┌─────┴─────┐│
           │  │  MOD-002   ││
           │  │ [Moteur    ││
           │  │  Telsa 80] ││
           │  │    │       ││
           │  │ ┌──┴──┐   ││
           │  │ │BROSSE│   ││
           │  │ │nylon │   ││
           │  │ └─────┘   ││
           │  └────────────┘│
           ▼                ▼
     ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  paves
```

| Composant | Spec | Source |
|-----------|------|--------|
| Plaque module | 100x80mm, PETG imprime, 2x trous M5 + plots centrage | Impression 3D |
| Moteur brosse | DC 12.6V 1A (Telsa 80) | Recup |
| Connecteur alim | XT60 male | Achat (~1 EUR) |
| Connecteur signal | JST-XH 3p male | Achat (~0.50 EUR) |
| Brosse | Nylon dur, disque ou coupe diam ~60mm | Brico (~5 EUR) |
| Vitesse rotation | ~1000-3000 RPM (a tester Phase 0) | - |

### 5.1b MOD-001 : Camera Scout (Phase 1)

| Composant | Spec | Source |
|-----------|------|--------|
| Plaque module | 100x80mm, PETG, 2x trous M5 | Impression 3D |
| GoPro Hero 3+ | Sur support orientable (tilt) | Stock |
| Servo inclinaison | SG90 (optionnel) | Achat (~2 EUR) |
| Connecteur | JST-XH (signal servo) | - |

### 5.2 Mecanisme montee/descente (axe Z)

La brosse doit pouvoir :
- **Descendre** : contact avec le joint du pave (~20mm de course)
- **Monter** : position haute quand le robot se deplace sans nettoyer

**Guidage lineaire recup imprimante :**

```
     Mecanisme Z (vue de cote)

     ═══════ plateau ═══════
         │             │
    tige lisse     tige lisse    ← recup Canon/Epson (diam 8mm)
         │             │
     ┌───┴─────────────┴───┐
     │   chariot mobile     │    ← palier imprime 3D (ou LM8UU)
     │   ┌─── IMS ───┐     │    ← Interface Module Standard
     │   │⊙M5    M5⊙ │     │       2x vis papillon + XT60 + JST
     │   └─────┬──────┘     │
     │   ======╪======      │    ← le module se clipse ici
     │   ┌─────┴──────┐     │
     │   │  MODULE     │     │
     │   └─────────────┘     │
     └──────────┬───────────┘
                │
         ressort rappel          ← recup imprimante (position haute par defaut)
                │
                ▼
     Position basse = nettoyage
```

| Piece | Source | Notes |
|-------|--------|-------|
| 2x tiges lisses diam 8mm | Recup Canon MG6450 / Epson XP-2150 | Guides chariot imprimante |
| 2x paliers lineaires | Imprimes 3D (PETG) ou LM8UU recup | Glissement sur tiges |
| 1x ressort de rappel | Recup imprimante | Position haute par defaut |
| Course Z | ~20-25mm | Suffisant pour atteindre fond joint |

**Actionnement Z :**
- **Phase 1 (simple)** : servo SG90 + came (5 EUR si achat)
- **Phase 2 (precis)** : moteur pas-a-pas recup + vis sans fin

## 6. Electronique

### 6.1 Architecture (v1.1 simplifiee)

> **Changement v1.1** : la recherche (R02, R03) montre que l'ESP32-CAM suffit pour
> la detection HSV et meme du CNN leger. Le RPi Zero 2W est reporte a Phase 2.
> Un seul processeur = un seul firmware, pas de communication inter-processeurs.

```
     Architecture Phase 1 (ESP32-CAM seul)

     ┌─────────────┐     WiFi      ┌──────────────┐
     │  ESP32-CAM  │◄────────────►│ Mac/Smartphone│
     │             │               │ (monitoring)  │
     │ OV2640 cam  │               │ (telecommande)│
     │ HSV detect  │               └──────────────┘
     │ GPIO control│
     │ WiFi AP/STA │
     └──┬───┬──┬───┘
        │   │  │
   ┌────┘   │  └────────┐
   │        │           │
┌──┴────┐ ┌─┴───┐ ┌────┴────────┐
│TB6612 │ │Servo│ │Capteurs     │
│FNG    │ │ Z   │ │ 2x IR Sharp │
│(MOSFET│ │     │ │ 2x bumper   │
│driver)│ └─────┘ │ 1x buzzer   │
└┬──┬───┘         │ (1x tension)│
 │  │             └─────────────┘
4x moteurs DC
+ moteur brosse (via MOSFET)
```

> **Phase 2 (si necessaire)** : ajouter RPi Zero 2W pour SLAM, cartographie,
> ou ML avance. L'ESP32-CAM passe en controleur bas-niveau.

### 6.2 Composants

| Composant | Modele | Source | Role |
|-----------|--------|--------|------|
| Processeur principal | **ESP32-CAM** | Stock | Camera OV2640, detection HSV, WiFi, GPIO, controle temps reel |
| Driver traction | **TB6612FNG** (double pont H MOSFET) | Achat ~3 EUR | 4 moteurs DC (2 canaux, G+D en parallele). Remplace L298N. |
| Driver brosse | MOSFET IRLZ44N + diode flyback | Recup ou ~1 EUR | Commutation moteur brosse 12V (PWM depuis ESP32) |
| Capteurs obstacle | 2x Sharp GP2Y0A21 (IR 10-80cm) | Achat ~2 EUR | Detection obstacles a distance (murs, pieds de table) |
| Capteurs contact | 2x micro-switch + bumper TPU | Recup ou ~1 EUR | Detection contact (bordures, murs) |
| Retour sonore | Buzzer piezo passif | Achat ~0.30 EUR | Batterie faible, obstacle, fin de mission |
| Monitoring batterie | Pont diviseur resistif sur ADC ESP32 | Composants recup | Tension batterie en temps reel, coupure si < 9.6V (3.2V/cellule) |
| Alimentation | Pack 3S 18650 (11.1V) | Recup Ryobi ou achat | Tout le robot |

> **Composants en reserve (Phase 2)** : RPi Zero 2W (stock), GoPro Hero 3+ (stock),
> module GPS NEO-6M (~3 EUR), LiDAR low-cost (~20 EUR).

**Pourquoi TB6612FNG au lieu de L298N :**

| Critere | L298N | TB6612FNG |
|---------|-------|-----------|
| Technologie | BJT (bipolaire) | **MOSFET** |
| Chute de tension | **~2V** (perte enorme sur 11.1V) | **~0.5V** |
| Rendement | ~70% | **~95%** |
| Dissipation thermique | Chauffe, necessite radiateur | Froid |
| Taille | 43x43mm | **20x20mm** |
| Prix | ~3 EUR | ~3 EUR |
| Courant max/canal | 2A | 1.2A (suffisant pour moteurs recup) |

> Source : communaute DIY robotique (LIAM-ESP, RoboFoundry). Le L298N est un
> heritage des annees 2000, le TB6612FNG est le standard actuel pour les petits robots.

### 6.3 Alimentation

**Pack 3S (11.1V nominal, 12.6V charge) :**

```
     Batterie 3S
     ┌─────────────────┐
     │ [18650] [18650]  │  si recup Ryobi : 2P par cellule (4Ah)
     │ [18650] [18650]  │  sinon : 1P (2Ah, suffisant proto)
     │ [18650] [18650]  │
     │      [BMS 3S]    │  protection charge/decharge
     └────────┬─────────┘
              │ 11.1V
         ┌────┼────────────┐
         │    │            │
    ┌────┴──┐ │       ┌────┴───┐
    │ Buck  │ │       │ Direct │
    │ 5V 2A │ │       │ 11.1V  │
    └───┬───┘ │       └───┬────┘
        │     │           │
    ESP32-CAM │      Moteurs DC
    + servo   │      + moteur brosse
    + capteurs│
              │
         ┌────┴───────┐
         │ Pont div.  │  → ADC ESP32 (GPIO 34/35)
         │ R1=100k    │  Vmesure = Vbat * R2/(R1+R2)
         │ R2=33k     │  11.1V → ~2.75V (safe pour ADC 3.3V)
         └────────────┘
```

> **Changement v1.1** : ajout monitoring tension batterie. Le BMS protege la batterie,
> mais sans monitoring le robot ne sait pas quand rentrer ou biper.
> Seuils : < 10.5V = bip avertissement, < 9.6V = arret moteurs + bip continu.

**Si cellules Ryobi HS :** achat 6x 18650 (~12 EUR) ou pack LiPo 3S RC (~15 EUR).

**Autonomie estimee (revisee v1.1) :**
- Moteurs traction : 4x 0.5A = 2A
- Moteur brosse : 1A
- Electronique (ESP32-CAM seul + capteurs) : **0.25A** (vs 0.5A avec RPi)
- Total : **~3.25A** → avec pack 4Ah = **~1h15 d'autonomie** (+15min vs v1)

## 7. Logiciel (apercu)

### 7.1 Phase 1 - Scout + telecommande

> **Changement v1.1** : tout tourne sur ESP32-CAM seul.

| Module | Plateforme | Fonction |
|--------|-----------|----------|
| Stream video | ESP32-CAM | Flux MJPEG WiFi vers Mac/smartphone |
| Detection mousse | **ESP32-CAM** | Seuillage HSV (vert sur gris) directement sur l'ESP32 (cf. R01 OWL) |
| Telecommande | Mac/smartphone | Pilotage WiFi (webapp simple) |
| Capteurs | ESP32 GPIO | IR distance + bumpers → evitement reactif |
| Monitoring | ESP32 ADC | Tension batterie → bip si faible |

### 7.2 Phase 1.5 - Nettoyeur semi-autonome (bump & turn)

> **Nouveau v1.1** : phase intermediaire inspiree de Tertill. Le robot patrouille
> seul en mode "random walk" et brosse quand il detecte du vert.

| Module | Plateforme | Fonction |
|--------|-----------|----------|
| Navigation | ESP32 | **Bump & turn** (Tertill) : avancer, tourner sur obstacle. Couverture aleatoire. |
| Detection mousse | ESP32-CAM | HSV vert-sur-gris → brosse ON si vert detecte |
| Controle Z | ESP32 | Servo descente brosse |
| Evitement obstacles | ESP32 | IR Sharp (anticipation) + bumpers (contact) |
| Securite | ESP32 | Monitoring batterie, arret si < 9.6V, tilt detection (MPU6050 optionnel) |

> **Pourquoi bump & turn** : Tertill a prouve que la couverture aleatoire suffit pour
> des surfaces < 50m2, et c'est infiniment plus simple qu'un SLAM. Notre terrasse = 30m2.
> En 1h de random walk, le robot couvre statistiquement >95% de la surface (ref. Tertill).

### 7.3 Phase 2 - Nettoyeur autonome intelligent

| Module | Plateforme | Fonction |
|--------|-----------|----------|
| Navigation | ESP32 + **RPi Zero 2W** | Balayage systematique OU suivi de joints par vision (R12) |
| Detection avancee | RPi + OWL | ML : classification mousse/herbe/lichen, segmentation |
| Cartographie | RPi + GPS NEO-6M | Heatmap zones mousse, log des passages |
| Verification | RPi + camera | Photo avant/apres passage, score de nettoyage |
| Coordination | RPi WiFi | Mode multi-robot si 2+ Forcair (futur lointain) |

## 8. Ce que nous n'avions pas anticipe (v1.1)

> Enseignements tires de l'etat de l'art (`../research/state-of-the-art.md`).
> Classe par criticite : CRITIQUE = doit etre traite avant Phase 1,
> IMPORTANT = Phase 1.5, NICE = Phase 2+.

### 8.1 CRITIQUE - Gestion des debris de brossage

**Probleme** : le design v1 ne dit pas **ou vont les debris** (mousse arrachee,
terre, petits cailloux). La brosse rotative projette les debris. Si non gere,
le robot re-salit la surface qu'il vient de nettoyer.

**Solutions observees dans les projets similaires :**

| Solution | Complexite | Efficacite | Retenue |
|----------|-----------|------------|---------|
| Jupe de confinement (TPU souple autour de la brosse) | Faible | Moyenne | **Phase 1** |
| Aspiration (petit ventilateur + bac) | Moyenne | Haute | Phase 2 (= MOD-004 Souffleur inverse) |
| Brossage vers l'exterieur (sens de rotation oriente) | Nulle | Faible | Phase 1 (complementaire) |

**Action** : imprimer une jupe TPU souple autour de la zone brosse. La jupe confine
les debris. Le robot les pousse vers le bord de la terrasse par mouvement avant.

```
     VUE EN COUPE - JUPE DE CONFINEMENT

     ══════ plateau ══════
           │         │
     ──────┤ axe Z   ├──────
           │         │
      ┌────┴─────────┴────┐
      │  ┌─ MOD-002 ──┐   │
      │  │  [moteur]   │   │
      │  │  [brosse]   │   │
      ├──┘  ▓▓▓▓▓▓▓▓   └──┤  ← jupe TPU souple (~3mm)
      │    debris confines │    imprimee, clipee sous le chassis
      └────────────────────┘
     ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  paves
```

**Cout** : ~1 EUR filament TPU. **Masse** : ~15g.

### 8.2 CRITIQUE - Etancheite electronique en usage exterieur

**Probleme** : le design v1 mentionne un capot mais pas de **classe IP**. La brosse
projette de l'eau, de la terre et de la mousse humide. L'ESP32-CAM et le driver
sont directement en dessous.

**Solutions observees :**
- **Tertill** : boitier scelle, connecteurs etanches, design IP67
- **LIAM-ESP** : boitier etanche avec presse-etoupes
- **ROMI** : compartiment electronique separe du compartiment outil

**Action Phase 1** :
- Separer electronique (haut, sous capot) et outil (bas, sous chassis) physiquement
- Joints en mousse adhesive entre capot et plateau (~1 EUR, Brico)
- Presse-etoupes PG7 pour les cables qui traversent le plateau (4x, ~2 EUR)
- Vernis conforme sur l'ESP32-CAM (spray silicone, ~3 EUR la bombe, recup atelier)
- Objectif : **IP44 minimum** (projections d'eau et particules)

**Cout** : ~3 EUR. **Masse** : ~10g.

### 8.3 CRITIQUE - Protection camera contre les projections

**Probleme** : la camera OV2640 de l'ESP32-CAM pointe vers le sol pour detecter
la mousse. La brosse rotative projette des debris **vers la camera**.

**Action** : vitre de protection en polycarbonate devant l'objectif. Decoupee dans
un emballage blister recup. Fixation sur le support ESP32-CAM existant.

**Cout** : 0 EUR (recup). **Masse** : ~2g.

### 8.4 IMPORTANT - Blocage et detection de panne

**Probleme** : aucun projet similaire ne fonctionne sans detection de blocage.
Le robot va se bloquer contre des obstacles (pieds de table, bordures en angle,
paves souleves). Sans detection, les moteurs forcent et grillent.

**Solutions observees :**
- **Tertill** : detection de courant moteur (stall = courant > seuil)
- **LIAM-ESP** : encodeurs sur roues + timeout
- **WEEDINATOR** : IMU pour detecter l'immobilite

**Action Phase 1** :
- Monitoring courant via mesure de tension sur resistance shunt (0.1 ohm) sur ADC ESP32
- Si courant > seuil pendant 2s → arreter moteurs, reculer, tourner 90-180 degres
- Optionnel Phase 1.5 : ajouter MPU6050 (IMU 6 axes, ~2 EUR) pour detecter :
  - Blocage (pas de mouvement malgre moteurs actifs)
  - Retournement (securite : arret immediat)
  - Inclinaison excessive (bord de terrasse, marche)

**Cout** : 0 EUR (shunt = resistance recup) ou ~2 EUR (MPU6050). **Masse** : ~3g.

### 8.5 IMPORTANT - Pression de brosse constante

**Probleme** : le design v1 utilise un servo SG90 + came pour l'axe Z. Mais le servo
maintient une **position** fixe, pas une **pression** constante. Si le pave est plus
haut ou plus bas que prevu, la brosse appuie trop ou pas assez.

**Solution observee (Aigamo, ROMI)** : pression par gravite ou ressort, pas par servo.

**Action revisee** :
- **Le ressort de rappel (recup) pousse la brosse VERS LE BAS** (inversement du v1 ou
  le ressort rappelait vers le haut)
- Le servo releve la brosse quand on ne veut PAS brosser (position haute = verrouillage)
- En mode brossage : le servo relache, le ressort + gravite appliquent une pression
  constante quel que soit le relief
- **Avantage** : le servo ne force pas en continu (economie batterie), et la pression
  s'adapte naturellement aux irregularites des paves

```
     AVANT (v1) :                    APRES (v1.1) :
     ressort ↑ (rappel haut)        ressort ↓ (pousse bas)
     servo ↓ (force vers bas)       servo ↑ (releve quand inactif)

     Servo fatigue en brossage       Servo au repos en brossage
     Pression variable               Pression constante par ressort
```

**Cout** : 0 EUR (meme composants, logique inversee). **Impact CAD** : modifier le
montage du ressort dans le mecanisme Z.

### 8.6 IMPORTANT - Navigation de bord de terrasse

**Probleme** : la terrasse a des **bords** (bordures, marches, pelouse). Le robot
doit detecter qu'il arrive au bord et ne pas tomber. Aucun capteur dans le design v1
ne gere ca.

**Solutions observees :**
- **Tertill** : bumper avant suffit (bordures surelevelees)
- **Tondeuses robot** : fil perimetrique enterre
- **Roomba** : capteurs cliff (IR pointant vers le sol)

**Action Phase 1** :
- 2x capteurs IR cliff (TCRT5000, ~0.50 EUR les 2) sous le chassis, avant
- Pointent vers le sol a ~45 degres vers l'avant
- Si pas de sol detecte (vide, herbe au lieu de paves) → arreter, reculer, tourner

**Cout** : ~0.50 EUR. **Masse** : ~2g.

### 8.7 NICE - Recharge et dock

**Probleme** : le design v1 suppose une recharge manuelle (debrancher la batterie).
Tous les robots commerciaux (Tertill, Ecovacs, Roomba) ont une solution de recharge
autonome.

**Pistes pour Phase 2** :
- **Contacts de charge** : 2 lames cuivre sur un dock, le robot se gare dessus (LIAM-ESP)
- **Panneau solaire** : petit panneau 5W sur le capot, recharge lente entre missions (Tertill, Acorn)
- **Induction Qi** : bobine sous le chassis, pad de charge au sol (~8 EUR)

**Pas d'action Phase 1** : recharge manuelle acceptee pour le prototype.

### 8.8 NICE - OTA (mise a jour firmware par WiFi)

**Probleme** : pour iterer rapidement, reflasher l'ESP32 par cable USB est penible
en exterieur. Tous les projets ESP32 matures implementent l'OTA.

**Action** : integrer ArduinoOTA ou ESP-IDF OTA dans le firmware des Phase 1.
Cout zero, juste du code. Permet de mettre a jour le robot depuis le WiFi terrasse.

### 8.9 Synthese des changements v1 → v1.1

| # | Sujet | v1 | v1.1 | Source |
|---|-------|----|------|--------|
| 1 | Processeur Phase 1 | RPi Zero 2W + ESP32-CAM | **ESP32-CAM seul** | R02, R03 |
| 2 | Motor driver | L298N | **TB6612FNG** | LIAM-ESP, RoboFoundry |
| 3 | Navigation Phase 1 | Balayage systematique | **Bump & turn** (Tertill) | Tertill, Aigamo |
| 4 | Capteurs obstacle | "Bumpers ou HC-SR04" (vague) | **2x IR Sharp + 2x bumper + 2x cliff** | Tertill, LIAM-ESP |
| 5 | Gestion debris | Non traite | **Jupe TPU confinement** | Observation terrain |
| 6 | Etancheite | Capot simple | **IP44 : joints mousse + presse-etoupes + vernis** | Tertill, LIAM-ESP |
| 7 | Pression brosse | Servo force vers bas | **Ressort pousse bas + servo releve** | Aigamo, ROMI |
| 8 | Monitoring batterie | Non traite | **Pont diviseur ADC + seuils alarme** | Standard robotique |
| 9 | Detection blocage | Non traite | **Shunt courant + optionnel MPU6050** | Tertill, LIAM-ESP |
| 10 | Protection camera | Non traite | **Vitre polycarbonate recup** | Bon sens |
| 11 | Detection bord terrasse | Non traite | **2x capteurs cliff TCRT5000** | Roomba, tondeuses |
| 12 | Brosse alternative | Nylon uniquement | **Nylon + acier doux (comparatif Phase 0)** | R13 (Rask) |
| 13 | Phase intermediaire | Phase 1 → Phase 2 | **Phase 1 → 1.5 (bump&turn) → 2** | Tertill |

## 9. Masses et equilibre

| Element | Masse v1 | Masse v1.1 | Position |
|---------|----------|-----------|----------|
| Cadre profiles 2020 (4x) | ~250g | ~250g | Perimetre |
| Plateau contreplaque | ~150g | ~150g | Centre |
| 4x moteurs traction | ~200g | ~200g | Coins, sous le plateau |
| 4x roues (moyeu+pneu+roulement) | ~160g | ~160g | Coins |
| Moteur brosse (Telsa 80) | ~150g | ~150g | Centre-avant |
| Mecanisme Z + brosse | ~100g | ~100g | Centre-avant |
| Electronique (RPi+ESP32+driver) | ~50g | **~30g** (ESP32+TB6612 seuls) | Centre-arriere |
| Capteurs (IR, bumpers, cliff, buzzer) | - | **~25g** | Perimetre |
| Jupe TPU confinement | - | **~15g** | Sous chassis |
| Etancheite (joints, presse-etoupes) | - | **~10g** | Plateau |
| Vitre protection camera | - | **~2g** | Support ESP32-CAM |
| Batterie 3S | ~150g | ~150g | Centre (lest pour equilibre) |
| Capot PETG | ~80g | ~80g | Dessus |
| Cables, visserie | ~100g | ~100g | Reparti |
| ~~GoPro + MOD-001~~ | ~~~120g~~ | **0g** (reporte Phase 2) | - |
| **TOTAL** | **~1.4 kg** | **~1.3 kg** | |

Sous les 2.5 kg de budget masse. Marge de 1.2 kg pour Phase 2 (RPi, GPS, LiDAR...).

## 9. Pieces a imprimer (Bambu Lab X1 Carbon)

### Phase 1 (proto fonctionnel) - v1.1

| Piece | Materiau | Qty | Taille estimee | Temps impr. | Changement v1.1 |
|-------|----------|-----|----------------|-------------|-----------------|
| Moyeu roue | PETG noir | 4 | 80x80x25mm | ~1h/pc | = |
| Pneu roue | TPU 95A noir | 4 | 80x80x10mm | ~45min/pc | = |
| Support moteur traction | PETG | 4 | 40x30x25mm | ~30min/pc | = |
| Chariot Z + IMS | PETG | 1 | 120x90x30mm | ~2h | = (logique ressort inversee) |
| Palier lineaire Z | PETG | 2 | 20x20x15mm | ~15min/pc | = |
| ~~Plaque MOD-001 (camera scout)~~ | ~~PETG~~ | ~~1~~ | - | - | **RETIRE** (GoPro reportee) |
| Plaque MOD-002 (brosse) | PETG | 1 | 100x80x20mm | ~30min | = |
| Capot proto | PETG gris | 1 | 200x150x40mm | ~3h | = (+ joints mousse colles) |
| ~~Support GoPro~~ | ~~PETG~~ | ~~1~~ | - | - | **RETIRE** (reportee Phase 2) |
| Support ESP32-CAM | PETG | 1 | 35x30x15mm | ~15min | + logement vitre protection |
| **Jupe confinement brosse** | **TPU 95A** | **1** | **120x100x15mm** | **~45min** | **NOUVEAU** |
| **Support capteurs IR (AV)** | **PETG** | **1** | **60x20x15mm** | **~15min** | **NOUVEAU** |
| **Bumper avant TPU** | **TPU 95A** | **1** | **250x30x10mm** | **~30min** | **NOUVEAU** (integre micro-switch) |
| **Supports cliff (x2)** | **PETG** | **2** | **15x10x10mm** | **~10min/pc** | **NOUVEAU** |
| **Total Phase 1 v1.1** | | **21 pcs** | | **~12-13h** | -2 pieces, +4 pieces |

### Version finale (cf image concept `../specs/concept-forcair-v1.jpg`)

| Piece | Materiau | Qty | Notes |
|-------|----------|-----|-------|
| Plateau | PETG noir | 2-3 pcs assemblees | Remplace le contreplaque |
| **Capot dome** | **PETG bleu translucide** | 1 | Piece maitresse, PCB visibles |
| Habillage lateral | PETG noir | 2 | Cache les profiles, finition lisse |
| Pare-choc avant | TPU noir | 1 | Protection + bumper capteur |
| **Total version finale** | | **+6 pcs** | **~6-8h supplementaires** |

> Filament supplementaire version finale : 1 bobine PETG bleu translucide (~25 EUR).

## 10. Plan de decoupe profiles 2020

```
Barre 1 (1000mm Motedis) :
├── 300mm (longueur G) ──┤── 300mm (longueur D) ──┤── 250mm (traverse AV) ──┤── 150mm reste
                                                                                    │
                                                                              pour Vrillair

Barre 2 (1000mm Motedis) :
├── 250mm (traverse AR) ──┤── 750mm reste pour Vrillair
```

**Forcair consomme seulement 1.1 m de profile** sur les 5m commandes.
Reste 3.9m pour Vrillair Structure S.

## 12. Ordre de montage (v1.1)

### Phase 0 - Validation actionneur (avant toute construction)
0a. Acheter brosses nylon + acier doux perceuse (~10 EUR)
0b. Tester manuellement sur un coin de terrasse (3 types de paves)
0c. Evaluer efficacite ET usure des joints (photos avant/apres)
0d. Valider que moteur Telsa 80 a le couple necessaire
0e. **Decision** : nylon, acier, ou les deux selon la zone

### Phase 1 - Base roulante + scout
1. Couper 4 profiles (300, 300, 250, 250mm)
2. Assembler cadre avec equerres + T-nuts
3. Imprimer 4 supports moteurs (adapter au diam moteurs recup)
4. Fixer supports sous les profiles avec T-nuts
5. Monter moteurs dans supports
6. Imprimer 4 roues (moyeu + pneu)
7. Monter roulements 608ZZ dans moyeux
8. Fixer roues sur axes moteurs (coupleurs)
9. Percer et fixer plateau contreplaque
10. Coller joints mousse adhesive sur le plateau (etancheite capot)
11. Monter presse-etoupes PG7 (4x passages cables plateau)
12. Monter electronique : ESP32-CAM + TB6612FNG + pont diviseur batterie
13. Monter capteurs : 2x IR Sharp (avant) + 2x TCRT5000 cliff (sous-avant)
14. Imprimer et monter bumper TPU avant (integre 2x micro-switch)
15. Imprimer et monter capot + buzzer piezo
16. Appliquer vernis conforme sur ESP32-CAM
17. Firmware : telecommande WiFi + stream video + monitoring batterie
18. **Phase 1 OK** : robot scout telecommande avec detection obstacles

### Phase 1.5 - Nettoyeur semi-autonome (bump & turn)
19. Monter mecanisme Z (tiges lineaires recup + paliers + **ressort vers bas**)
20. Monter MOD-002 (brosse validee Phase 0) sur IMS
21. Imprimer et monter jupe TPU confinement sous chassis
22. Imprimer vitre protection camera (polycarbonate recup)
23. Firmware : bump & turn + detection HSV mousse + brosse ON/OFF + stall detection
24. **Phase 1.5 OK** : robot autonome "Tertill-like" qui brosse la mousse

### Phase 2 - Nettoyeur intelligent
25. Ajouter RPi Zero 2W (SLAM, OWL, cartographie)
26. Ajouter GPS NEO-6M (log des zones traitees)
27. Remonter GoPro sur MOD-001 pour cartographie haute resolution
28. Firmware : navigation systematique ou suivi de joints

### Version finale - Esthetique
29. Imprimer carrosserie PETG noir + capot bleu translucide
30. Habillage lateral + pare-choc TPU definitif
31. (Optionnel) Panneau solaire 5W sur le capot

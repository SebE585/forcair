# Forcair - Etat de l'art et recherche bibliographique

> Version : 2026-04-03
> Objectif : alimenter la reflexion technique et preparer un eventuel papier

## 1. Positionnement de Forcair

Forcair est un robot autonome desherbeur de paves, DIY, open-source, budget < 75 EUR.
C'est une niche tres specifique : **desherbage autonome sur surfaces dures** (paves, dalles).

La litterature couvre bien le desherbage agricole (champs) mais tres peu les surfaces urbaines/domestiques.
Les projets DIY existants ciblent presque tous les jardins/potagers.
**C'est une opportunite de contribution originale.**

---

## 2. Projets DIY et open-source similaires

### 2.1 Detection de mauvaises herbes

| Projet | URL | Techno | Reutilisable pour Forcair |
|--------|-----|--------|---------------------------|
| **OpenWeedLocator (OWL)** | [GitHub](https://github.com/geezacoleman/OpenWeedLocator) | RPi + camera, algo vert-sur-brun (ExG/HSV) | **Tres pertinent** : detection mousse verte sur paves gris = cas quasi identique. Publie dans Nature (Scientific Reports). |
| Nindamani / Open Weeding Delta | [GitHub](https://github.com/AutoRoboCulture/Nindamani-the-weed-removal-robot) | Camera + TensorFlow, bras delta imprime 3D | Concept bras delta pour arrachage cible. Trop complexe pour v0.1. |
| Robot solaire Fresnel (Hackaday) | [Hackaday](https://hackaday.com/2023/06/30/gardening-robot-uses-sunlight-to-incinerate-weeds/) | RPi, TF Lite, lentille Fresnel | Pipeline camera → TF Lite → action fonctionnel sur Pi. Approche thermique originale. |

### 2.2 Navigation et plateformes robotiques

| Projet | URL | Techno | Reutilisable pour Forcair |
|--------|-----|--------|---------------------------|
| **LIAM-ESP** | [GitHub](https://github.com/trycoon/liam-esp) | ESP32, GNSS-RTK, ultrasons | Code navigation ESP32 directement reutilisable. Meme plateforme cible. |
| **ESP32 + micro-ROS ultra low-cost** | [Medium (RoboFoundry)](https://robofoundry.medium.com/) | ESP32, micro-ROS, moteurs N20 | Architecture ideale pour Forcair ESP32-only. Tutoriel pas-a-pas. |
| WEEDINATOR | [Hackaday.io](https://hackaday.io/project/204846-weedinator-2026-agricultural-robot) | STM32 + RPi dual-layer | Architecture 2 niveaux (low-level + high-level) bien documentee. |
| Acorn Rover | [GitHub](https://github.com/Twisted-Fields/acorn-precision-farming-rover) | RPi CM4, Python, 4WD, solaire | Schemas PCB KiCad open-source. Architecture logicielle propre. |
| ROMI Rover (H2020) | [Docs](https://docs.romi-project.eu/Rover/hardware/) | RPi 4, moteurs fauteuil roulant | Moteurs recup + doc hardware complete. Modele open-hardware europeen. |
| OSGAR | [GitHub](https://github.com/robotika/osgar) | Python, ROS-independent | Framework leger navigation autonome, tourne sur RPi Zero. |
| FarmBot | [farm.bot](https://farm.bot/) | RPi 3, Arduino Mega, RAMPS | CNC statique, mais code detection mauvaises herbes et communaute enorme. |

### 2.3 Concepts mecaniques et effecteurs

| Projet | URL | Techno | Reutilisable pour Forcair |
|--------|-----|--------|---------------------------|
| **Aigamo Robot** | [GitHub](https://github.com/takespace/aigamo) | Arduino, moteurs DC, palettes rotatives | Perturbation mecanique passive (remuer/brosser) = adapte aux joints. |
| Nellie | [Instructables](https://www.instructables.com/Nellie-the-Weed-Picking-Robot/) | 3x Arduino, camera Pixy, pince servo | Projet DIY tres budget, logique detection + action instructive. |

### 2.4 Produits commerciaux inspirants

| Produit | Concept | Ce qui inspire Forcair |
|---------|---------|------------------------|
| **Tertill** (discontinue) | Roomba du jardin, solaire, bump & turn, fil coupe | Navigation ultra-simple (bumpers + random walk). Le plus proche de Forcair en philosophie. Discontinue → niche libre. |
| Carbon Robotics LaserWeeder | 8 lasers 150W + IA, 100k herbes/h | Concept destruction thermique ciblee. Version DIY avec petit laser de gravure = piste futur. |
| FarmDroid FD20 | Robot solaire danois, seme + desherbe par GPS | Cartographier les zones "a traiter" vs "a eviter" = applicable a Forcair. |

---

## 3. Papiers scientifiques

### 3.1 Detection par vision / Edge AI

| Ref | Auteurs, Annee | Titre | Venue | Pertinence Forcair |
|-----|---------------|-------|-------|---------------------|
| **R01** | Coleman et al., 2022 | OpenWeedLocator (OWL): an open-source, low-cost device for fallow weed detection | Scientific Reports (Nature), 12, 3017 | **Reference** : algo vert-sur-brun sur RPi, open-source. Green-on-brown → green-on-gray pour paves. [DOI](https://doi.org/10.1038/s41598-021-03858-9) |
| **R02** | Flores et al., 2024 | TinyML Classification for Agriculture Objects with ESP32 | MDPI Digital, 5(4) | CNN TFLite sur ESP32-CAM, ~7.6ms inference. Valide la faisabilite ESP32-CAM pour Forcair. |
| R03 | Almadhor et al., 2025 | Optimized embedded AI: efficient implementation of CNNs on ESP32-CAM | Computing (Springer) | Benchmark CNN sur ESP32-CAM : precision proche du haut de gamme, cout 6x inferieur. |
| R04 | Dworak et al., 2024 | Benchmarking Deep Learning Models for Object Detection on Edge Computing Devices | arXiv:2409.16808 | Benchmark YOLOv8/SSD sur RPi 3/4/5 + Edge TPU. SSD MobileNet V1 = 10ms sur RPi 5 + TPU. |
| R05 | Saltik et al., 2025 | Improving Lightweight Weed Detection via Knowledge Distillation | CVPPA @ ICCV 2025 | YOLO11n sur RPi 5 en 105ms. Distillation +2.5% mAP sans alourdissement. |
| R06 | Sapkota et al., 2025 | Star-YOLO: lightweight model for weed detection in cotton fields | Computers and Electronics in Agriculture | Architecture YOLO ultra-legere, techniques d'allegement transferables. |
| R07 | Nair et al., 2025 | Multiclass weed and crop detection using optimized YOLO models on edge devices | Smart Agricultural Technology | Guide selection modele selon compromis precision/vitesse embarquee. |

### 3.2 Navigation autonome low-cost

| Ref | Auteurs, Annee | Titre | Venue | Pertinence Forcair |
|-----|---------------|-------|-------|---------------------|
| **R08** | Ellouze et al., 2024 | An Autonomous Irrigation Robot Based on ROS2, YOLOv8 and ESP32 WMN Architecture | IEEE MELECON 2024 | **Architecture de reference** : RPi 4 (vision + SLAM) + ESP32 (moteurs via FreeRTOS/Micro-ROS) + ROS2 Nav2. |
| R09 | Pereira et al., 2025 | Hybrid robot navigation: monocular depth estimation and visual odometry | Computers & Electrical Engineering | Navigation mono-camera low-cost, alternative au LiDAR. Applicable RPi Camera. |
| R10 | Bayode et al., 2025 | Low-cost implementation of an autonomous navigation robot with LiDAR using RPi | ResearchGate | SLAM 2D sur RPi + LiDAR low-cost. Realisable pour un petit robot outdoor. |
| R11 | Singh et al., 2025 | Autonomous navigation of ROS2 based Turtlebot3 using intelligent approach | IJIT (Springer) | RL (TD3, DDPG) sur Turtlebot3, framework reproductible pour la couche navigation. |
| **R12** | 2025 | Novel pavement crack detection sensor using coordinated mobile robots | Transportation Research Part C | Detection fissures/joints chaussees par vision → transposable a la detection des joints de paves. |

### 3.3 Desherbage mecanique et thermique sur surfaces dures

| Ref | Auteurs, Annee | Titre | Venue | Pertinence Forcair |
|-----|---------------|-------|-------|---------------------|
| **R13** | Rask & Kristoffersen, 2007 | A review of non-chemical weed control on hard surfaces | Weed Research, 47(5), 370-380 | **Papier de reference** : compare brossage, flambage, eau chaude sur paves. 4-6 brossages/an suffisent. |
| **R14** | Cauwer et al., 2014 | Integrating preventive and curative non-chemical weed control for concrete block pavements | Weed Research, 54(2) | Specifiquement paves autobloquants (= cas Forcair). Preventif + curatif = -50% traitements. |
| R15 | Hansen et al., 2004 | Strategies for non-chemical weed control on public paved areas in Denmark | Pest Management Science, 60(6) | Protocoles et frequences d'intervention validees sur 6 sites danois. |
| R16 | Bauer et al., 2020 | Thermal weed control technologies for conservation agriculture: a review | Weed Research, 60(3) | Temperatures/durees necessaires : >60C pendant quelques secondes. Dimensionnement thermique. |
| R17 | Wie et al., 2024 | Toward Precise Robotic Weed Flaming Using a Mobile Manipulator | arXiv:2407.04929 | Controle de flamme robotisee en exterieur (vent, pression). Adaptable a micro-bruleur. |

### 3.4 Surveys robots desherbeurs

| Ref | Auteurs, Annee | Titre | Venue | Pertinence Forcair |
|-----|---------------|-------|-------|---------------------|
| R18 | Hussain et al., 2024 | Recent Advances in Agricultural Robots for Automated Weeding | AgriEngineering (MDPI), 6(3) | Survey complet : detection + action + navigation. Vue d'ensemble. |
| R19 | Xie et al., 2022 | Key technologies of machine vision for weeding robots: a review | Computers and Electronics in Agriculture | Benchmark modeles vision (CNN, YOLO, Faster R-CNN). Cadre theorique. |
| R20 | Gao et al., 2024 | Advances in ground robotic technologies for site-specific weed management | Computers and Electronics in Agriculture | Robots terrestres de precision. Robovator : +18-41% vs manuel. |
| R21 | Li et al., 2025 | Design of autonomous laser weeding robot based on DIN-LW-YOLO | Computers and Electronics in Agriculture | Robot laser + YOLO allege. mAP 88.5%, taux desherbage 92.6%. |
| R22 | Ghatrehsamani et al., 2023 | Robots and shocks: emerging non-herbicide weed control options | NZ J. Crop & Hort. Science | Comparatif cout/efficacite des methodes non-herbicides emergentes. |

### 3.5 Robotique DIY low-cost

| Ref | Auteurs, Annee | Titre | Venue | Pertinence Forcair |
|-----|---------------|-------|-------|---------------------|
| R23 | FOSSBot, 2022 | An Open Source and Open Design Educational Robot | Electronics (MDPI), 11(16) | Patterns architecture hardware + logiciel pour robot DIY open-source. |
| R24 | 2016 | Combining Raspberry Pi and Arduino for a low-cost autonomous vehicle | IEEE Consumer Electronics | Papier fondateur architecture dual RPi + Arduino (= RPi + ESP32). |

---

## 4. Analyse : ce que la recherche change pour Forcair

### 4.1 Confirmation des choix actuels

La recherche **valide** les choix du design v1 :

| Choix actuel | Validation |
|-------------|------------|
| Brosse rotative nylon | R13, R14 : le brossage est la methode la plus efficace sur surfaces dures. 4-6 passages/an suffisent. |
| Architecture RPi + ESP32 | R08, R24 : architecture dual-processeur standard et validee pour robots autonomes low-cost. |
| Detection HSV (vert sur fond) | R01 (OWL) : algo ExG/HSV publie dans Nature, fonctionne sur RPi, open-source. Green-on-brown → green-on-gray pour paves. |
| Chassis profile alu + impression 3D | Acorn, ROMI, FOSSBot : pattern standard des robots open-hardware. |
| Budget ~75 EUR | ESP32+ROS2 (RoboFoundry) : robot fonctionnel possible a ce budget. |

### 4.2 Insights qui changent la reflexion

| Insight | Source | Impact sur Forcair |
|---------|--------|--------------------|
| **Navigation Tertill (bump & turn)** est suffisante pour petite surface | Tertill, Aigamo | Phase 1 : pas besoin de SLAM, bumpers + random walk suffisent pour 30m2. Economise RPi + LiDAR. |
| **ESP32-CAM peut faire du ML** (7.6ms inference CNN) | R02, R03 | Phase 2 : detection mousse possible sur ESP32-CAM seul, sans RPi. Simplifie la BOM. |
| **Preventif + curatif = -50% passages** | R14 (Cauwer) | Ajouter MOD-003 (spray anti-mousse preventif) en complement de MOD-002 (brosse curative). |
| **Detection de joints par vision** est un probleme resolu (fissures) | R12 | Forcair peut suivre les joints au lieu de brosser a l'aveugle → precision + economie d'energie. |
| **4-6 brossages/an suffisent** | R13 (Rask) | Forcair n'a pas besoin d'etre rapide ni endurant. 1h d'autonomie = largement suffisant. |
| **OSGAR** = framework navigation leger sans ROS | OSGAR | Alternative a ROS2 : plus leger, tourne sur RPi Zero. A evaluer. |
| **Micro-ROS sur ESP32** = standard emergent | R08, ESP32+ROS2 | L'ESP32 peut etre un noeud ROS2 natif via micro-ROS. Futur-proof. |

### 4.3 Pistes nouvelles a considerer

| Piste | Source | Faisabilite Forcair | Priorite |
|-------|--------|---------------------|----------|
| Laser de gravure pour desherbage thermique | Carbon Robotics, R21 | Module MOD-006 futur, securite oculaire critique | Basse (v3+) |
| Panneau solaire pour recharge autonome | Tertill, Acorn, FarmDroid | Petit panneau 5W sur le capot, recharge lente entre missions | Moyenne (v2) |
| Cartographie GPS des zones traitees | FarmDroid | ESP32 + module GPS NEO-6M (~3 EUR), log des zones brossees | Moyenne (v2) |
| Suivi de joints par vision (line following) | R12 (crack detection) | ESP32-CAM HSV → detection joints → brossage cible uniquement | **Haute (v1.5)** |
| Mesh WiFi multi-robots | R08 (Ellouze) | 2+ Forcair coordonnes sur grande surface | Basse (v3+) |

---

## 5. Impact sur la BOM

### 5.1 BOM v1 actuelle vs BOM v1.1 (post-recherche)

La recherche suggere des **simplifications** (retirer des composants) et des **ajouts** (composants peu couteux a fort impact).

#### Composants a RETIRER ou REPORTER

| Composant | BOM v1 | Raison du retrait | Economie |
|-----------|--------|-------------------|----------|
| RPi Zero 2W | Phase 1 | R02/R03 montrent que l'ESP32-CAM suffit pour la detection HSV et meme du CNN. Reporter a Phase 2 si necessaire. | Simplifie le cablage, l'alim (pas de buck 5V dedie), et le dev logiciel. |
| GoPro Hero 3+ (module MOD-001) | Phase 1 | La camera OV2640 de l'ESP32-CAM suffit pour detection mousse (R01, R02). GoPro = overkill pour Phase 1. | Retire un module, simplifie le design. |

> **Note** : RPi et GoPro restent en stock pour Phase 2 (cartographie haute resolution, SLAM). On ne les jette pas, on les reporte.

#### Composants a AJOUTER

| Composant | Pourquoi | Source | Cout estime |
|-----------|----------|--------|-------------|
| 2x capteurs IR obstacle (GP2Y0A21) | Navigation Tertill-style : detect obstacle a 10-80cm. Plus fiable que bumpers mecaniques seuls. | R08, Tertill, LIAM-ESP | ~2 EUR les 2 (AliExpress) |
| 2x micro-switch bumpers | Detection de contact (murs, bordures). Approche Tertill validee. | Tertill | ~1 EUR les 2 (recup ou achat) |
| Module GPS NEO-6M (optionnel Phase 2) | Log des zones traitees, cartographie. Identifie par FarmDroid comme differentiant. | FarmDroid | ~3 EUR (AliExpress) |
| Buzzer piezo | Retour sonore (batterie faible, obstacle, fin de mission). Standard sur les robots open-source. | FOSSBot, LIAM-ESP | ~0.30 EUR |

#### Composants MODIFIES

| Composant | BOM v1 | BOM v1.1 | Raison |
|-----------|--------|----------|--------|
| Motor driver | L298N (double pont H) | **TB6612FNG** ou **DRV8833** | L298N chute 2V et chauffe. TB6612/DRV8833 = MOSFET, rendement 95%, plus petit, meme prix (~2-3 EUR). Recommande par la communaute DIY robotique (RoboFoundry, LIAM-ESP). |
| Moteurs traction | 4x DC recup (5-12V) | Garder recup, mais **prevoir fallback N20 200RPM** | R13 (Rask) : le brossage necessite une pression constante → le robot doit avoir du couple. Moteurs recup a tester en Phase 0. |
| Brosse nylon | Disque perceuse ~60mm | **Brosse coupe fil acier doux 50mm** | R13 : les brosses acier sont plus efficaces sur mousse incrustee. Nylon OK pour entretien leger. Acheter les 2 types (~10 EUR total) pour comparatif Phase 0. |

### 5.2 BOM v1.1 revisee

| Piece | Source | Cout | Changement |
|-------|--------|------|------------|
| 4x profiles 2020 (300+300+250+250mm) | Motedis | Inclus commande partagee | = |
| 4x equerres + fixations | Motedis | Inclus commande partagee | = |
| Plateau contreplaque 5mm | Brico | ~3 EUR | = |
| 4x roues (moyeu PETG + pneu TPU) | Impression 3D | ~4 EUR filament | = |
| 4x roulements 608ZZ | AliExpress | Inclus commande partagee | = |
| 4x coupleurs d'arbre | AliExpress | Inclus commande partagee | = |
| 4x supports moteurs | Impression 3D PETG | ~2 EUR filament | = |
| 4x moteurs DC traction | Recup imprimantes | 0 EUR | = (fallback N20 si trop faibles) |
| Moteur brosse (12.6V DC) | Recup Telsa 80 | 0 EUR | = |
| Brosse nylon perceuse | Brico | ~5 EUR | = |
| **+ Brosse acier doux 50mm** | **Brico** | **~5 EUR** | **NOUVEAU (comparatif Phase 0)** |
| Mecanisme Z (tiges + paliers) | Recup + impression 3D | ~1 EUR | = |
| ESP32-CAM | Stock | 0 EUR | = (devient le processeur principal Phase 1) |
| ~~RPi Zero 2W~~ | ~~Stock~~ | ~~0 EUR~~ | **REPORTE Phase 2** |
| ~~GoPro Hero 3+~~ | ~~Stock~~ | ~~0 EUR~~ | **REPORTE Phase 2** |
| Motor driver **TB6612FNG** | AliExpress | ~3 EUR | **REMPLACE L298N** (meilleur rendement) |
| **2x capteurs IR GP2Y0A21** | **AliExpress** | **~2 EUR** | **NOUVEAU** |
| **2x micro-switch bumpers** | **Recup ou achat** | **~1 EUR** | **NOUVEAU** |
| **Buzzer piezo** | **AliExpress** | **~0.30 EUR** | **NOUVEAU** |
| Batterie 3S (18650 recup ou achat) | Recup Ryobi ou achat | 0-15 EUR | = |
| Capot PETG | Impression 3D | ~3 EUR filament | = |
| **Total Forcair v1.1** | | **~15-30 EUR** | **+~8 EUR vs v1, mais plus robuste** |
| **+ quote-part quincaillerie partagee** | Motedis + AliExpress | **~40 EUR** | = |

### 5.3 BOM Phase 2 (ajouts futurs, deja en stock)

| Piece | Source | Cout | Declencheur |
|-------|--------|------|-------------|
| RPi Zero 2W | Stock | 0 EUR | Si ESP32-CAM insuffisant pour navigation avancee |
| GoPro Hero 3+ | Stock | 0 EUR | Cartographie haute resolution |
| Module GPS NEO-6M | AliExpress | ~3 EUR | Log zones traitees |
| Panneau solaire 5W | AliExpress | ~8 EUR | Recharge autonome entre missions |
| LiDAR RPLIDAR A1 (ou equiv) | AliExpress | ~20 EUR | SLAM 2D si necessaire (probablement pas pour 30m2) |

### 5.4 Impact sur la masse

| Element | Masse v1 | Masse v1.1 | Delta |
|---------|----------|------------|-------|
| Electronique (RPi+ESP32+driver) | ~50g | ~30g (ESP32-CAM + TB6612 seuls) | -20g |
| GoPro + support MOD-001 | ~120g | 0g (reporte) | -120g |
| 2x capteurs IR + bumpers + buzzer | 0g | ~25g | +25g |
| Brosse acier (en plus de nylon) | 0g | ~30g (testee Phase 0, une seule montee) | 0g (choix) |
| **Total** | **~1.4 kg** | **~1.3 kg** | **-115g** |

---

## 6. Architecture logicielle revisee (Phase 1)

La simplification hardware (ESP32-CAM seul) implique une simplification logicielle :

```
     Architecture Phase 1 (simplifiee post-recherche)

     ┌─────────────┐     WiFi      ┌──────────────┐
     │  ESP32-CAM  │◄────────────►│ Mac/Smartphone│
     │             │               │ (monitoring)  │
     │ OV2640 cam  │               └──────────────┘
     │ HSV detect  │
     │ GPIO control│
     └──┬───┬──┬───┘
        │   │  │
   ┌────┘   │  └────────┐
   │        │           │
┌──┴──┐ ┌──┴──┐   ┌────┴────┐
│TB66 │ │Servo│   │IR x2    │
│12FNG│ │ Z   │   │Bumper x2│
│     │ │     │   │Buzzer   │
└┬──┬─┘ └─────┘   └─────────┘
 │  │
4x moteurs DC
```

**Avantage** : un seul firmware a ecrire (ESP32), pas de communication inter-processeurs.
**Algorithme** : OWL simplifie (R01) adapte au vert-sur-gris, directement sur ESP32-CAM.

---

## 7. Strategie de publication (pistes pour papier)

### Angle original identifie

La litterature couvre bien :
- Desherbage agricole robotise (champs, rangs de culture)
- Desherbage thermique/chimique sur surfaces dures (manuellement)

**Gap identifie** : aucun papier ne traite le **desherbage autonome robotise sur surfaces pavees domestiques**.

### Titre de travail

> "Forcair: A Low-Cost Open-Source Autonomous Weeding Robot for Paved Surfaces"

### Contributions potentielles

1. **Adaptation de l'algorithme OWL (green-on-brown) au green-on-gray** pour paves — validation experimentale
2. **Benchmark effecteurs** (brosse nylon vs acier vs thermique) sur paves autobloquants avec metriques quantitatives
3. **Architecture minimale ESP32-CAM only** pour robot de maintenance urbaine < 100 EUR
4. **Protocole d'evaluation** : surface nettoyee/heure, consommation energetique, usure des joints (R13 identifie l'usure comme risque)

### Venues cibles

| Venue | Type | Pourquoi |
|-------|------|---------|
| HardwareX (Elsevier) | Journal open hardware | Publie des designs open-source reproductibles. OWL y est passe. |
| MDPI Electronics / Robotics | Journal open access | Section DIY robotics, peer-reviewed. |
| Hackaday.io | Communaute | Visibilite + feedback communaute avant soumission journal. |
| IEEE MELECON / ICAR | Conference | Si resultats experimentaux solides. |

---

## 8. References completes

### Projets open-source
- [OWL] https://github.com/geezacoleman/OpenWeedLocator
- [Nindamani] https://github.com/AutoRoboCulture/Nindamani-the-weed-removal-robot
- [Aigamo] https://github.com/takespace/aigamo
- [LIAM-ESP] https://github.com/trycoon/liam-esp
- [Acorn] https://github.com/Twisted-Fields/acorn-precision-farming-rover
- [OSGAR] https://github.com/robotika/osgar
- [FarmBot] https://farm.bot/
- [ROMI] https://docs.romi-project.eu/Rover/hardware/
- [WEEDINATOR] https://hackaday.io/project/204846-weedinator-2026-agricultural-robot
- [Nellie] https://www.instructables.com/Nellie-the-Weed-Picking-Robot/
- [ESP32+ROS2] https://robofoundry.medium.com/

### Papiers scientifiques
- [R01] Coleman et al. (2022). Scientific Reports, 12, 3017. doi:10.1038/s41598-021-03858-9
- [R02] Flores et al. (2024). MDPI Digital, 5(4), 48.
- [R03] Almadhor et al. (2025). Computing (Springer). doi:10.1007/s00607-025-01559-z
- [R04] Dworak et al. (2024). arXiv:2409.16808
- [R05] Saltik et al. (2025). CVPPA @ ICCV 2025. arXiv:2507.12344
- [R06] Sapkota et al. (2025). Computers and Electronics in Agriculture.
- [R07] Nair et al. (2025). Smart Agricultural Technology.
- [R08] Ellouze et al. (2024). IEEE MELECON 2024. doi:10.1109/MELECON.2024.10788325
- [R09] Pereira et al. (2025). Computers & Electrical Engineering.
- [R10] Bayode et al. (2025). ResearchGate/392256188
- [R11] Singh et al. (2025). IJIT (Springer). doi:10.1007/s41870-025-02500-5
- [R12] (2025). Transportation Research Part C.
- [R13] Rask & Kristoffersen (2007). Weed Research, 47(5), 370-380.
- [R14] Cauwer et al. (2014). Weed Research, 54(2).
- [R15] Hansen et al. (2004). Pest Management Science, 60(6).
- [R16] Bauer et al. (2020). Weed Research, 60(3).
- [R17] Wie et al. (2024). arXiv:2407.04929
- [R18] Hussain et al. (2024). AgriEngineering (MDPI), 6(3), 187.
- [R19] Xie et al. (2022). Computers and Electronics in Agriculture.
- [R20] Gao et al. (2024). Computers and Electronics in Agriculture.
- [R21] Li et al. (2025). Computers and Electronics in Agriculture.
- [R22] Ghatrehsamani et al. (2023). NZ J. Crop & Hort. Science.
- [R23] FOSSBot (2022). Electronics (MDPI), 11(16), 2606.
- [R24] (2016). IEEE Consumer Electronics Conference.

# Forcair - TODO

> Backlog operationnel du projet. Journal de bord : docs/journal/.
> Estimations (X j) = charge cote Sebastien (jours-homme maker, temps libre).
> Statut global : pre-prototype. Conception figee (design-v1), fabrication non commencee.

## Etat des lieux (2026-05-30)

Fait :
- Etat de l'art (24 papiers, 12+ projets) -> research/state-of-the-art.md
- Design mecanique v1 fige -> hardware/design-v1.md
- CAO parametrique CadQuery : chassis, roues (moyeu+pneu), support moteur,
  capot dome, plaque IMS, MOD-001 camera, MOD-002 brosse, support ESP32-CAM
  (+ exports STEP/STL)
- BOM v1 (BOM.yaml, standard sourcier.shop, FR/EN)
- Identite visuelle : brief + logo + banniere
- Brouillon page Hackaday

A trancher avant fabrication :
- Couple moteurs DC recup suffisant ? (sinon fallback N20 200RPM)
- Type de brosse (nylon vs acier doux) -> sort de la Phase 0
- Robustesse detection HSV a la luminosite variable

## Infra repo (objet de la session du 30/05)

- [x] .gitignore (DS_Store, pycache, secrets ; garde STL/STEP/assets)
- [x] TODO.md a la racine (ce fichier)
- [x] docs/journal/ + premiere entree
- [ ] Creer le depot Gitea seb/forcair sur Ulysse:3000 (0.2 j)
- [ ] Ajouter le remote + premier push (0.1 j)
- [ ] Decider si forcair part aussi en public GitHub SebE585/forcair
      (mentionne dans README/Hackaday mais pas encore cree)
- [ ] Verifier les photos specs/photos/Reception AliExpress (T-Ring/M42 EOS
      = adaptateur photo, a confirmer comme pieces forcair ou a deplacer)

## Phase 0 - Validation actionneur (manuel)

But : valider quel outil demousse les joints sans abimer les paves.

- [ ] Acheter 2-3 brosses perceuse nylon + acier doux 50mm (Brico, ~10 EUR) (0.2 j)
- [ ] Test manuel a la perceuse sur un coin de terrasse (0.3 j)
- [ ] Comparatif nylon vs acier : efficacite vs usure joints (0.3 j)
- [ ] Trancher moteur brosse : Telsa 80 recup vs autre (0.2 j)
- [ ] Photos avant/apres pour build log Hackaday (0.2 j)

**Total Phase 0 : ~1.2 j**

## Phase 1 - Base roulante + vision

But : robot 4WD telecommande qui detecte la mousse par vision.

Mecanique :
- [ ] Commander profiles 2020 + quincaillerie (Motedis + AliExpress) (0.3 j)
- [ ] Couper profiles et assembler le cadre (0.5 j)
- [ ] Demonter imprimantes HS : moteurs DC + tiges lineaires (0.5 j)
- [ ] Imprimer 4 roues (moyeu PETG + pneu TPU) (0.5 j)
- [ ] Imprimer 4 supports moteurs (adapter au moteur recup mesure) (0.3 j)
- [ ] Assembler la base roulante 4WD (0.5 j)

Electronique + firmware :
- [ ] Cabler ESP32-CAM + TB6612FNG + 4 moteurs (0.5 j)
- [ ] Chaine alim : 3S 18650 + buck 5V (0.3 j)
- [ ] Firmware telecommande WiFi (Mac/smartphone) (1.0 j)
- [ ] Pipeline vision : detection mousse HSV vert-sur-gris (OWL simplifie) (1.5 j)
- [ ] Navigation bump & turn (2x IR + 2x bumpers + buzzer) (1.0 j)
- [ ] Cartographie zone (camera embarquee) (0.5 j)

**Total Phase 1 : ~8.7 j**

## Phase 2 - Module nettoyeur

But : brossage asservi a la detection, boucle fermee.

- [ ] Mecanisme axe Z (tiges recup + servo SG90 + ressort pression) (1.0 j)
- [ ] Integrer brosse validee en Phase 0 (MOD-002) (0.5 j)
- [ ] Asservissement : brosse ON seulement sur zone verte (1.0 j)
- [ ] Boucle fermee : verification photo avant/apres passage (0.5 j)

**Total Phase 2 : ~3.0 j**

## Phase 3+ - Pistes (non planifiees)

- Suivi de joints par vision (line following, R12) -- priorite haute v1.5
- Module GPS NEO-6M : log des zones traitees (v2)
- Panneau solaire 5W : recharge entre missions (v2)
- Module spray anti-mousse MOD-003 (preventif + curatif, R14)
- Papier HardwareX / MDPI : robot demousseur de paves domestiques (gap biblio)

## Liens projets

- Depistair : inventaire pieces recup
- Vrillair : usinage pieces custom
- Blindair : rangement composants

# Recup - Fiche de mesure moteur DC (traction)

> A remplir en desossant les vieilles imprimantes.
> Les cotes mesurees se reportent dans hardware/cad/motor_mount.py
> (le support est parametrique) puis on re-exporte le STL.

## Pourquoi mesurer

`motor_mount.py` part de valeurs par defaut (moteur cylindrique 28 mm x 40 mm).
Tes moteurs recup seront differents. Sans mesure, le berceau ne serrera pas bien.

## Cotes a relever (par moteur)

| Cote | Symbole | Variable motor_mount.py | Moteur A | Moteur B | Moteur C | Moteur D |
|------|---------|-------------------------|----------|----------|----------|----------|
| Diametre corps (mm) | D | MOTOR_DIAMETER | | | | |
| Longueur corps (mm) | L | MOTOR_LENGTH | | | | |
| Diametre axe (mm) | d | (coupleur, pas le mount) | | | | |
| Longueur axe utile (mm) | la | | | | | |
| Tension nominale (V) | U | | | | | |
| Source (imprimante) | | | | | | |

Mesure le diametre au pied a coulisse a 2-3 endroits (les moteurs ne sont pas
parfaitement ronds). Prendre le max.

## Verifications

- [ ] Le moteur tourne (test 5-9 V sur une alim de labo ou pile)
- [ ] Sens de rotation reversible (inverser polarite)
- [ ] Couple a vide correct (pas de point dur)
- [ ] Idealement 4 moteurs identiques (sinon : 2+2, gerer en paires G/D)

## Autres recup utiles a sortir en meme temps

- [ ] Tiges lineaires lisses Ø6 ou Ø8 (axe Z + axes roue) -> mesurer le Ø
- [ ] Ressort de rappel (mecanisme Z, pousse-bas)
- [ ] Coupleurs / pignons (transmission axe moteur -> axe roue Ø8 du 608ZZ)
- [ ] Micro-switchs (bumpers Phase 1)

## Apres mesure

1. Editer motor_mount.py : MOTOR_DIAMETER, MOTOR_LENGTH (+ MOTOR_CLEARANCE si besoin).
2. Re-exporter : `python motor_mount.py` (genere cradle + cap STEP/STL).
3. Imprimer 1 support test, valider le serrage avant de lancer les 4.

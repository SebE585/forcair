# Phase 0 - Protocole de test brosse (manuel)

> But : valider que le brossage demousse les joints SANS abimer les paves/joints.
> C'est le go/no-go du projet. Tant que ce test n'est pas concluant, le reste
> (robot, vision, navigation) est premature.
> Reference : Rask & Kristoffersen 2007 (R13) identifie l'usure du joint comme
> le risque principal du brossage mecanique.

## 1. Materiel

| Element | Detail |
|---------|--------|
| Brosse | (a remplir : nylon / acier doux, diametre, forme disque ou coupe) |
| Entrainement | (a remplir : perceuse / visseuse / Dremel / moteur Telsa 80) |
| Vitesse | (a noter si reglable : RPM ou position gachette) |
| EPI | Lunettes obligatoires (projection debris + brins acier), gants |
| Mesure | Telephone (photos) + reglet ou pied a coulisse (profondeur joint) |

## 2. Zones de test

Tester sur plusieurs natures de joint (le terrain en a plusieurs) :

| Zone | Type | Etat mousse initial | Largeur joint |
|------|------|---------------------|---------------|
| Z1 | Paves autobloquants (terrasse) | | ~10 mm |
| Z2 | Dalles carrees (allee) | | ~8 mm |
| Z3 | (abords piscine, si pertinent) | | |

Choisir des zones DISCRETES (coin peu visible) : le test peut marquer le joint.

## 3. Protocole (par zone)

1. **Photo AVANT** (cadrage net, lumiere naturelle, repere d'echelle si possible).
2. Mesurer/noter la profondeur de mousse dans le joint.
3. Brosser : passe lente et reguliere, pression LEGERE d'abord.
4. **Photo APRES** (meme cadrage que l'avant).
5. Inspecter le joint : mousse residuelle ? sable du joint arrache ? pave raye ?
6. Si mousse residuelle : 2e passe, pression accrue, re-noter.
7. Repeter par zone et par reglage (vitesse / pression).

Photos rangees dans `docs/phase-0/photos/` : `Z1_avant.jpg`, `Z1_apres.jpg`, etc.

## 4. Tableau de releve

| Essai | Zone | Brosse | Vitesse | Pression | Passes | Mousse enlevee (%) | Usure joint | Pave abime | Verdict |
|-------|------|--------|---------|----------|--------|--------------------|-----|-----|---------|
| E1 | Z1 | | | legere | 1 | | none/leger/fort | oui/non | |
| E2 | Z1 | | | moyenne | | | | | |
| E3 | Z2 | | | | | | | | |
| E4 | | | | | | | | | |

Echelle usure joint : none = rien / leger = un peu de sable deplace / fort = joint creuse.

## 5. Criteres de decision

GO si, sur au moins une zone :
- mousse enlevee >= ~80 %,
- usure joint = none ou leger (pas de joint creuse, pas de sable massivement arrache),
- aucun pave raye.

A trancher en fin de test :
- [ ] Brosse retenue : nylon / acier / les deux selon la zone
- [ ] Vitesse cible (pour dimensionner le moteur brosse)
- [ ] Pression cible (valide l'approche ressort-pousse-bas du mecanisme Z, design v1.2 section 8.5)
- [ ] Le moteur Telsa 80 a-t-il le couple necessaire ? (sinon revoir l'actionneur)

## 6. Observations libres

(notes, surprises, idees pendant le test)

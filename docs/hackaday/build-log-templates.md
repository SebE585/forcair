# Templates Build Logs Hackaday.io

> Les build logs sont des articles de blog courts postes sur la page projet Hackaday.
> Ils documentent chaque etape du projet. C'est le coeur de la communication.
>
> Format : titre accrocheur + texte court (300-800 mots) + photos/videos + lecon apprise.
> Ton : personnel, technique mais accessible, honnete (montrer les echecs aussi).

---

## Build Log #1 : Phase 0 - "Does a brush even work?"

> A poster DES que le test perceuse + brosse est fait.
> C'est le premier contenu, le plus important. Il valide ou invalide tout le projet.

### Titre
**"Phase 0: Testing brush types on 20-year-old pavers (spoiler: it works)"**

### Contenu (adapter apres le test reel)

```markdown
Before building a robot, I needed to answer one question:
**can a rotating brush actually clean moss from paver joints without
destroying them?**

The scientific literature says yes (Rask & Kristoffersen, 2007 - tested
on Danish public pavers). But my pavers are 20 years old with sand joints,
not mortar. Time to test for real.

#### Setup

I grabbed my Bosch drill and two brush attachments from the hardware store:
- Nylon brush disc, 50mm (~5 EUR)
- Soft steel wire brush disc, 50mm (~5 EUR)

I marked 4 test zones (50x50cm each) on my terrace with masking tape
and took photos before each test.

#### Results

[PHOTO: 4 zones avant]

**Zone A - Nylon, 1 pass:**
[PHOTO avant/apres]
[Description des resultats]

**Zone B - Nylon, 3 passes:**
[PHOTO avant/apres]
[Description des resultats]

**Zone C - Steel wire, 1 pass:**
[PHOTO avant/apres]
[Description des resultats]

**Zone D - Steel wire, 3 passes:**
[PHOTO avant/apres]
[Description des resultats]

#### Joint damage assessment

[PHOTO gros plan des joints apres brossage]
[Description : le sable est-il parti ? Les bords du pave sont-ils abimes ?]

#### Motor requirements

With the drill at [X] RPM, the brush needed [light/moderate/heavy] pressure.
This tells me the robot's brush motor needs approximately [X]W and
the spring pressure on the Z-axis should be around [X]g.

My salvaged Tesla 80 motor runs at ~3000 RPM at 12V, which should be
[sufficient/insufficient] based on this test.

#### What I learned

1. [Lesson 1 - e.g. "Steel wire is overkill for regular maintenance,
   but necessary for neglected pavers"]
2. [Lesson 2 - e.g. "The nylon brush doesn't damage sand joints at all"]
3. [Lesson 3 - e.g. "Debris goes everywhere - confirming I need a
   containment skirt on the robot"]

#### What's next

With the brush approach validated, I'm moving to Phase 1: building the
wheeled base. The aluminum 2020 frame parts are ordered from Motedis.

[PHOTO de l'image concept du robot]

Full project details and CAD files on GitHub: [link]
```

### Photos necessaires (checklist)

- [ ] Vue d'ensemble des 4 zones marquees au ruban
- [ ] Les 2 brosses a cote de la perceuse
- [ ] Zone A avant (vue de dessus, meme angle)
- [ ] Zone A apres
- [ ] Zone B avant
- [ ] Zone B apres
- [ ] Zone C avant
- [ ] Zone C apres
- [ ] Zone D avant
- [ ] Zone D apres
- [ ] Gros plan joint apres brossage acier (dommages ?)
- [ ] Gros plan joint apres brossage nylon (dommages ?)
- [ ] Les debris produits (mousse arrachee)
- [ ] Image concept du robot (la belle image generee)

### Conseils photo
- Meme angle et distance pour chaque avant/apres (poser le smartphone sur un support fixe)
- Lumiere naturelle (pas de flash)
- Inclure une reference d'echelle (piece de monnaie, regle)
- Si possible, video courte (10-20s) du brossage en action

---

## Build Log #2 : "Aluminum bones" (assemblage chassis)

### Titre
**"Phase 1.1: Cutting aluminum and assembling the 2020 frame"**

### Structure
```markdown
The Motedis order arrived: [X]m of 2020 aluminum profile, corner brackets,
T-nuts, and hardware.

#### Cutting the profiles

[PHOTO des barres avant decoupe]

Forcair needs 4 pieces: 300mm (x2) + 250mm (x2) = 1.1m total.
I cut them with [scie a metaux / scie circulaire / dremel].

[PHOTO des 4 pieces decoupees]

Tip: [conseil pratique sur la decoupe]

#### Assembly

[PHOTO assemblage etape par etape]

The corner brackets make this trivially easy - no welding, no glue.
Just T-nuts and M4 bolts. The whole frame assembled in [X] minutes.

[PHOTO du cadre assemble, vu de dessus]

#### Weight check

Frame weight: [X]g (budget was 250g).
[Conforme / Ecart et pourquoi]

#### What's next

Printing the wheels and motor mounts. The TPU tires should be interesting...

[PHOTO du cadre a cote de l'image concept]
```

---

## Build Log #3 : "Rolling on custom wheels" (roues + moteurs)

### Titre
**"Phase 1.2: 3D printed wheels and salvaged printer motors"**

### Structure
```markdown
#### Printing the wheels

[PHOTO plateau impression Bambu Lab]

Each wheel is two parts:
- PETG hub with 608ZZ bearing pocket (1h print)
- TPU 95A tire with tread pattern (45min print)

[PHOTO des pieces imprimees]

The TPU tire press-fits onto the PETG hub. Satisfying click.
[VIDEO courte du montage si possible]

#### Salvaging motors

I dismantled a Canon MG6450 and an Epson XP-2150. [PHOTO des imprimantes]

Inside, each printer yielded [X] DC motors, [X] linear rods, and [X] springs.

[PHOTO des moteurs extraits]

Testing each motor: [voltage, RPM, stall current]

#### First roll

[VIDEO du chassis qui roule pour la premiere fois]

It moves! The TPU tires grip well on dry pavers.
On wet pavers: [observation].

#### Issues found

1. [Probleme rencontre et solution]
2. [Autre probleme]
```

---

## Build Log #4 : "It sees green" (vision ESP32-CAM)

### Titre
**"Phase 1.3: ESP32-CAM detects moss with 10 lines of code"**

### Structure
```markdown
The detection algorithm is deliberately simple: if the camera sees
green pixels on gray background, there's moss.

#### The algorithm

Inspired by OpenWeedLocator (OWL), but adapted for pavers:
- OWL detects green-on-brown (soil)
- Forcair detects green-on-gray (pavers)

[CODE snippet du seuillage HSV]

#### Testing on real pavers

[PHOTO vue camera : paves avec mousse, zones detectees en surbrillance]

Detection rate on my terrace: [X]% true positive, [X]% false positive.

The main false positives are: [feuilles, lichen, ombres vertes...]

#### Running on ESP32-CAM

Frame rate: [X] FPS on the ESP32-CAM with OV2640 at QVGA.
[Sufficient/insufficient] for bump & turn navigation.
```

---

## Build Log #5 : "First autonomous run" (bump & turn)

### Titre
**"Phase 1.5: Forcair's first solo patrol on my terrace"**

> C'est LE build log viral. Premiere video du robot autonome.

### Structure
```markdown
[VIDEO 30-60s du robot en action autonome sur la terrasse]

After [X] weeks of building, Forcair completed its first autonomous
patrol of my 30m2 terrace.

#### How it navigates

Bump & turn (inspired by Tertill and Roomba):
1. Drive forward
2. If IR sensor detects obstacle → turn [random angle]
3. If bumper hits → reverse, turn [larger random angle]
4. If cliff sensor triggers → reverse, turn 180 degrees
5. If camera sees green → lower brush, scrub, raise brush, continue

No SLAM, no GPS, no map. Just simple reactive behavior.

#### Coverage test

I let it run for [X] minutes and tracked its path.
[IMAGE ou PHOTO de la couverture]

Coverage result: [X]% of the terrace surface reached.

#### Cleaning effectiveness

[PHOTO avant/apres d'une zone nettoyee par le robot]

Compared to the Phase 0 drill test:
- Robot brush speed: [X] RPM vs drill: [X] RPM
- Cleaning quality: [comparable / needs more passes / better]

#### Battery life

Started at 12.6V, stopped at 9.6V after [X] minutes.
[Conforme a l'estimation de 1h15 ? Pourquoi l'ecart ?]

#### What went wrong

1. [Probleme 1 et comment je l'ai resolu]
2. [Probleme 2]
3. [Probleme 3]

Honest assessment: it works, but [nuances].

#### What's next

[Plans pour ameliorer / Phase 2]
```

---

## Conseils generaux pour les build logs Hackaday

1. **Poster regulierement** (1x/semaine minimum quand actif). La regularite > la perfection.
2. **Montrer les echecs**. La communaute Hackaday respecte l'honnetete. Un echec documente vaut mieux qu'un succes vague.
3. **Photos > texte**. Chaque etape doit avoir au moins 2-3 photos.
4. **Video courte** pour les moments cles (premiere fois que ca roule, premiere detection, premier nettoyage).
5. **Demander du feedback** en fin de post ("What brush type would you try?", "How would you handle the cliff detection?").
6. **Tagger les projets similaires** et mentionner les inspirations. La communaute apprecie la generosite.
7. **Repondre aux commentaires**. Hackaday est une conversation, pas un blog.
8. **Lien vers GitHub** a chaque post pour les gens qui veulent creuser.

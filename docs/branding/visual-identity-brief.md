# Forcair - Brief Identite Visuelle

> A utiliser avec ChatGPT (DALL-E) ou Midjourney pour generer les assets visuels.
> Date : 2026-04-03

## 1. Positionnement

**Forcair** est un robot desherbeur autonome open-source pour paves et terrasses.
Projet DIY, low-cost (~75 EUR), imprime en 3D, electronique recup.

**Cible** : makers, bricoleurs tech-savvy, communaute open hardware, jardiniers geeks.
**Ton** : technique mais accessible, propre, pas "garage sale". Inspire confiance.
**Reference culturelle** : nomme d'apres le vehicule de Jayce et les Conquerants de la Lumiere (annees 80). Clin d'oeil nostalgique, pas retro.

## 2. Direction artistique

### Palette de couleurs

| Role | Couleur | Hex | Reference |
|------|---------|-----|-----------|
| Primaire | Bleu translucide | #4DA6FF | Le capot PETG bleu translucide du robot |
| Secondaire | Gris anthracite | #2D2D2D | Les profiles aluminium 2020 |
| Accent | Vert mousse | #6B8E23 | La mousse = l'ennemi (et l'ecologie) |
| Fond | Blanc casse | #F5F5F0 | Proprete, lisibilite |
| Texte | Noir doux | #1A1A1A | Lisibilite |

### Typographie
- **Titres** : Space Grotesk (Bold) — geometrique, technique, moderne
- **Corps** : Inter — lisible, neutre, universel
- **Code/specs** : JetBrains Mono — standard dev

### Esprit visuel
- Lignes propres, angles nets (comme les profiles 2020)
- Transparence / X-ray (on voit l'interieur, comme le capot bleu translucide)
- Contraste nature (paves, mousse verte) vs tech (alu, PCB, LED)
- Pas de rendu 3D ultra-realiste → plutot style "blueprint technique" ou "photo atelier propre"

## 3. Prompts ChatGPT / DALL-E

### 3.1 Logo principal

```
Prompt DALL-E :
"Minimalist logo for 'Forcair', an open-source autonomous weeding robot.
The logo combines a small wheeled robot silhouette with a circular brush
underneath. Clean geometric lines, inspired by aluminum extrusion profiles.
Color: translucent blue (#4DA6FF) on white background.
Style: flat vector, no gradients, technical/engineering aesthetic.
The robot silhouette should be compact, low-profile, with 4 wheels visible
from a 3/4 top-down view. A subtle circular motion line around the brush
suggests rotation. No text in the image."
```

```
Variante avec texte :
"Same logo as above, with the word 'FORCAIR' in Space Grotesk Bold font
to the right of the icon. Below in smaller text: 'open-source paver weeding robot'.
Translucent blue and dark gray color scheme."
```

### 3.2 Logo icone (favicon / avatar GitHub)

```
Prompt DALL-E :
"Square icon logo for a robotics project called Forcair. A top-down view
of a small square robot with 4 wheels at the corners, seen from above,
with a rotating brush circle visible underneath through a translucent blue
shell. Minimalist, flat vector style, single color: translucent blue on
dark gray background. 512x512px, suitable as GitHub avatar or favicon."
```

### 3.3 Banniere GitHub / Hackaday (1280x640)

```
Prompt DALL-E :
"Wide banner image (2:1 ratio) for an open-source robotics project.
Left side: a close-up photo-realistic render of interlocking concrete pavers
with green moss growing in the joints, outdoor sunlight.
Right side: a clean technical blueprint/schematic of a small 4-wheeled robot
with a rotating brush underneath, drawn in translucent blue lines on dark
gray background. The two halves blend in the middle.
Style: split between nature/problem (left) and tech/solution (right).
Clean, modern, professional. No text."
```

```
Variante avec texte :
"Same split composition. Overlaid text in the center:
'FORCAIR' in large white Space Grotesk Bold,
below: 'Open-Source Autonomous Paver Weeding Robot' in smaller white text.
Below that: small icons for GitHub, 3D printer, ESP32 chip."
```

### 3.4 Photo concept "hero shot"

```
Prompt DALL-E :
"Photo-realistic render of a small autonomous robot on a patio of
interlocking concrete pavers with moss in the joints. The robot is compact
(30x25x10cm), has an aluminum frame made of 20x20mm extrusion profiles,
4 black rubber wheels, and a translucent blue dome shell on top through
which green PCB boards and electronic components are visible inside.
A small rotating brush is visible underneath the robot, actively cleaning
moss from a paver joint. Golden hour outdoor lighting, shallow depth of field.
The surrounding pavers show the contrast between cleaned joints (gray, clean)
and uncleaned joints (green moss). Style: product photography, editorial."
```

### 3.5 Illustration "avant / apres"

```
Prompt DALL-E :
"Split image showing a before/after comparison of concrete interlocking
pavers. Left side labeled 'BEFORE': pavers with heavy green moss growth
in all joints, looking neglected. Right side labeled 'AFTER': same pavers
but joints are perfectly clean, gray, no moss. A subtle translucent blue
robot silhouette is positioned at the dividing line between the two sides,
as if it's cleaning from left to right. Clean, bright, outdoor photography style."
```

### 3.6 Schema technique stylise (pour README)

```
Prompt DALL-E :
"Technical exploded view diagram of a small wheeled robot on a white
background. The robot has 4 layers shown separated vertically:
1. Bottom: 4 wheels with motors on aluminum frame rails
2. Middle: plywood platform with battery and motor driver board
3. Upper: ESP32-CAM module and sensors
4. Top: translucent blue dome cover
Style: technical illustration, isometric view, thin clean lines,
minimal color (blue for dome, green for PCBs, gray for aluminum).
Blueprint aesthetic, numbered callout lines pointing to each component.
No text labels (those will be added later)."
```

## 3.7 IMPORTANT : image concept existante

L'image `specs/concept-forcair-v1.jpg` est deja excellente et definit le ton visuel :
- Robot compact sur paves authentiques
- Capot bleu translucide avec PCB visibles
- Brosse en action sur les joints
- Golden hour, profondeur de champ
- Piscine en arriere-plan (contexte terrasse domestique)

**Utiliser cette image comme reference** dans tous les prompts ChatGPT :
ajouter "Use this reference image for the robot's appearance and visual style"
et uploader l'image en meme temps que le prompt.

Les nouvelles images generees doivent etre **coherentes** avec cette reference.

## 4. Assets a generer (checklist)

| Asset | Format | Usage | Priorite |
|-------|--------|-------|----------|
| Logo principal (avec texte) | PNG 1024px + SVG | README, Hackaday, partout | **P0** |
| Logo icone (carre) | PNG 512px | GitHub avatar, favicon | **P0** |
| Banniere (avec texte) | PNG 1280x640 | Header GitHub, Hackaday | **P0** |
| Hero shot (robot sur paves) | PNG 1920px | README, site, reseaux | P1 |
| Avant/apres illustration | PNG 1280px | Hackaday build log Phase 0 | P1 |
| Schema technique eclate | PNG 1920px | README, documentation | P1 |
| Open Graph image | PNG 1200x630 | Apercu liens partages (Slack, Twitter) | P2 |

## 5. Elements textuels de marque

### Tagline (une phrase)
> **"The open-source robot that cleans your patio while you relax."**

### Tagline FR
> **"Le robot open-source qui desherbe vos paves pendant que vous vous reposez."**

### Description courte (README, Hackaday)
> Forcair is a low-cost (<100 EUR), open-source autonomous robot that removes
> moss and weeds from paved surfaces. Built with aluminum extrusion profiles,
> 3D printed parts, and an ESP32-CAM. Named after a vehicle from *Jayce and
> the Wheeled Warriors*.

### Pitch en 3 lignes
> 1. Moss between your pavers? Meet Forcair.
> 2. A 1.3kg autonomous robot with a rotating brush, ESP32 vision, and bump & turn navigation.
> 3. Fully open-source hardware and software. Build yours for under 100 EUR.

## 6. Usage des assets

- **GitHub** : logo icone (avatar) + banniere (social preview) + hero shot (README)
- **Hackaday.io** : logo + banniere + photos relles de build (pas de rendus)
- **Papier HardwareX** : schema technique eclate + photos reelles de tests
- **Reseaux sociaux** : hero shot + avant/apres + tagline

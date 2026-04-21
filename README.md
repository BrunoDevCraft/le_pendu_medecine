# Le Pendu — Médecine v0.2 (Web)
**BrunoDevCraft · Licence MIT**

---

## Structure du projet

```
le_pendu_medecine/
├── index.html
├── css/
│   └── style.css
├── js/
│   ├── words.js      ← Dictionnaire médical (160+ mots)
│   └── game.js       ← Logique du jeu
└── assets/
    ├── images/       ← Vos images ici (voir ci-dessous)
    ├── sounds/       ← Vos sons ici (voir ci-dessous)
    └── dico/         ← Dictionnaire JSON optionnel (extension future)
```

---

## Images à placer dans `assets/images/`

| Nom de fichier       | Usage                                      |
|----------------------|--------------------------------------------|
| `niveau_01.jpg`      | Image bonus niveau 1 (après 5 victoires)   |
| `niveau_02.jpg`      | Image bonus niveau 2 (après 10 victoires)  |
| `niveau_03.jpg`      | Image bonus niveau 3 (après 15 victoires)  |
| `niveau_04.jpg`      | Image bonus niveau 4 (après 20 victoires)  |
| `niveau_05.jpg`      | Image bonus niveau 5 (après 25 victoires)  |
| `niveau_06.jpg`      | Image bonus niveau 6 (après 30 victoires)  |

> Formats acceptés : `.jpg`, `.jpeg`, `.png`, `.webp`  
> Si une image est absente, un placeholder s'affiche automatiquement.

---

## Sons à placer dans `assets/sounds/`

| Nom de fichier     | Usage                         |
|--------------------|-------------------------------|
| `background.mp3`   | Musique de fond (en boucle)   |
| `victory.mp3`      | Son de victoire               |
| `defeat.mp3`       | Son de défaite                |
| `correct.mp3`      | Lettre correcte               |
| `wrong.mp3`        | Lettre incorrecte             |
| `click.mp3`        | Clic bouton (optionnel)       |

> Formats acceptés : `.mp3`, `.ogg`, `.wav`  
> Tous les sons sont **optionnels** — le jeu fonctionne sans eux.

---

## Comment jouer

1. Ouvrir `index.html` dans un navigateur (Chrome, Firefox, Edge…)
2. Cliquer ou appuyer sur une touche pour démarrer
3. Deviner les lettres du terme médical via le clavier à l'écran ou le clavier physique
4. Maximum 6 erreurs par mot avant la défaite
5. 3 vies au total — perdez-les toutes et c'est la fin de partie
6. Toutes les 5 victoires, un écran bonus s'affiche avec votre image

---

## Personnalisation

### Ajouter des mots au dictionnaire
Éditez `js/words.js` et ajoutez des entrées dans le tableau `WORDS_DATA` :

```js
{ word: "votre_mot", definition: "La définition ici", category: "Catégorie" },
```

### Modifier le nombre de vies ou d'essais
Éditez `js/game.js`, section `CONFIG` en haut du fichier :

```js
const CONFIG = {
  maxAttempts:  6,   // Erreurs maximum par mot
  initialLives: 3,   // Vies au départ
  bonusEvery:   5,   // Écran bonus toutes les N victoires
  ...
};
```

---

## Crédits images & sons
- Images libres de droit : https://pixabay.com/fr/ · https://www.istockphoto.com/fr/
- Sons libres de droit : https://pixabay.com/fr/

---

*Distribué sous licence MIT — © 2024 BrunoDevCraft*

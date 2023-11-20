Jeu du Pendu en médecine

Attention: Certains antivirus détecte l'exécutable du jeu pour "Windows10" comme un faux postif!
	   Tester avec "Virustotal.com" le 16/11/2023, sur les 72 antivirus, seul 4 le classe comme suspect dont Avast, Zillya, Bkav Pro, AVG.
	   Concernant le fichier Le_pendu_medecine_V2.py, ce dernier ayant subi le même test, il n'y a aucun antivirus le détectant comme suspect.

I°) Description
	Le jeu "Le_pendu_medecine_0.1.exe" est une application simple qui vous permet de jouer au célèbre jeu du pendu. Devinez les mots pour éviter de faire pendre le personnage.

II°) Prérequis
	- Python 3.x
	- Pygame library (installez avec `pip install pygame`)

III°) Comment jouer
	
	 1. Pour lancer le jeu sur Ubuntu (linux);
		Solution 1 :	
			Ouvrir un terminal, puis entrer les lignes:
			cd 'chemin où vous avez enregistré le dossier contenant le jeu sur votre ordinateur' (Validez par 'entrer')
			python3 ./le_pendu_medecine_0.1.py (Validez par "entrer")

	    	Solution 2 (fonctionnelle):
			Installer VS code sur votr machine, puis les dépendances nécessaire au jeu tel que pygame, random, textwrap via: pip install 'nom du module'.
			
	
	2. Appuyez sur une touche ou cliquez pour commencer le jeu après l'écran de titre.
	3. Devinez les lettres pour compléter le mot et éviter de perdre des vies.
	4. Gagnez des images en devinant correctement et en terminant les niveaux bonus.
	5. Appuyez sur "Continuer" pour passer au niveau suivant ou sur "Fermer" pour quitter le jeu.

IV°) Structure du code
	- `pendu.py`: Le fichier principal contenant le code du jeu.
	- `assets/`: Dossier contenant les images, la musique et les fichiers audio.
	- `assets/dictionnaire/mots.txt`: Fichier texte contenant la liste des mots utilisés dans le jeu.
	- `assets/annexe/`: informations complémentaire

V°) Contrôles
	- Utilisez les touches du clavier pour deviner les lettres.
	- Cliquez sur les boutons "Continuer" ou "Fermer" lorsqu'ils apparaissent à la fin du jeu.

VI°) Remarques
	- Le jeu comporte des niveaux bonus toutes les 5 victoires.
	- Assurez-vous d'avoir le volume activé pour profiter de la musique du jeu.

VII°) Crédits
	- Les fichiers ont été sélectionné sur les sites libre de droit et gratuit suivant:
		- Images:https://pixabay.com/fr/
		       https://www.istockphoto.com/fr/
		- Musiques:https://pixabay.com/fr/ 

VIII°) Licence
Ce jeu est distribué sous la licence de projet open-source MIT.

---

Auteur: BrunoDevCraft 


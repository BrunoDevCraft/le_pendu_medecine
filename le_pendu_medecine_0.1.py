#!/usr/bin/env python3

# -*- coding: utf-8 -*-

import os
import pygame
import random
import sys
import textwrap

# Initialisation de Pygame
pygame.init()

# Ajout de ces lignes pour définir la clock
clock = pygame.time.Clock()
FPS = 60  # Définissez le framerate cible, par exemple, 60 images par seconde pour une meilleure fluidité du jeu

# Définition des couleurs
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 128, 0)

# Définition de la fenêtre
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jeu du Pendu")

# Chargement des images du pendu (dans la boucle pour le rafraîchissement sur l'écran bonus)
script_dir = os.path.dirname(__file__)
assets_dir = os.path.join(script_dir, 'assets')
pendu_images = [pygame.image.load(os.path.join(assets_dir, f"images/pendu{i}.png")) for i in range(7)]

# Chargez l'image de fond pour l'écran intermédiaire du choix
bg_continue_screen_path = os.path.join(assets_dir, 'images/Continue_00.jpg')
bg_continue_screen = pygame.image.load(bg_continue_screen_path)

# Liste des images bonus
bonus_images = [
    os.path.join(assets_dir,"images/niveau_01.jpg"),
    os.path.join(assets_dir,"images/niveau_02.jpg"),
    os.path.join(assets_dir,"images/niveau_03.jpg"),
    os.path.join(assets_dir,"images/niveau_04.jpg"),
    os.path.join(assets_dir,"images/niveau_05.jpg"),
    os.path.join(assets_dir,"images/niveau_06.jpg"),
]

# Initialisez l'indice de l'image bonus actuelle
current_bonus_index = 0

# Chargement de la liste de mots à partir d'un fichier séparé
with open(os.path.join(assets_dir,"dictionnaire/mots.txt"), "r") as file:
    words = [line.strip().split(":") for line in file.readlines()]

# Sélection d'un mot aléatoire parmi la liste du dictionnaire
random_word, definition = random.choice(words)

# Initialisation des variables du jeu
score = 0
correct_letters = set()
incorrect_letters = set()
incorrect_letters_set = set()  # Nouvelle variable pour suivre les lettres incorrectes déjà identifiées
attempts = 0
defeat_count = 0
victories = 0 # Variable pour suivre le nombre de victoires
show_bonus_screen = False # Variable pour contrôler l'affichage de l'écran bonus

# Variables pour gérer l'affichage de l'image "fin_00.jpg"
show_dead_image = False
start_time_dead_image = 0

# Variables au début du jeu pour définir le nombre de vies initial
initial_lives = 3
lives = 3

# Variables pour définir la police et la surface de texte pour afficher le nombre de vies
lives_font = pygame.font.Font(None, 36)
lives_surface = lives_font.render(f"Vies: {lives}", True, BLACK)
lives_rect = lives_surface.get_rect(topleft=(WIDTH - 120, 10))

# Variables pour afficher le nombre de vies dans la boucle principale
win.blit(lives_surface, lives_rect.topleft)

# Police de caractères
font = pygame.font.Font(None, 36)

# Surface de texte pour afficher le score
score_surface = font.render(f"Score: {score}", True, BLACK)
score_rect = score_surface.get_rect(topleft=(10, 10))

# Déclaration des rectangles des boutons de l'écran intermédiaire
continue_rect = pygame.Rect(0, 0, 0, 0)
close_rect = pygame.Rect(0, 0, 0, 0)

# Chargement de la musique à l'extérieur de la boucle principale
pygame.mixer.init()
pygame.mixer.music.load(os.path.join(assets_dir,"sounds/follow-the-leader-action-trailer-glitch-intro-146760.mp3"))
pygame.mixer.music.set_volume(0.5)  # Réglez le volume selon vos besoins

# Initialisation de la musique de victoire
victory_sound = pygame.mixer.Sound(os.path.join(assets_dir,"sounds/happy-summer-long-10627.mp3"))
# Chargement de la musique de défaite
defeat_sound = pygame.mixer.Sound(os.path.join(assets_dir,"sounds/dramatic-atmosphere-with-piano-and-violin-143149.mp3"))

# Jouez la musique de présentation en dehors de la boucle principale
pygame.mixer.music.play(-1)  # -1 pour répéter en boucle

# Fonction pour afficher le message de victoire ou de défaite en plein écran
def display_fullscreen_message(message, game_over=False):
    win.fill(WHITE)
    
    # Affichez l'image de fin de jeu
    game_image = pygame.image.load(os.path.join(assets_dir, f"images/game_over.png")) if game_over else pygame.image.load(os.path.join(assets_dir, f"images/game_win.png"))
    game_rect = game_image.get_rect(center=(WIDTH // 2, HEIGHT // 1.75))
    win.blit(game_image, game_rect.topleft)
    
    # Affichez le message au-dessus de l'image
    message_surface = font.render(message, True, RED)
    message_rect = message_surface.get_rect(center=(WIDTH // 2, HEIGHT // 3))
    win.blit(message_surface, message_rect.topleft)
    
    pygame.display.update()
    pygame.time.delay(2000)

# Fonction pour afficher l'écran de présentation
def display_title_screen():
    win.fill(WHITE)

    # Titre du jeu
    title_font = pygame.font.Font(None, 72)
    title_surface = title_font.render("Le Pendu", True, BLACK)
    win.blit(title_surface, (WIDTH // 2 - title_surface.get_width() // 2, 70))

    # Chargez une image depuis un fichier
    image = pygame.image.load(os.path.join(assets_dir, "images/corde_pendu.png"))

    # Affichez l'image à la position souhaitée
    win.blit(image, (305, 160))

    # Bouton "START"
    start_font = pygame.font.Font(None, 48)
    start_surface = start_font.render("START", True, BLACK)
    start_rect = start_surface.get_rect(center=(WIDTH // 2.05, 525))
    pygame.draw.rect(win, WHITE, start_rect)
    win.blit(start_surface, start_rect.topleft)
    pygame.display.update()
  
# Fonction pour afficher l'écran de fin
def display_end_screen():
    global continue_rect, close_rect
    
    win.blit(bg_continue_screen, (0, 0)) # Remplacez la couleur de fond blanche par l'image de fond

    # Message de l'écran intermédiaire
    end_message_font = pygame.font.Font(None, 48)
    end_message_surface = end_message_font.render("Partie terminée ?", True, WHITE)
    end_message_rect = end_message_surface.get_rect(center=(WIDTH // 2 - 135, HEIGHT // 3))
    win.blit(end_message_surface, end_message_rect.topleft)

    # Bouton "Continuer" et "Fermer"
    button_font = pygame.font.Font(None, 36)
    
    continue_surface = button_font.render("Continuer", True, BLACK)
    continue_rect = continue_surface.get_rect(center=(WIDTH // 2 -150, HEIGHT // 2))
    pygame.draw.rect(win, WHITE, continue_rect)
    win.blit(continue_surface, continue_rect.topleft)
    
    close_surface = button_font.render("Fermer", True, BLACK)
    close_rect = close_surface.get_rect(center=(WIDTH // 2 - 150, HEIGHT // 1.5))
    pygame.draw.rect(win, WHITE, close_rect)
    win.blit(close_surface, close_rect.topleft)

    pygame.display.update()

# Boucle principale du jeu
show_title_screen = True
running = True

# Appel initial pour afficher l'écran de présentation
display_title_screen()

while running:
    # Réinitialisation des variables du jeu au début de chaque itération de la boucle
    incorrect_letters_set = set()  # Réinitialisation de incorrect_letters_set
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if show_title_screen:
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                show_title_screen = False  # Passer à la phase de jeu
                pygame.mixer.music.stop()  # Arrêtez la musique lorsque le jeu commence
                display_title_screen()  # Afficher l'écran de titre une fois au début
                pygame.time.delay(250)  # Laisser l'écran de titre affiché pendant 2 secondes
                               
    # Phase de jeu (pendant le jeu proprement dit)
        if not show_title_screen:
            if lives > 0:  # Ajoutez cette condition pour vérifier si le joueur a encore des vies
                if event.type == pygame.KEYDOWN:
                    if event.unicode.isalpha():
                        letter = event.unicode.lower()
                        if event.unicode.isupper():
                            # La lettre est en majuscule
                            print(f"Lettre en majuscule détectée: {letter}")
                        if letter in correct_letters or letter in incorrect_letters:
                            # La lettre a déjà été choisie (correcte ou incorrecte), ignorez-la
                            continue
                        if letter in random_word.lower():  # Convertissez le mot à deviner en minuscules:
                            correct_letters.add(letter)
                    
                        else:
                            # La lettre est incorrecte
                            incorrect_letters.add(letter)
                            incorrect_letters_set.add(letter)  # Ajoutez la lettre à l'ensemble des lettres incorrectes identifiées
                            attempts += 1
                win.fill(WHITE)
                    
                # Variables pour mettre à jour et afficher le nombre de vies dans la boucle principale
                lives_surface = lives_font.render(f"Vies: {lives}", True, BLACK)
                win.blit(lives_surface, lives_rect.topleft)
                
                # Affichage du mot à deviner
                word_display = ""
                for letter in random_word:
                    if letter == " ":
                        # Ajouter un espace directement à word_display pour les espaces dans le mot réel
                        word_display += " "
                    else:
                        # Afficher la lettre si elle a été correctement devinée, sinon afficher un underscore
                        word_display += letter if letter.lower() in correct_letters else "_ "
                
                word_surface = font.render(word_display, True, BLACK)
                win.blit(word_surface, (WIDTH // 2 - word_surface.get_width() // 2, 100))

                # Affichage de la définition du mot
                definition_surface = font.render("", True, BLACK)
                definition_rect = definition_surface.get_rect(center=(WIDTH // 2, 150))
        
                # Adapter la définition en plusieurs lignes si nécessaire
                wrapped_definition = textwrap.fill(definition, width=40)
                for i, line in enumerate(wrapped_definition.split('\n')):
                    line_surface = font.render(line, True, BLACK)
                    win.blit(line_surface, (definition_rect.centerx - line_surface.get_width() // 2, definition_rect.centery + i * 30))
        
                # Affichage des lettres incorrectes
                incorrect_surface = font.render("Lettres incorrectes: " + " ".join(incorrect_letters), True, RED)
                win.blit(incorrect_surface, (10, 500))

                # Affichage du pendu
                win.blit(pendu_images[attempts], (270, 270))

                # Vérification de la victoire ou de la défaite
                if set([letter for letter in random_word.lower() if letter.isalpha()]) == correct_letters:
                    victories += 1  # Incrémenter le nombre de victoires
                    score += 1  # Incrémenter le score
                    score_surface = font.render(f"Score: {score}", True, BLACK)
                    victory_sound.play()  # Jouer la musique de victoire
                    display_fullscreen_message("You Win!")
                    display_end_screen()
            
                    # Afficher l'écran bonus toutes les 5 victoires
                    if victories % 5 == 0:
                        show_bonus_screen = True
          
                    waiting_for_input = True
                    while waiting_for_input:
                        for event in pygame.event.get():
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                mouse_x, mouse_y = pygame.mouse.get_pos()
                                if continue_rect.collidepoint(mouse_x, mouse_y):
                                    # L'utilisateur a appuyé sur "Continuer"
                                    waiting_for_input = False
                                    victory_sound.stop()  # Arrêter la musique de victoire
                                    # Réinitialiser les variables du jeu
                                    correct_letters = set()
                                    incorrect_letters = set()
                                    attempts = 0
                                    random_word, definition = random.choice(words)
                                    score_surface = font.render(f"Score: {score}", True, BLACK)  # Mettre à jour la surface du score
                                elif close_rect.collidepoint(mouse_x, mouse_y):
                                    # L'utilisateur a appuyé sur "Fermer"
                                    running = False
                                    waiting_for_input = False
                                    victory_sound.stop()  # Arrêter la musique de victoire
                            elif event.type == pygame.QUIT:
                                running = False
                                waiting_for_input = False
                        pygame.time.delay(100)
                
                elif attempts >= 6 or lives <= 0:
                    defeat_count += 1
                    lives -= 1
        
                    display_fullscreen_message("You Lose!", game_over=True)
                    defeat_sound.play()  # Jouer la musique de défaite
                    display_end_screen()
            
                    waiting_for_input = True
                    while waiting_for_input:
                        for event in pygame.event.get():
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                mouse_x, mouse_y = pygame.mouse.get_pos()
                                if continue_rect.collidepoint(mouse_x, mouse_y):
                                    # L'utilisateur a appuyé sur "Continuer"
                                    waiting_for_input = False
                                    defeat_sound.stop()  # Arrêter la musique de défaite
                                    # Réinitialiser les variables du jeu
                                    correct_letters = set()
                                    incorrect_letters = set()
                                    attempts = 0
                                    random_word, definition = random.choice(words)
                                elif close_rect.collidepoint(mouse_x, mouse_y):
                                    # L'utilisateur a appuyé sur "Fermer"
                                    running = False
                                    waiting_for_input = False
                            elif event.type == pygame.QUIT:
                                running = False
                                waiting_for_input = False
                        pygame.time.delay(100)
            
                    else:
                        # Le joueur a perdu toutes ses vies, afficher l'image "fin_00.jpg"
                        if lives <= 0:
                            win.fill(WHITE)
                            dead_image = pygame.image.load(os.path.join(assets_dir, "images/fin_00.jpg"))
                            dead_rect = dead_image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                            win.blit(dead_image, dead_rect.topleft)
                    
                            defeat_sound.play()  # Jouer la musique de défaite
                    
                            pygame.display.update()

                            # Attendre pendant quelques secondes avant de quitter le jeu
                            pygame.time.delay(10000)  # 5 secondes en millisecondes
                            pygame.quit()
                            running = False
                
                # Mettre à jour l'affichage du score dans la boucle principale
                win.blit(score_surface, score_rect.topleft)     
                pygame.display.flip()  # Mettez à jour l'affichage complet de la fenêtre
                clock.tick(FPS)  # Mise à jour du jeu à un framerate constant

                # Affichez l'écran bonus après 5, 10, 15, etc. victoires
                if show_bonus_screen:
                    win.fill(WHITE)

                    # Choisissez une image bonus /aléatoire
                    bonus_image_path = bonus_images[current_bonus_index]
                    #bonus_image_path = random.choice(bonus_images)
                    bonus_image = pygame.image.load(bonus_image_path)
                    bonus_rect = bonus_image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                    win.blit(bonus_image, bonus_rect.topleft)
        
                    # Incrémentez l'indice de l'image bonus actuelle
                    current_bonus_index = (current_bonus_index + 1) % len(bonus_images)
            
                    # Affichez le message au-dessus de l'image
                    bonus_message_surface = font.render(f"Niveau {victories // 5} réussi ! Passer au niveau suivant ?", True, GREEN)
                    bonus_message_rect = bonus_message_surface.get_rect(center=(WIDTH // 2 + 35, HEIGHT // 4 + 125))
                    win.blit(bonus_message_surface, bonus_message_rect.topleft)

                    # Boutons "OUI" et "NON"
                    button_font = pygame.font.Font(None, 34)

                    # Bouton OUI
                    yes_surface = button_font.render("OUI", True, BLACK)
                    yes_rect = yes_surface.get_rect(center=(WIDTH // 2 - 180, HEIGHT // 1.75))
                    pygame.draw.rect(win, WHITE, yes_rect)
                    pygame.draw.rect(win, BLACK, yes_rect, 2)  # Ajout d'une bordure
                    win.blit(yes_surface, yes_rect.topleft)

                    # Bouton NON
                    no_surface = button_font.render("NON = Fermer", True, BLACK)
                    no_rect = no_surface.get_rect(center=(WIDTH // 2 + 175, HEIGHT // 1.75))
                    pygame.draw.rect(win, WHITE, no_rect)
                    pygame.draw.rect(win, BLACK, no_rect, 2)  # Ajout d'une bordure
                    win.blit(no_surface, no_rect.topleft)

                    pygame.display.update()

                    waiting_for_input = True
                    while waiting_for_input:
                        for event in pygame.event.get():
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                mouse_x, mouse_y = pygame.mouse.get_pos()
                            if yes_rect.collidepoint(mouse_x, mouse_y):
                                # L'utilisateur a appuyé sur "OUI"
                                waiting_for_input = False
                                show_bonus_screen = False  # Revenir à la boucle principale du jeu
                                # Ajoutez ici le code pour passer au niveau suivant si nécessaire (optionnel)
                            elif no_rect.collidepoint(mouse_x, mouse_y):
                                # L'utilisateur a appuyé sur "NON"
                                pygame.quit()

                            elif event.type == pygame.QUIT:
                                running = False
                                waiting_for_input = False

                        pygame.time.delay(100)

# Quand le jeu se termine, quittez Pygame et terminez le programme
pygame.quit()
sys.exit()
#########################################
# groupe 3 MPCI 5
# Anthonin Le nevez
# Kaïs Cheboub
# Anessa Diallo
# Enzo Reale
# Phkar Romdoul
#
#########################################


import tkinter as tk
import random

##################
# Constantes

LARGEUR = 300
HAUTEUR = 300

# Variable


PLACEMENT = True
Joueur = 0

T = [3*[0] for i in range(3)]

###################
# Fonctions

def grille():
    """Creation de la grille de jeu"""
    global LARGEUR, HAUTEUR
    """creation de l'arrière plan"""
    canvas.create_rectangle(100,100, 300, 300, fill='grey')
    for i in range (100, LARGEUR+100, 100):
        """creation des lignes horizontales et verticales"""
        canvas.create_line(i, 100, i, 300) #Creation des lignes Verticales
        canvas.create_line(100, i, 300, i) #Creation des lignes Horizontales
    for i in range (100, LARGEUR+100, 100):
        for j in range (100, HAUTEUR+100, 100):
            """creation des lignes diagonnales et des points de croisement"""
            canvas.create_line(200, 200, i, j) #Creation des lignes Diagonnales
            canvas.create_oval(i-10, j-10, i+10, j+10) #Creation des point de croisement

def tour():
    """Defini un tour de jeu"""
    global Joueur, T
    if Joueur == 0 :
        if PLACEMENT == True:
            canvas.bind("<Button-1>", place_pion) #Lance la fonction "place_pion" avec l'evenement clic gauche
        else :
            xt, yt = canvas.bind("<Button-1>", recupère_pion) #Lance la fonction "recupère_pion" avec l'evenement clic gauche
            print(xt, yt)
            canvas.bind("<Button-1>", xt, yt, replace_pion) #Lance la fonction "replace_pion" avec l'evenement clic gauche
    else :
        if PLACEMENT == True:
            canvas.bind("<Button-1>", place_pion) #Lance la fonction "place_pion" avec l'evenement clic gauche
        else :
            xt, yt = canvas.bind("<Button-1>", recupère_pion) #Lance la fonction "recupère_pion" avec l'evenement clic gauche
            print(xt, yt)
            canvas.bind("<Button-1>", xt, yt, replace_pion) #Lance la fonction "replace_pion" avec l'evenement clic gauche
    
def recupère_pion(event):
    global HAUTEUR, LARGEUR, Joueur, T
    x, y = event.x, event.y #Coordonée du point cliqué
    """ Parcour le terrain de jeu """
    for i in range (100, LARGEUR+100, 100):
        for j in range (100, HAUTEUR+100, 100):
            if i-10 <= x and x <= i+10 and j-10 <= y and y <= j+10:
                if Joueur == 0 and  T[(i//100)-1][(j//100)-1] == 2 :
                    return i//100, j//100
                elif Joueur == 1 and T[(i//100)-1][(j//100)-1] == 1 :
                    return i//100, j//100
    
def replace_pion(event, xt, yt):
    global HAUTEUR, LARGEUR, Joueur, T
    x, y = event.x, event.y #Coordonée du point cliqué
    """ Parcour le terrain de jeu """
    for i in range (100, LARGEUR+100, 100):
        for j in range (100, HAUTEUR+100, 100):
            if (xt == (i//100)-1 or xt == (i//100)-2 and yt == (j//100)-1) or \
                    (yt == (j//100) or yt == (j//100)-2 and xt == (i//100)-1) or \
                    (xt == (i//100) and yt == (j//100)) or (xt == (i//100)-2 and yt == (j//100)-2) or \
                    (xt == (i/100) and yt == (j//100)-2) or (xt == (i//100)-2 and yt == (j//100)):
                if i-10 <= x and x <= i+10 and j-10 <= y and y <= j+10:
                    if Joueur == 0 and  T[(i//100)-1][(j//100)-1] == 1 :
                        T[xt][yt] = 1
                        T[(i//100)-1][(j//100)-1] = 2
                        canvas.create_oval(i-10, j-10, i+10, j+10, fill="blue") #Creation du cercle du joueur 1 "bleu"
                        canvas.create_oval(((xt+1)*100)-10, ((yt+1)*100)-10, ((xt+1)*100)+10, ((yt+1)*100)+10, fill="red") #Creation du cercle du joueur 2 "rouge"
                    elif Joueur == 1 and T[(i//100)-1][(j//100)-1] == 2 :
                        T[xt][yt] = 2
                        T[(i//100)-1][(j//100)-1] = 1
                        canvas.create_oval(i-10, j-10, i+10, j+10, fill="red") #Creation du cercle du joueur 2 "rouge"
                        canvas.create_oval(((xt+1)*100)-10, ((yt+1)*100)-10, ((xt+1)*100)+10, ((yt+1)*100)+10, fill="blue") #Creation du cercle du joueur 1 "bleu"

def place_pion(event):
    """Place le pion"""
    global HAUTEUR, LARGEUR, Joueur, T
    x, y = event.x, event.y #Coordonée du point cliqué
    """ Parcour le terrain de jeu """
    for i in range (100, LARGEUR+100, 100):
        for j in range (100, HAUTEUR+100, 100):
        
            """ Si le point cliqué se trouve dans le cercle et qu'il n'a pas deja été choisis """
            if i-10 <= x and x <= i+10 and j-10 <= y and y <= j+10 and T[(i//100)-1][(j//100)-1] == 0:
                if Joueur == 0 :
                    T[(i//100)-1][(j//100)-1] = 1 #Le cercle deviens selectionné et ne peut plus l'être
                    canvas.create_oval(i-10, j-10, i+10, j+10, fill="blue") #Creation du cercle du joueur 1 "bleu"
                    score()
                    Joueur = 1 - Joueur
                    print(Joueur)
                else :
                    T[(i//100)-1][(j//100)-1] = 2 #Le cercle deviens selectionné et ne peut plus l'être
                    canvas.create_oval(i-10, j-10, i+10, j+10, fill="red") #Creation du cerlce du joueur 2 "Rouge"
                    score()
                    Joueur = 1 - Joueur
                    print(Joueur)
    affichetab(T)


""" Regard toutes les combinaisons possible"""  
def score():
    global T, victoire, Joueur
    if T[0][0] == T[0][1] == T[0][2] and T[0][0] != 0 :
        if T[0][0] == 1 : #joueur 1 vaincueur
            canvas.delete('all')
            canvas.create_text(200, 200, text='Joueur 1 vaincueur')
        else : #joueur 2 vaincueur
            canvas.delete('all')
            canvas.create_text(200, 200, text='Joueur 2 vaincueur')

    elif T[0][0] == T[1][1] == T[2][2] and T[0][0] != 0 :
        if T[0][0] == 1 : #joueur 1 vaincueur
            canvas.delete('all')
            canvas.create_text(200, 200, text='Joueur 1 vaincueur')
        else : #joueur 2 vaincueur
            canvas.delete('all')
            canvas.create_text(200, 200, text='Joueur 2 vaincueur')

    elif T[0][0] == T[1][0] == T[2][0] and T[0][0] != 0 :
        if T[0][0] == 1 : #joueur 1 vaincueur
            canvas.delete('all')
            canvas.create_text(200, 200, text='Joueur 1 vaincueur')
        else : #joueur 2 vaincueur
            canvas.delete('all')
            canvas.create_text(200, 200, text='Joueur 2 vaincueur')

    elif T[1][0] == T[1][1] == T[1][2] and T[1][0] != 0 :
        if T[1][0] == 1 : #joueur 1 vaincueur
            canvas.delete('all')
            canvas.create_text(200, 200, text='Joueur 1 vaincueur')
        else : #joueur 2 vaincueur
            canvas.delete('all')
            canvas.create_text(200, 200, text='Joueur 2 vaincueur')

    elif T[2][0] == T[2][1] == T[2][2] and T[2][0] != 0 :
        if T[2][0] == 1 : #joueur 1 vaincueur
            canvas.delete('all')
            canvas.create_text(200, 200, text='Joueur 1 vaincueur')
        else : #joueur 2 vaincueur
            canvas.delete('all')
            canvas.create_text(200, 200, text='Joueur 2 vaincueur')

    elif T[0][1] == T[1][1] == T[2][1] and T[0][1] != 0 :
        if T[0][1] == 1 : #joueur 1 vaincueur
            canvas.delete('all')
            canvas.create_text(200, 200, text='Joueur 1 vaincueur')
        else : #joueur 2 vaincueur
            canvas.delete('all')
            canvas.create_text(200, 200, text='Joueur 2 vaincueur')

    elif T[0][2] == T[1][2] == T[2][2] and T[0][2] != 0 :
        if T[0][2] == 1 : #joueur 1 vaincueur
            canvas.delete('all')
            canvas.create_text(200, 200, text='Joueur 1 vaincueur')
        else : #joueur 2 vaincueur
            canvas.delete('all')
            canvas.create_text(200, 200, text='Joueur 2 vaincueur')

    elif T[0][2] == T[1][1] == T[2][0] and T[0][2] != 0 :
        if T[0][2] == 1 : #joueur 1 vaincueur
            canvas.delete('all')
            canvas.create_text(200, 200, text='Joueur 1 vaincueur')
        else : #joueur 2 vaincueur
            canvas.delete('all')
            canvas.create_text(200, 200, text='Joueur 2 vaincueur')

"""affiche le tableau"""
def affichetab(tab):
    global PLACEMENT
    cpt = 0
    for j in range (3):
        for i in range (3):
            print(tab[i][j], end='')
            if tab[i][j] != 0:
                cpt +=1
        print()
    if cpt == 9:
        PLACEMENT = False
    print (PLACEMENT)
    
######################
# programme principal

racine = tk.Tk()
canvas = tk.Canvas(racine, bg="white", width=400, height=400)
canvas.grid()
grille()
tour()
affichetab(T)
racine.mainloop()

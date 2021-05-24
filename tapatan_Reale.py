#########################################
# groupe 3 MPCI 5
# Anessa Diallo
# Anthonin Le nevez
# Kaïs Cheboub
# Enzo Reale
# Phkar Romdoul
# Verdon Justin
# https://github.com/uvsq21919843/Projet-Jeu-tapatant.git
#########################################


import tkinter as tk #Importe la bibliotheque "tkinter"
import random #Importe la bibliotheque "random"

#########################################
#Variables et constantes du programme

T = [] #Cree la zone de jeu
nmbtour = 0 #Compteur du nombre de tour
Scorej1 = 0 #Compteur du Score du j1
Scorej2 = 0 #Compteur du Score du j2
caseActive = (-1,-1) #Case selectionner
histo = {} #Historique des position
debut = 0
joueur = 1


#########################################
#Fonctions du programme

#WIDGET-------------------------------------------------------------------------------------------

def creation_button():
    global sj1, sj2
    
    sj1 = tk.IntVar()
    sj1.set(Scorej1)
    scj1 = tk.Label(menu, textvariable = sj1, fg='red')
    j1 = tk.Label(menu, text = "Score J1 : ", fg='red')
    scj1.grid(row=0, column=1)
    j1.grid(row=0, column=0)


    information = tk.Label(menu, text="Information", fg='black')
    information.grid(row=0, column = 2)
    
    sj2 = tk.IntVar()
    sj2.set(Scorej2)
    scj2 = tk.Label(menu, textvariable = sj2, fg='blue')
    j2 = tk.Label(menu, text = "Score J2 : ", fg='blue')
    scj2.grid(row=0, column=4)
    j2.grid(row=0, column=3)

    Save = tk.Button(menu, text="Sauvegarder", width=9, height=1, overrelief='sunken', command = Sauvegarder)
    Save.grid(row=1, column=0, columnspan=2)

    Play = tk.Button(menu, text="Jouer",width=8, height=1, overrelief='sunken', command = generer)
    Play.grid(row=1, column=2)

    Charge = tk.Button(menu, text="charger", width=8, height=1, overrelief='sunken', command = Charger)
    Charge.grid(row=1, column=3, columnspan=2)
    
    

#CREATION DE TERRAIN------------------------------------------------------------------------------

def creationT():
    rechargement()
    grille()

def rechargement():
    global T
    if len(T) != 0:
        del T[:]
        canvas.delete("all")
    T = [3*[(0,0)] for i in range(3)] #Cree la zone de jeu

def grille():
    canvas.create_rectangle(100,100, 300, 300, fill='gold', outline='black') #Creation des lignes exterieur
    for j in range (1, 4):
        for i in range (1, 4):
            canvas.create_line(200, 200, i*100, j*100) #Creation des lignes Diagonnales et interieur
            canvas.create_oval((i*100)+25 , (j*100)+25 , (i*100)-25 , (j*100)-25 , outline='black') #Creation des cercles

#CREATION DE PION---------------------------------------------------------------------------------

def cree_pionJ2(i, j):
    T[i-1][j-1] = (2, canvas.create_oval(i*100-25, j*100-25, i*100+25, j*100+25, fill="blue")) #Le cercle deviens selectionné et ne peut plus l'être
    
def cree_pionJ1(i, j):
    T[i-1][j-1] = (1, canvas.create_oval(i*100-25, j*100-25, i*100+25, j*100+25, fill="red")) #Le cercle deviens selectionné et ne peut plus l'être
    


#JEU----------------------------------------------------------------------------------------------

def generer():
    global histo, debut, joueur, nmbtour, Scorej1, sj1, Scorej2, sj2
    creationT()
    histo = {}
    debut = 0
    joueur = 1
    nmbtour = 0
    Scorej1 = 0
    sj1.set(Scorej1)
    Scorej2 = 0
    sj2.set(Scorej2)


def jouer(event):
    "determiner ce qu'il se passe quand on clique"
    global debut
    if debut :
        joueur = (nmbtour%2)+1
    else :
        if nmbtour%2:
            joueur = 1
        else :
            joueur = 2
    if nmbtour < 6:
        #Phase de placement
        placement(event.x, event.y) #Lance la fonction "place_pion" avec l'evenement clic gauche
        if nmbtour == 6:
            matchnul()
            victoire()
    else :
        deplace(event.x, event.y, joueur)
    victoire()

def placement(x, y):
    global nmbtour, debut
    """ Parcour le terrain de jeu """
    for j in range (1, 4):
        for i in range (1, 4):
            """ Si le point cliqué se trouve dans le cercle et qu'il n'a pas deja été choisis """
            if i*100-25 <= x and x <= i*100+25 and j*100-25 <= y and y <= j*100+25 and T[i-1][j-1] == (0,0):
                if debut:
                    if nmbtour % 2 :
                        cree_pionJ1(i, j)         
                    else :
                        cree_pionJ2(i, j)   
                    nmbtour += 1
                else :
                    if nmbtour % 2 :
                        cree_pionJ2(i, j)         
                    else :
                        cree_pionJ1(i, j)   
                    nmbtour += 1

def deplace(i, j, joueur) :
    global nmbtour, caseActive
    x,y=getCase(i, j)
    a,b=caseActive[0], caseActive[1]
    if (T[x][y] != (0,0)) :
        selectionne(i, j,joueur)
        return
    if x == -1 or y == -1 :
        return
    #si une des deux cases est la case du milieu, le deplacement est autorise
    if ( (x==1 and y==1) or (a==1 and b==1) ) :
        #echange
        T[x][y] = (joueur,T[a][b][1])
        T[a][b] = (0,0)
        canvas.move(T[x][y][1], (x-a)*100, (y-b)*100)
        nmbtour+=1
        matchnul()
    else : 
        #si les deux cases sont adjacentes
        if (x==a and abs(y-b)== 1) :
            #echange
            T[x][y] = (joueur,T[a][b][1])
            T[a][b] = (0,0)
            canvas.move(T[x][y][1], (x-a)*100, (y-b)*100)
            nmbtour+=1
            matchnul()
        elif (y==b and abs(x-a)== 1 ) :
            #echange
            T[x][y] = (joueur,T[a][b][1])
            T[a][b] = (0,0)
            canvas.move(T[x][y][1], (x-a)*100, (y-b)*100)
            nmbtour+=1 
            matchnul()

def getCase(x, y) :
    for j in range (1, 4):
        for i in range (1, 4):
            """ Si le point cliqué se trouve dans le cercle et qu'il n'a pas deja été choisis """
            if i*100-25 <= x and x <= i*100+25 and j*100-25 <= y and y <= j*100+25 :
                return (i-1),(j-1)
    return -1,-1

def selectionne(i, j, joueur) :
    """selectione un pion du joueur specifie"""
    global caseActive 
    x,y=getCase(i, j)
    if (x == -1 or y == -1) :
        return
    if T[x][y][0] == joueur :
        caseActive = (x,y)
        return caseActive


#IA NON FINI--------------------------------------------------------------------------------------
"""
def play(mode):
    if mode == 1:
        print("JcJ")
    elif mode == 2:
        print("JcIA")
    else:
        print("IAcIA")

def joueria(event):
    "determiner ce qu'il se passe quand on clique"
    global debut
    if debut :
        joueur = (nmbtour%2)+1
    else :
        if nmbtour%2:
            joueur = 1
        else :
            joueur = 2
    
    if nmbtour < 6:
        #Phase de placement
        if joueur == 1 :
            placement(event.x, event.y) #Lance la fonction "place_pion" avec l'evenement clic gauche
            if nmbtour == 6:
                matchnul()
                victoire()
        else :
            placementIA(joueur)
    else :
        if joueur == 1:
            deplace(event.x, event.y, joueur)
        else :
            deplaceIA(joueur)
    victoire()

def placementIA(joueur):
    for j in range(3):
        for i in range(3):
            if T[i][j][0] == 0:
                if CanWin(joueur, i ,j) :
                    placeIA(joueur, i, j)
                    return
                if CanLose(joueur, i, j):
                    placeIA(joueur, i, j)
                    return
    i, j = AleatIA(joueur)
    placeIA(joueur, i, j)

def deplacementIA(joueur):
    for j in range(3):
        for i in range(3):
            if T[i][j][0] == 0:
                case = CanWin(joueur, i, j)
                if case != (-1, -1):
                    if deplaceIA(joueur, case):
                        return
                case = CanLose(joueur, i, j)
                if case != (-1, -1):
                    if deplaceIA(joueur, case):
                        return
    deplaceIA(joueur, AleatIA(joueur))

def CanWin(joueur, x, y):
    if (T[x][y][0] == 0) :
        t = T.copy()
        print(type(t[x][y][0]))
        print(type(joueur))
        t[x][y][0] = joueur
        j = []
        for j in range(3):
            for i in range(3):
                if t[i][j][0] == joueur:
                    j.append((i, j))
        if ((j[0][0] == j[1][0] and j[1][0] ==  j[2][0]) or (j[0][1] == j[1][1] and j[1][1] ==  j[2][1]) or ((j[0]==(0,0) or j[0]==(1,1) or j[0]==(2,2)) and (j[1]==(0,0) or j[1]==(1,1) or j[1]==(2,2)) and (j[2]==(0,0) or j[2]==(1,1) or j[2]==(2,2))) or ((j[0]==(0,2) or j[0]==(2,0) or j[0]==(1,1)) and (j[1]==(0,2) or j[1]==(2,0) or j[1]==(1,1)) and (j[2]==(0,2) or j[2]==(2,0) or j[2]==(1,1)))) :
            return True
    return False

def CanLose(joueur, x, y):
    joueur = 2 if joueur == 1 else 1
    if (T[x][y][0] == 0) :
        t = T.copy()
        t [x][y][0] = joueur
        j = []
        for j in range(3):
            for i in range(3):
                if t[i][j][0] == joueur:
                    j.append((i, j))
        if ((j[0][0] == j[1][0] and j[1][0] ==  j[2][0]) or (j[0][1] == j[1][1] and j[1][1] ==  j[2][1]) or ((j[0]==(0,0) or j[0]==(1,1) or j[0]==(2,2)) and (j[1]==(0,0) or j[1]==(1,1) or j[1]==(2,2)) and (j[2]==(0,0) or j[2]==(1,1) or j[2]==(2,2))) or ((j[0]==(0,2) or j[0]==(2,0) or j[0]==(1,1)) and (j[1]==(0,2) or j[1]==(2,0) or j[1]==(1,1)) and (j[2]==(0,2) or j[2]==(2,0) or j[2]==(1,1)))) :
            return True
    return False

def AleatIA(joueur):
        t = T.copy()
        j = []
        for y in range(3):
            for x in range(3):
                if t[x][y][0] == 0:
                    j.append((x, y))
        rand = random.randrange(len(j))
        return (j[rand][0], j[rand][1])

def placeIA(joueur, i, j):
    global nmbtour
    if joueur == 1:
        cree_pionJ1(i, j)
    else :
        cree_pionJ2(i, j)
    nmbtour +=1
"""

#CONDITION-----------------------------------------------------------------------------------------

def matchnul():
    global nmbtour, debut
    cle = ""
    for j in range(3):
        for i in range(3):
            cle += str(T[i][j][0])
    if cle in histo:
        histo[cle] += 1
        if histo[cle] == 3:
            creationT()
            nmbtour = 0
            debut = 1 - debut
    else :
        histo[cle] =1

def victoire():
    global nmbtour, debut, Scorej1, Scorej2
    j1 = []
    j2 = []
    for j in range(3):
        for i in range(3):
            if T[i][j][0] == 1:
                j1.append((i, j))
            elif T[i][j][0] == 2:
                j2.append((i,j))
    if len(j1) == 3:
        if ((j1[0][0] == j1[1][0] and j1[1][0] ==  j1[2][0]) or (j1[0][1] == j1[1][1] and j1[1][1] ==  j1[2][1]) or ((j1[0]==(0,0) or j1[0]==(1,1) or j1[0]==(2,2)) and (j1[1]==(0,0) or j1[1]==(1,1) or j1[1]==(2,2)) and (j1[2]==(0,0) or j1[2]==(1,1) or j1[2]==(2,2))) or ((j1[0]==(0,2) or j1[0]==(2,0) or j1[0]==(1,1)) and (j1[1]==(0,2) or j1[1]==(2,0) or j1[1]==(1,1)) and (j1[2]==(0,2) or j1[2]==(2,0) or j1[2]==(1,1)))):
            creationT()
            Scorej1 += 1
            sj1.set(Scorej1)
            nmbtour = 0
            debut = 1 - debut
  
    if len(j2) == 3:
        if ((j2[0][0] == j2[1][0] and j2[1][0] ==  j2[2][0]) or (j2[0][1] == j2[1][1] and j2[1][1] ==  j2[2][1]) or ((j2[0]==(0,0) or j2[0]==(1,1) or j2[0]==(2,2)) and (j2[1]==(0,0) or j2[1]==(1,1) or j2[1]==(2,2)) and (j2[2]==(0,0) or j2[2]==(1,1) or j2[2]==(2,2))) or ((j2[0]==(0,2) or j2[0]==(2,0) or j2[0]==(1,1)) and (j2[1]==(0,2) or j2[1]==(2,0) or j2[1]==(1,1)) and (j2[2]==(0,2) or j2[2]==(2,0) or j2[2]==(1,1)))):
            creationT()
            Scorej2 += 1
            sj2.set(Scorej2)
            nmbtour = 0
            debut = 1 - debut
    victot()

def victot():
    global Scorej1, Scorej2
    if Scorej1 == 3:
        canvas.delete("all")
        canvas.create_text(200, 200, text = "Felicitation ! \nJ1 gagnant!!", fill="red")
    elif Scorej2 == 3:
        canvas.delete("all")
        canvas.create_text(200, 200, text = "Felicitation ! \nJ2 gagnant!!", fill="blue")



#DONNÉE---------------------------------------------------------------------------------------------

def Sauvegarder():
    global Scorej1, Scorej2, debut, histo, joueur
    score = [Scorej1, Scorej2]
    fic = open("sauvegarde","w")
    fic.write(str(debut) + "\n")
    fic.write(str(nmbtour) + "\n")
    fic.write(str(score[0]) + " " + str(score[1]) + "\n")
    for j in range(3):
        for i in range(3):
            fic.write(str(T[i][j][0]) + " " + str(T[i][j][1]) + "\n")
    for cle, valeur in histo.items():
        fic.write(str(cle) + " " + str(valeur) + "\n")
    fic.close()

def Charger():
    global debut, histo, nmbtour, Scorej1, Scorej2, joueur
    fic = open('sauvegarde', 'r')
    cpt = 1
    histo = {}
    histolist = []
    for x in fic :
        if cpt == 1:
            debut = int(x)
        elif cpt == 2:
            nmbtour = int(x)
        elif cpt == 3:
            Scorej1 = int(x.split()[0])
            sj1.set(Scorej1)
            Scorej2 = int(x.split()[1])
            sj2.set(Scorej2)
        elif cpt > 3 and cpt < 13 :
            histolist.append((int(x.split()[0]), int(x.split()[1])))

        else :
            cle = int(x.split()[0])
            histo[cle] = int(x.split()[1])
        cpt +=1
   
    creationT()
    cpt = 0
    for j in range(3):
        for i in range(3):
            T[i][j] = histolist[cpt]
            if T[i][j][0] == 1:
                cree_pionJ1(i+1, j+1)
            elif T[i][j][0] == 2:
                cree_pionJ2(i+1, j+1)
            cpt += 1





#########################################
#Main du programme

racine = tk.Tk()
menu = tk.Frame(racine, width=400)
menu.grid(row=1, column=0)
canvas = tk.Canvas(racine, bg="grey", width=400, height=400)
canvas.grid(row=0, column=0)

creation_button()
creationT()

canvas.bind("<Button-1>", jouer)


racine.mainloop()

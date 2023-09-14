######################## Mini-projet Mastermind ########################

###### import modules #######

import random

##### Les variables globales #######

#Constantes
tailleCode = 5
nbEssaieMax = 10
possibilitesCouleur = ["B", "J", "M", "N", "O", "R", "V", "W"]

# Variables
partieFinie = False
nbEssaie = 1
resultatPartie = ""
listeIa = [possibilitesCouleur[:] for i in range(tailleCode)]

##### Les fonctions auxiliaires et tests #######

def genererCode(taille, couleurs):
    """
    Génère un code pour la partie du MM
    """
    assert type(taille) == int
    assert type(couleurs) == list
    listeCode = [0] * taille
    for i in range(taille):
        listeCode[i] = couleurs[random.randint(0, len(couleurs)-1)]
    return listeCode
assert len(genererCode(tailleCode, possibilitesCouleur)) == tailleCode

def valeurDans(valeur, liste):
    """
    Vérifie si une valeur est présente dans une liste
    """
    assert type(liste) == list
    for i in range(len(liste)):
        if liste[i] == valeur:
            return True
    return False

def convertirTentative(tentative):
    """
    Convertie la tentative en liste
    """
    assert type(tentative) == str
    liste = [0] * tailleCode
    for i in range(len(tentative)):
        liste[i] = tentative[i]
    return liste

def verifierTenta(liste, couleurs, taille):
    """
    Vérifie si la taille de la réponse est bonne et si toutes les couleurs
    existent bien
    """
    assert type(liste) == list
    assert type(couleurs) == list
    assert type(taille) == int
    resultat = True
    if len(liste) != taille:
        return False
    for caractere in liste:
        if not valeurDans(caractere, possibilitesCouleur):
            resultat = False
    return resultat

def verifierCode(listeInput, listeCode, taille):
    """
    Vérifie le code envoyer, renvoie une liste avec la couleur des marques
    ●: Bonne couleur au bon endroit
    ◦: Bonne couleur mais au mauvais endroit
     : Mauvaise couleur, elle n'est pas dans le code.
    """
    assert type(listeInput) == list
    assert type(listeCode) == list
    assert type(taille) == int
    codeReponse = [0] * taille
    for i in range(len(listeInput)):
        if listeInput[i] == listeCode[i]:
            codeReponse[i] = "●"
        elif valeurDans(listeInput[i], listeCode):
            codeReponse[i] = "◦"
        else:
            codeReponse[i] = " "
    return codeReponse

def afficherReponse(listeCode):
    """
    Affiche de manière plus élégante la réponse de l'ordinateur
    """
    assert type(listeCode) == list
    texteReponse = "-  "
    for i in listeCode:
        texteReponse = texteReponse + "|" + i + "|  "
    texteReponse = texteReponse + "-"
    return texteReponse

def faireJouerIa(listeCoups):
    coup = ""
    for i in listeCoups:
        coup = coup + i[random.randint(0, len(i)-1)]
    return coup

def analyserReponse(reponse, listeCoups, derniereAction):
    for i in range(len(reponse)):
        if reponse[i] == "●":
            # Enlève toutes les autres couleurs de la case
            listeCoups[i] = [derniereAction[i]]
        elif reponse[i] == "◦":
            # Enlève la couleur dans la case en question
            if valeurDans(derniereAction[i], listeCoups[i]):
                listeCoups[i].pop(listeCoups[i].index(derniereAction[i]))
        elif reponse[i] == " ":
            # Enlève la couleur dans toute les cases
            for y in range(len(listeCoups)):
                if valeurDans(derniereAction[i], listeCoups[y]):
                    listeCoups[y].pop(listeCoups[y].index(derniereAction[i]))


##### programme principal #######

codePartie = genererCode(tailleCode, possibilitesCouleur)
demanderIa = input("-  Faire jouer l'ia (o/n) ? - ").lower()
while not(demanderIa in ("o", "n")):
    print("-    Réponse invalide...    -")
    demanderIa = input("-  Faire jouer l'ia (o/n) ? - ").lower()
print("")
if demanderIa == "o":
    iaJoue = True
else:
    iaJoue = False
while not partieFinie:
    if iaJoue:
        tentative = faireJouerIa(listeIa)
    else:
        # Les différentes couleurs ne doivent pas être espacées lors de l'input
        tentative = input(f"{nbEssaie}  ")
    tentativeListe = convertirTentative(tentative)
    estValide = verifierTenta(tentativeListe, possibilitesCouleur, tailleCode)
    if estValide:
        if tentativeListe == codePartie:
            reponseOrdi = verifierCode(tentativeListe, codePartie, tailleCode)
            print(afficherReponse(reponseOrdi))
            partieFinie = True
            resultatPartie = "G"
        else:
            reponseOrdi = verifierCode(tentativeListe, codePartie, tailleCode)
            if iaJoue:
                analyserReponse(reponseOrdi, listeIa, tentative)
            print(afficherReponse(reponseOrdi))
            nbEssaie = nbEssaie + 1
            if nbEssaie == nbEssaieMax+1:
                partieFinie = True
                resultatPartie = "P"
    else:
        print("- Une des couleurs n'existe pas ou le code saisie n'a pas la bonne taille -")

print("")
if resultatPartie == "G":
    print("- MASTERMIND !")
else:
    print("Vous avez perdu...")

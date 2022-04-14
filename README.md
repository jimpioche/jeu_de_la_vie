Le Jeu De La Vie est un jeu de simulation; c'est un automate cellulaire. Des règles très simples de vie et de mort des cellules (représentées par des cases) sont programmées et la simulation est lancée. Des formes très simples peuvent conduire à des formes d'une très grande complexité. On dit que le Jeu De La Vie est un pont entre le déterminisme et le hasard.
Les fichiers sources sont organisés de la manière suivante:

    jdlv_data.py: 
    
    contient les définitions comme la taille de la grille, des cellules, des couleurs et des pinceaux...Ce fichier est importé dans les autres qui ont besoin 
                  de ces définitions.
                
    jdlv_outils.py:
    
    contient les fonctions de base comme is_alive, is_dead, kill_case, revive_casse, mais aussi des fonctions qui permmettent de modifier les valeurs dans les widgets comme les lineEdit ou les menus déroulants...

    jdlv_model.py : 
    
    contient la définition du model (dans notre contexte, de la grille) => une liste de listes dont les éléments sont des dictionnaires à deux attributs ('s' poru le statut morte ou vivante et 'c' pour la couleur de la case).             
    
    jdlv.ui : 
    
    fichier représentant la GUI (coquille vide à ce stade) c'est la Graphical User Interface.
    
    jdlv_vue_fromUi.py :
    
    c'est la transformation en Python du fichier précédent.
    
    jdlv_vue.py : 
    
    s'appuie sur le fichier précédent pour finaliser la GUI. On y trouve en particulier la fonction update qui affiche le model dans la grille et donc l'état des cases à chaque itértion de la boucle WHILE qui se trouve dans le fichier jdlv_controleur.py (voir juste après).
    
    jdlv_controleur.py : 
    
    contient la définition des actions lorsqu'on clique sur les différents widgets (qui sont cliquables) par exemple les boutons, le menu déroulant, les cases de la grille
    
    jdlv.qrc : 
    
    contient les images au format XML.
    
    jdlv_rc.py : 
    
    c'est la transformation en Python du fichier précédent.
    
    
    
    jdlv_my_tools.py
    
    jdlv_other_functions.py
    
    jdlv_main.py


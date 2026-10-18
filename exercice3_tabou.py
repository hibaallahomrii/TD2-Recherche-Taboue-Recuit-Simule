
# Exercice 3 : Voyageur de commerce
# Methode : Recherche Taboue

import math

# Distances entre les villes
distances = {
    (1, 2): 14, (1, 3): 15, (1, 8): 17,
    (2, 3): 13, (2, 4): 14, (2, 5): 20, (2, 8): 21,
    (3, 4): 11, (3, 5): 21, (3, 6): 17,
    (3, 7): 9, (3, 8): 9,
    (4, 5): 11, (4, 6): 10, (4, 7): 8, (4, 8): 20,
    (5, 6): 15, (5, 7): 18,
    (6, 7): 9,
    (7, 8): 13
}

# Les distances sont les memes dans les deux sens
for (a, b), distance in list(distances.items()):
    distances[(b, a)] = distance


# Calculer le cout d'un circuit
def cout_circuit(circuit):
    total = 0

    for i in range(len(circuit) - 1):
        a = circuit[i]
        b = circuit[i + 1]

        if (a, b) not in distances:
            return math.inf

        total += distances[(a, b)]

    return total


# Algorithme de recherche taboue
def recherche_taboue(max_iterations=100, duree_taboue=5):

    # Circuit initial
    courant = [1, 2, 3, 4, 5, 6, 7, 8, 1]
    meilleure = courant[:]

    liste_taboue = {}

    for iteration in range(max_iterations):
        voisins = []

        # Echanger deux villes pour creer un voisin
        for i in range(1, 8):
            for j in range(i + 1, 8):

                voisin = courant[:]
                voisin[i], voisin[j] = voisin[j], voisin[i]

                cout = cout_circuit(voisin)

                # Ignorer les circuits avec une liaison inexistante
                if math.isinf(cout):
                    continue

                mouvement = tuple(sorted((courant[i], courant[j])))
                est_tabou = liste_taboue.get(mouvement, -1) > iteration

                if not est_tabou or cout < cout_circuit(meilleure):
                    voisins.append((cout, voisin, mouvement))

        if not voisins:
            break

        # Choisir le voisin autorise de cout minimal
        voisins.sort(key=lambda element: element[0])
        cout, courant, mouvement = voisins[0]

        # Interdire temporairement le mouvement inverse
        liste_taboue[mouvement] = iteration + duree_taboue

        # Memoriser la meilleure solution
        if cout < cout_circuit(meilleure):
            meilleure = courant[:]

    return meilleure, cout_circuit(meilleure)


# Programme principal
if __name__ == "__main__":

    circuit, cout = recherche_taboue()

    print("EXERCICE 3 - RECHERCHE TABOUE")
    print("Meilleur circuit trouve :", " -> ".join(map(str, circuit)))
    print("Cout total :", cout)

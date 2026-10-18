
# Exercice 3 : Voyageur de commerce
# Methode : Recuit Simule
# Nombre d'iterations : 5

import math
import random

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

# Les distances sont identiques dans les deux sens
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


# Algorithme du recuit simule
def recuit_simule():

    random.seed(8)

    # Solution initiale
    courant = [1, 2, 3, 4, 5, 6, 7, 8, 1]
    meilleure = courant[:]

    # Temperature initiale
    temperature = 20

    # Facteur de refroidissement
    alpha = 0.8

    print("Circuit initial :", courant)
    print("Cout initial :", cout_circuit(courant))

    # Effectuer exactement 5 iterations
    for iteration in range(1, 6):

        voisins_valides = []

        # Generer des circuits voisins
        for i in range(1, 8):
            for j in range(i + 1, 8):

                voisin = courant[:]
                voisin[i], voisin[j] = voisin[j], voisin[i]

                cout = cout_circuit(voisin)

                if not math.isinf(cout):
                    voisins_valides.append((voisin, cout))

        if not voisins_valides:
            print("Aucun voisin valide.")
            break

        # Choisir un voisin au hasard
        voisin, nouveau_cout = random.choice(voisins_valides)

        ancien_cout = cout_circuit(courant)

        # Calculer la variation du cout
        delta = nouveau_cout - ancien_cout

        # Regle de Metropolis
        if delta <= 0:
            accepter = True
            probabilite = 1.0
        else:
            probabilite = math.exp(-delta / temperature)
            accepter = random.random() < probabilite

        # Accepter ou refuser le voisin
        if accepter:
            courant = voisin

        # Garder la meilleure solution trouvee
        if cout_circuit(courant) < cout_circuit(meilleure):
            meilleure = courant[:]

        # Afficher les informations de l'iteration
        print("\nIteration", iteration)
        print("Temperature :", round(temperature, 3))
        print("Cout avant :", ancien_cout)
        print("Cout du voisin :", nouveau_cout)
        print("Variation delta :", delta)
        print("Probabilite :", round(probabilite, 3))
        print("Voisin accepte :", accepter)
        print("Cout courant :", cout_circuit(courant))
        print("Meilleur cout :", cout_circuit(meilleure))

        # Diminuer la temperature
        temperature = alpha * temperature

    return meilleure, cout_circuit(meilleure)


# Programme principal
if __name__ == "__main__":

    circuit, cout = recuit_simule()

    print("\nRESULTAT FINAL - RECUIT SIMULE")
    print("Meilleur circuit :", " -> ".join(map(str, circuit)))
    print("Cout total :", cout)
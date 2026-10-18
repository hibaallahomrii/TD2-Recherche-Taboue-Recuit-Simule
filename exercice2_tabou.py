# Exercice 2 - Recherche taboue pour le transport de containers
# Objectif : minimiser le cout total de transport.

# Cout du transport d'un container depuis chaque depot vers chaque magasin.
couts = [
    [5, 3, 4],  # Depot D1 vers M1, M2, M3
    [6, 7, 2]   # Depot D2 vers M1, M2, M3
]

# Demandes des magasins et stocks des depots.
demandes = [4, 5, 8]
stocks = [8, 9]


def cout_total(allocation_d1):
    """
    allocation_d1[j] = nombre de containers envoyes de D1 vers Mj.
    Le reste de la demande du magasin est fourni par D2.
    """
    total = 0
    for j in range(3):
        depuis_d1 = allocation_d1[j]
        depuis_d2 = demandes[j] - depuis_d1
        total += depuis_d1 * couts[0][j]
        total += depuis_d2 * couts[1][j]
    return total


def recherche_taboue(max_iterations=100, duree_taboue=5):
    # Solution initiale : D1 envoie [4, 4, 0], soit 8 containers.
    allocation = [4, 4, 0]
    meilleure = allocation[:]
    liste_taboue = {}

    for iteration in range(max_iterations):
        voisins = []

        # Un voisin est obtenu en deplacant un container de D1
        # d'un magasin vers un autre, sans changer le stock total de D1.
        for origine in range(3):
            for destination in range(3):
                if origine == destination:
                    continue
                if allocation[origine] == 0:
                    continue
                if allocation[destination] == demandes[destination]:
                    continue

                voisin = allocation[:]
                voisin[origine] -= 1
                voisin[destination] += 1

                mouvement = (origine, destination)
                mouvement_inverse = (destination, origine)
                est_tabou = liste_taboue.get(mouvement_inverse, -1) > iteration
                cout_voisin = cout_total(voisin)

                # Critere d'aspiration : autoriser un mouvement tabou
                # s'il donne une solution meilleure que la meilleure connue.
                if (not est_tabou) or cout_voisin < cout_total(meilleure):
                    voisins.append((cout_voisin, voisin, mouvement))

        if not voisins:
            break

        # Choisir le voisin autorise ayant le cout le plus faible.
        voisins.sort(key=lambda element: element[0])
        cout_voisin, allocation, mouvement = voisins[0]

        # Interdire temporairement le mouvement inverse.
        liste_taboue[mouvement] = iteration + duree_taboue

        if cout_total(allocation) < cout_total(meilleure):
            meilleure = allocation[:]

    return meilleure, cout_total(meilleure)


if __name__ == "__main__":
    meilleure, cout = recherche_taboue()

    # allocation_d1 donne les containers envoyes par D1.
    # D2 fournit le reste de chaque demande.
    allocation_d2 = [
        demandes[j] - meilleure[j]
        for j in range(3)
    ]

    print("EXERCICE 2 - RECHERCHE TABOUE")
    print("Allocation de D1 vers M1, M2, M3 :", meilleure)
    print("Allocation de D2 vers M1, M2, M3 :", allocation_d2)
    print("Cout total minimal trouve :", cout)
    print("Verification : stock D1 =", sum(meilleure))
    print("Verification : stock D2 =", sum(allocation_d2))
    print("Demandes recues :", [
        meilleure[j] + allocation_d2[j] for j in range(3)
    ])

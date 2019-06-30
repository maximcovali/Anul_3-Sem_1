import pandas as pd
import numpy as np
import grafice
import functii
import gui
import scipy.cluster.hierarchy as hclust
import scipy.spatial.distance as hdist

pd.set_option('display.max_columns', None)

try:
    nume_fisier = gui.FileDialog("*.csv")
    if nume_fisier is "":
        exit(1)
    optiuni_trasare = gui.Check(["Trasare axe discriminante", "Trasare histograme", "Grupare variabile"],
                                "Optiuni model:")
    axe_discriminante = optiuni_trasare.__contains__("Trasare axe discriminante")
    histograme = optiuni_trasare.__contains__("Trasare histograme")
    grupare_variabile = optiuni_trasare.__contains__("Grupare variabile")
    tabel = pd.read_csv(nume_fisier, na_values=":")
    functii.inlocuire_na_df(tabel)
    nume_variabile = list(tabel)
    coloana_index = gui.Combo(nume_variabile, "Selectati variabila index")
    coloana_etichete = gui.Combo(nume_variabile, "Selectati coloana de etichete")
    tabel.index = [str(v) for v in tabel[coloana_index]]
    tabel.index.name = coloana_index
    nume_instante = tabel[coloana_index].values
    if len(nume_variabile) < 20:
        variabile_prelucrate = gui.Check(nume_variabile, "Selectati variabilele de lucru")
    else:
        variabile_prelucrate = gui.ListBox(nume_variabile, "Selectati variabilele de lucru")
    x = tabel[variabile_prelucrate].values
    # Creare ierarhie instante
    metoda = gui.Combo(hclust._LINKAGE_METHODS.keys(), "Metoda pentru clasificare instante:")
    if metoda == 'ward' or metoda == 'centroid' or metoda == 'weighted':
        distanta = 'euclidean'
    else:
        distanta = gui.Combo(hdist._METRICS_NAMES, "Metrica pentru clasificarea instantelor:")
    h = hclust.linkage(x, method=metoda, metric=distanta)
    # Identificare partitie de stabilitate maxima
    m = np.shape(h)[0]  # Numar maxim de jonctiuni
    # Se scade din m indexul celei mai mari diferente dintre doua distante de jonctionare consecutive
    # pentru a determina numarul de clustere din partitia cea mai stabila
    k = m - np.argmax(h[1:m, 2] - h[:(m - 1), 2])
    # Identificare clustere in partitia de maxima stabilitate
    g_max, coduri = functii.clustere(h, k)
    # Afisare cluster
    functii.afisare_cluster(g_max, tabel.index, coloana_index, "Cluster_Output/P_max.csv")
    # Determinare culori clustere
    culori_clustere = functii.culori_clustere(h, k, coduri)
    grafice.dendrograma(h, etichete=tabel[coloana_etichete],
                        titlu="Grupare instante. Partitia de maxima stabilitate. Metoda:" + metoda +
                              ". Metrica:" + distanta, culori=culori_clustere)
    if k > 2 and axe_discriminante:
        z, zg, grupe = functii.lda_cluster(x, g_max)
        # grafice.scatter(z[:, 0], z[:, 1], g_max, tabel[coloana_etichete], zg[:, 0], zg[:, 1], grupe, grupe,
        #                 titlu='Partitia de maxima stabilitate (' + str(k) + ' clustere)')
        grafice.plot_clustere(z[:, 0], z[:, 1], g_max, grupe, etichete=tabel.index, titlu='Partitia optimala')
    if histograme:
        for v in variabile_prelucrate:
            grafice.histograme(tabel[v].values, g_max, var=v)
    grafice.show()
    # Ierarhie variabile
    if grupare_variabile:
        metoda_v = gui.Combo(hclust._LINKAGE_METHODS.keys(), "Metoda pentru clasificare variabile:")
        distanta_v = gui.Combo(hdist._METRICS_NAMES, "Metrica pentru clasificare variabile:")
        h1 = hclust.linkage(x.transpose(), method=metoda_v, metric=distanta_v)
        grafice.dendrograma(h1, etichete=variabile_prelucrate, titlu="Grupare variabile. Metoda:" + metoda_v +
                                                                     ". Metrica:" + distanta_v)
        grafice.show()
    n = np.shape(x)[0]
    # Pregatire o lista de selectii pentru partitii incepand de la partitia cu doua clustere
    lista_selectii = [str(i) + ' clustere' for i in range(2, n - 1)]
    partitii = gui.ListBox(lista_selectii, "Partitii dorite:")
    # Creare tabela cu partitia de maxima stabilitate si partitiile selectate
    t_partitii = pd.DataFrame(index=tabel.index)
    t_partitii['P_max'] = g_max
    for v in partitii:
        k = lista_selectii.index(v) + 2  # Numar de clustere dorit
        g, coduri = functii.clustere(h, k)
        # Salvare partitie
        functii.afisare_cluster(g, tabel.index, coloana_index,
                                "Cluster_Output/P_" + str(k) + ".csv")
        culori_clustere = functii.culori_clustere(h, k, coduri)
        grafice.dendrograma(h, tabel[coloana_etichete],
                            titlu='Partitia cu ' + v,
                            culori=culori_clustere)
        t_partitii["P_" + v] = g
        if k > 2 and axe_discriminante:
            z, zg, grupe = functii.lda_cluster(x, g)
            grafice.plot_clustere(z[:, 0], z[:, 1], g, grupe, etichete=tabel.index, titlu='Partitia cu ' + v)
        if histograme:
            for v in variabile_prelucrate:
                grafice.histograme(tabel[v].values, g, var=v)
        grafice.show()
    t_partitii.to_csv("Cluster_Output/Partitii.csv")
except Exception as ex:
    print("Eroare!", ex.with_traceback(), sep="\n")

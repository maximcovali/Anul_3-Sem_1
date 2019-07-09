import functii
import gui
import grafice
import pandas as pd

try:
    nume_fisier = gui.FileDialog("*.csv")
    if nume_fisier is "":
        exit(1)
    tabel = pd.read_csv(nume_fisier)
    nume_variabile = [v for v in tabel.columns]
    coloana_index = gui.Check(nume_variabile, "Selectati variabila index")[0]
    coloana_etichete = gui.Check(nume_variabile, "Selectati coloana de etichete")[0]
    tabel.index = [str(v) for v in tabel[coloana_index]]
    nume_instante = tabel[coloana_index]
    variabile_prelucrate = gui.Check(nume_variabile, "Selectati variabilele de lucru")
    m = len(variabile_prelucrate)
    t = tabel[variabile_prelucrate]
    X = t.values
    functii.inlocuire_na(X)
    R, alpha, a, Rxc, C = functii.acp(X)
    functii.tabelare(a, ['a' + str(i) for i in range(1, m + 1)], variabile_prelucrate, "PCA_Output\\loadings.csv")
    R_tab = functii.tabelare(R, nume_coloane=variabile_prelucrate, nume_instante=variabile_prelucrate,
                             tabel="PCA_Output\\R.csv")
    grafice.corelograma(R_tab, "Corelograma corelatii")
    functii.tabelare_varianta(alpha)
    j_Cattel, j_Kaiser = grafice.plot_varianta(alpha)
    Rxc_tab = functii.tabelare(Rxc, nume_coloane=["C" + str(i) for i in range(1, m + 1)],
                               nume_instante=variabile_prelucrate, tabel="PCA_Output\\Rxc.csv")
    grafice.corelograma(Rxc_tab, "Corelatii factoriale")
    S, q, beta, Comun = functii.evaluare(C, alpha, Rxc)
    k_s = min(j_Kaiser, j_Cattel)
    for i in range(1, k_s):
        grafice.t_scatter(S[:, 0], S[:, i], tabel[coloana_etichete], "a1", "a" + str(i + 1),
                          "Plot scoruri. Axele 1:" + str(i + 1))
        grafice.cercul_corelatiilor(Rxc_tab, 0, i,
                                    "Cercul corelatiilor. Axele 1:" + str(i + 1))
    functii.tabelare(S, nume_coloane=["C" + str(i) for i in range(1, m + 1)],
                     nume_instante=nume_instante, tabel="PCA_Output\\F.csv")
    functii.tabelare(q, nume_coloane=["a" + str(i) for i in range(1, m + 1)],
                     nume_instante=nume_instante, tabel="PCA_Output\\cos2.csv")
    functii.tabelare(beta, nume_coloane=["a" + str(i) for i in range(1, m + 1)],
                     nume_instante=nume_instante, tabel="PCA_Output\\contributii.csv")
    Comun_tab = functii.tabelare(Comun, nume_coloane=["C" + str(i) for i in range(1, m + 1)],
                                 nume_instante=variabile_prelucrate, tabel="PCA_Output\\Comunalitati.csv")
    grafice.corelograma(Comun_tab, "Comunalitati", 0)
    grafice.show()
except Exception as ex:
    """print("Eroare!", ex.with_traceback(), sep="\n")"""
    print(ex.with_traceback)

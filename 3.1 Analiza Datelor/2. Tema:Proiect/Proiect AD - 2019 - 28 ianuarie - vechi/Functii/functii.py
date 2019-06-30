import numpy as np
import pandas as pd
import pandas.api.types as pdt


def standardizare(X):
    medii = np.mean(X, axis=0)
    abaterestd = np.std(X, axis=0)
    Xstd = (X - medii) / abaterestd
    return Xstd


def inversare(t, y=None):
    if type(t) is pd.DataFrame:
        for c in t.columns:
            minim = t[c].min()
            maxim = t[c].max()
            if abs(minim) > abs(maxim):
                t[c] = -t[c]
                if y is not None:
                    k = t.columns.get_loc(c)
                    y[:, k] = -y[:, k]
    else:
        for i in range(np.shape(t)[1]):
            minim = np.min(t[:, i])
            maxim = np.max(t[:, i])
            if np.abs(minim) > np.abs(maxim):
                t[:, i] = -t[:, i]


def acp(X):
    R = np.corrcoef(X, rowvar=False)
    # calcul vector si valori proprii
    valp, vecp = np.linalg.eig(R)
    # sortare valori proprii si vectori proprii
    k_inv = [k for k in reversed(np.argsort(valp))]
    alpha = valp[k_inv]
    a = vecp[:, k_inv]
    inversare(a)
    # calcul corelatii factoriale
    Rxc = a * np.sqrt(alpha)
    # calcul componente
    # standardizare X
    medii = np.mean(X, axis=0)
    abaterestd = np.std(X, axis=0)
    Xstd = (X - medii) / abaterestd
    coloana = Xstd @ a
    return R, alpha, a, Rxc, coloana



# Functie pentru inlocuirea valorilor lipsa
# prin medie/modul
def inlocuire_na_df(t):
    for c in t.columns:
        if pdt.is_numeric_dtype(t[c]):
            if t[c].isna().any():
                medie = t[c].mean()
                t[c] = t[c].fillna(medie)
        else:
            if t[c].isna().any():
                modul = t[c].mode()
                t[c] = t[c].fillna(modul[0])



def inlocuire_na(X):
    medii = np.nanmean(X, axis=0)
    k_nan = np.where(np.isnan(X))
    X[k_nan] = medii[k_nan[1]]




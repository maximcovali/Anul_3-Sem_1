import numpy as np
import pandas as pd
import scipy.stats as sts
import pandas.api.types as pdt
import sklearn.preprocessing as pp
import collections
import scipy.linalg as lin
import sklearn.discriminant_analysis as disc
import grafice


# Calcul centrii, frecvente grupe, etichete grupe si matrice de imprastiere
# x - tabel date
# y - variabila de grupare
def imprastiere(x, y):
    n, m = np.shape(x)
    medii = np.mean(x, axis=0)
    counter = collections.Counter(y)
    g = np.array([i for i in counter.keys()])  # preluare etichete
    ng = np.array([i for i in counter.values()])  # preluare frecvente
    q = len(g)
    xg = np.ndarray(shape=(q, m))
    for k, i in zip(g, range(len(g))):
        xg[i, :] = np.mean(x[y == k, :], axis=0)
    xg_med = xg - medii
    sst = n * np.cov(x, rowvar=False, bias=True)
    ssb = np.transpose(xg_med) @ np.diag(ng) @ xg_med
    ssw = sst - ssb
    return g, ng, xg, sst, ssb, ssw


def standardizare(x):
    medii = np.mean(x, axis=0)
    abaterestd = np.std(x, axis=0)
    Xstd = (x - medii) / abaterestd
    return Xstd


def centrare(x):
    medii = np.mean(x, axis=0)
    return x - medii


# Regularizare vectori proprii
def regularizare(t, y=None):
    if type(t) is pd.DataFrame:
        for c in t.columns:
            minim = t[c].min()
            maxim = t[c].max()
            if abs(minim) > abs(maxim):
                t[c] = -t[c]
                if y is not None:
                    k = t.columns.get_loc(c)#determina indexul coloanei
                    y[:, k] = -y[:, k]
    else:
        for i in range(np.shape(t)[1]):
            minim = np.min(t[:, i])
            maxim = np.max(t[:, i])
            if np.abs(minim) > np.abs(maxim):
                t[:, i] = -t[:, i]


# Regularizare vectori proprii
def regularizare2(x, y):
    for i in range(np.shape(x)[1]):
        minim = np.min(x[:, i])
        maxim = np.max(x[:, i])
        if np.abs(minim) > np.abs(maxim):
            x[:, i] = -x[:, i]
            y[:, i] = -y[:, i]


def acp(X):
    R = np.corrcoef(X, rowvar=False)
    # calcul vector si valori proprii
    valp, vecp = np.linalg.eig(R)
    # sortare valori proprii si vectori proprii
    k_inv = [k for k in reversed(np.argsort(valp))]
    alpha = valp[k_inv]
    a = vecp[:, k_inv]
    regularizare(a)
    # calcul corelatii factoriale
    Rxc = a * np.sqrt(alpha)
    # calcul componente
    # standardizare X
    medii = np.mean(X, axis=0)
    abaterestd = np.std(X, axis=0)
    Xstd = (X - medii) / abaterestd
    C = Xstd @ a
    return R, alpha, a, Rxc, C


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


def tabelare_varianta(alpha):
    m = len(alpha)
    varianta_cumulata = np.cumsum(alpha)
    procent_varianta = alpha * 100 / m
    procent_cumulat = np.cumsum(procent_varianta)
    tabel_varianta = pd.DataFrame(data={"Varianta": alpha,
                                        "Varianta Cumulata": varianta_cumulata,
                                        "Procent varianta": procent_varianta,
                                        "Procent cumulat": procent_cumulat
                                        })
    tabel_varianta.to_csv("varianta.csv")


def tabelare(X, nume_coloane=None, nume_instante=None, tabel=None):
    X_tab = pd.DataFrame(X)
    if nume_coloane is not None:
        X_tab.columns = nume_coloane
    if nume_instante is not None:
        X_tab.index = nume_instante
    if tabel is None:
        X_tab.to_csv("tabel.csv")
    else:
        X_tab.to_csv(tabel)
    return X_tab


def evaluare(C, alpha, R):
    n = np.shape(C)[0]
    # Calcul scoruri
    S = C / np.sqrt(alpha)
    # Calcul cosinusuri
    C2 = C * C
    suml = np.sum(C2, axis=1)
    q = np.transpose(np.transpose(C2) / suml)
    # Calcul contributii
    beta = C2 / (alpha * n)
    # Calcul comunalitati
    R2 = R * R
    Comun = np.cumsum(R2, axis=1)
    return S, q, beta, Comun


def bartlett_test(n, l, x, e):
    m, q = np.shape(l)
    v = np.corrcoef(x, rowvar=False)
    psi = np.diag(e)
    v_ = l @ np.transpose(l) + psi
    I_ = np.linalg.inv(v_) @ v
    det_v_ = np.linalg.det(I_)
    urma = np.trace(I_)
    chi2 = (n - 1 - (2 * m + 4 * q - 5) / 2) * (urma - np.log(det_v_) - m)
    g_lib = ((m - q) * (m - q) - m - q) / 2
    p_value = sts.chi2.cdf(chi2, g_lib)
    return chi2, p_value


def bartlett_factor(x):
    n, m = np.shape(x)
    r = np.corrcoef(x, rowvar=False)
    chi2 = -(n - 1 - (2 * m + 5) / 6) * np.log(np.linalg.det(r))
    g_lib = m * (m - 1) / 2
    p_value = 1 - sts.chi2.cdf(chi2, g_lib)
    return chi2, p_value


def bartlett_wilks_test(r, n, p, q, m):
    r_inv = np.flipud(r)
    l = np.flipud(np.cumprod(1 - r_inv * r_inv))
    dof = (p - np.arange(m)) * (q - np.arange(m))
    chi2 = (-n + 1 + (p + q + 1) / 2) * np.log(l)
    p_value = 1 - sts.chi2.cdf(chi2, dof)
    return p_value, chi2, dof


# Analiza canonica
def cca(x, y):
    n, p = np.shape(x)
    q = np.shape(y)[1]
    x = pp.StandardScaler(with_std=False).fit_transform(x)
    y = pp.StandardScaler(with_std=False).fit_transform(y)
    vx = np.cov(x, rowvar=False)
    vy = np.cov(y, rowvar=False)
    cov = np.cov(x, y, rowvar=False)
    vxy = cov[:p, p:]
    vyx = np.transpose(vxy)
    vx_inv = np.linalg.inv(vx)
    vy_inv = np.linalg.inv(vy)
    h1 = vx_inv @ vxy
    h2 = vy_inv @ vyx
    m = min(p, q)
    if p == m:
        h = h1 @ h2
        valp, vecp = np.linalg.eig(h)
        k_inv = [k for k in reversed(np.argsort(valp))]
        r2 = valp[k_inv]
        a = vecp[:, k_inv]
        r = np.sqrt(r2)
        b = (h2 @ a) @ np.diag(1 / r)
        z = x @ a
        u = y @ b
    else:
        h = h2 @ h1
        valp, vecp = np.linalg.eig(h)
        k_inv = [k for k in reversed(np.argsort(valp))]
        r2 = valp[k_inv]
        b = vecp[:, k_inv]
        r = np.sqrt(r2)
        a = (h1 @ b) @ np.diag(1 / r)
        z = x @ a
        u = y @ b
    z = pp.normalize(z, axis=0)
    u = pp.normalize(u, axis=0)
    return r, r2, z, u


def codificare(t, vars):
    for v in vars:
        t[v] = pd.Categorical(t[v]).codes


def lda(sst, ssb, n, q):
    m = len(sst)
    cov_inv = np.linalg.inv(sst)
    h = cov_inv @ ssb
    if np.allclose(h, np.transpose(h)):
        valp, vecp = np.linalg.eig(h)
    else:
        c = lin.sqrtm(ssb)
        h = np.transpose(c) @ cov_inv @ c
        valp, vecp_ = np.linalg.eig(h)
        vecp = cov_inv @ c @ vecp_
    k_inv = np.flipud(np.argsort(valp))
    r = min(m, q - 1)
    alpha = np.real(valp[k_inv[:r]])
    u = np.real(vecp[:, k_inv[:r]])
    regularizare(u)
    l = alpha * (n - q) / ((1 - alpha) * (q - 1))
    return alpha, l, u


# Calcul functii de clasificare pentru lda si pentru bayes
def functii_clasificare(x, xg, cov, ng):
    n = np.shape(x)[0]
    q = np.shape(xg)[0]
    cov_inv = np.linalg.inv(cov / n)
    f = xg @ cov_inv
    f0 = np.empty(shape=(q,))
    for i in range(q):
        f0[i] = -0.5 * f[i, :] @ xg[i, :]
    f0_b = f0 + np.log(ng / n)  # Termenii liberi pentru bayes
    return f, f0, f0_b


# Calcul functii de clasificare pe variabile discriminate
def functii_clasificare_z(z, zg, ng):
    n = np.shape(z)[0]
    q = np.shape(zg)[0]
    cov_inv = np.diag(1.0 / np.var(z, axis=0))
    f = zg @ cov_inv
    f0 = np.empty(shape=(q,))
    for i in range(q):
        f0[i] = -0.5 * f[i, :] @ zg[i, :]
    f0_b = f0 + np.log(ng / n)  # Termenii liberi pentru bayes
    return f, f0, f0_b


# Predictie pe baza scorurilor de clasificare bayesiene
def predict_bayes(x, xg, cov, ng, g):
    n, m = np.shape(x)
    cov = cov / n
    q = len(g)
    dist = np.linalg.inv(cov)
    clasif = np.empty(shape=(n,), dtype=np.int64)
    s = np.empty(shape=(n, q))
    log_p_apriori = 2 * np.log(ng / n)
    for i in range(n):
        for k in range(q):
            d = (x[i, :] - xg[k, :]) @ dist @ (x[i, :] - xg[k, :])
            s[i, k] = log_p_apriori[k] - d
        clasif[i] = np.argmax(s[i, :])
    return g[clasif]


# Predictie pe baza functiilor de clasificare
def predict(x, f, f0, g):
    n, m = np.shape(x)
    clasif = np.empty(shape=(n,), dtype=np.int64)
    for i in range(n):
        rez = f @ x[i, :] + f0
        clasif[i] = np.argmax(rez)
    return g[clasif]


def discrim_acuratete(y, clasif, g):
    q = len(g)
    n = len(y)
    mat_c = pd.DataFrame(data=np.zeros((q, q)), index=g, columns=g)
    for i in range(n):
        mat_c.loc[y[i], clasif[i]] += 1
    acuratete_grupe = np.diag(mat_c) * 100 / np.sum(mat_c, axis=1)
    mat_c['acuratete'] = acuratete_grupe
    return mat_c


def putere_discriminare(ssb, ssw, n, q):
    r = (n - q) / (q - 1)
    f = r * np.diag(ssb) / np.diag(ssw)
    p_value = 1 - sts.f.cdf(f, q - 1, n - q)
    return f, p_value


# def lda_cluster(x, g):
#     lda = disc.LinearDiscriminantAnalysis()
#     lda.fit(x, g)
#     u = lda.scalings_
#     regularizare(u)
#     zg = lda.means_ @ u
#     z = x @ u
#     grupe = lda.classes_
#     return z, zg, grupe


# def clustere(h, k):
#     n = np.shape(h)[0] + 1
#     g = np.arange(0, n)
#     for i in range(n - k):
#         k1 = h[i, 0]
#         k2 = h[i, 1]
#         g[g == k1] = n + i
#         g[g == k2] = n + i
#     g_ = pd.Categorical(g)
#     return ['c' + str(i) for i in g_.codes], g_.codes


# def afisare_cluster(g, etichete, nume_etichete, fisier):
#     g_ = np.array(g)
#     grupe = list(set(g))
#     m = len(grupe)
#     tabel = pd.DataFrame(index=grupe)
#     clustere = np.full(shape=(m), fill_value="", dtype=np.chararray)
#     for i in range(m):
#         cluster = etichete[g_ == grupe[i]]
#         cluster_str = ""
#         for v in cluster:
#             cluster_str = cluster_str + (v+" ")
#         clustere[i] = cluster_str
#     tabel[nume_etichete] = clustere
#     tabel.to_csv(fisier)


# # h - ierarhia
# # k - numar de culori
# # coduri - codurile clusterelor
# def culori_clustere(h, k, coduri):
#     culori = np.array(grafice._CULORI)
#     nr_culori = len(culori)
#     m = np.shape(h)[0]
#     n = m + 1
#     # culori_clustere = np.full(shape=(2 * n * 1,), fill_value="", dtype=np.chararray)
#     culori_clustere = np.full(shape=(2 * n * 1,), dtype=np.chararray)
#     # stabilire culoare clustere singleton
#     for i in range(n):
#         culori_clustere[i] = culori[coduri[i] % nr_culori]
#     # Stabilire culoare jonctiuni
#     for i in range(m):
#         k1 = int(h[i, 0])
#         k2 = int(h[i, 1])
#         if culori_clustere[k1] == culori_clustere[k2]:
#             culori_clustere[n + i] = culori_clustere[k1]
#         else:
#             culori_clustere[n + i] = 'k'
#     return culori_clustere

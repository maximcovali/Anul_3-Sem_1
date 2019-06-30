import seaborn as sb
import matplotlib.pyplot as plt
import matplotlib.colors as color
import numpy as np
import gui
import scipy.cluster.hierarchy as hclust

_CULORI = ['y', 'r', 'b', 'g', 'c', 'm', 'sienna', 'coral', 'darkblue', 'lime','grey',
           'tomato', 'indigo', 'teal', 'orange', 'darkgreen']


# x sy y sunt masive numpy cu doua coloane
def biplot(x, y, xlabel="x", ylabel="y", title="Biplot", l1=None, l2=None):
    f = plt.figure(figsize=(10, 7))
    ax = f.add_subplot(1, 1, 1)
    assert isinstance(ax, plt.Axes)
    ax.set_title(title, fontsize=14)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.scatter(x[:, 0], x[:, 1], c='r', label='Set X')
    ax.scatter(y[:, 0], y[:, 1], c='b', label='Set Y')
    if l1 is not None:
        for i in range(len(l1)):
            ax.text(x[i, 0], x[i, 1], l1[i])
    if l2 is not None:
        for i in range(len(l2)):
            ax.text(y[i, 0], y[i, 1], l2[i])
    ax.legend()


def corelograma(t, title=None, valmin=-1, valmax=1):
    f = plt.figure(title, figsize=(8, 7))
    f1 = f.add_subplot(1, 1, 1)
    f1.set_title(title, fontsize=16, color='b', verticalalignment='bottom')
    sb.heatmap(np.round(t, 2), cmap='bwr', vmin=valmin, vmax=valmax, annot=True)


def plot_varianta(alpha, titlu='Plot varianta'):
    n = len(alpha)
    f = plt.figure(titlu, figsize=(10, 7))
    f1 = f.add_subplot(1, 1, 1)
    f1.set_title(titlu, fontsize=16, color='b', verticalalignment='bottom')
    f1.set_xticks(np.arange(1, n + 1))
    f1.set_xlabel('Componenta', fontsize=12, color='r', verticalalignment='top')
    f1.set_ylabel('Varianta', fontsize=12, color='r', verticalalignment='bottom')
    f1.plot(np.arange(1, n + 1), alpha, 'ro-')
    f1.axhline(1, c='g')
    j_Kaiser = np.where(alpha < 1)[0][0]
    eps = alpha[:n - 1] - alpha[1:]
    d = eps[:n - 2] - eps[1:]
    j_Cattel = np.where(d < 0)[0][0]
    f1.axhline(alpha[j_Cattel + 1], c='m')
    return j_Cattel + 2, j_Kaiser


def t_scatter(x, y, label=None, tx="", ty="", titlu='Scatterplot'):
    f = plt.figure(figsize=(10, 7))
    f1 = f.add_subplot(1, 1, 1)
    f1.set_title(titlu, fontsize=16, color='b', verticalalignment='bottom')
    f1.set_xlabel(tx, fontsize=12, color='r', verticalalignment='top')
    f1.set_ylabel(ty, fontsize=12, color='r', verticalalignment='bottom')
    f1.scatter(x=x, y=y, c='r')
    if label is not None:
        n = len(label)
        for i in range(n):
            f1.text(x[i], y[i], label[i])


def t_scatter_s(x, y, x1, y1, label=None, label1=None, tx="", ty="", titlu='Scatterplot set suplimentar'):
    f = plt.figure(titlu, figsize=(10, 7))
    f1 = f.add_subplot(1, 1, 1)
    f1.set_title(titlu, fontsize=16, color='b', verticalalignment='bottom')
    f1.set_xlabel(tx, fontsize=12, color='r', verticalalignment='top')
    f1.set_ylabel(ty, fontsize=12, color='r', verticalalignment='bottom')
    f1.scatter(x=x, y=y, c='r')
    f1.scatter(x=x1, y=y1, c='b')
    if label is not None:
        n = len(label);
        p = len(label1)
        for i in range(n):
            f1.text(x[i], y[i], label[i], color='k')
        for i in range(p):
            f1.text(x1[i], y1[i], label1[i], color='k')


def cercul_corelatiilor_2(t1, t2, xlabel="x", ylabel="y", titlu="", s1="Set x", s2="Set y"):
    f = plt.figure(figsize=(8, 7))
    ax = f.add_subplot(1, 1, 1)
    x = [v for v in np.arange(0, np.math.pi * 2, 0.01)]
    cosx = np.cos(x)
    sinx = np.sin(x)
    ax.plot(cosx, sinx)
    ax.axhline(0, color='k')
    ax.axvline(0, color='k')
    ax.set_title(titlu)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.scatter(t1.iloc[:, 0], t1.iloc[:, 1], c='r', label=s1)
    ax.scatter(t2.iloc[:, 0], t2.iloc[:, 1], c='b', label=s2)
    ax.legend()
    n = len(t1)
    m = len(t2)
    for i in range(n):
        ax.text(t1.iloc[i, 0], t1.iloc[i, 1], t1.index[i])
    for i in range(m):
        ax.text(t2.iloc[i, 0], t2.iloc[i, 1], t2.index[i])


def cercul_corelatiilor(R, k1, k2, titlu="Cercul corelatiilor"):
    plt.figure(titlu, figsize=(6, 6))
    plt.title(titlu, fontsize=16, color='b', verticalalignment='bottom')
    x = [v for v in np.arange(0, np.math.pi * 2, 0.01)]
    cosx = np.cos(x);
    sinx = np.sin(x)
    plt.plot(cosx, sinx)
    plt.axhline(0, color='g');
    plt.axvline(0, color='g')
    plt.scatter(R.iloc[:, k1], R.iloc[:, k2], c='r')
    plt.xlabel(R.columns[k1], fontsize=12, color='r', verticalalignment='top')
    plt.ylabel(R.columns[k2], fontsize=12, color='r', verticalalignment='bottom')
    for i in range(len(R)):
        plt.text(R.iloc[i, k1], R.iloc[i, k2], R.index[i])


# Plot scoruri discriminante si centrii
def scatter(x, y, g, etichete, x1, y1, g1, etichete1,
            titlu='Plot instante in axele discriminante', lx='z1', ly='z2'):
    q = len(etichete1)
    # rampa = plt.get_cmap('rainbow',q)
    f = plt.figure(figsize=(10, 7))
    ax = f.add_subplot(1, 1, 1)
    ax.set_title(titlu, fontsize=16, color='b')
    ax.set_xlabel(lx, fontsize=12, color='b')
    ax.set_ylabel(ly, fontsize=12, color='b')
    sb.scatterplot(x=x, y=y, hue=g, ax=ax, hue_order=g1)
    sb.scatterplot(x=x1, y=y1, hue=g1, ax=ax, legend=False, marker='s',
                   s=200)
    for i in range(len(etichete)):
        ax.text(x[i], y[i], etichete[i])
    for i in range(len(etichete1)):
        ax.text(x1[i], y1[i], etichete1[i], fontsize=16)


def plot_clustere(x, y, g, grupe, etichete=None, titlu="Plot clustere"):
    g_ = np.array(g)
    f = plt.figure(figsize=(10, 7))
    ax = f.add_subplot(1, 1, 1)
    ax.set_title(titlu, fontsize=16, color='b')
    nr_grupe = len(_CULORI)
    for v in grupe:
        x_ = x[g_ == v]
        y_ = y[g_ == v]
        k = int(v[1:])
        if len(x_) == 1:  # Cluster singleton
            ax.scatter(x_, y_, color='k', label=v)
        else:
            ax.scatter(x_, y_, color=_CULORI[k % nr_grupe], label=v)
    ax.legend()
    if etichete is not None:
        for i in range(len(etichete)):
            ax.text(x[i], y[i], etichete[i])


# Functie care traseaza distributia de probabilitate pe grupe
def distributie(z, y, g, titlu=""):
    f = plt.figure(figsize=(10, 7))
    assert isinstance(f, plt.Figure)
    ax = f.add_subplot(1, 1, 1)
    assert isinstance(ax, plt.Axes)
    ax.set_title(titlu, fontsize=14, color='b')
    for v in g:
        sb.kdeplot(data=z[y == v], shade=True, ax=ax, label=v)
    # plt.show()


def histograme(x, g, var):
    grupe = set(g)
    g_ = np.array(g)
    m = len(grupe)
    l = np.trunc(np.sqrt(m))
    if l * l != m:
        l += 1
    c = m // l
    if c * l != m:
        c += 1
    axe = []
    f = plt.figure(figsize=(12, 7))
    for i in range(1, m + 1):
        ax = f.add_subplot(l, c, i)
        axe.append(ax)
        ax.set_xlabel(var, fontsize=12, color='b')
    for v, ax in zip(grupe, axe):
        y = x[g_ == v]
        ax.hist(y, bins=10, label=v, rwidth=0.9, range=(min(x), max(x)))
        ax.legend()


def dendrograma(h, etichete=None, titlu='Grupare ierarhica', threshold=None, culori=None):
    f = plt.figure(figsize=(10, 7))
    ax = f.add_subplot(1, 1, 1)
    ax.set_title(titlu, fontsize=14, color='b')
    if culori is None:
        hclust.dendrogram(h, labels=etichete, leaf_rotation=30, ax=ax, color_threshold=threshold)
    else:
        hclust.dendrogram(h, labels=etichete, leaf_rotation=30, ax=ax,
                          link_color_func=lambda k: culori[k])


def show():
    plt.show()

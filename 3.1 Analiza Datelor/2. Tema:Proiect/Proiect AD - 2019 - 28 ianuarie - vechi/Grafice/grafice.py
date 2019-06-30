import seaborn as sb
import matplotlib.pyplot as plt
import numpy as np

def corelograma(t,title=None,valmin=-1,valmax=1):
    f = plt.figure(title)
    f1 = f.add_subplot(1,1,1)
    f1.set_title(title,fontsize=14,color='b',verticalalignment='bottom')
    sb.heatmap(np.round(t,2),cmap='bwr',vmin=valmin,vmax=valmax,annot=True)


def plot_varianta(alpha, titlu='Plot varianta'):
    n = len(alpha)
    f = plt.figure(titlu,figsize=(10,7))
    f1 = f.add_subplot(1,1,1)
    f1.set_title(titlu,fontsize=10,color='b',verticalalignment='bottom')
    f1.set_xticks(np.arange(1,n+1))
    f1.set_xlabel('Componenta',fontsize=10,color='r',verticalalignment='top')
    f1.set_ylabel('Varianta',fontsize=10,color='r',verticalalignment='bottom')
    f1.plot(np.arange(1, n + 1),alpha,'ro-')
    f1.axhline(1,c='g')
    j_Kaiser = np.where(alpha < 1)[0][0]
    eps = alpha[:n - 1] - alpha[1:]
    d = eps[:n-2]-eps[1:]
    j_Cattel = np.where(d<0)[0][0]
    f1.axhline(alpha[j_Cattel + 1], c='m')
    return j_Cattel+2,j_Kaiser


def t_scatter(x,y,label=None,tx="",ty="",titlu='Scatterplot'):
    f = plt.figure(titlu, figsize=(10, 7))
    f1 = f.add_subplot(1, 1, 1)
    f1.set_title(titlu,fontsize=10,color='b',verticalalignment='bottom')
    f1.set_xlabel(tx,fontsize=10,color='r',verticalalignment='top')
    f1.set_ylabel(ty,fontsize=10,color='r',verticalalignment='bottom')
    f1.scatter(x=x,y=y,c='r')
    if label is not None:
        n = len(label)
        for i in range(n):
            f1.text(x[i],y[i],label[i])

def t_scatter_s(x,y,x1,y1,label=None,label1=None,tx="",ty="",titlu='Scatterplot set suplimentar'):
    f = plt.figure(titlu, figsize=(10, 7))
    f1 = f.add_subplot(1, 1, 1)
    f1.set_title(titlu,fontsize=16,color='b',verticalalignment='bottom')
    f1.set_xlabel(tx,fontsize=12,color='r',verticalalignment='top')
    f1.set_ylabel(ty,fontsize=12,color='r',verticalalignment='bottom')
    f1.scatter(x=x,y=y,c='r')
    f1.scatter(x=x1,y=y1,c='b')
    if label is not None:
        n = len(label);p = len(label1)
        for i in range(n):
            f1.text(x[i],y[i],label[i],color='k')
        for i in range(p):
            f1.text(x1[i],y1[i],label1[i],color='k')

def cercul_corelatiilor(R,k1,k2,titlu="Cercul corelatiilor"):
    plt.figure(titlu,figsize=(6,6))
    plt.title(titlu, fontsize=16, color='b',verticalalignment='bottom')
    x =[v for v in np.arange(0,np.math.pi*2,0.01)]
    cosx = np.cos(x);sinx = np.sin(x)
    plt.plot(cosx,sinx)
    plt.axhline(0,color='g');plt.axvline(0,color='g')
    plt.scatter(R.iloc[:,k1],R.iloc[:,k2],c='r')
    plt.xlabel(R.columns[k1],fontsize=12,color='r',verticalalignment='top')
    plt.ylabel(R.columns[k2],fontsize=12,color='r',verticalalignment='bottom')
    for i in range(len(R)):
        plt.text(R.iloc[i,k1],R.iloc[i,k2],R.index[i])


def show():
    plt.show()

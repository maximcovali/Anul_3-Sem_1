# Import biblioteci si module externe
import Functii.functii as functii
import pandas as pd
import numpy as np
import Gui.gui as gui
import Grafice.grafice as grafice
import scipy.cluster.hierarchy as clusth
import matplotlib.pyplot as plt



# Citire date
t = pd.read_csv('Teritorial/Teritorial2016/Mortalitate.csv', index_col=0)
# print(t)
# preluare nume variabile
nume_variabile = np.array(t.columns)
# selectie variabile model
variabile_model = gui.Check(nume_variabile, "Selectati variabilele modelului:")
x = t[variabile_model].values
# print(x)
functii.inlocuire_na(x)
R, alpha, a, Rxc, coloana = functii.acp(x)
nume_componente = ['C' + str(i) for i in range(1, len(variabile_model) + 1)] #ca sa apara C1, C2

rxc_t = pd.DataFrame(data=Rxc, index=variabile_model, columns=nume_componente)
rxc_t.to_csv("Rxc.csv")


C_t = pd.DataFrame(data=coloana, index=t.index, columns=nume_componente)
C_t.to_csv("C.csv")

grafice.corelograma(rxc_t, title="Corelograma corelatii Variabile-Componente")
grafice.t_scatter(coloana[:, 0], coloana[:, 1], np.array(t.index), 'C1', 'C2', "Plot componente - axele 1x2")
grafice.show()


# cluster
functii.inlocuire_na_df(t)
z = clusth.linkage(t[variabile_model].values,method='ward')
print(z)
clusth.dendrogram(z,labels=t.index)
plt.show()
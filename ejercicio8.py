# -*- coding: utf-8 -*-
"""
Created on Mon Jun  7 20:02:08 2021

@author: gonza
"""

'''
K-means es uno de los algoritmos más básicos en Machine Learning no supervisado. 
Es un algoritmo de clusterización, que agrupa datos que comparten características similares. 
Recordemos que entendemos datos como n realizaciones del vector aleatorio X.

El algoritmo funciona de la siguiente manera:

 1_ El usuario selecciona la cantidad de clusters a crear n. 
 2_ Se seleccionan n elementos aleatorios de X como posiciones iniciales del los centroides C.
 3_ Se calcula la distancia entre todos los puntos en X y todos los puntos en C.
 4_ Para cada punto en X se selecciona el centroide más cercano de C.
 5_ Se recalculan los centroides C a partir de usar las filas de X que pertenecen a cada centroide.
 6_ Se itera entre 3 y 5 una cantidad fija de veces o hasta que la posición de los centroides no cambie dada una tolerancia.
 
Se debe por lo tanto implementar la función k_means(X, n) de manera tal que, al finalizar, devuelva la posición de los 
centroides y a qué cluster pertenece cada fila de X.

Hint: para (2) utilizar funciones de np.random, para (3) y (4) usar los ejercicios anteriores, para (5) es válido 
utilizar un for. Iterar 10 veces entre (3) y (5).
'''

'''
datos = n realizaciones del vector aleatorio X

'''

print("\n---- Ejercicio 8 ----")
print("Implementación Básica de K-means\n")

import numpy as np
import pickle
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

MAX_ITERATIONS = 5

class SyntheticDataset(object):
    
    def __init__(self, n_samples, n_cluster, nv_overlap):
        self.n_samples = n_samples
        self.n_cluster = n_cluster
        self.nv_overlap = nv_overlap
       # self.data, self.cluster_ids = self._build_cluster()
        
    def train_valid_slpit(self):
        idxs = np.random.permutation(self.n_samples)
        n_train_samples = int(self.n_samples * 0.8)
        train = self.data[idxs[:n_train_samples]]
        train_cluster_ids = self.cluster_ids[idxs[:n_train_samples]]
        valid = self.data[idxs[n_train_samples:]]
        valid_cluster_ids = self.cluster_ids[idxs[n_train_samples:]]
        return train, train_cluster_ids, valid, valid_cluster_ids
    
    @staticmethod
    def reduce_dimension(data, n_components):
        data_std = StandardScaler().fit_transform(data)
        pca = PCA(n_components=n_components)
        return pca.fit_transform(data_std)
        
    def _build_cluster(self):
        centroids = self.nv_overlap * np.random.random_sample((self.n_cluster, 2))
        data = np.repeat(centroids, self.n_samples/self.n_cluster, axis=0)
        print("Centroides \n", centroids)
        #print("Data sin ruido\n", data)
        #s = np.random.normal(mu, sigma, 1000)
        normal_noise = np.random.normal(loc=0, scale=0.5, size=(len(data), 2))
        data = data + normal_noise
        self.data = data
        #print("Data con ruido\n", data)
        cluster_ids = np.array([
            [0],
            [1],
        ])
        cluster_ids = np.repeat(cluster_ids, self.n_samples / 2, axis=0)
        return data, cluster_ids

def k_means(data, n_cluster, nv_overlap):  # el usuario selecciona la cantidad de clusters a crear n
    '''
    numpy.eye(N, M=None, k=0, dtype=<class 'float'>, order='C', *, like=None)
    Return a 2-D array with ones on the diagonal and zeros elsewhere.
    '''
    #data = self.data
    centroids = nv_overlap * np.random.random_sample((n_cluster, 2))
    for i in range(MAX_ITERATIONS):
        print("Iteration # {}".format(i))
        centroids, cluster_ids = k_means_loop(data, centroids)
    return centroids, cluster_ids

def k_means_loop(data, centroids):
    # encontrar el label de cada fila de X en funcion de los centroides
    print("Centroides nuevos \n", centroids)
    print("Centroid shape", centroids.shape)
    expanded_centroids = centroids[:, None]
    print("Expanded centroid shape", expanded_centroids.shape)
    print("Data shape", data.shape)

    distances = np.sqrt(np.sum((expanded_centroids - data) ** 2, axis=2))
    print("Distances shape", data.shape)
    arg_min = np.argmin(distances, axis=0)
    print("arg_min shape", arg_min.shape)

    # rederterminar los centroides
    for i in range(centroids.shape[0]):
        centroids[i] = np.mean(data[arg_min == i, :], axis=0)
    return centroids, arg_min




if __name__ == '__main__':
    print("Creamos el dataset")
    synthetic_dataset = SyntheticDataset(n_samples= 200, n_cluster = 4, nv_overlap = 20)

    data, cluster_ids = synthetic_dataset._build_cluster()
    x, y = zip(*data)
    plt.scatter(x,y)
    plt.show()
    centroids, cluster_ids = k_means(data, n_cluster = 4, nv_overlap = 20)

print("Nuevos centroides \n", centroids)
print("Pertenencia de los puntos  a los respectivos centroides\n", cluster_ids)
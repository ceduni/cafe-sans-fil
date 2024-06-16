'''
Ce fichier contient le code des algorithmes de la section 2 du document
"Logique" du wiki.
'''
import numpy as np

# This method takes the actual user and the menu as parameters and return.
def meal_not_consumed(menu, user) -> list:
    return

def intersection(A: list, B: list) -> list:
    res = []
    for elem in A:
        if elem in B:
            res.append(elem)
    return res

### Test the code with each similarity and choose the best one.
def jaccard(A: list, B: list):
    A.extend(B)
    inter = intersection(A, B)
    return len(inter) / len(A)

def cosine_similarity(x,y):
    return

def pearson_correlation(x,y):
    return
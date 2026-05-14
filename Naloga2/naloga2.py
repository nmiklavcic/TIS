"""
Naloga 2 - Ocena kanala in izracun kapacitete.

V tej datoteki so podani prototipi funkcij, ki jih morate implementirati.
Funkcije naj uporabljajo samo standardno knjiznico Python, modul math in numpy.
"""

import numpy as np
import math
    
def estimate_channel(x: list[int], y: list[int], m: int, n: int) -> np.ndarray:
    """
    Oceni diskretni kanal iz opazovanih vhodnih in izhodnih simbolov.

    Parametri
    ----------
    x : list[int]
        Dovoljeni vhodni simboli so stevila od 0 do m-1.
    y : list[int]
        Dovoljeni izhodni simboli so stevila od 0 do n-1.
    m : int
        Stevilo moznih vhodnih simbolov.
    n : int
        Stevilo moznih izhodnih simbolov.

    Vrne
    -------
    W : np.ndarray
        Dvodimenzionalna matrika velikosti n x m z elementi W[y, x] = P(Y=y | X=x).

    Sprozi
    ------
    ValueError
        Ce sta x in y razlicnih dolzin ali se kaksen simbol pojavi zunaj dovoljenega obsega.
    """
    # Tukaj napisite svojo kodo.
    
    if len(x) != len(y) :
        raise ValueError
    
    
    xapp = [0 for _ in range(m)]
    appears = [[0 for _ in range(m)] for _ in range(n)]
    
    for i in range(0,len(x)) :
        if x[i] >= m or y[i] >= n or x[i] < 0 or y[i] < 0 :
            raise ValueError
        else :
            appears[y[i]][x[i]] += 1
            xapp[x[i]] += 1
            # DEBUG
            # print(xapp)
    
    # DEBUG
    # print(" ")
    # print(xapp)
    W = np.zeros((n, m))
    
    for i in range(m) :
        for j in range(n) :
            # DEBUG 
            # print(appears[i][j]/(m*n), xapp[i]/len(x))
            # print()
            W[j][i] = (appears[j][i]/len(x))/(xapp[i]/len(x))
    
    return W 


def blahut_arimoto(
    W: np.ndarray,
    tol: float = 1e-9,
    max_iter: int = 1000,
) -> np.ndarray:
    """
    Izracuna vhodno porazdelitev in kapaciteto kanala z algoritmom Blahut-Arimoto.

    Parametri
    ----------
    W : np.ndarray
        Dvodimenzionalna matrika velikosti n x m z elementi W[y, x] = P(Y=y | X=x).
    tol : float
        Toleranca za preverjanje konvergence.
    max_iter : int
        Najvecje stevilo iteracij.

    Vrne
    -------
    p_star : np.ndarray
        Priblizek optimalne vhodne porazdelitve dolzine m

    Sprozi
    ------
    ValueError
        Ce ima W kaksen stolpec ni veljavna porazdelitev.
    """
    # Tukaj napisite svojo kodo.
    pass


def compute_capacity(W: np.ndarray, p: np.ndarray) -> float:
    """
    Izracuna I(X;Y) za dan kanal W in vhodno porazdelitev p.

    Parametri
    ----------
    W : np.ndarray
        Dvodimenzionalna matrika velikosti n x m z elementi W[y, x] = P(Y=y | X=x).
    p : np.ndarray
        Enodimenzionalna vhodna porazdelitev dolzine m, kjer je p[x] = P(X=x).

    Vrne
    -------
    C_bits : float
        Vrednost I(X;Y) v bitih.
    """
    # Tukaj napisite svojo kodo.
    pass


def estimate_capacity(
    x: list[int],
    y: list[int],
    m: int,
    n: int,
    tol: float = 1e-9,
    max_iter: int = 1000,
) -> float:
    """
    Oceni kanal iz podatkov in vrne njegovo kapaciteto.

    Parametri
    ----------
    x : list[int]
        Vhodni simboli so stevila od 0 do m-1.
    y : list[int]
        Izhodni simboli so stevila od 0 do n-1.
    m : int
        Stevilo moznih vhodnih simbolov.
    n : int
        Stevilo moznih izhodnih simbolov.
    tol : float
        Toleranca za algoritem Blahut-Arimoto.
    max_iter : int
        Najvecje stevilo iteracij algoritma Blahut-Arimoto.

    Vrne
    -------
    C_bits : float
        Ocenjena kapaciteta kanala v bitih.
    """
    # Tukaj napisite svojo kodo.
    pass


def make_bsc_dataset(
    n: int,
    p: float,
    seed: int | None = None,
) -> tuple[list[int], list[int]]:
    """
    Ustvari nakljucne podatke za binarni simetricni kanal.

    Generira n vhodnih simbolov enakomerno iz {0, 1}. Vsak simbol se z
    verjetnostjo p obrne. Z izbiro seed dobite ponovljive podatke.
    """
    rng = np.random.default_rng(seed)
    x = rng.integers(0, 2, size=n).tolist()
    flip = rng.random(n) < p
    y = [xi ^ int(f) for xi, f in zip(x, flip)]
    return x, y


def make_bec_dataset(
    n: int,
    epsilon: float,
    seed: int | None = None,
) -> tuple[list[int], list[int]]:
    """
    Ustvari nakljucne podatke za binarni kanal z brisanjem (BEC).

    Generira n vhodnih simbolov enakomerno iz {0, 1}. Vsak simbol se z
    verjetnostjo epsilon izbrise (izhodni simbol 2). Z izbiro seed dobite
    ponovljive podatke.
    """
    rng = np.random.default_rng(seed)
    x = rng.integers(0, 2, size=n).tolist()
    erased = rng.random(n) < epsilon
    y = [2 if e else xi for xi, e in zip(x, erased)]
    return x, y


def make_zchannel_dataset(
    n: int,
    p: float,
    seed: int | None = None,
) -> tuple[list[int], list[int]]:
    """
    Ustvari nakljucne podatke za binarni Z-kanal.

    Generira n vhodnih simbolov enakomerno iz {0, 1}. Vhod 0 se vedno prenese
    kot 0. Vhod 1 se z verjetnostjo p prenese kot 0, sicer kot 1. Z izbiro
    seed dobite ponovljive podatke.
    """
    rng = np.random.default_rng(seed)
    x = rng.integers(0, 2, size=n).tolist()
    flip = rng.random(n) < p
    y = [0 if xi == 0 else (0 if f else 1) for xi, f in zip(x, flip)]
    return x, y


if __name__ == "__main__":
    x = [3,2,0,2,3,0,2,1,0,1,2,0,2,4,2,4,2,2,3,2]
    y = [2,3,0,4,2,0,2,5,2,0,5,5,3,3,5,0,5,3,5,0]
    a = estimate_channel(x, y, 5, 6)
    print(x)
    print(y)
    print()
    print("      Y  Y  Y  Y  Y  Y")
    print("      0  1  2  3  4  5")
    for i in range(0, len(a)) :
        print("X:",i,a[i])
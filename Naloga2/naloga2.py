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
    m = len(W[0])
    n = len(W)
    

    
    i = 0
    p = np.ones(m) / m
    
    
    if not np.allclose(W.sum(axis=0), 1.0):
        raise ValueError("W columns must sum to 1")

    
    while i < max_iter :
        
        r = W @ p
        r = np.where(r > 0, r, 1.0)
        ratio = np.where(W > 0, W / r[:, np.newaxis], 1.0)
        log_ratio = np.where(W > 0, np.log(ratio), 0.0)
        c = (W * log_ratio).sum(axis=0)

        unnorm = p * np.exp(c)
        p_new = unnorm / unnorm.sum()

        if np.max(np.abs(p_new - p)) < tol:
            return p_new

        p = p_new


        
    return p


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
    q = W @ p  # output marginal

    q_safe = np.where(q > 0, q, 1.0)
    H_Y = -np.sum(np.where(q > 0, q * np.log2(q_safe), 0.0))

    H_Y_given_X = 0.0
    for xi in range(len(p)):
        col = W[:, xi]
        col_safe = np.where(col > 0, col, 1.0)
        H_Y_given_X += p[xi] * (-np.sum(np.where(col > 0, col * np.log2(col_safe), 0.0)))

    
    I = H_Y - H_Y_given_X
    
    return I


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
    W = estimate_channel(x, y, m, n)
    p_star = blahut_arimoto(W, tol, max_iter)
    I = compute_capacity(W, p_star)
    return I 



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
    print(x)
    print(y)
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
    print(x)
    print(y)
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
    print(x)
    print(y)
    return x, y


if __name__ == "__main__":
    # BSC with p=0.1 — expected capacity ≈ 1 - H(0.1) ≈ 0.531 bits
    print("=== BSC (p=0.1) ===")
    x, y = make_bsc_dataset(100, p=0.1, seed=42)
    W = estimate_channel(x, y, 2, 2)
    print("Channel matrix W:\n", W)
    p_star = blahut_arimoto(W)
    print("Optimal input distribution:", p_star)
    print("Capacity:", compute_capacity(W, p_star), "bits")

    print()

    # BEC with epsilon=0.3 — expected capacity = 1 - 0.3 = 0.7 bits
    print("=== BEC (epsilon=0.3) ===")
    x, y = make_bec_dataset(100, epsilon=0.3, seed=42)
    W = estimate_channel(x, y, 2, 3)
    print("Channel matrix W:\n", W)
    p_star = blahut_arimoto(W)
    print("Optimal input distribution:", p_star)
    print("Capacity:", compute_capacity(W, p_star), "bits")

    print()

    # Z-channel with p=0.5
    print("=== Z-channel (p=0.5) ===")
    x, y = make_zchannel_dataset(100, p=0.5, seed=42)
    W = estimate_channel(x, y, 2, 2)
    print("Channel matrix W:\n", W)
    p_star = blahut_arimoto(W)
    print("Optimal input distribution:", p_star)
    print("Capacity:", compute_capacity(W, p_star), "bits")

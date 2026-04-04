#### Stiskanje podatkov ####
# - Stiskanje bre izgube
#   Navadno namenjen za tekstovne datoteke
#   Pdobno kot WinZip, WinRAR, grzip ...
#   Uporabili bomo alg za kodiranje bajtnih parov
#
## Algoritem kodiranja bajtnih parov ##
## Byte Pair Encoding ##
# - Uporabljan pri segmentaciji besedil v žetone pri
#   jezikovnih modelih kot so GPT-2 GPT-3 in BERT
# - Delovanje :
#   Deluje na principu iterativnega združevanja
#   najpogostejših PAROV znakov v nizu. V vsakem
#   koraku alg poiščemo najpogostelši par znakov in 
#   ga zamenjamo z indeksom znakov v slovarju.
#   Postopek ponavljamodokler v nizu ne najdemo več
#   parov ki jih lahko združimo ali pa dokler ne 
#   presežemo določenega števila vnosov v slovarju
#
# - Dejanski agoritem z besedami:
#
# ENCODE ALG
#
# 1. Inicializiramo začetni seznam vrednosti znakov S (nabor ASCII)
# 2. Znake ASCII v vhodnem nizu zamenjamo z indeksi i S - 256 znakov ASCII so indeksirani z indeksi od 0 do 255
# 3. Ponavljaš :
#    a) preštej pojavitve vseh parov znakov [z1,z2] v vhodnem nizu
#    b) poišči najpogostejši par znakov Z = najpogostejši [z1,z2]
#    c) če je frekvenca Z < 2 ali pa je presežena dovoljena dolžina S (4096), prekini
#    d) na konec seznama S dodaš Z
#    e) k = indeks(Z)
#    f) zamenjaj vse pare znakov Z v vhodnem nizu s k
#
# DECODE ALG
#
# 1. preberi seznam znakov S
# 2. i = dolzina(s) - 1
# 3. ponavlhah dokler i >= 256:
#    a) zamenjaj vse pohavitve i v vhodnem nizu s S[i]
#    b) i=i-1
# 4. indekse v izhodnem nizu zamnjaj z znaki ASCII

import json
from pathlib import Path


def encode(vhod: list) -> tuple[list, list]:
    """
    Izvede kodiranje vhodnega sporocila z algoritmom BPE.

    Parameters
    ----------
    vhod : list
        Seznam vhodnih znakov ASCII.

    Returns
    -------
    (izhod, izhodS) : tuple[list, list]
        izhod : list
            Kodirano vhodno sporocilo v obliki indeksov.
        izhodS : list
            Seznam ASCII kod in parov indeksov.
    """
    # dobimo začetni seznam znakov S (nabor ASCII)
    # generiramo seznam S z indeksi od 0 do 255, ki predstavljajo znake ASCII
    S = list(range(256))
    
    # Iteriramo skozi vhod in piščemo najpogostejše pare znakov
    for i in range(256, 4096):
        # preštejemo pojavitve vseh parov znakov v vhodnem nizu in jih shranimo v slovar
        pari={}
        for j in range(len(vhod)-1):
            par=(vhod[j],vhod[j+1])
            if par in pari:
                pari[par] += 1
            else:
                pari[par] = 1
        
    
    izhod = []
    izhodS = []
    return (izhod, izhodS)


def decode(vhod: list, S: list) -> list:
    """
    Izvede dekodiranje vhodnega zaporedja indeksov z algoritmom BPE.

    Parameters
    ----------
    vhod : list
        Seznam vhodnih indeksov.
    S : list
        Seznam ASCII kod in parov indeksov.

    Returns
    -------
    izhod : list
        Dekodirano vhodno sporocilo v obliki ASCII znakov.
    """
    izhod = []
    return izhod


def compute_compression_ratio(vhod: list, izhod: list ) -> float:
    """
    Izracuna kompresijsko razmerje.

    Parameters
    ----------
    vhod : list
        Vhodno zaporedje.
    izhod : list
        Izhodno zaporedje.
    

    Returns
    -------
    R : float
        Kompresijsko razmerje.
    """
    R = float("nan")
    return R


def read_raw_text(path: str) -> list:
    """
    Prebere besedilno datoteko in vrne seznam znakov.

    Parameters
    ----------
    path : str
        Pot do vhodne datoteke .txt.

    Returns
    -------
    list
        Seznam znakov iz datoteke.
    """
    return list(Path(path).read_text(encoding="ascii"))


def write_raw_text(path: str, znaki: list) -> None:
    """
    Zapise seznam znakov v besedilno datoteko.

    Parameters
    ----------
    path : str
        Pot do izhodne datoteke .txt.
    znaki : list
        Seznam znakov za zapis.
    """
    Path(path).write_text("".join(znaki), encoding="ascii")


def read_coded_msg(path: str) -> tuple[list, list]:
    """
    Prebere JSON datoteko z izhodoma funkcije encode.

    Parameters
    ----------
    path : str
        Pot do vhodne datoteke .json.

    Returns
    -------
    tuple[list, list]
        Par seznamov (izhod, izhodS).
    """
    data = json.loads(Path(path).read_text(encoding="ascii"))
    return data["izhod"], data["izhodS"]


def write_coded_msg(path: str, izhod: list, izhodS: list) -> None:
    """
    Zapise izhoda funkcije encode v JSON datoteko.

    Parameters
    ----------
    path : str
        Pot do izhodne datoteke .json.
    izhod : list
        Kodirano sporocilo.
    izhodS : list
        Seznam ASCII kod in parov indeksov.
    """
    data = {
        "izhod": izhod,
        "izhodS": izhodS,
    }
    Path(path).write_text(
        json.dumps(data, ensure_ascii=False, indent=4),
        encoding="ascii",
    )

if __name__ == "__main__":
    # Preberemo vhodno besedilo iz datoteke
    # Datoteka je textovna, podati moramo path do nje 
    pathInput = input("Pot do vhoda: ")
    pathOutput = input("Pot do izhoda: ")
    pathTestOutput = input("Pot do testnega izhoda: ")
    vhod = read_raw_text(pathInput)
    
    # Kličemo funkcijo encode in dobimo izhod in izhodS
    izhod, izhodS = encode(vhod)
    
    # Zapišemo kodirano sporočilo v JSON na željen izhod
    write_coded_msg(pathOutput, izhod, izhodS)
    
    # Primerjamo izhod ki smo ga dobili z kodiranjem in testnim izhodom
    # Preberemo izhod JSON datoteke
    izhod, izhodS = read_coded_msg(pathOutput)
    
    # Preberemo testni izhod JSON datoteke
    test_izhod, test_izhodS = read_coded_msg(pathTestOutput)
    
    # Preverimo ali se izhod in test_izhod ujemata
    if izhod == test_izhod and izhodS == test_izhodS:
        print("Match")
    else:
        print("Error - no match")
        # izpišemo razliko med izhodom in test_izhodom
        print("Izhod:", izhod)
        print("Testni izhod:", test_izhod)
        
    # Izračunamo kompresijsko razmerje in ga izpišemo
    R = compute_compression_ratio(vhod, izhod)
    print("Kompresijsko razmerje:", R)
        
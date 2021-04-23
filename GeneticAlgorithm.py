import math
import random

# define fungsi untuk mencari nilai minimum
def fungsi_h(x1, x2):
    return ((math.cos(x1) * math.sin(x2)) - (x1 / (math.pow(x2, 2) + 1)))


# fungsi dekoder genotif
def Dec(gen):
    fenotif = []
    x1, x2 = 0, 0
    i, j = 0, 0
    while (i < len(gen)):
        while (j < len(gen[i])):
            if ((gen[i][j] == 0) and (gen[i][j + 1] == 0)):
                if (j == 0):
                    x1 = 0
                else:
                    x2 = 0
            elif ((gen[i][j] == 0) and (gen[i][j + 1] == 1)):
                if (j == 0):
                    x1 = 1
                else:
                    x2 = 1
            elif ((gen[i][j] == 1) and (gen[i][j + 1] == 0)):
                if (j == 0):
                    x1 = 2
            elif ((gen[i][j] == 1) and (gen[i][j + 1] == 1)):
                if (j == 0):
                    x1 = -1
                else:
                    x2 = -1
            j += 2
        j = 0
        i += 1
        fenotif.append([x1,x2])
    return fenotif


# fitness
def Fit(h):
    a = 0.1
    return (1 / (h + a))


# seleksi orangtua
def SelO(NFitnes):
    OT = []
    tempOT = []
    fitcop = NFitnes.copy()
    fitcop = sorted(fitcop, key=float)
    b, a = fitcop[0],fitcop[-1]
    print("Nilai RB dan RA: ",b,a)
    print()
    while(len(fitcop) != 2):
        i = 0
        found = False
        NRO = random.uniform(b,a)
        print("Nilai random seleksi orangtua: ",NRO)
        while((i < len(fitcop)) and not found):
            if(NRO <= fitcop[i]):
                IDXO = NFitnes.index(fitcop[i])
                tempOT.append(IDXO)
                print("Nilai Fitness: ", fitcop[i])
                fitcop.pop(i)
                b,a = fitcop[0],fitcop[-1]
                found = True
            i += 1
        if(len(fitcop)==2):
            tempOT.append(NFitnes.index(fitcop[0]))
            tempOT.append(NFitnes.index(fitcop[1]))
    i = 0
    while (i < len(tempOT)):
        OT.append([tempOT[i],tempOT[i+1]])
        i += 2
    return OT

#crossover
def XOver(OT,gen):
    NGen = []
    for cot in range(len(OT)):
        x1,x2 = OT[cot][0],OT[cot][1]
        temp1,temp2 = [],[]
        print("Pasangan ",cot," dengan kromosom: ")
        print("Kromosom 1: ",gen[x1])
        print("Kromosom 2: ",gen[x2])
        i = random.randrange(1,4)
        for x in range(i):
            temp1.append(gen[x1][x])
            temp2.append(gen[x2][x])
        for x in range(i,4):
            temp1.append(gen[x2][x])
            temp2.append(gen[x1][x])
        NGen.append(temp1)
        NGen.append(temp2)
        print("Diperoleh anak: ")
        print(temp1)
        print(temp2)
        print()
    return NGen

#Mutasi
def Mut(GA):
    CCD = 0.5
    for x in range(len(GA)):
        for y in range(len(GA[x])):
            i = random.uniform(0,1)
            if (i < CCD):
                if(GA[x][y] == 1):
                    GA[x][y] = 0
                else:
                    GA[x][y] = 1

#penggantian generasi
def NewGen(GL,GB,OT):
    temp = GL.copy()
    for x in range(len(OT)):
        a,b = OT[x][0],OT[x][1]
        GL[a] = GB[a]
        GL[b] = GB[b]
    print("Generasi Sebelum di lakukan generational model: ")
    for tua in temp:
        print(tua)
    print("Setelah dilakukan generational model: ")
    for muda in GB:
        print(muda)

#pendeklarasian variable global
#2,-1 0,-1 -1,0 1,-1 1,-1 0,0 0,1 1,0 1,1 2,0 2,1 -1,-1
GEN     = [[1, 0, 1, 1], [0, 0, 1, 1], [1, 1, 0, 0], [0, 1, 1, 1], [0, 1, 1, 1], [0, 0, 0, 0], [0, 0, 0, 1], [0, 1, 0, 0],
        [0, 1, 0, 1], [1, 0, 0, 0], [1, 0, 0, 1], [1, 1, 1, 1]]
nilaiH  = []
nilaiF  = []
Generation = 100
iterasi = 1


while (iterasi < Generation):
    fen = []
    h   = []
    fit = []
    OT  = []

    #pelakuan dekoding pada genotif
    print("Tahap Dekoding Genotif")
    fen = Dec(GEN)
    print("Genotif: ")
    for G in GEN:
        print(G)
    print()
    print("Fenotif: ")
    for F in fen:
        print(fen)
    print()

    #Pencarian h
    print("Tahap Pencarian Nilai h")
    x = 0
    while (x < len(fen)):
        a = fen[x][0]
        b = fen[x][1]
        h.insert(x,fungsi_h(a,b))
        print("Hasil Pencarian nilai h adalah : ",h[x])
        x += 1
    nilaiH = h.copy()
    print()


    #pencarian nilai fitness
    print("Tahap Pencarian nilai fitness")
    x = 0
    while (x < len(h)):
        print("Genotif ",GEN[x]," dengan nilai h ",h[x]," ")
        fit.insert(x,Fit(h[x]))
        print("Nilai Fitness: ",fit[x])
        x += 1
    nilaiF = fit.copy()
    print()

    #pencarian seleksi orangtua
    print("Tahap Seleksi Orangtua")
    OT = SelO(fit)
    print()
    print("Orangtua yang terpilih: ")
    x = 0
    while (x < len(OT)):
        print(OT[x])
        x += 1
    print()

    #CrossOver
    print("Tahap Crossover")
    Child = XOver(OT,GEN)
    print("Genotif Anak akan menjadi: ")
    for c in Child:
        print(c)
    print()

    #tahapan permutasian gen
    print("Tahap Permutasian Gen")
    Mut(Child)
    print("Hasil Mutasi dari gen anak: ")
    for c in Child:
        print(c)
    print()

    #tahap perubahan generasi menggunakan Generational Model
    print("Tahap Perubahan Generasi")
    NewGen(GEN,Child,OT)
    print()

    print("Hasil h dari setiap gen: ")
    i = 0
    while (i<len(nilaiH)):
        print(nilaiH[i])
        i += 1
    print()
    print("Hasil Fitness dari setiap gen: ")
    i = 0
    while (i < len(nilaiF)):
        print(nilaiF[i])
        i += 1

    MAX = 0
    INDEX = 0
    i = 0
    while(i<len(nilaiF)):
        if(MAX<nilaiF[i]):
            MAX = nilaiF[i]
            INDEX = i
            i += 1
        else:
            i += 1
    print()
    print("Kromosom Terbaik dapat ditemukan pada index ke ", INDEX, " yang merupakan genotif ", Child[INDEX],
          " dengan nilai fitness ", MAX, " dan nilai dekode kromosom ", nilaiH[INDEX])
    iterasi += 1


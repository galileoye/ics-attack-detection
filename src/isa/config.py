OPC1_IP = '172.27.18.68'
OPC1_PORT = '6061'

OPC2_IP = '172.27.18.68'
OPC2_PORT = '6072'

SIM_TIME = 200

#Process Variables
L1  = 0
L2  = 1
T1  = 2
T2  = 3
V1  = 4
V2  = 5
P   = 6
F1  = 7
F2  = 9
F3  = 10
H   = 11

def printvalues(mode, L1, L2, T1, T2, V1, V2, P, F1, F2, F3, H):
    st =   (mode+",\t" 
            "L1: "+str("{0:.4f}".format(L1))+",\t"
            "L2: "+str("{0:.4f}".format(L2))+",\t"
            "T1: "+str("{0:.4f}".format(T1))+",\t"
            "T2: "+str("{0:.4f}".format(T2))+",\t"
            "V1: "+str("{0:.4f}".format(V1))+",\t"
            "V2: "+str("{0:.4f}".format(V2))+",\t"
            "P:  "+str("{0:.4f}".format(P))+",\t"
            "F1: "+str("{0:.4f}".format(F1))+",\t"
            "F2: "+str("{0:.4f}".format(F2))+",\t"
            "F3: "+str("{0:.4f}".format(F3))+",\t"
            "H:  "+str("{0:.4f}".format(H))+"\n")
    print(st)


datalen = 1000
seq = 30
padding = 10
batch_size = 64
nb_classes = 1
nb_epoch = 5
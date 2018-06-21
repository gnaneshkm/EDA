"""Name : Pranav Govindala Shivaram """
""" Martriculation Number: 453466 """


import sys
TRACKING = set()


class Circuit:

     def readNetlist(self,file):
        """ Description of this function..."""
        with open(file,'r') as f:
            content = f.readlines()
        self.nets = int(content[0].strip())
        self.inputs  = content[1].strip().split()
        self.inputs.sort()
        self.outputs = content[2].strip().split()
        self.outputs.sort()

        # read mapping
        self.mapping = {}

        for c in range(3,len(content)):
            line = content[c].strip().split()
            if len(line)==0:
                i=c+1
                break

            self.mapping[line[1]] = int(line[0])

        # read gates
        self.gates = []
        for c in range(i,len(content)):
            bits = content[c].strip().split()
            if len(bits)>0:
                gate = bits.pop(0)
            ports = map(int,bits)
            self.gates.append((gate,ports))



     def read_CNF(self,flag,c2):
        CNF =[]
        lit =[]
        gates=self.gates
        for gate in gates:
            if gate[0]=="xor":
                for g in gate[1]: #
                    if flag==2:
                        lit.append(g+c2.nets) #
                    else:
                        lit.append(g)
                CNF.append([lit[2],lit[0],-lit[1]])#3 1 -2
                CNF.append([-lit[2],lit[0],lit[1]])#-3 1 2 => corrected the -2 that was present
                CNF.append([-lit[2],-lit[0],-lit[1]])#-3 -1 -2
                CNF.append([lit[2],-lit[0],lit[1]])#3 -1 2
                del lit[:]

            elif gate[0]=="and":
                for g in gate[1]: #
                    if flag==2:
                        lit.append(g+c2.nets) #
                    else:
                        lit.append(g)
                CNF.append([lit[2],-lit[0],-lit[1]])
                CNF.append([-lit[2],lit[0]])
                CNF.append([-lit[2],lit[1]])
                del lit[:]

            elif gate[0]=="inv":

                for g in gate[1]: #
                    if flag==2:
                        lit.append(g+c2.nets) #
                    else:
                        lit.append(g)
                CNF.append([lit[1],lit[0]])
                CNF.append([-lit[1],-lit[0]])
                del lit[:]

            elif gate[0]=="or":
                for g in gate[1]: #
                    if flag==2:
                        lit.append(g+c2.nets) #
                    else:
                        lit.append(g)
                CNF.append([-lit[2],lit[0],lit[1]])
                CNF.append([lit[2],-lit[0]])
                CNF.append([lit[2],-lit[1]])
                del lit[:]
        return CNF


class DavisAlgorithm:

    #Apply Heuristics
    def ApplyHeu(self,var, CNF_t):
        global TRACKING
        for clause in CNF_t:
            for literal in clause:
                if abs(literal)==abs(var):
                    if literal/var > 0: #check signal is 1 or 0
                        # Unit Clause
                        #CNF_t.remove(clause)
                        CNF_t = [x for x in CNF_t if x != clause]
                    else:
                        # Pure Literal
                        clause.remove(literal)

        TRACKING.add(var)
        for clause in CNF_t:
            if len(clause)==1:
                if clause[0]!=[[]]:
                    CNF_t = self.ApplyHeu(clause[0], CNF_t)
                break
        return CNF_t

    def davisputnam(self,shortCNF, guessVar, count):
        global TRACKING
        copyTrack = TRACKING.copy()
        shortCNF = self.ApplyHeu(guessVar, shortCNF)
        if count==0:
            count=1
            global CNFtemp
            CNFtemp= shortCNF
    #Check for Empty CNF
        if len(shortCNF)==0:
            print("Solution has been found!")

            return True
        else:
            #check the empty clause
            for clause in shortCNF:
                if len(clause)==0:
                    TRACKING = copyTrack
                    return False
        # Guessing
        copyshortCNF = [ele[:] for ele in shortCNF]
        last = abs(shortCNF[-1][-1])
        result = self.davisputnam(shortCNF, last, count) # Call with 1

        if result==False:
            TRACKING = copyTrack
            result = self.davisputnam(CNFtemp, -last, count) # Call with 0

        if result==False:
            TRACKING = copyTrack

        return result

    def check_equivalence(self,circuit1,circuit2,CNF_1,CNF_2):


        xor1=[]
        CNF_xor1=[]
        op1=[]
        op2=[]

        for op1 in circuit1.outputs:
            xor1.append(circuit1.mapping[circuit1.outputs[0]])
        for op2 in circuit2.outputs:
            xor1.append(circuit2.mapping[circuit2.outputs[0]]+circuit1.nets)
        xor1.append(circuit1.nets+circuit2.nets+1)

        CNF_xor1.append([xor1[2],xor1[0],-xor1[1]])
        CNF_xor1.append([-xor1[2],xor1[0],xor1[1]])
        CNF_xor1.append([-xor1[2],-xor1[0],-xor1[1]])
        CNF_xor1.append([xor1[2],-xor1[0],xor1[1]])

        CNF_inn=[]# INPUTS CONNECTION
        inn1=[]
        ip1=[]
        for input1, input2 in zip(circuit1.inputs, circuit2.inputs):
            CNF_inn.append([circuit1.mapping[input1],-(circuit2.mapping[input2]+circuit1.nets)])
            CNF_inn.append([-circuit1.mapping[input1],(circuit2.mapping[input2]+circuit1.nets)])
        xors_cnf=[]#OUTPUTS CONNECTION WITH XOR

        increment = 1
        INC=[]
        for gate1, gate2 in zip(circuit1.outputs, circuit2.outputs):
            xors_cnf.append([(circuit1.nets+circuit2.nets+increment),circuit1.mapping[gate1],-(circuit2.mapping[gate2]+circuit1.nets)])#3 1 -2
            xors_cnf.append([-(circuit1.nets+circuit2.nets+increment),circuit1.mapping[gate1],(circuit2.mapping[gate2]+circuit1.nets)])#-3 1 2 => corrected the -2 that was present
            xors_cnf.append([-(circuit1.nets+circuit2.nets+increment),-circuit1.mapping[gate1],-(circuit2.mapping[gate2]+circuit1.nets)])#-3 -1 -2
            xors_cnf.append([(circuit1.nets+circuit2.nets+increment),-circuit1.mapping[gate1],(circuit2.mapping[gate2]+circuit1.nets)])#3 -1 2
            increment += 1
            INC.append(circuit1.nets+circuit2.nets+increment-1)
        #print(xors_cnf)
        # Appending the OR gates
        CNF=CNF_1+CNF_2+xors_cnf+CNF_inn
        CNF.append(INC)
        CNF.append([max(INC)+len(INC)-1])# static '1'


        varE = CNF[-1][-1]
        count =0
        result=self.davisputnam(CNF, varE, count)
##        print (TRACKING)
        return result

    def print_result(self,res,c1,c2):
        if res:
            print ("Not Equivalent. Counter example:")

            print ("Inputs:")
            for inp in c1.inputs:
                if [trk for trk in TRACKING if c1.mapping[inp] == trk]:
                    print (inp,"=1")
                else:
                    print (inp,"=0")

            print("Outputs of Circuit1:")
            for oup in c1.outputs:
                if [trk for trk in TRACKING if c1.mapping[oup] == trk]:
                    print (oup,"=1")
                else:
                    print (oup,"=0")

            print("Outputs of Circuit2:")
            for oup in c2.outputs:
                if [trk for trk in TRACKING if c2.mapping[oup]+c1.nets == trk]:
                    print (oup,"=1")
                else:
                    print (oup,"=0")

        else:
            print("Equivalent!")

if __name__=='__main__':

    #Command to run the code > python final_code.py D:/abc.txt D:/def.txt
    circuit1=Circuit()
    circuit2=Circuit()
    #Pass filename for reaiondNetlist function
    # read netlists
    circuit1.readNetlist(open("xor2.net", "r"))
    circuit2.readNetlist(open("xor2_nand.net", "r"))

    circuit1_CNF = circuit1.read_CNF(1, circuit1)
    circuit2_CNF = circuit2.read_CNF(2, circuit2)

    #prints circuit1
    print(circuit1_CNF)
    #prints circuit2
    print(circuit2_CNF)


    davis_obj=DavisAlgorithm()
    result=davis_obj.check_equivalence(circuit1,circuit2,circuit1_CNF,circuit2_CNF)
    davis_obj.print_result(result,circuit1,circuit2)



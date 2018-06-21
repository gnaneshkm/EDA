
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


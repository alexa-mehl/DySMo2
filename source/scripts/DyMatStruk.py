
import DyMat, numpy
import matplotlib.pyplot as plt

class DyMatStruk(DyMat.DymolaMat):

    def plotVar(self, varName):
        d = self.data(varName)
        a, aname, tmp = self.abscissa(varName)
        plt.plot(a[:], d[:])

    def plotVars(self, varName1 ,varName2):
        d1 = self.data(varName1)
        d2 = self.data(varName2)
        plt.plot(d1[:], d2[:])

    def getVarArray(self, varNames):
        v = [numpy.array(self.data(n), ndmin=2) for n in varNames]
        a, aname, tmp = self.abscissa(varNames[0])
        v.insert(0, numpy.array(a, ndmin=2))
        return numpy.concatenate(v, 0)


    def getEndVal(self, varName):
        d = self.data(varName)
        return d[-1]

    def getEndValTime(self, varName):
        d = self.data(varName)
        a, aname, tmp = self.abscissa(varName)
        return a[-1], d[-1]


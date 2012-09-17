# -*- coding: utf-8 -*-
"""
  Copyright (C) 2012  Alexandra Mehlhase <a.mehlhase@tu-berlin.de>, All Rights Reserved
  
  This file is part of modelica3d 
  (https://mlcontrol.uebb.tu-berlin.de/redmine/projects/modelica3d-public).

  This program is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.
   
  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""


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


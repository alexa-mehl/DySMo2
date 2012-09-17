#!/usr/bin/env python

# Copyright (c) 2011, Joerg Raedler (Berlin, Germany)
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
# Redistributions of source code must retain the above copyright notice, this list
# of conditions and the following disclaimer. Redistributions in binary form must
# reproduce the above copyright notice, this list of conditions and the following
# disclaimer in the documentation and/or other materials provided with the
# distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
# ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import scipy.io

_trans = lambda a: [''.join(s).rstrip() for s in zip(*a)]


class DymolaMat:
    """Access result files from dymola"""
    
    def __init__(self, fileName):
        """open the file, parse contents"""
        self.fileName = fileName
        self.mat = scipy.io.loadmat(fileName)
        self._vars = {}
        self._blocks = []
        names = _trans(self.mat['name']) # names
        descr = _trans(self.mat['description']) # descriptions
        for i in range(len(names)):
            d = self.mat['dataInfo'][0][i] # data block
            x = self.mat['dataInfo'][1][i]
            c = abs(x) - 1  # column
            s = cmp(x, 0) # sign
            if c:
                self._vars[names[i]] = (descr[i], d, c, s)
                if not d in self._blocks:
                    self._blocks.append(d)
            else:
                self._absc = (names[i], descr[i])

    def blocks(self):
        """return numbers of data blocks"""
        return self._blocks

    def names(self, block=None):
        """return the names of all variables (or all of the block)"""
        if block is None:
            return self._vars.keys()
        else:
            return [k for (k, v) in self._vars.items() if v[1] == block]

    def description(self, varName):
        """return the description of a variable"""
        return self._vars[varName][0]

    def abscissa(self, blockOrName):
        """return the values, name and description of the abscissa
        that belongs to a variable or block"""
        try:
            b = int(blockOrName)
        except:
            b = self._vars[blockOrName][1]
        di = 'data_%d' % (b)
        return self.mat[di][0], self._absc[0], self._absc[1]

    def data(self, varName):
        """return the values of a variable"""
        tmp, d, c, s = self._vars[varName]
        di = 'data_%d' % (d)
        dd = self.mat[di][c]
        if s < 0:
            dd *= -1
        return dd

    def writeVar(self, varName):
        """write the values of a variable and its abscissa to stdout"""
        d = self.data(varName)
        a, aname, tmp = self.abscissa(varName)
        print '# %s | %s' % (aname, varName)
        for i in range(d.shape[0]):
            print '%f %g' % (a[i], d[i])


if __name__ == '__main__':
    import sys
    dm = DymolaMat(sys.argv[1])
    if len(sys.argv) < 3:
        for n in dm.names():
            print n
    else:
        dm.writeVar(sys.argv[2])

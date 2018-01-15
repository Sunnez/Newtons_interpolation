#!/usr/bin/env python3

import sys
import sympy as sym

def solutions(Px, outputFile):
    x = -1.0
    maxX = 1.0
    while x < maxX:
        y = Px.subs(sym.Symbol('x'), sym.Float(x))
        print(x," ",y,file=outputFile)
        x = x + 0.01

def output(Fx):
    outputFile = open("Fx",'w', encoding="utf-8")
    outputFile.seek(0)
    outputFile.truncate()
    solutions(Fx, outputFile)
    outputFile.close()

def main() :
    x = sym.Symbol('x')
    Fx = 1/(1+25*x*x)
    output(Fx)

if __name__ == "__main__":
    main()

#end of file 


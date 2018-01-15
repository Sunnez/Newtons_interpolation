#!/usr/bin/env python3
#
# Author: Timothy Baker
# Class: CS517 Fall 2017
# Professor: Dr. Weidong Li

import sys
import sympy as sym

# get the input from the user
#
#     x   an algebraic symbol 
#     n   the nth degree polynomial interpolation
#     y   the function that will be interpolated
#     Xi  a set, X={X1, X2, ... , Xn}, of equally spaced points
def determineVariables():
    args = sys.argv
    x = sym.Symbol('x')
    n = 0
    y = 1/(1+25*x*x) # default f(x)
    if len(args) == 2 :
        n = int(args[1])
    elif len(args) > 2 :
        n = int(args[1])
        y = args[2] # user can provide f(x)
    else :
        n = input("Enter n: ") # no command line input
        y = input("Enter fx(in terms of 'x'): ")
    Xi = getXi(n+1) # equally spaced points
    return x, n, y, Xi

# produces a set X={X1, X2,..., Xn} , where X is the 
# set of equally spaced points along a function.  These
# points are produced using a function y=f(x).  The 
# function y is then interpolated using newton's method
# and the equally spaced points.
#
#         Xi = 2i/n - 1
#
def getXi(n):
    Xi = []
    for i in range(0,n+1): 
        Xi.append(((2*i)/(n)) - 1)
    return Xi

# find F(Xi) for all values x in the set X
def solveY(y, t, Xi):
    Fxi = []
    for i in range(0, len(Xi)):
        Fxi.append(y.subs(t, Xi[i]).evalf())
    return Fxi

# divided squares, arguments are tuples in the
# form: Xi =(Fxi, Xi), Xj = (Fxj, Xj)
def divide_and_conquer(Xi, Xj):
    return (Xj[0] - Xi[0])/(Xj[1] - Xi[1])

# recursive function to apply the divided differences
def newtonsMethod(Xi,Fxi,n,coefficients,count):
    if n == 0:
        return coefficients
    else:
        count = count + 1
        coefficients.append(float(Fxi[0]))
        oldFxi = Fxi
        Fxi = []
        for i in range(0,n):
            Fxi.append(divide_and_conquer((oldFxi[i],Xi[i]),(oldFxi[i+1],Xi[i+count])))
        return newtonsMethod(Xi,Fxi,n-1,coefficients, count)

# returns (X-X0)(X-X1)(X-X2)...(X-Xn-1)
def getXs(XsLeft, Xi):
    Xs = ""
    for i in range(0,XsLeft):
        Xs = Xs + "*(x - " + str(Xi[i]) +") "        
    return Xs

# returns nth degree polynomial with a0, a1, ..., an
# coefficients
def getPx(coefficients, Xi):
    Px = ""
    for i in range(0,len(coefficients)):
        Px = Px + " + " + str(coefficients[i]) + " " + getXs(len(Xi) - (len(Xi)-i), Xi)
    return Px

# output the x and y coordinates for the interpolated
# function in two columns, x and f(x), respectively, 
# incrementing X by 1/100 at a time from [-1,1]
def output(Px, n):
    fileName = "n=%d" % n
    outputFile = open(fileName,'w+', encoding="utf-8")
    outputFile.seek(0)
    outputFile.truncate()
    x = -1.0
    maxX = 1.0
    while x < maxX:
        y = Px.subs(sym.Symbol('x'), sym.Float(x))
        print(x," ",y,file=outputFile)
        x = x + 0.01
    outputFile.close()

def main() :
    x, n, y, Xi = determineVariables()
    Fxi = solveY(y, x, Xi)
    coefficients = newtonsMethod(Xi,Fxi,n+1,[], 0)
    Px = getPx(coefficients, Xi)
    Px = sym.sympify(Px)
    Px = sym.simplify(Px)
    output(Px, n)

if __name__ == "__main__":
    main()

#end of file 


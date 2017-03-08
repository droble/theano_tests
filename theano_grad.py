# -*- coding: utf-8 -*-
"""
Created on Mon Mar 06 22:25:31 2017

@author: Admin
"""

import numpy as np
import theano
import theano.tensor as T
from theano import pp

def doScalarDerivative() : 
    x = T.dscalar( 'x' )
    y = x ** 2
    dy = T.grad( y, x )
    
    f = theano.function( [x], dy )
    
    print f(4)

    # end doScalarDerivative

def doSimpleLogistic() :
    X = T.dmatrix( 'X' )
    S = 1 / ( 1 + T.exp( -X ) )
    logistic = theano.function( [X], S )
    
    print logistic( [[0, 1], [-1, -2]] ) 

    # end doSimpleLogistic

def logisticRegression() :
    
    
    X = T.dmatrix( "X" ) 
    Y = T.dmatrix( "Y" )
    
    
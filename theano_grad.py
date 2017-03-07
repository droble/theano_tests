# -*- coding: utf-8 -*-
"""
Created on Mon Mar 06 22:25:31 2017

@author: Admin
"""

import numpy
import theano
import theano.tensor as T
from theano import pp

x = T.dscalar( 'x' )
y = x ** 2
dy = T.grad( y, x )

f = theano.function( [x], dy )

print f(4)


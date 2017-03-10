# -*- coding: utf-8 -*-
"""
Created on Mon Mar 06 22:25:31 2017

@author: Admin
"""

import numpy as np
import theano
import theano.tensor as T
from theano import pp

# Make some data for the regression. Hours studied vs whether the 
# student passed or failed. (From the Wikipedia Logistic Regression page.)

hours = np.array ( [[0.50,0.75,1.00,1.25,1.50,1.75,1.75,2.00,2.25,2.50,
                     2.75,3.00,3.25,3.50,4.00,4.25,4.50,4.75,5.00,5.50]] ).T
passfail = np.array ( [0,0,0,0,0,0,1,0,1,0,1,0,1,0,1,1,1,1,1,1] )

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

def logisticRegression ( input_values, target_class, training_steps = 10 ) :
    """Logisitic Regression using Theano
    
    input_values -- N x features matrix. Each row is a location in 
    feature-dimensional space. 
    
    target_class -- N element vector, classifying each location 
    as either 1 or 0. 
    """
    
    N     = input_values.shape[0]
    feats = input_values.shape[1]
    
    if target_class.shape[0] != N : 
        raise ValueError ( "Number of rows in input_values must match number "
        "of rows in target_class." )
        
    # Declare the symbolic variables. 
        
    x = T.dmatrix( "x" ) 
    y = T.dvector( "y" )
    
    # Initialize the weight vector and the bias. 
    
    w = theano.shared( np.random.randn( feats ), name="w" )
    b = theano.shared( 0., name="b" )
    
    print ( "Initial model: " )
    print ( w.get_value() )
    print ( b.get_value() )
    print ( "Input data" )
    print ( "input_values: ", input_values.shape )
    print ( input_values )
    print ( "target_class: ", target_class.shape )
    print ( target_class )
    
    # Construct the Theano expression graph. 
    
    t = T.dot( x, w ) + b
    p_1 = 1 / ( 1 + T.exp( -t ) )
    
    prediction = p_1 > 0.5 
    
    xent = -y * T.log( p_1 ) - ( 1 - y ) * T.log( 1 - p_1 )
    cost = xent.mean() + 0.01 * ( w ** 2 ).sum() 
    
    dw, db = T.grad ( cost, [w, b] )
    
    # Compile it. 
    
    train = theano.function( inputs = [x, y], 
                             outputs = [prediction, xent], 
                             updates = ( ( w, w - 0.1 * dw ), 
                                         ( b, b - 0.1 * db ) ) )
                                         
    predict = theano.function( inputs = [x], outputs = prediction )
    
    # Try an initial prediction. 
    
    print "Initial prediction: "
    print predict ( input_values )
    
    # Train it! 
    
    for i in xrange( training_steps ) : 
        pred, err = train ( input_values, target_class )
        
    print( "Final model:" )
    print( w.get_value() )
    print( b.get_value() )
    print( "target values for D:" )
    print( target_class )
    print( "prediction on D:" )
    print( predict( input_values ) )
                                
    
    
    

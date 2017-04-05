# -*- coding: utf-8 -*-
"""
Created on Tue Apr  4 17:43:44 2017

@author: doug
"""

import numpy as np 

def adjacencyMatrix( faces, numverts = None ) : 
    """Makes an adjaceny matrix from the faces of a polygonal structure."""

    if not numverts :     
        numverts = np.amax( faces ) - np.amin( faces ) + 1

    if not numverts : 
        raise ValueError( "adjacencyMatrix: no vertices in object" )
    
    adj = np.zeros( ( numverts, numverts ) )
    
    for f in obj.faces : 
        for i in range ( -1, 2 ) : 
            edge = np.sort( ( f[i], f[i+1] ) )
            adj[ edge[0], edge[1] ] = 1
            
    return adj
    
# end adjacencyMatrix
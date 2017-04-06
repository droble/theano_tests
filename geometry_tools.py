# -*- coding: utf-8 -*-
"""
Created on Tue Apr  4 17:43:44 2017

@author: doug
"""

import numpy as np 

def adjacencyMatrix( omesh ) : 
    """Makes an adjaceny matrix from the faces of a polygonal structure."""
    
    adj = np.zeros( ( omesh.n_vertices(), omesh.n_vertices() ) )
    
    for fh in omesh.faces() : 

        face = []

        for vh in omesh.fv( fh ) :
            face.append( vh.idx() )

        for i in range ( -1, len( face ) - 1 ) : 
            edge = np.sort( ( face[i], face[i+1] ) )
            adj[ edge[0], edge[1] ] = 1
            
    return adj + adj.T
    
# end adjacencyMatrix


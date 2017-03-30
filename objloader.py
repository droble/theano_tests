# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 14:53:13 2017

@author: doug
"""
import numpy as np

import plotly.offline as py
from plotly.tools import FigureFactory as FF

def MTL( filename ) :
    contents = {}
    mtl = None
    
    for line in open(filename, "r"):
        
        if line.startswith('#'): 
            continue
            
        values = line.split()
        
        if not values:
            continue
            
        if values[0] == 'newmtl':
            mtl = contents[values[1]] = {}
            
        elif mtl is None:
            raise ValueError, "mtl file doesn't start with newmtl stmt"
            
        elif values[0] == 'map_Kd':
            # load the texture referred to by this declaration
            mtl[values[0]] = values[1]

        else:
            mtl[values[0]] = map(float, values[1:])
    return contents

# end MTL

class OBJ:
    def __init__( self ):
        """Loads a Wavefront OBJ file. """
        
        # I want to make sure that all the members are numpy arrays. So 
        # there's this. 
        
        self.vertices       = np.array( [[]] )
        self.normals        = np.array( [[]] ) 
        self.texcoords      = np.array( [[]] ) 
        self.faces          = np.array( [[]] ) 
        self.face_normals   = np.array( [[]] )
        self.face_texcoords = np.array( [[]] )
        self.face_materials = []
    
    def read( self, filename, swapyz=False ) : 
        """Loads a Wavefront .obj file.""" 
        
        material = None
        my_vertices       = []
        my_normals        = [] 
        my_texcoords      = [] 
        my_faces          = [] 
        my_face_normals   = []
        my_face_texcoords = []
        
        for line in open(filename, "r"):
            
            if line.startswith('#'): 
                continue
                
            values = line.split()
            
            if not values: 
                continue
                
            if values[0] == 'v':
                v = map(float, values[1:4])
                if swapyz:
                    v = v[0], v[2], v[1]
                my_vertices.append(v)
                
            elif values[0] == 'vn':
                v = map(float, values[1:4])
                if swapyz:
                    v = v[0], v[2], v[1]
                my_normals.append(v)
                
            elif values[0] == 'vt':
                my_texcoords.append(map(float, values[1:3]))
                
            elif values[0] in ('usemtl', 'usemat'):
                material = values[1]
                
            elif values[0] == 'mtllib':
                my_mtl = MTL(values[1])
                
            elif values[0] == 'f' or values[0] == 'fo' :
                face = []
                texcoords = []
                norms = []
                
                for v in values[1:4]:
                    
                    w = v.split('/')
                    
                    face.append( int(w[0]) -1 )
                    
                    if len(w) >= 2 and len(w[1]) > 0:
                        texcoords.append(int(w[1]))
                    else:
                        texcoords.append(0)
                        
                    if len(w) >= 3 and len(w[2]) > 0:
                        norms.append(int(w[2]))
                    else:
                        norms.append(0)
                    
                if len(face) == 3 : 
                    my_faces.append( face )
                    my_face_normals.append( norms )
                    my_face_texcoords.append( texcoords )
                    self.face_materials.append( material )
                        
                # Deal with quads. 
                        
                face = []
                texcoords = []
                norms = []       
                
                if ( len(values[1:]) == 4 ):
                    for v in ( values[3], values[4], values[1] ) :
                        
                        w = v.split('/')
                        
                        face.append( int(w[0]) -1 )
                        
                        if len(w) >= 2 and len(w[1]) > 0:
                            texcoords.append(int(w[1]))
                        else:
                            texcoords.append(0)
                            
                        if len(w) >= 3 and len(w[2]) > 0:
                            norms.append(int(w[2]))
                        else:
                            norms.append(0)    
                
                if len( face ) == 3 : 
                    my_faces.append( face )
                    my_face_normals.append( norms )
                    my_face_texcoords.append( texcoords )
                    self.face_materials.append( material )

        
        self.vertices       = np.asarray( my_vertices )
        self.normals        = np.asarray( my_normals )
        self.texcoords      = np.asarray( my_texcoords )
        self.faces          = np.asarray( my_faces, dtype=int )
        self.face_normals   = np.asarray( my_face_normals, dtype=int )
        self.face_texcoords = np.asarray( my_face_texcoords, dtype=int )

    # end read

# end class OBJ                

def plotOBJ ( obj, cmap = 'YlOrRd', title="3D Object" ) : 
    """Use plotly to plot a Wavefront obj file on your web browser.""" 

    fig = FF.create_trisurf( x = obj.vertices[:,0], 
                             y = obj.vertices[:,1],
                             z = obj.vertices[:,2], 
                             simplices = obj.faces, 
                             colormap = cmap, 
                             title = title )
    py.plot( fig )

# end plotOBJ

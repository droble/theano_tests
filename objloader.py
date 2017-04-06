# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 14:53:13 2017

@author: doug
"""
import numpy as np

import plotly
import plotly.offline as pyoff
import plotly.figure_factory as plff


def readMTL( filename ) :
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

# end readMTL

class objMesh :
    def __init__( self ):
        """A simple mesh representation that mimics (and can read)
        Wavefront .obj files."""
        
        # I want to make sure that all the members are numpy arrays. So 
        # there's this. 
        
        self.vertices       = np.array( [[]] )
        self.normals        = np.array( [[]] ) 
        self.texcoords      = np.array( [[]] ) 
        self.faces          = np.array( [[]] ) 
        self.face_normals   = np.array( [[]] )
        self.face_texcoords = np.array( [[]] )
        self.face_materials = []

    # end __init__

    def clear( self ) :
        """Clears out the object's data."""
        
        self.vertices       = np.array( [[]] )
        self.normals        = np.array( [[]] ) 
        self.texcoords      = np.array( [[]] ) 
        self.faces          = []
        self.face_normals   = np.array( [[]] )
        self.face_texcoords = np.array( [[]] )
        self.face_materials = []

    # end clear
    
    def read( self, filename, swapyz=False ) : 
        """Loads a Wavefront .obj file.""" 
        
        clear( self )
        
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
                my_mtl = readMTL(values[1])
                
            elif values[0] == 'f' or values[0] == 'fo' :
                
                # At this point, I insist that all geometry be triangulized. 
                # So, read in the faces and triangulate them. This assumes all 
                # faces are convex. This will fail SO HARD with concave faces.
                # First, get rid of the "f". 
                
                values = values[1:]

                # Loop until we don't have any triangles in the face. (Faces 
                # with less than three vertices will be ignored.)

                while len( values ) > 2 : 
                    
                    # Process the triangle at the front of the list. 

                    face = []
                    texcoords = []
                    norms = []
                    
                    for v in values[0:3] : 
                    
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
                    
                    # Put the new face information in the master lists. 

                    my_faces.append( face )
                    my_face_normals.append( norms )
                    my_face_texcoords.append( texcoords )
                    self.face_materials.append( material )

                    # Now, remove the center vertex in the triangle,
                    # we will never use it again. And rotate the list. 

                    values.pop( 1 )
                    values = values[1:] + values[:1]

                # end while

            # end elif
        
        self.vertices       = np.asarray( my_vertices )
        self.normals        = np.asarray( my_normals )
        self.texcoords      = np.asarray( my_texcoords )
        self.faces          = my_faces
        self.face_normals   = np.asarray( my_face_normals, dtype=int )
        self.face_texcoords = np.asarray( my_face_texcoords, dtype=int )

    # end read

    def openmesh ( self, om ) :
        """Converts an Open Mesh representation into an simpler,
        easier to plot using plotly representation based on the
        Wavefront .obj file. """

        self.clear()
        
        # Deal with the vertex locations. 

        self.vertices = np.zeros( ( om.n_vertices(), 3 ) )

        for vh in om.vertices() :
            self.vertices[ vh.idx() ] = \
                np.array ( [ om.point( vh )[0], 
                             om.point( vh )[1], 
                             om.point( vh )[2] ] )

        # Now, the faces.

        face_list = []
        
        for fh in om.faces() :

            face = []
            
            for vh in mesh.fv( fh ) :
                face.append( vh.idx() )

            face_list.append( face )

        self.faces = face_list

    # end openmesh
    
# end class objMesh                

def plotObjMesh ( obj, cmap = 'YlOrRd', title="3D Object" ) : 
    """Use plotly to plot a Wavefront obj file on your web browser.""" 

    # Plotly uses a square aspect ratio no matter what. This can
    # distort the heck out of the data. Figure out the appropriate
    # aspect ratio.

    vmax = np.max( obj.vertices, axis = 0 )
    vmin = np.min( obj.vertices, axis = 0 )
    
    extent = vmax - vmin
    minaxis = np.min( extent )

    if minaxis > 0 :
        extent = extent / minaxis
    else :
        extent = np.asarray( [ 1, 1, 1 ] )

    fig = plff.create_trisurf \
          ( x = obj.vertices[:,0], 
            y = obj.vertices[:,1],
            z = obj.vertices[:,2], 
            simplices = obj.faces, 
            colormap = cmap, 
            title = title,
            aspectratio = { 'x' : extent[0],
                            'y' : extent[1],
                            'z' : extent[2] } )

    pyoff.plot( fig )

# end plotObjMesh



import numpy as np
# Golden Ration, let's call it PHI
PHI = (1 + np.sqrt(5) ) / 2
IHP = 1/PHI

def is_platonic_number(num):
    if num in list(PLATONIC_SOLIDS.keys()):
        return True
    else: 
        return False

class PlatonicSolid:
    @classmethod
    def calc_coordinates(cls, circumradius):
        normalized_coords = cls.coordinates / np.linalg.norm(cls.coordinates, axis=1)[..., None]
        return normalized_coords * circumradius
    
class Tetrahedron(PlatonicSolid):
    coordinates = np.array([
        [ 1,  1,  1],
        [ 1, -1, -1],
        [-1,  1, -1],
        [-1, -1,  1], ])
    
class Octahedron(PlatonicSolid):
    coordinates = np.array([
        [ 1,  0,  0],
        [ 0,  1,  0],
        [-1,  0,  0],
        [ 0,  0,  1],
        [ 0, -1,  0],
        [ 0,  0, -1],  ])
    
class Cube(PlatonicSolid):
    coordinates = np.array([
        [  1,  1,  1],
        [  1,  1, -1],
        [  1, -1, -1],
        [  1, -1,  1],
        [ -1, -1,  1],
        [ -1, -1, -1],
        [ -1,  1, -1],
        [ -1,  1,  1], ])

class Icosahedron(PlatonicSolid):
    coordinates = np.array([
        [     0,    1,  PHI],
        [     0,    1, -PHI],
        [     0,   -1,  PHI],
        [     0,   -1, -PHI],
        [     1,   PHI,   0],
        [     1,  -PHI,   0],
        [    -1,   PHI,   0],
        [    -1,  -PHI,   0],
        [    PHI,    0,   1],
        [    PHI,    0,  -1],
        [   -PHI,    0,   1],
        [   -PHI,    0,  -1],  ])
    
class Dodecahedron(PlatonicSolid):
    coordinates = np.array([
        [     1,    1,    1],
        [     1,    1,   -1],
        [     1,   -1,    1],
        [     1,   -1,   -1],        
        [    -1,    1,    1],
        [    -1,    1,   -1],
        [    -1,   -1,    1],
        [    -1,   -1,   -1],
        [     0,   IHP,  PHI],
        [     0,   IHP, -PHI],
        [     0,  -IHP,  PHI],
        [     0,  -IHP, -PHI],        
        [   IHP,   PHI,    0],
        [   IHP,  -PHI,    0],
        [  -IHP,   PHI,    0],
        [  -IHP,  -PHI,    0],        
        [   PHI,     0,  IHP],
        [   PHI,     0, -IHP],
        [  -PHI,     0,  IHP],
        [  -PHI,     0, -IHP], ])
    

PLATONIC_SOLIDS = {
    4: Tetrahedron,
    6: Octahedron,
    8: Cube,
    12: Icosahedron,
    20: Dodecahedron,  
}
import numpy as np
from helper.UniformSphericalSampling import sample_sphere_uniformly_geometric as ssug
from helper.Quaternions import QuatProc
from helper.platonic_solids import PLATONIC_SOLIDS, is_platonic_number
#import matplotlib.pyplot as plt
#from mpl_toolkits.mplot3d import Axes3D

def ULA(imd, num_mics):
    '''
    :param imd: inter-microphone distances
    :param num_mics: number of microphones
    :return: offset vectors for the ULA to the array center (real numbers)
    '''
    mics_pos = np.arange(num_mics)*imd
    center = mics_pos[-1]/2
    mics_pos = mics_pos - center
    return np.array([mics_pos,[0]*num_mics,[0]*num_mics]).T

def sample_circle(num):
    '''
    :param num: number of circle points to be sampled
    :return: complex samples (2D) for the microphone positions
    '''
    samples = np.array(np.exp(1j*np.pi*2*np.arange(num)/num))
    return samples

def CUA(rad, num_mics):
    '''
    :param rad: radius of the circular uniform array
    :param num_mics: number of microphones
    :return:  offset vectors for the CUA (real numbers)
    '''
    mics_pos = rad*sample_circle(num_mics)
    mics_pos = np.array([np.real(mics_pos),np.imag(mics_pos),[0]*num_mics])
    return mics_pos.T

def SUA(rad,num_mics):
    """
    Function that samples a Sphere uniformly with num_mics microphones
    :param rad: radius of the sphere
    :param num_mics: number of microphones on the sphere
    :return: positions of the microphones on the sphere
    """
    if is_platonic_number(num_mics):
            return PLATONIC_SOLIDS[num_mics].calc_coordinates(rad)
    azimuth, elevation = ssug(num_mics)
    proc = QuatProc()
    rotaxy = np.array([0,1,0])
    rotaxz = np.array([0,0,1])
    start_point = np.array([1,0,0])
    mics = []
    for idx, az in enumerate(azimuth):
        #turn vector over y axis for the proper elevation
        mic = proc.rotate(elevation[idx], rotaxy, start_point)
        # get azimuth around z axis
        mic = proc.rotate(azimuth[idx],rotaxz,mic)
        mics.append(mic)
    return rad*np.array(mics)

'''
points = SUA(2,200)

np.max(points[:,0])
points
from mpl_toolkits import mplot3d

%matplotlib inline
import numpy as np
import matplotlib.pyplot as plt



ax = plt.axes(projection='3d')

# Data for three-dimensional scattered points
xdata = points[:,0]
ydata = points[:,1]
zdata = points[:,2]
points.shape
ax.scatter3D(xdata, ydata, zdata, cmap='Greens');

plt.plot(np.sort(np.around(np.sqrt((np.sum((points[None,...]-points[:,None,...])**2,axis=-1))),3).reshape(-1)))


points.shape

np.around(np.sum(points,axis=0),4)




print(np.around(points,3)
'''

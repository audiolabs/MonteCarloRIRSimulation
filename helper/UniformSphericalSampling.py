import numpy as np
def sample_sphere_uniformly_geometric(N):
    """
    Sample a sphere uniformly
    This function creates azimuth and elevation angles such that they uniformly sample a sphere surface with N points
    Implementation according to
    << Comments on Generating sensor signals in isotropic noise fields >>
    E. A. P. Habets and S. Gannot (2010)
    
    :param N: Number of points on the sphere
    :type N: int

    :return: azimuth angle between - pi and pi and elevation angle between -pi/2 and pi/2
    :rtype: float tuple
    """
    k = np.arange(1,N+1)
    h = -1+2*(k-1)/(N-1)
    elevation = np.arccos(h)
    azimuth = np.cumsum((np.asarray([0]+list(3.6/np.sqrt(N*(1-h**2))[1:-1]) +[0]) )%(2*np.pi))%(2*np.pi)
    azimuth[-1]=0
    return (azimuth-np.pi,elevation-np.pi/2)

def sample_halfsphere_uniformly_geometric(N):
    """
    Sample a halfsphere uniformly
    This function creates azimuth and elevation angles such that they uniformly sample a sphere surface with N points
    Implementation according to
    << Comments on Generating sensor signals in isotropic noise fields >>
    E. A. P. Habets and S. Gannot (2010)
    
    :param N: approx. Number of points on the sphere
    :type N: int

    :return: azimuth angle between - pi and pi and elevation angle between -pi/2 and pi/2
    :rtype: float tuple
    """
    az, el = sample_sphere_uniformly_geometric(2*N)
    azimuth = az[el>=0]
    elevation = el[el>=0]
    return (azimuth, elevation)


def sample_sphere_uniformly_stochastic():
    """
    Sample a sphere uniformly
    This function creates azimuth and elevation angles such that they uniformly sample a sphere surface

    :return: azimuth angle between - pi and pi and elevation angle between -pi/2 and pi/2
    :rtype: float tuple
    """
    # it is very important to have normally distributed sampling ... uniform sampling would be wrong!!!!
    rv = np.random.randn(3)
    rv = rv/np.linalg.norm(rv)
    rv_xy = rv*np.array([1,1,0])
    rv_xy = rv_xy/np.linalg.norm(rv_xy)
    elevation = np.arcsin(np.linalg.norm(np.cross(rv_xy,rv)))*np.sign(rv[-1])
    azimuth = np.arccos(np.dot(np.array([1,0,0]),rv_xy))*np.sign(rv[-2])
    return (azimuth,elevation)

def sample_halfsphere_uniformly_stochastic():
    azimuth, elevation = sample_sphere_uniformly_stochastic()
    return azimuth, np.abs(elevation)

def sample_sphere_uniformly2_stochastic():
    """
    Sample a sphere uniformly
    This function creates azimuth and elevation angles such that they uniformly sample a sphere surface

    :return: azimuth angle between - pi and pi and elevation angle between -pi/2 and pi/2
    :rtype: float tuple
    """
    theta = np.random.rand()*2*np.pi
    u = np.random.rand()*2 - 1

    x = np.sqrt(1-u**2)*np.cos(theta)
    y = np.sqrt(1-u**2)*np.sin(theta)
    z = u

    rv = np.array([x,y,z])
    rv = rv/np.linalg.norm(rv)
    rv_xy = rv*np.array([1,1,0])
    rv_xy = rv_xy/np.linalg.norm(rv_xy)

    elevation = np.arcsin(np.linalg.norm(np.cross(rv_xy,rv)))*np.sign(rv[-1])
    azimuth = np.arccos(np.dot(np.array([1,0,0]),rv_xy))*np.sign(rv[-2])
    return (azimuth,elevation)
'''
For Visualization
az = []
el = []
for a in range(10000):
    azimuth, elevation = sample_sphere_uniformly_stochastic()
    az.append(azimuth)
    el.append(elevation)
az2 = []
el2 = []
for a in range(10000):
    azimuth2, elevation2 = sample_sphere_uniformly2_stochastic()
    az2.append(azimuth2)
    el2.append(elevation2)
az3, el3 = sample_sphere_uniformly_geometric(10000)

az.sort()
el.sort()
az2.sort()
el2.sort()
az3.sort()
el3.sort()

plt.plot(az)
plt.plot(az2)
plt.plot(az3)
plt.title('Azimuth')
plt.figure()
plt.title('Elevation')
plt.plot(el)
plt.plot(el2)
plt.plot(el3)
'''

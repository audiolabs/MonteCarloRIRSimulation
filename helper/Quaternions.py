import numpy as np
class Quaternion():
    '''
    This it the quaternion class, where x, y z are the 2. 3. and 4. quaternion dimension and the first dimension is zero (If a point is to be translated to an quaternion). If the quaternion is used for rotation it is ([cos(angle/2), sin(angle/2)*x, sin(angle/2)*y, sin(angle/2)*z]) where angle is the angle to rotate around vector x y z
    '''
    def __init__(self,w,x,y,z):
        self.vec = np.array([w, x, y,z])

class QuatProc():
    '''
    This class processes quaternions
    '''
    def __init__(self):
        self._ONE_MAT = np.array([[[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]],[[0,-1,0,0],[1,0,0,0],[0,0,0,-1],[0,0,1,0]],[[0,0,-1,0],[0,0,0,1],[1,0,0,0],[0,-1,0,0]],[[0,0,0,-1],[0,0,-1,0],[0,1,0,0],[1,0,0,0]]])

    def multiply(self,qut1, qut2):
        """
        Function that multiplies two quarternions
        Multiplies two input quarternions by getting a multiplication matrix from the second one.

        :param qut1: First Quarternion
        :type qut1: Quaternion
        :param qut2: Second Quarternion
        :type qut2: Quaternion

        :return: Third Quarternion which contains the result of the multiplication
        :rtype: Quaternion
        """
        qut3 = Quaternion(0,0,0,0)
        qut3.vec = np.squeeze(np.squeeze(qut1.vec[None,:])@self._get_mul_matrix(qut2))
        return qut3

    def conjug(self,qut1):
        """
        Function that conjugates a Quarternion

        :param qut1: First Quarternion
        :type qut1: Quaternion
        :return: Second Quarternion which contains the result of the conjugation
        :rtype: Quaternion
        """

        qut2 = Quaternion(0,0,0,0)
        qut2.vec = qut1.vec*np.array([1,-1,-1,-1])
        return qut2

    def rotate(self, angle, rotation_axis, point):
        """
        Function that rotates a point around an axis using quarternions
        Rotation of point around axis by translating the point and
        the axis in quarternion coordinates and multiplying those accordingly

        :param angle: Angle between 0 and 2 pi to rotate the point
        :type angle: float
        :param rotation_axis: (np.array([a,b,c])) 3-dim axis to rotate around
        :param qut1: First Quarternion
        :param point: (np.array([a,b,c])) Point to rotate around rotation axis
        :return: rp (np.array([a,b,c])): rotated point
        """

        point_qut = Quaternion(0,*np.squeeze(point))
        rot_qut = self._rotax_to_quat(rotation_axis, angle)
        # rotate
        res_qut = self.multiply(rot_qut,self.multiply(point_qut,self.conjug(rot_qut)))
        return res_qut.vec[1:]

    def _get_mul_matrix(self, qut):
        """
        translate quarternion in rotation matrix
        The rotation matrix defines the ways how quarternions rotate

        :param qut: Quarternion to extract vector for the rotation matrix
        :rtype qut: Quaternion
        :return: rm (np.array 4x4: multiplication matrix
        """
        return np.squeeze(self._ONE_MAT[...,None,:]@np.squeeze(qut.vec)[None,None,:,None])

    def _rotax_to_quat(self,rot_ax,angle):
        """
        Translates a rotation axis and an angle to a quarternion

        :param angle: Angle between 0 and 2 pi
        :type angle: float
        :param rot_ax: (3x1 vector) Vector to rotate around
        :type rot_ax: float vector
        :param rot_quat: Quarternion with rotation information
        :type rot_quat: Quaternion
        """
        if np.sum(rot_ax**2) ==0:
            print('no rotation axis given ... Error')
            return
        rot_ax = rot_ax/np.linalg.norm(rot_ax)
        rot_quat = Quaternion(np.cos(angle/2),*(np.sin(angle/2)*rot_ax))
        return rot_quat

    def random_rotation(self):
        """
        returns a random rotation vector Be aware that just uniformly creating a random vector is wrong, it has to be sampled from a normal distribution

        :return rv: vector pointing in a random direction
        :rtype: float array
        """
        rv = np.random.randn(3)
        rv = rv/np.linalg.norm(rv)
        return rv

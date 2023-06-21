
import rir_generator as pyrir
import pickle
import sys
import numpy as np
from helper import ArrayStructures
from helper.UniformSphericalSampling import sample_sphere_uniformly_geometric as ssug
from helper.UniformSphericalSampling import sample_halfsphere_uniformly_geometric as shug
from helper.Quaternions import QuatProc
from config.config import c, rate, wdist

proc = QuatProc()

def sample_room(room,wdist=wdist):
    """Function that samples a square room uniformly. The sample has to be within a certain distance to the wall

    :param room: (array) x,y,z room dimensions
    :param wdist: (float) minimal distance to walls of the sampling point

    :return: (array) x,y,z sampled room position
    :rtype: float array
    """
    sample_area = room - 2*wdist
    if (sample_area<0).any():
        print('room too small to sample!')
        return
    pos = np.random.rand(3)*sample_area + wdist
    return pos

def write(data, outfile):
    """Function that writes a pickles file

    :param data: data to write in the pickle file
    :param outfile: (str) str to save the file
    """
    f = open(outfile, "w+b")
    pickle.dump(data, f)
    f.close()

def verify_positions(room, a,b,wdist = wdist):
    """Function that raises an internal error if array or microphone is out of the room or too close to the wall

    :param room: room dimension
    :param a:
    :param b:
    :param wdist: critical distance to walls when to raise error
    """
    if (a>room-wdist).any() or (b>room-wdist).any():
        return False
    if (a<wdist).any() or (b<wdist).any():
        return False
    return True

def verify_DOA(mics, sourcevecoff, doa):
    """Function that raises an internal error if array or microphone is out of the room or too close to the wall

    :param mics: positions of the microphones
    :param sourcevecoff: vector from array center to the source
    :param doa: angle of arrival in rad
    """
    sourcevecoff = sourcevecoff/ np.linalg.norm(sourcevecoff)
    ar_vec = mics[-1]-mics[0]
    ar_vec = ar_vec/np.linalg.norm(ar_vec)
    angle = np.arccos(round(np.dot(ar_vec,sourcevecoff),4))
    if np.abs(angle-doa)>1e-2:
        print('DOA Error')
        return False

    return True



def generate_source_vec(sad,Az, El):
    """Function that generates a source vector with given length and given Azimuth and Elevation w.r.t. array center The rotation is performed using quaternions

    :param sad: Distance between source and arraycenter
    :type sad: float
    :param Az: Azimuth angle in rad
    :type Az: float
    :param El: Elevation angle in rad
    :type El: float
    :return: Vector which points from array center to source
    :rtype: float array
    """
    rotaxy = np.array([0,-1,0])
    rotaxz = np.array([0,0,1])
    start_point = np.array([1,0,0])
    source = proc.rotate(El, rotaxy, start_point)
    # get azimuth around z axis
    source = proc.rotate(Az,rotaxz,source)
    return source*sad

def generate_rir(Azimuth, Elevation, source_array_dist, Room, ReverberationTime, dist,num_mics,array_type):
    """Function that generates 'M' room impulse responses for a given 'DOA'. Array and source are randomly positionend and rotated in a room using quaternions.

    :param Azimuth: (float) Azimuth angle of the source to the array center in rad
    :param Elevation: (float) Elevation angle of the source to the array center in rad
    :param source_array_dist: (float) distance of source signal to array center
    :param Room: (array) x, y, z dimension of room
    :param ReverberationTime: (float) Reverberation time of the current room
    :param dist: (float) intermicrophone distance for ULA or radius for CUA
    :param num\_mics: (int) number of microphones
    :param array\_type: (str) one of ULA, CUA, SUA

    :return: Tuple of a unit-norm vector pointing from array to source and an array of room impulse responses
    :rtype: Tuple
    """
    # compute mic poses in room
    count = 0

    offsets = getattr(ArrayStructures,array_type)(dist,num_mics)    # compute source pos in room
    source_vec_off = generate_source_vec(source_array_dist, Azimuth, Elevation)[None,...]
    RIRs = []
    dirRIRs = []

    # get a random rotation vector

    # compute room positions
    i = 0
    while 1:
        i = i + 1

        print(i)
        Mic_center = sample_room(Room)

        # get random rotation using quaternions
        rv = proc.random_rotation()
        # uniform distributed sampling, no gauss :) as cylinder around axi
        rangle = np.random.rand()*2*np.pi


        # rotate everything randomly in the room
        cursource_vec_off = proc.rotate(rangle, rv, source_vec_off)

        curoffsets = offsets.copy()
        for a in range(offsets.shape[0]):
            curoffsets[a,:] = proc.rotate(rangle, rv, offsets[a,:])

        Mics = Mic_center + curoffsets
        source_vec = cursource_vec_off + Mic_center
        #print('Estimate{:.2f}'.format(np.arccos(round(np.sum(cursource_vec_off*(Mic_center-Mics[0])/np.linalg.norm(Mic_center-Mics[0])),4))/np.pi*180))
        #print('Azimuth{:.2f}'.format(Azimuth/np.pi*180))
        if not verify_positions(Room, Mics, source_vec):
            continue
   
        #if not verify_DOA(Mics, cursource_vec_off, Azimuth):
           # print('aaaa')
            #import ipdb; ipdb.set_trace()
            #exit()

        print(Mics, source_vec, Room)
        for cnt in range(num_mics):
            RIRs.append(pyrir.generate(c, rate, Mics[cnt,...], source_vec, Room, reverberation_time=ReverberationTime,nsample=int(ReverberationTime*rate), order=-1))
            dirRIRs.append(pyrir.generate(c, rate, Mics[cnt,...], source_vec, Room, reverberation_time=ReverberationTime,nsample=int(ReverberationTime*rate), order=0))
        break
    return (np.squeeze(source_vec_off/np.linalg.norm(source_vec_off)),np.concatenate(RIRs,axis=-1),np.concatenate(dirRIRs,axis=-1))


def main():
    """This function gets input parameter from RIR_parameter.py and computes RIRs from them

    :param roomx: x position of room
    :type roomx: str
    :param roomy: y position of room
    :type roomy: str
    :param roomz: z position of room
    :type roomz: str
    :param j: source array distance
    :type j: str
    :param ReverberationTime: T60 of the room
    :type ReverberationTime: str
    :param dist: inter-microphone distance (ULA) or radius (CUA, ..)
    :type dist: str
    :param path: path so save
    :type path: str
    :param array_type: selects the type of array
    :type array_type: str
    :param num_mics: Number of microphones
    :type num_mics: str
    :param indx: How often to go through these parameters based on parameter file ... just used to change the saving name
    :type indx: str
    """
    print(sys.argv)
    _, roomx,roomy,roomz, j, ReverberationTime , dist, path, array_type, num_mics,indx, DOA_count= sys.argv
    indx = int(indx)
    num_mics = int(num_mics)
    DOA_count = int(DOA_count)
    data_path = str(path)
    dist = float(dist)
    Room = np.array([float(roomx),float(roomy),float(roomz)])
    j =  float(j)
    ReverberationTime = float(ReverberationTime)
    source_array_dist = float(j)
    RIRs = []
    dirRIRs = []
    Vecs = []
    if array_type =='ULA':
        delta_angle = 180/(DOA_count-1) 
        Azimuths = (np.arange(0,180+ delta_angle,delta_angle)) / 180 * np.pi
        Elevations = [0]
        for caz, azimuth in enumerate(Azimuths):
            vec, rir,dirrir = generate_rir(azimuth,0, source_array_dist, Room, ReverberationTime, dist, num_mics, array_type)
            RIRs.append(rir)
            dirRIRs.append(dirrir)
            Vecs.append(vec)
    elif array_type=='CUA':
        Azimuths,Elevations = shug(DOA_count)
        for caz, azimuth in enumerate(Azimuths):
            vec, rir, dirrir = generate_rir(azimuth, Elevations[caz], source_array_dist, Room, ReverberationTime, dist, num_mics, array_type)
            RIRs.append(rir)
            dirRIRs.append(dirrir)
            Vecs.append(vec)
    elif array_type=='SUA':
        Azimuths,Elevations = ssug(DOA_count)
        for caz, azimuth in enumerate(Azimuths):
            vec, rir,dirrir = generate_rir(azimuth, Elevations[caz], source_array_dist, Room, ReverberationTime, dist, num_mics, array_type)
            RIRs.append(rir)
            dirRIRs.append(dirrir)
            Vecs.append(vec)
        
    else:
        print('array type not known')
        exit()
    filename = data_path + "/Room{}{}{}Rev{}Array{}SMD{}ind{}sadist{}.pickle".format(roomx,roomy,roomz,ReverberationTime,array_type,dist,indx,str(j))
    Dict = {'RIR': np.asarray(RIRs), 'Dist': dist,'Vecs': Vecs,'DirectRIR':np.asarray(dirRIRs)}
    write(Dict, filename)
if __name__ == '__main__':
    main()

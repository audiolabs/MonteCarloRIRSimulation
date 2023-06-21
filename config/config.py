
# insert a list of source array-center distances in meters [1.2, 2.3,...]
source_array_dist = [1.2, 2.3]
# insert a list of reverberation times
revs = [0.2, 0.8] 
# specify the array architecture from spherical uniform array (SUA) circular uniform array (CUA) or uniform linear array (ULA)
array_type = 'SUA' 
# specify the number of microphones in the array 
num_mics = 4  
# specify the inter-microphone distance of neighboring microphones (ULA) or the distance of each microphone to the center (CUA, SUA)
dmic = 0.08 
# specify the path to save the room impulse responses 
data_path = 'output'
 # specify the rooms used for the indivual sets in the form of [[room1x, room1y, room1z],[room2....],[...]...]
rooms = [[5,7,3], [9,4,3]]
# specify the condisered array-center source distances 
dists = [1.3,1.7]
# specify the considered reverberation times in seconds
reverberationtimes = [0.38,0.7]
# specify how often all these parameters are combined with each other
reps = 1
# speed of sound
c = 343
# sampling frequency
rate = 16000
# minimal distance of source and microphones to walls
wdist = 1.
# Number of source positions for each configuration (divides the direciton-of-arrival (DOA) space)
doa_count  = 37
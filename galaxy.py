from numpy import array, zeros, random, sqrt, exp, pi, sin, cos
import scipy.integrate as integrate
from scipy.optimize import fsolve
import matplotlib.pyplot as plt
import sys

def func(x,Distribution,Point): 
    """------------------------------------------------------------------------
    func: 
    Equation that follows the point of the wanted distribution that matches the 
    random one of a uniform distribution
    ---------------------------------------------------------------------------
    Arguments:
       x            : Random variable in the wanted distribution (unkonwn)
       Distribution : Wanted distribution
       Point        : Random variable in the uniform distribution
    ------------------------------------------------------------------------"""
    return integrate.quad(Distribution,0,x)[0]-Point

def spiral_galaxy(N, max_mass, BHM, center, ini_radius, beta, alpha):
    '''-----------------------------------------------------------------------
    spiral_galaxy:
    Use a radial distrubution of masses proportional to the brightness surface
    distributation to create a plain Bulb and Disk resembling an spiral galaxy
    --------------------------------------------------------------------------
    Arguments:
       N            : Number of particles
       max_mass     : Biggest mass of the stars in the system 
       BHM          : Black Hole's mass
       center       : Black Hole position
       ini_radius   : Galaxy radius
    ------------------------------------------------------------------------'''
    # Generates N random particles 
    positions = zeros(3*N)
    momenta = zeros(3*N)
    # Random masses varies between 1 solar mass and max_mass solar masses
    masses = random.random(N)*(max_mass-1.) + 1.
    #Parameters of the model of density of starts
    initial_density=.1
    const_bulb=.3
    const_disc=.8
    bulb_radius=0.2
    #Model of density normalized
    f1 = lambda x: initial_density*exp(-x**(1/4)/const_bulb)        #Bulb
    f2 = lambda x: f1(bulb_radius)*exp(-(x-bulb_radius)/const_disc) #Disc
    f = lambda x:  f1(x) if x<bulb_radius else f2(x)                #Piecewise 
    norm = integrate.quad(f,0,1)[0]                                  
    uf=lambda x: f(x)/norm                                          #Density function with integral=1
    #Random angle generation
    gamma=random.random(N)*2*pi
    #Uniform distribution to get random points
    random.seed(413)
    Uniform=random.random(N)
    #Empty array for the points mapped from the uniform distribution
    Map=zeros(N)   
    for i in range(N):
        #Calls the function that maps the ramdom points to the wanted distribution for the radius 
        Map[i]=fsolve(func,0,args=(uf,Uniform[i]))*ini_radius
        #Change to cartesian coordinates
        positions[3*i+0] = Map[i]*(cos(gamma[i])*cos(alpha)+
                                  sin(gamma[i])*cos(beta)*sin(alpha)) + center[0]
        positions[3*i+1] = Map[i]*(sin(gamma[i])*cos(beta)*cos(alpha)-
                                  cos(gamma[i])*sin(alpha))+ center[1]
        positions[3*i+2] = Map[i]*sin(gamma[i])*sin(beta) + center[2]
        # Keplerina velocity to define the momentum in the plain of the disc 
        Kep_v = sqrt(G*BHM/Map[i])
        vec_mom=array([-Map[i]*(sin(gamma[i])*cos(alpha)-cos(gamma[i])*cos(beta)*sin(alpha)),
                       Map[i]*(cos(gamma[i])*cos(beta)*cos(alpha)+sin(gamma[i])*sin(alpha)), 
                       Map[i]*cos(gamma[i])*sin(beta)])/Map[i]
        momenta[3*i+0] = masses[i]*Kep_v*vec_mom[0]
        momenta[3*i+1] = masses[i]*Kep_v*vec_mom[1]
        momenta[3*i+2] = masses[i]*Kep_v*vec_mom[2]
        
    return masses, positions, momenta

# ----------------------------MAIN-------------------------------- #
# Gravitational constant in units of kpc^3 M_sun^-1 Gyr-2
G = 4.4985022e-6/8000
# Number of bodies (may be smaller according to the distribution chosen).
N = int(sys.argv[1])
# Mass of the N bodies.
max_mass = 50. # Solar masses
# Supermassive Central Black Hole data
BHM = 1.e6 # Solar masses
BHposition = array([.5, .5, .5]) # Location of the SBH
#Parameters of the galaxy plane orientation 
beta=pi*int(sys.argv[2])/10     #Inclination
alpha=pi*int(sys.argv[3])/10    #Angle in the plain x,y
# Initial radius of the distribution
ini_radius = 10/20 #kpc
masses, positions, momenta = spiral_galaxy(N, max_mass, BHM, BHposition, ini_radius, beta, alpha)
#Save
print("#\t",N+1)
print(BHposition[0],"\t", BHposition[1], "\t", BHposition[2],"\t0\t0\t0\t", BHM)
for ii in range(N):
    print("{:.6f}".format(positions[3*ii+0]),"\t",
          "{:.6f}".format(positions[3*ii+1]),"\t",
          "{:.6f}".format(positions[3*ii+2]),"\t",
          "{:.6f}".format(momenta[3*ii+0]),"\t",
          "{:.6f}".format(momenta[3*ii+1]),"\t",
          "{:.6f}".format(momenta[3*ii+2]),"\t",
          "{:.6f}".format(masses[ii]))
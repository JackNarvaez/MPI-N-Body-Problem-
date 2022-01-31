/*---------------------------------------------
Evolution of a system of particles enclosed in
a box of unit sides, the only interaction is 
gravitation.
---------------------------------------------*/

#include <mpi.h>
#include <iostream>
#include <fstream> 
#include <sstream> 
#include <vector>
#include <random>
#include <cstdlib>
#include <cmath>
#include "NBodies.h"

int main(int argc, char **argv){

    int N; // Number of Particles
    int rep = std::atoi(argv[1]);
    int pId;  // Rank of process
    int nP;  // Number of processes
    int tag{0}; 
    int root{0};    // root process
    MPI_Status status;
    std::string input = "random.txt";
    read_NParticles(input, N);

    /*Initializes MPI*/
    MPI_Init(&argc, &argv);  
    MPI_Comm_size(MPI_COMM_WORLD, &nP);
    MPI_Comm_rank(MPI_COMM_WORLD, &pId);

    // Array size of each process
    std::vector<int> len(nP, 0);
    int end, begin;
    for(int ii=0; ii<nP; ii++){
        end = double(N)/nP*(ii+1);
        begin = double(N)/nP*ii;
        len[ii] = end-begin;
    }

    // Position, Momemtum and Force arrays
    std::vector<double> Pos(4*len[pId],0.0);    // [x, y, z, mass]
    std::vector<double> Mom(3*len[pId],0.0);
    std::vector<double> Force(3*len[pId],0.0);

    // Fill position and momentum vectors with the initial conditions
    Initial_state(input, Pos, Mom, len, N,  tag, pId, nP, root, status);
    // Calculate total force felt by all particles
    double tstart = 0.0;
    double tend = 0.0;
    double total_time = 0.0;
    for (int ii = 0; ii < rep; ii++){
      if (root == pId){
	tstart = MPI_Wtime();
      }
      Total_Force(Pos, Force, len, N, tag, pId, nP, root, status);
      if (root == pId) {
	tend = MPI_Wtime();
	total_time += tend - tstart;
	if (ii == (rep-1)){
	  std::cout<<nP<<"\t"<<total_time/rep<<"\n";
	}
      }
    }
    /*Finalizes MPI*/
    MPI_Finalize();

    return 0;
}
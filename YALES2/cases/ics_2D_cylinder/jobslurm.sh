#!/bin/bash
#SBATCH --partition=ib --constraint="ib&haswell_1"
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=2
#SBATCH --time=3:00:00
#SBATCH --mem-per-cpu=2G
#SBATCH --job-name=1j
#SBATCH --output=output.dat
#SBATCH --mail-type=ALL
#SBATCH --mail-user=glove1@uvm.edu

source ~/.bashrc
module use $HOME/yales2/modules && module load $(cd $HOME/yales2/modules; ls)
cd ~/Simulations/yales2/ics_2D_cylinder
mpirun ~/Simulations/yales2/ics_2D_cylinder/2D_cylinder

module use $HOME/yales2/modules && module load $(cd $HOME/yales2/modules; ls)
mpirun -n 10 ./2D_cylinder

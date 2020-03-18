###############################################################################
### PARAMETERS

DT=600.

###############################################################################
### RUNNING

for (( i=0; i<31; i++ )); do
   python mcmc_pal5.py -i ${i} -o ../pal5_mcmc/mwpot14-fitsigma-${i}.dat \
          --dt=${DT} --td=10. --fitsigma -m 6 &
done
wait

###############################################################################
### END
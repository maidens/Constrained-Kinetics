clear all
close all
clc

file = 'pc9154_data.mat'
load(file)

[Sscale, Mzscale] = flips_scaling_factors(flips, Nt); 

save(file)
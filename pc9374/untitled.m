clear all
close all
clc

file = 'pc9375_data.mat'
load(file)

[Sscale, Mzscale] = flips_scaling_factors(flips, Nt); 

save(file)
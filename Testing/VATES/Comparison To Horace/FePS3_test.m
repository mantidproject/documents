%% August 2014 preliminary analysis FePS3 on MERLIN

indir='Z:/Helen/';
par_file='C:/mprogs/InstrumentFiles/one2one_125.par';     % detector parameter file
dir_sqw='C:/Files/merlin/';        % output sqw file

%% initialise

efix1=75;%incident energy in meV
efix2=31.8; 
emode=1;%direct geometry
alatt=[5.947,10.3,6.722];%lattice parameters [a,b,c]
angdeg=[90,107.16,90];%lattice angles [alpha,beta,gamma]
uvec=[0,0,1];%u=// to incident beam
vvec=[0,1,0];%v= perpendicular to the incident beam, pointing towards the large angle detectors on Merlin in the horizontal plane
omega=0;dpsi=0;gl=0;gs=0;%offset angles in case of crystal misorientation (see the Horace manual for details)
psi=0;

%% load and generate sqw files 

% 7K
sqw_7K_75meV=[dir_sqw 'MER23357_75meV_on2one.sqw'];
spe_7K_75meV=[indir 'MER23357_75meV_on2one.nxspe'];

sqw_7K_32meV=[dir_sqw 'MER23357_31.8meV_on2one.sqw'];
spe_7K_32meV=[indir 'MER23357_31.8meV_on2one.nxspe'];

gen_sqw (spe_7K_75meV, par_file, sqw_7K_75meV, efix1, emode, alatt, angdeg, uvec, vvec, psi, omega, dpsi, gl, gs);
gen_sqw (spe_7K_32meV, par_file, sqw_7K_32meV, efix2, emode, alatt, angdeg, uvec, vvec, psi, omega, dpsi, gl, gs);

%% projection choice

proj.u = [0,1,0];
proj.v = [3,0,-1];
proj.type = 'rrr';
proj.uoffset = [0,0,0,0];
proj.lab1='k';
proj.lab2='h';
proj.lab3='l';
proj.lab4='E';

%% now slice and slice some more !

%% 32meV

% slice around h=0, with k along x-axis
Qh_0_slice=cut_sqw(read_sqw(sqw_7K_32meV),proj,0.075,[-0.1,0.1],[-Inf,Inf],[12,0,20]);
plot(Qh_0_slice)
lx(0,3)
lz(0,50)
keep

%% 75 meV

% slice with h along x-axis for different k positions
Qk_0p5_slice_75=cut_sqw(read_sqw(sqw_7K_75meV),proj,[0.4,0.6],0.075,[-Inf,Inf],[0,0,50]);
Qk_1_slice_75=cut_sqw(read_sqw(sqw_7K_75meV),proj,[0.9,1.1],0.075,[-Inf,Inf],[10,0,50]);
Qk_1p5_slice_75=cut_sqw(read_sqw(sqw_7K_75meV),proj,[1.4,1.6],0.075,[-Inf,Inf],[10,0,50]);

plot(Qk_0p5_slice_75)
lx(-3,3)
ly(0,50)
lz(0,100)
keep

plot(Qk_1_slice_75)
lx(-3,3)
ly(0,50)
lz(0,75)
keep

plot(Qk_1p5_slice_75)
lx(-3,3)
ly(0,50)
lz(0,75)
keep
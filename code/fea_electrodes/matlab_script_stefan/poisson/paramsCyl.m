function p=paramsCyl()

% returns all geometry parameters for plate capacitor actuator

% simulation parameters
p.sim.coordsys='cylindrical';% type of coordinate system
p.sim.Size=0.020;            % thickness and radius of simulation box
%p.sim.N=321;                 % number of points - hires
p.sim.N=201;                 % number of points - lores
p.sim.total_iter=100000;     % total iterations
p.sim.update_iter=5000;      % iterations between drawing updates
p.sim.iter_stepsize=0.1;     % dimensionless iteration step size parameter
                             % can affect convergence
d=p.sim.Size;


p.expBC.use=true;            % boolean use exponential BC?
p.expBC.R0=.015;             % exponential BC drop-off characteristic dist
p.expBC.V0=0;                % exponential BC drop-off target voltage


p.plate1.diameter=0.0762;      % diameter of front plate
p.plate1.hole_diameter=0.003;  % hole diameter in front plate
p.plate1.zpos=d/2+0.0045;      % z position of front plate
p.plate1.V=150.0;              % voltage on front plate


p.plate2.diameter=0.0762;      % diameter of back plate
p.plate2.hole_diameter=0.003;  % hole diameter in back plate
p.plate2.zpos=d/2-0.0045;      % z position of back plate
p.plate2.V=-150.0;             % voltage on back plate


p.optic.diameter=0.0254;     % optic diameter
p.optic.thickness=0.007;     % optic thickness
p.optic.zpos_com=d/2;        % optic center of mass position
%p.optic.eps=3.82;           % dielectric constant of optic (eps=1+chi)
p.optic.eps=13.436;          % dielectric constant of AlGaAs (D. E. Aspnes, S. M. Kelso, R. A. Logan and R. Bhat. Optical properties of AlxGa1-xAs, J. Appl. Phys. 60, 754-767 (1986))


p.boundaryConditionModel=0;  % select boundary condition model code
p.materialModel=0;           % select material model code


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Parameters below are for testing and evaluation

% cross-section definitions for testing
p.xsec1.label='Center of optic';
p.xsec1.type='z';
p.xsec1.rho=0;
p.xsec1.z1=p.plate2.zpos;
p.xsec1.z2=p.plate1.zpos;

p.xsec2.label='Edge of hole';
p.xsec2.type='z';
p.xsec2.rho=p.plate1.hole_diameter/2;
p.xsec2.z1=p.plate2.zpos;
p.xsec2.z2=p.plate1.zpos;

p.xsec3.label='Edge of optic';
p.xsec3.type='z';
p.xsec3.rho=p.optic.diameter/2;
p.xsec3.z1=p.plate2.zpos;
p.xsec3.z2=p.plate1.zpos;

p.xsec4.label='Edge of plate';
p.xsec4.type='z';
p.xsec4.rho=p.plate1.diameter/2;
p.xsec4.z1=p.plate2.zpos;
p.xsec4.z2=p.plate1.zpos;

p.xsec5.label='Halfway out on optic';
p.xsec5.type='z';
p.xsec5.rho=p.optic.diameter/4;
p.xsec5.z1=p.plate2.zpos;
p.xsec5.z2=p.plate1.zpos;

p.xsec11.label='Front plate';
p.xsec11.type='rho';
p.xsec11.rho1=0;
p.xsec11.rho2=p.sim.Size;
p.xsec11.z=p.plate1.zpos;

p.xsec12.label='Front of optic';
p.xsec12.type='rho';
p.xsec12.rho1=0;
p.xsec12.rho2=p.sim.Size;
p.xsec12.z=p.optic.zpos_com+p.optic.thickness/2;

p.xsec13.label='Middle of optic';
p.xsec13.type='rho';
p.xsec13.rho1=0;
p.xsec13.rho2=p.sim.Size;
p.xsec13.z=p.optic.zpos_com;

p.xsec14.label='Back of optic';
p.xsec14.type='rho';
p.xsec14.rho1=0;
p.xsec14.rho2=p.sim.Size;
p.xsec14.z=p.optic.zpos_com-p.optic.thickness/2;

p.xsec15.label='Back plate';
p.xsec15.type='rho';
p.xsec15.rho1=0;
p.xsec15.rho2=p.sim.Size;
p.xsec15.z=p.plate2.zpos;

% reference model for field and voltage
% (This is the analytic solution for a simple plate capacitor)
r.V=p.plate1.V-p.plate2.V;
r.b=p.optic.thickness;
r.a=p.plate1.zpos-p.optic.zpos_com-r.b/2;
r.c=p.optic.zpos_com-p.plate2.zpos-r.b/2;
r.eps=p.optic.eps;
r.Ea=r.V/(r.a+r.c+r.b/r.eps);
r.Eb=r.V/(r.eps*(r.a+r.c) + r.b);
r.Ec=r.Ea;
r.zr=p.plate2.zpos+[0, r.c, r.c+r.b, r.c+r.b+r.a];
r.Vr=[p.plate2.V, p.plate2.V+r.c*r.Ec, p.plate1.V-r.a*r.Ea, p.plate1.V];
r.fV=@(z) interp1(r.zr,r.Vr,z);
p.refmodel=r;


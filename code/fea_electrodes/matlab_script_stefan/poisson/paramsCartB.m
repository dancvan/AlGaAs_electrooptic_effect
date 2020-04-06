function p=paramsCartB()

% returns all geometry parameters for plate capacitor actuator
% butterfly drive

% simulation parameters
p.sim.coordsys='cartesian';  % type of coordinate system
p.sim.Size=0.05;             % thickness and radius of simulation box
p.sim.N=201;                 % number of points
p.sim.total_iter=40000;      % total iterations
p.sim.update_iter=1000;      % iterations between drawing updates
p.sim.iter_stepsize=0.1;     % dimensionless iteration step size parameter
                             % can affect convergence
d=p.sim.Size;


p.expBC.use=true;            % boolean use exponential BC?
p.expBC.R0=1e5;              % exponential BC drop-off characteristic dist
p.expBC.V0=0;                % exponential BC drop-off target voltage


p.plate1.width=0.02;         % diameter of plate
p.plate1.rhopos=d/2-0.0125;  % rho center position of plate
p.plate1.zpos=d/2+0.01;      % z position of plate
p.plate1.V=0.5;              % voltage on plate

p.plate2.width=0.02;         % diameter of plate
p.plate2.rhopos=d/2+0.0125;  % rho center position of plate
p.plate2.zpos=d/2+0.01;      % z position of plate
p.plate2.V=-0.5;             % voltage on plate

p.plate3.width=0.02;         % diameter of plate
p.plate3.rhopos=d/2-0.0125;  % rho center position of plate
p.plate3.zpos=d/2-0.01;      % z position of plate
p.plate3.V=-0.5;             % voltage on plate

p.plate4.width=0.02;         % diameter of plate
p.plate4.rhopos=d/2+0.0125;  % rho center position of plate
p.plate4.zpos=d/2-0.01;      % z position of plate
p.plate4.V=0.5;              % voltage on plate

p.optic.width=0.04;          % optic diameter
p.optic.thickness=0.015;     % optic thickness
p.optic.rhopos_com=d/2;      % optic center of mass position
p.optic.zpos_com=d/2;        % optic center of mass position
p.optic.eps=3.82;            % dielectric constant of optic (eps=1+chi)


p.boundaryConditionModel=1;  % select boundary condition model code
p.materialModel=1;           % select material model code


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Parameters below are for testing and evaluation

% cross-section definitions for testing
p.xsec1.label='Center of optic';
p.xsec1.type='z';
p.xsec1.rho=d/2;
p.xsec1.z1=p.plate3.zpos;
p.xsec1.z2=p.plate1.zpos;

p.xsec2.label='Edge of hole';
p.xsec2.type='z';
p.xsec2.rho=p.plate1.rhopos + p.plate1.width/2;
p.xsec2.z1=p.plate3.zpos;
p.xsec2.z2=p.plate1.zpos;

p.xsec3.label='Edge of optic';
p.xsec3.type='z';
p.xsec3.rho=p.optic.rhopos_com - p.optic.width/2;
p.xsec3.z1=p.plate3.zpos;
p.xsec3.z2=p.plate1.zpos;

p.xsec4.label='Edge of plate';
p.xsec4.type='z';
p.xsec4.rho=p.plate1.rhopos - p.plate1.width/2;
p.xsec4.z1=p.plate3.zpos;
p.xsec4.z2=p.plate1.zpos;

p.xsec5.label='Halfway out on optic';
p.xsec5.type='z';
p.xsec5.rho=p.optic.rhopos_com - p.optic.width/4;
p.xsec5.z1=p.plate3.zpos;
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
p.xsec15.z=p.plate3.zpos;

% reference model for field and voltage
% (This is the analytic solution for a simple plate capacitor)
r.V=p.plate1.V-p.plate3.V;
r.b=p.optic.thickness;
r.a=p.plate1.zpos-p.optic.zpos_com-r.b/2;
r.c=p.optic.zpos_com-p.plate3.zpos-r.b/2;
r.eps=p.optic.eps;
r.Ea=r.V/(r.a+r.c+r.b/r.eps);
r.Eb=r.V/(r.eps*(r.a+r.c) + r.b);
r.Ec=r.Ea;
r.zr=p.plate3.zpos+[0, r.c, r.c+r.b, r.c+r.b+r.a];
r.Vr=[p.plate3.V, p.plate3.V+r.c*r.Ec, p.plate1.V-r.a*r.Ea, p.plate1.V];
r.fV=@(z) interp1(r.zr,r.Vr,z);
p.refmodel=r;


% Cartesian and Cylindrical 2D Laplace solver
% capable of handing dielectric materials
% Stefan Ballmer, sballmer@syr.edu, 20200403

%clear all
%close all
global N R d step idx V rho z invrho edgeBCset Chi_e Vref
global LAP GRADrho GRADz GRADrhop GRADzp GRADrhom GRADzm
global Drhop Drhom Dzp Dzm
global p isCyl
p=parameters();
isCyl=strcmp(p.sim.coordsys,'cartesian');

edgeBCset=false;

N=p.sim.N;
R=p.sim.Size;
step=R/(N-1);
d=step*(N-1);


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% coordinate fields
rho_=transpose((0:N-1)*step);
z_=(0:N-1)*step;
rho=reshape(rho_*ones(1,N),N^2,1);
z  =reshape(ones(N,1)*z_,N^2,1);
invrho=1./rho;
invrho(rho==0)=0;


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% index ranges
% i_rho=1:N
% i_z  =1:N
% idx  =1:N^2
idx = @(i_rho,i_z) i_rho + (i_z-1)*N;
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% initialize the fields
V=zeros(N*N,1);
setBoundaryConditions()
setDielectric_Chi_e()
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% set up Lapace operator
LAP=generateLaplace();
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% set up Gradient operator
[GRADrho,GRADz,GRADrhop,GRADzp,GRADrhom,GRADzm]=generateGradient();
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% set up displacement operators
[Drhop,Drhom,Dzp,Dzm]=generateDisplacement();
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% set up dielectric operator
OP=generateOperator();
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% pre-operations
GRADrho_Chi_e=GRADrho*Chi_e;
GRADz_Chi_e  =GRADz  *Chi_e;
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


if 1
figure(1);
for itr=1:p.sim.total_iter
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % Iteration:
    tstp=p.sim.iter_stepsize;
    %V=V+step*step*tstp*LAP*V; % Solve LAP*V=0
    V =V+step*step*tstp*OP *V; % Solve dielectric configuration
    setBoundaryConditions()
    if mod(itr,p.sim.update_iter)==0
        plotField(V)
        drawnow()
    end
end
end

mkdir(datestr(today('datetime')))
curr_dir = [pwd '/' datestr(today('datetime')) '/']

figure(1);
plotField(V);
saveas(figure(1),[curr_dir datestr((today('datetime'))) '_potential_map']);

figure(11); plotXsec(p.xsec1);
saveas(figure(11),[curr_dir datestr((today('datetime'))) '_center_of_optic']);

figure(12); plotXsec(p.xsec2);
saveas(figure(12),[curr_dir datestr((today('datetime'))) '_edge_of_hole']);
%figure(13); plotXsec(p.xsec3);
%figure(14); plotXsec(p.xsec4);
figure(15); plotXsec(p.xsec5);
saveas(figure(15),[curr_dir datestr((today('datetime'))) '_halfway_out_on_optic']);
figure(21); plotXsec(p.xsec11);
saveas(figure(21),[curr_dir datestr((today('datetime'))) '_front_plate']);
figure(22); plotXsec(p.xsec12);
saveas(figure(22),[curr_dir datestr((today('datetime'))) '_front_of_optic']);
%figure(23); plotXsec(p.xsec13);
%figure(24); plotXsec(p.xsec14);
%figure(25); plotXsec(p.xsec15);




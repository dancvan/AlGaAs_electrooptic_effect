function setBoundaryConditions_vary(rho_inner,rho_outer,d_sample_electrode,Vp,Vm)

global N R d step idx V rho z edgeBCset Vref

vtop=0;
vbot=-0;

%rho_inner=0.005;
%rho_outer=0.05;
%d_sample_electrode=0.01;
%Vp= 1;
%Vm=-Vp;

if ~edgeBCset
    % set z=0 BC
    V(idx(1:N,1))=vbot;
    % set z=d BC
    V(idx(1:N,N))=vtop;
    % set rho=d BC
    V(idx(N,1:N))=interp1([1,N],[vbot,vtop],1:N);
    
    zz=max(min(z-d/2,d_sample_electrode),-d_sample_electrode);
    Vref=((zz)/d_sample_electrode)*Vp;
    
    edgeBCset=true;
end

bc=0;
if bc==0
    
    indrho=1+(round(rho_inner/step):round(rho_outer/step));
    indzb=1+round((d/2-d_sample_electrode)/step);
    indzt=1+round((d/2+d_sample_electrode)/step);
    V(idx(indrho,indzb))=Vm;
    V(idx(indrho,indzt))=Vp;
    setExpBC(1e6*d);
elseif bc==1
    Vp=1;
    Vm=0;
    %V(idx( 1,26:80))= Vp;
    V(idx( 1:30,26))= Vp;
    V(idx(30,26:75))= Vp;
    V(idx(10:30,75))= Vp;
    V(idx( 1:35,21))= Vm;
    V(idx(35,21:80))= Vm;
    V(idx( 5:35,80))= Vm;
    V(idx( 5,70:80))= Vm;
    V(idx( 5:25,70))= Vm;
    %V(idx(25,31:70))= Vm;    
    %V(idx( 5:25,31))= Vm;    
    setExpBC(step,Vm);
elseif bc==2
    Vp=1;
    Vm=-1;
    V(idx( 1,60))= Vp;
    V(idx( 1,40))= Vm;
    setExpBC(d);
end

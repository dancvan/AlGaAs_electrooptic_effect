function setBoundaryConditions()

global N R d step idx V rho z edgeBCset Vref p isCyl

% different bc for for different simulations. 
bc=p.boundaryConditionModel;

if bc==0    
    Vp=p.plate1.V;
    Vm=p.plate2.V;
    vtop=Vp;
    vbot=Vm;
else
    vtop=0;
    vbot=0;
end

if ~edgeBCset
    % set z=0 BC
    V(idx(1:N,1))=vbot;
    % set z=d BC
    V(idx(1:N,N))=vtop;
    % set rho=d BC
    V(idx(N,1:N))=interp1([1,N],[vbot,vtop],1:N);
    if not(isCyl)
        % set rho=0 BC
        V(idx(1,1:N))=interp1([1,N],[vbot,vtop],1:N);
    end  
    edgeBCset=true;
end

if bc==0    
    rho_inner1=p.plate1.hole_diameter/2;
    rho_outer1=p.plate1.diameter/2;
    rho_inner2=p.plate2.hole_diameter/2;
    rho_outer2=p.plate2.diameter/2;
    indrhob=1+(round(rho_inner2/step):round(rho_outer2/step));
    indrhot=1+(round(rho_inner1/step):round(rho_outer1/step));
    indzb=1+round((p.plate2.zpos)/step);
    indzt=1+round((p.plate1.zpos)/step);
    V(idx(indrhob,indzb))=Vm; % set plate 2 voltage
    V(idx(indrhot,indzt))=Vp; % set plate 1 voltage
    if p.expBC.use
        setExpBC(p.expBC.R0,p.expBC.V0);
    end
elseif bc==1
    pl=p.plate1;
    indrho=1+(round((pl.rhopos-pl.width/2)/step):round((pl.rhopos+pl.width/2)/step));
    indz=1+round((pl.zpos)/step);
    V(idx(indrho,indz))=pl.V;
    pl=p.plate2;
    indrho=1+(round((pl.rhopos-pl.width/2)/step):round((pl.rhopos+pl.width/2)/step));
    indz=1+round((pl.zpos)/step);
    V(idx(indrho,indz))=pl.V;
    pl=p.plate3;
    indrho=1+(round((pl.rhopos-pl.width/2)/step):round((pl.rhopos+pl.width/2)/step));
    indz=1+round((pl.zpos)/step);
    V(idx(indrho,indz))=pl.V;
    pl=p.plate4;
    indrho=1+(round((pl.rhopos-pl.width/2)/step):round((pl.rhopos+pl.width/2)/step));
    indz=1+round((pl.zpos)/step);
    V(idx(indrho,indz))=pl.V;  
    if p.expBC.use
        setExpBC(p.expBC.R0,p.expBC.V0);
    end
elseif bc==2
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
elseif bc==3
    Vp=1;
    Vm=-1;
    V(idx( 1,60))= Vp;
    V(idx( 1,40))= Vm;
    setExpBC(d);
end



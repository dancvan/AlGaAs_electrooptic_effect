function setDielectric_Chi_e()

global N R d step idx V rho z edgeBCset Chi_e Ch Vref p

Chi_e=zeros(N*N,1);

Chi_e_val=p.optic.eps-1; % switching frop epsilon to chi
material=p.materialModel;
if material==0
    ind=and(abs(z-p.optic.zpos_com) <(p.optic.thickness/2),rho<(p.optic.diameter/2));
    Chi_e(ind)=Chi_e_val;    
elseif material==1
    ind=and(abs(z-p.optic.zpos_com) <(p.optic.thickness/2),abs(rho-p.optic.rhopos_com) <(p.optic.width/2));
    Chi_e(ind)=Chi_e_val;    
end

Ch=Chi_e/2; % array with 1/2 of dielectric constat - used frequently.


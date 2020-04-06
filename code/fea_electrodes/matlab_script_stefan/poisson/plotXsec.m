function plotXsec(xsec)

global N R d step idx V rho z p

if xsec.type=='z'
    indrho=1+round(xsec.rho/step);
    indz=1+(round(xsec.z1/step):round(xsec.z2/step));
    ind=idx(indrho,indz);
    zz=z(ind);
    VV=V(ind);
    plot(zz,VV,zz,p.refmodel.fV(zz));
    grid on
    xlabel('z position (m)')
    ylabel('Volt')
    title(xsec.label);
    legend('cross-section','reference model');
end
if xsec.type=='rho'
    indrho=1+(round(xsec.rho1/step):round(xsec.rho2/step));
    indz=1+round(xsec.z/step);
    ind=idx(indrho,indz);
    rr=rho(ind);
    VV=V(ind);
    plot(rr,VV);
    grid on
    xlabel('rho position (m)')
    ylabel('Volt')
    title(xsec.label);
end
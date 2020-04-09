function plotXsec(xsec,field,fieldunitlabel)

global N R d step idx V rho z p

noref=true;
if ~exist('field','var')
    field=V;
    fieldunitlabel='Volt';
    noref=false;
end


if xsec.type=='z'
    indrho=idxrnd(xsec.rho);
    indz=idxrnd(xsec.z1):idxrnd(xsec.z2);
    ind=idx(indrho,indz);
    zz=z(ind);
    VV=field(ind);
    if noref
        plot(zz,VV);
        grid on
        xlabel('z position (m)')
        ylabel(fieldunitlabel)
        title(xsec.label);
        legend('cross-section');
    else
        plot(zz,VV,zz,p.refmodel.fV(zz));
        grid on
        xlabel('z position (m)')
        ylabel(fieldunitlabel)
        title(xsec.label);
        legend('cross-section','reference model');
    end
end
if xsec.type=='rho'
    indrho=idxrnd(xsec.rho1):idxrnd(xsec.rho2);
    indz=idxrnd(xsec.z);
    ind=idx(indrho,indz);
    rr=rho(ind);
    VV=field(ind);
    plot(rr,VV);
    grid on
    xlabel('rho position (m)')
    ylabel(fieldunitlabel)
    title(xsec.label);
end
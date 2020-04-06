function LAP=generateLaplace()
% generate Laplace operator in cartesian or cylindrial coordinates
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% BC for cartesian coordinates:
%  - defined to be 0 for z=min (izy=1) and z=max (izy=N)
%  - defined to be 0 for rho=max (irhoy=N)
%  - defined to be 0 for rho=min (irhoy=1)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% BC for cylindrical coordinates:
%  - defined to be 0 for z=min (izy=1) and z=max (izy=N)
%  - defined to be 0 for rho=max (irhoy=N)
%  - defined continuous for rho=min (irhoy=1)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Stefan Ballmer 2020/04/02

global N step idx isCyl

LAP=spalloc(N*N,N*N,5*N*N);
if isCyl % cylindrical coordinates
    for izy=2:(N-1)
        irhoy=1;
        LAP(idx(irhoy,izy),idx(irhoy  ,izy  ))=-6;
        LAP(idx(irhoy,izy),idx(irhoy+1,izy  ))= 4;
        LAP(idx(irhoy,izy),idx(irhoy  ,izy-1))= 1;
        LAP(idx(irhoy,izy),idx(irhoy  ,izy+1))= 1;
        for irhoy=2:(N-1)
            n=(irhoy-1);
            LAP(idx(irhoy,izy),idx(irhoy  ,izy  ))=-4;
            LAP(idx(irhoy,izy),idx(irhoy-1,izy  ))= 1-1/2/n;
            LAP(idx(irhoy,izy),idx(irhoy+1,izy  ))= 1+1/2/n;
            LAP(idx(irhoy,izy),idx(irhoy  ,izy-1))= 1;
            LAP(idx(irhoy,izy),idx(irhoy  ,izy+1))= 1;
        end
    end
else % cartesian coordinates
    for izy=2:(N-1)
        for irhoy=2:(N-1)
            LAP(idx(irhoy,izy),idx(irhoy  ,izy  ))=-4;
            LAP(idx(irhoy,izy),idx(irhoy-1,izy  ))= 1;
            LAP(idx(irhoy,izy),idx(irhoy+1,izy  ))= 1;
            LAP(idx(irhoy,izy),idx(irhoy  ,izy-1))= 1;
            LAP(idx(irhoy,izy),idx(irhoy  ,izy+1))= 1;
        end
    end
end
LAP=LAP/(step^2);


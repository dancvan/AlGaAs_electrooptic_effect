function [GRADrho,GRADz,GRADrhop,GRADzp,GRADrhom,GRADzm]=generateGradient()
% generate Gradient operator in cartesian or cylindrial coordinates
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% BC:
%  - defined to be 0 if any of the inputs is outside the field
%  - 1/2-shifted gradients ..p & ..m: defined to be 0 if either one has
%                                     has inputs ouside the field
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Stefan Ballmer 2020/04/02

global N step idx

GRADrho=spalloc(N*N,N*N,2*N*N);
for izy=1:N
  for irhoy=2:(N-1)
      GRADrho(idx(irhoy,izy),idx(irhoy-1,izy  ))= -1/2;
      GRADrho(idx(irhoy,izy),idx(irhoy+1,izy  ))= +1/2;
  end
end
GRADrho=GRADrho/step;

GRADz=spalloc(N*N,N*N,2*N*N);
for izy=2:(N-1)
  for irhoy=1:N
      GRADz(idx(irhoy,izy),idx(irhoy  ,izy-1))= -1/2;
      GRADz(idx(irhoy,izy),idx(irhoy  ,izy+1))= +1/2;
  end
end
GRADz=GRADz/step;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% position +1/2 shifted gradients
GRADrhop=spalloc(N*N,N*N,2*N*N);
for izy=1:N
  for irhoy=2:(N-1)
      GRADrhop(idx(irhoy,izy),idx(irhoy  ,izy  ))= -1;
      GRADrhop(idx(irhoy,izy),idx(irhoy+1,izy  ))= +1;
  end
end
GRADrhop=GRADrhop/step;

GRADzp=spalloc(N*N,N*N,2*N*N);
for izy=2:(N-1)
  for irhoy=1:N
      GRADzp(idx(irhoy,izy),idx(irhoy  ,izy  ))= -1;
      GRADzp(idx(irhoy,izy),idx(irhoy  ,izy+1))= +1;
  end
end
GRADzp=GRADzp/step;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% position -1/2 shifted gradients
GRADrhom=spalloc(N*N,N*N,2*N*N);
for izy=1:N
  for irhoy=2:(N-1)
      GRADrhom(idx(irhoy,izy),idx(irhoy-1,izy  ))= -1;
      GRADrhom(idx(irhoy,izy),idx(irhoy  ,izy  ))= +1;
  end
end
GRADrhom=GRADrhom/step;

GRADzm=spalloc(N*N,N*N,2*N*N);
for izy=2:(N-1)
  for irhoy=1:N
      GRADzm(idx(irhoy,izy),idx(irhoy  ,izy-1))= -1;
      GRADzm(idx(irhoy,izy),idx(irhoy  ,izy  ))= +1;
  end
end
GRADzm=GRADzm/step;




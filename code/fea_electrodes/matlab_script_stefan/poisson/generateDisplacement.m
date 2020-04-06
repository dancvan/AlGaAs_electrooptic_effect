function [Drhop,Drhom,Dzp,Dzm]=generateDisplacement()
% generate Displacement operator (by step) in cylindrial coordinates
% BC:
%  - defined to be 0 is shifting from outside
% Stefan Ballmer 2019/10/03

global N idx

Drhop=spalloc(N*N,N*N,1*N*N);
for izy=1:(N-0)
  for irhoy=2:(N-0)
      Drhop(idx(irhoy,izy),idx(irhoy-1,izy  ))= 1;
  end
end

Drhom=spalloc(N*N,N*N,1*N*N);
for izy=1:(N-0)
  for irhoy=1:(N-1)
      Drhom(idx(irhoy,izy),idx(irhoy+1,izy  ))= 1;
  end
end

Dzp=spalloc(N*N,N*N,1*N*N);
for izy=2:(N-0)
  for irhoy=1:(N-0)
      Dzp(idx(irhoy,izy),idx(irhoy  ,izy-1))= 1;
  end
end

Dzm=spalloc(N*N,N*N,1*N*N);
for izy=1:(N-1)
  for irhoy=1:(N-0)
      Dzm(idx(irhoy,izy),idx(irhoy  ,izy+1))= 1;
  end
end

function setExpBC(R0,V0)

%new edge boundary conditions:
%exponential drop-off on scale R0:

global step d N V idx isCyl

if ~exist('R0','var')
    R0=d;
end

if ~exist('V0','var')
    V0=0;
end

V(idx(1:N,N))=V0+exp(-step/R0)*(V(idx(1:N,N-1))-V0);
V(idx(1:N,1))=V0+exp(-step/R0)*(V(idx(1:N,  2))-V0);
V(idx(N,1:N))=V0+exp(-step/R0)*(V(idx(N-1,1:N))-V0);
if not(isCyl)
    V(idx(1,1:N))=V0+exp(-step/R0)*(V(idx(2,1:N))-V0);
end

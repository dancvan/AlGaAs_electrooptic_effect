function idx=idxrnd(dist)

%find nearest index and check for overflow

global N step

idx=1+round(dist/step);
idx(idx<1)=1;
idx(idx>N)=N;

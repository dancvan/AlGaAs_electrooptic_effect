n = 319; m = 239;     % n x m pixels area/data matrix
I0 = [20,0,20,0,20,0];  % Inital (guess) parameters
[X,Y]=meshgrid(-n/2:n/2,-m/2:m/2); Z=zeros(m+1,n+1,2); Z(:,:,1)=X; Z(:,:,2)=Y;
f = @(I0,X,Y) I0(1).*exp(-2*(X.^2/(I0(3))^2)-2*(Y.^2/(I0(5))^2));
dc_sig = csvread('frame0101_raw.csv');
fit_coeff = lsqcurvefit(f,I0,X,Y,dc_sig);
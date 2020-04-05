function plotField(V)

global N rho z


%surface(reshape(rho,N,N),reshape(z,N,N),reshape(V,N,N));
%surf(reshape(rho,N,N),reshape(z,N,N),reshape(V,N,N));
mesh(reshape(rho,N,N),reshape(z,N,N),reshape(V,N,N));
%contour(reshape(rho,N,N),reshape(z,N,N),reshape(V,N,N),-1:0.05:1);
xlabel('rho')
ylabel('z')
colorbar




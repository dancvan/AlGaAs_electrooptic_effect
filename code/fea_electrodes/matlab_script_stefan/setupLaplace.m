% Cylindrical Laplace solver

clear all
close all
global N R d step idx V rho z edgeBCset Vref


edgeBCset=false;

N=101;
R=0.1;
step=R/(N-1);
d=step*(N-1);

rho_=transpose((0:N-1)*step);
z_=(0:N-1)*step;
rho=reshape(rho_*ones(1,N),N^2,1);
z  =reshape(ones(N,1)*z_,N^2,1);

% index ranges
% i_rho=1:N
% i_z  =1:N
% idx  =1:N^2
idx = @(i_rho,i_z) i_rho + (i_z-1)*N;

%% Setting Boundary condition parameters
rho_inner=0.005;
rho_outer=0.05;
d_sample_electrode=.008:.002:.04;
Vp= 25;
Vm=-Vp;
center_y_deriv = zeros(length(d_sample_electrode),(N-1)); 
for i=1:length(d_sample_electrode)
    % set up Lapace operator
    LAP=spalloc(N*N,N*N,5*N*N);
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
    LAP=LAP/(step^2);

    V=zeros(N*N,1);
    
    %V=z.*z/2 + rho.*rho/2;
    setBoundaryConditions_vary(rho_inner,rho_outer, d_sample_electrode(i),Vp,Vm)
    
    if 1
    for itr=1:20000
        V=V+step*step*0.1*LAP*V;
        setBoundaryConditions_vary(rho_inner,rho_outer, d_sample_electrode(i),Vp,Vm)
        if mod(itr,100)==0
            %plotField(V)
            drawnow()
        end
    end
    end
    plotField(V);
    V_grid = reshape(V,N,N);
    center_y_deriv(i,:) = V_grid(1,2:end) - V_grid(1,1:(end-1));
end

figure(59)
for i = 1:length(d_sample_electrode) 
    plot((1:length(center_y_deriv(1,:))), center_y_deriv(i,:)/.001)
    hold on
end
xlabel('z [mm]')
ylabel('$E_y$ ($\frac{dV}{dy}$) @ $\rho = 0$ [V/m]', 'Interpreter', 'Latex')

figure(63)
plot(d_sample_electrode(:)/.001, center_y_deriv(:,50)/.001)
xlabel('d [mm]')
ylabel('$E_y$ @ $\rho = 0$ and $z = 0$  [V/m]', 'Interpreter', 'Latex')

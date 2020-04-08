function plot_field_comps()

 global N rho z step V
 global p

 rho_dim = 0;
 z_dim = 1;
 quiver = 0;
 
 
[E_rho, E_z] = gradient(reshape(V,N,N)',step);

if rho_dim ~= 0;
    figure(54)
    mesh(reshape(rho,N,N), reshape(z,N,N), E_rho')
    hold on
    E_rho = E_rho'
    scatter3(1*step, p.xsec12.z,E_rho(1,(p.xsec12.z/step)),20,'green')
    disp(['E_rho @ front and center of optic is ', E_rho(1,(p.xsec12.z/step)),' [V/m]'])
    xlabel('rho [m]','FontSize', 25)
    ylabel('z [m]','FontSize',25)
    zlabel('E_rho [V/m]', 'FontSize',25)
    title('E_{\rho}', 'FontSize' , 30)
else z_dim ~= 0;
    figure(58)
    mesh(reshape(rho,N,N), reshape(z,N,N), E_z')
    hold on
    E_z = E_z';
    scatter3(1*step, p.xsec12.z,E_z(1,(p.xsec12.z/step)),20,'red')
    disp(['E_z @ front and center of optic is ',num2str(E_z(1,(p.xsec12.z/step))),' [V/m]'])
    xlabel('rho [m]','FontSize',25)
    ylabel('z [m]','FontSize',25)
    zlabel('E_z [V/m]', 'FontSize',25)
    title('E_{z}','FontSize',30)
end 

X = ['E_z/E_rho ratio is ', num2str(E_z(1,(p.xsec12.z/step)) / E_rho(1,(p.xsec12.z/step)))];
disp(X)

if quiver ~= 0;
    figure(62)
    quiver((1:N)*step, (1:N)*step', E_rho, E_z)
end
end 

 
 
 
 
 
 
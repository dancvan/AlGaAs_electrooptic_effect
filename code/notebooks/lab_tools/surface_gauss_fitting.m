function surface_gauss_fitting(image_array)
    zdata = image_array; 
    z_max = max(zdata); 
    [min_val,idx]=min(zdata(:)); 
    [row,col]=ind2sub(size(zdata),idx); 
    xcrssec = zdata(row,:);
    ycrssec = zdata(:,col)';
    
    n = 319; m = 239;     % n x m pixels area/data matrix
    xcoeffs = gaussian_fit([-20,150,20,-5], 1:length(xcrssec),xcrssec)
    ycoeffs = gaussian_fit([-20,150,20,-5], 1:length(ycrssec),ycrssec)
    
    gauss = @(coeffs,x) coeffs(1)*exp(-(x-coeffs(2)).^2./(2*coeffs(3))) + coeffs(4);
    
    figure(34)
    plot(1:length(xcrssec),gauss(xcoeffs,1:length(xcrssec)))
    hold on 
    plot(1:length(xcrssec),xcrssec)
    title('Gaussian data and fit (x cross section)','FontSize',30)
    
    figure(43)
    plot(1:length(ycrssec),gauss(ycoeffs,1:length(ycrssec)))
    hold on
    plot(1:length(ycrssec),ycrssec)
    title('Gaussian data and fit (y cross section)','FontSize',30)
    
    
    
    
end 
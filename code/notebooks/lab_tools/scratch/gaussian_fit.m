function fit_coeffs = gaussian_fit(init_guess,xdata, ydata)

    gauss = @(coeffs,xdata) coeffs(1)*exp(-(xdata-coeffs(2)).^2./(2*coeffs(3))) + coeffs(4);    %defines a temporary gaussian function in matlab
                                                                            %in terms of 3 coeffients and xdata you want to fit over
                                                                            
    fit_coeffs = lsqcurvefit(gauss,init_guess,xdata,ydata);                 %Apply matlab's least square fitting function
                                                                            
                                                                            %Resulting fitted parameters:     
    a = fit_coeffs(1);                                                      % Ampltude coeff             
    b = fit_coeffs(2);                                                      % horizontal offset coeff 
    c = fit_coeffs(3);                                                      % stretch coeff
    d = fit_coeffs(4);                                                      % vertical offset coeff
end 


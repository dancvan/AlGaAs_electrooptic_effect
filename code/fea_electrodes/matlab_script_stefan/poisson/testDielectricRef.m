% for testing - get reference field
if 0
    V_=1;
    Vu_=V_/(3+2*Chi_e_val);
    indp=z>=2*d/3;
    indm=z<=  d/3;
    Vref(ind) = (z(ind)-d/2) * V_/(d/3)/(1.5+Chi_e_val) ;
    E=V_/(d/3)*(1+Chi_e_val)/(1.5+Chi_e_val);
    Vref(indm)= -V_ + z(indm) * E ;
    Vref(indp)=  V_ + (z(indp)-d) * E ;
    
end
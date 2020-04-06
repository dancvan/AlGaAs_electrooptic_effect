function OP=generateOperator()

% dielectric operator - replaces LAP*V if dielectrics are present
global Ch invrho step N
global LAP GRADrho GRADrhop GRADzp GRADrhom GRADzm
global Drhop Drhom Dzp Dzm
global isCyl

if isCyl
    G0=spalloc(N*N,N*N,1*N*N);
    G1=spdiags(1./(1+Ch) ,0,G0);
    G2=spdiags(Ch.*invrho,0,G0);
    Rm=spdiags(Drhom*Ch,0,G0);
    Rp=spdiags(Drhop*Ch,0,G0);
    Zm=spdiags(Dzm  *Ch,0,G0);
    Zp=spdiags(Dzp  *Ch,0,G0);
    OP=LAP  + ...
        G1*( ...
        G2*GRADrho + ...
        (Rm*GRADrhop-Rp*GRADrhom)/step + ...
        (Zm*GRADzp  -Zp*GRADzm  )/step );
else
    G0=spalloc(N*N,N*N,1*N*N);
    G1=spdiags(1./(1+Ch) ,0,G0);
    Rm=spdiags(Drhom*Ch,0,G0);
    Rp=spdiags(Drhop*Ch,0,G0);
    Zm=spdiags(Dzm  *Ch,0,G0);
    Zp=spdiags(Dzp  *Ch,0,G0);
    OP=LAP  + ...
        G1*( ...
        (Rm*GRADrhop-Rp*GRADrhom)/step + ...
        (Zm*GRADzp  -Zp*GRADzm  )/step );
end

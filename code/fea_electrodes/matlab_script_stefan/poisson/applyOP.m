function OPV=applyOP(V)

% dielectric operator - replaces LAP*V if dielectrics are present
global Ch invrho step N
global LAP GRADrho GRADrhop GRADzp GRADrhom GRADzm
global Drhop Drhom Dzp Dzm

OPV=(1+Ch).*(LAP*V)  + ...
    (Ch.*invrho).*(GRADrho*V) + ...
    ((Drhom*Ch).*(GRADrhop*V)-(Drhop*Ch).*(GRADrhom*V))/step + ...
    ((Dzm  *Ch).*(GRADzp  *V)-(Dzp*  Ch).*(GRADzm  *V))/step ;

% for convergance scaling:
OPV=OPV./(1+Ch);

if 0
end

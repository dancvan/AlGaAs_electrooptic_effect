%% Plotting front of optic (immediately inside and outside field)

close all
c = get(gca,'colororder');
c([1,3],:) = c([3,1],:);
c([2,4],:) = c([4,2],:);
set(gca, 'ColorOrder', c, 'NextPlot','ReplaceChildren')
plotXsec(p.xsec12,GRADzp*V,'Ez [V/m]')
hold on
plotXsec(p.xsec12,GRADzm*V,'Ez [V/m]')
set(findall(gca, 'Type', 'Line'),'LineWidth',5);
saveas(gcf,['../../../../results/simulations/electrodes/disk' '/' datestr(today('datetime')) '/' datestr((today('datetime'))) '_e_field_inside_outside_normal']);
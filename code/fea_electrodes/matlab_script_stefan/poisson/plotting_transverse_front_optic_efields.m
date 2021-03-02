%% Plotting front of optic (immediately inside and outside field)

figure(712)
c = get(gca,'colororder');
c([1,3],:) = c([3,1],:);
c([2,4],:) = c([4,2],:);
set(gca, 'ColorOrder', c, 'NextPlot','ReplaceChildren')
plotXsec(p.xsec12,GRADrhop*V,'Erho [V/m]');
hold on
plotXsec(p.xsec12,GRADrhom*V,'Erho [V/m]');
set(findall(gca, 'Type', 'Line'),'LineWidth',5);
saveas(gcf,[curr_dir datestr((today('datetime'))) '_b_e_field_inside_outside']);
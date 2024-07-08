clc;clear; close all
%% MOD-DH

d1 = 40;
d2 = 0;
d3 = 116;
d4 = 0;


a1 = 0;
a2 = 0;
a3 = 0;
a4 = 0;


alpha1 = 0;
alpha2 = pi/2;
alpha3 = -pi/2;
alpha4 = pi/2;


L1=Link([0     d1       a1       alpha1     ],'modified');
L2=Link([0     d2       a2       alpha2     ],'modified');
L3=Link([0     d3       a3       alpha3     ],'modified');
L4=Link([0     d4       a4       alpha4     ],'modified');


%L1.qlim = [(-165/180)*pi,(165/180)*pi];
%L2.qlim = [(-95/180)*pi, (70/180)*pi];
%L3.qlim = [(-85/180)*pi, (95/180)*pi];
%L4.qlim = [(-180/180)*pi,(180/180)*pi];
%L5.qlim = [(-115/180)*pi,(115/180)*pi];

robot=SerialLink([L1 L2 L3 L4 ],'name','liflo');
robot.tool=transl(0,168.86,0)
%robot.plot([0,0,0,0,0]);
robot.display();
robot.teach;
hold on;
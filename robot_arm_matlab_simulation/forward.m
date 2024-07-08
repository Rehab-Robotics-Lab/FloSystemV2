clear;
clc;
%% 正解
%输入端
theta1=0;
theta2=0;
theta3=0;
theta4=0;

%参数
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


MDH = [theta1          d1       a1       alpha1;
       theta2          d2       a2       alpha2;    
       theta3          d3       a3       alpha3;
       theta4          d4       a4       alpha4;
];
   
T01=[cos(MDH(1,1))               -sin(MDH(1,1))                 0              MDH(1,3);
     sin(MDH(1,1))*cos(MDH(1,4))  cos(MDH(1,1))*cos(MDH(1,4))  -sin(MDH(1,4)) -sin(MDH(1,4))*MDH(1,2);
     sin(MDH(1,1))*sin(MDH(1,4))  cos(MDH(1,1))*sin(MDH(1,4))   cos(MDH(1,4))  cos(MDH(1,4))*MDH(1,2);
      0                           0                             0              1];
T12=[cos(MDH(2,1))               -sin(MDH(2,1))                 0              MDH(2,3);
     sin(MDH(2,1))*cos(MDH(2,4))  cos(MDH(2,1))*cos(MDH(2,4))  -sin(MDH(2,4)) -sin(MDH(2,4))*MDH(2,2);
     sin(MDH(2,1))*sin(MDH(2,4))  cos(MDH(2,1))*sin(MDH(2,4))   cos(MDH(2,4))  cos(MDH(2,4))*MDH(2,2);
      0                           0                             0              1];
T23=[cos(MDH(3,1))               -sin(MDH(3,1))                 0              MDH(3,3);
     sin(MDH(3,1))*cos(MDH(3,4))  cos(MDH(3,1))*cos(MDH(3,4))  -sin(MDH(3,4)) -sin(MDH(3,4))*MDH(3,2);
     sin(MDH(3,1))*sin(MDH(3,4))  cos(MDH(3,1))*sin(MDH(3,4))   cos(MDH(3,4))  cos(MDH(3,4))*MDH(3,2);
      0                           0                             0              1];
T34=[cos(MDH(4,1))               -sin(MDH(4,1))                 0              MDH(4,3);
     sin(MDH(4,1))*cos(MDH(4,4))  cos(MDH(4,1))*cos(MDH(4,4))  -sin(MDH(4,4)) -sin(MDH(4,4))*MDH(4,2);
     sin(MDH(4,1))*sin(MDH(4,4))  cos(MDH(4,1))*sin(MDH(4,4))   cos(MDH(4,4))  cos(MDH(4,4))*MDH(4,2);
      0                           0                             0              1];


T04 = T01*T12*T23*T34*transl(0,168.86,0)

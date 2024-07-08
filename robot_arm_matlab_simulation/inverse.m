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

robot=SerialLink([L1 L2 L3 L4 ],'name','liflo');
robot.tool=transl(0,168.86,0)
%%【输入端】（可修改）输入末端位姿矩阵→输出各个关节角
T1 =    [   
    1.0000         0         0         0
         0    0.0000   -1.0000    0.0000
         0    1.0000    0.0000  324.8600
         0         0         0    1.0000
       ]
%SerialLink.ikine Inverse kinematics by optimization without joint limits
%
% Q = R.ikine(T) are the joint coordinates (1xN) corresponding to the robot
% end-effector pose T which is an SE3 object or homogenenous transform
% matrix (4x4), and N is the number of robot joints.
%
% This method can be used for robots with any number of degrees of freedom.
% 这个方法适用于任意自由度的机器人
%
% Options::
% 'ilimit',L        maximum number of iterations (default 500)      迭代次数
% 'rlimit',L        maximum number of consecutive step rejections (default 100)      最大连续拒绝次数
% 'tol',T           final error tolerance (default 1e-10)   最终误差容限
% 'lambda',L        initial value of lambda (default 0.1)   步长
% 'lambdamin',M     minimum allowable value of lambda (default 0)	步长的最小值
% 'quiet'           be quiet	输出保持安静
% 'verbose'         be verbose		输出内容详细
% 'mask',M          mask vector (6x1) that correspond to translation in X, Y and Z, 
%                   and rotation about X, Y and Z respectively.		mask向量，表示机器人自由度
% 'q0',Q            initial joint configuration (default all zeros)     迭代的初始关节形位
% 'search'          search over all configurations      搜索所有形位
% 'slimit',L        maximum number of search attempts (default 100)     最大搜索尝试数目
% 'transpose',A     use Jacobian transpose with step size A, rather than
%                   Levenberg-Marquadt      使用步长为A的雅可比转置，而不是LM方法
%
% Trajectory operation::
%
% In all cases if T is a vector of SE3 objects (1xM) or a homogeneous
% transform sequence (4x4xM) then returns the joint coordinates
% corresponding to each of the transforms in the sequence.  Q is MxN where
% N is the number of robot joints. The initial estimate of Q for each time
% step is taken as the solution from the previous time step.
% 使用上一步的解作为当前步的初始值
%
% Underactuated robots::    欠驱动机器人
%
% For the case where the manipulator has fewer than 6 DOF the solution
% space has more dimensions than can be spanned by the manipulator joint
% coordinates.
% 欠驱动机器人解空间维数比关节坐标维数多？
%
% In this case we specify the 'mask' option where the mask
% vector (1x6) specifies the Cartesian DOF (in the wrist coordinate
% frame) that will be ignored in reaching a solution.  The mask vector
% has six elements that correspond to translation in X, Y and Z, and rotation
% about X, Y and Z respectively.  The value should be 0 (for ignore) or 1.
% The number of non-zero elements should equal the number of manipulator DOF.
% 使用“mask”矢量指定失去的自由度，机器人自由度等于改矢量的非零元素的个数。
%
% For example when using a 3 DOF manipulator rotation orientation might be
% unimportant in which case use the option: 'mask', [1 1 1 0 0 0].
% 举个例子，当使用三自由度机械手时，旋转方向可能不重要（不影响逆运动学求解），mask向量设置为[1 1 1 0 0 0]
%
% For robots with 4 or 5 DOF this method is very difficult to use since
% orientation is specified by T in world coordinates and the achievable
% orientations are a function of the tool position.
% 对于4或5个自由度的机器人，这种方法较难使用
%
% References::
% - Robotics, Vision & Control, P. Corke, Springer 2011, Section 8.4.
%
% Notes::
% - This has been completely reimplemented in RTB 9.11
% - Does NOT require MATLAB Optimization Toolbox.   不需要matlab优化工具箱
% - Solution is computed iteratively.   采用迭代的方法
% - Implements a Levenberg-Marquadt variable step size solver.
%   通过LM变步长求解器实现
% - The tolerance is computed on the norm of the error between current
%   and desired tool pose.  This norm is computed from distances
%   and angles without any kind of weighting.
%   误差是根据当前工具姿态和期望（求解）姿态的范数计算
% - The inverse kinematic solution is generally not unique, and
%   depends on the initial guess Q0 (defaults to 0).
%   求解的值不唯一，且与初值有关，初值Q0默认为0
% - The default value of Q0 is zero which is a poor choice for most
%   manipulators (eg. puma560, twolink) since it corresponds to a kinematic
%   singularity.
%   Q0设置为[0 0 0 0 0 0]，这对于部机器人（puma560，twolink）不是好选择，因为其对应运动学奇点
% - Such a solution is completely general, though much less efficient
%   than specific inverse kinematic solutions derived symbolically, like
%   ikine6s or ikine3.
% 	这是通用的解法，所以效率不高
% - This approach allows a solution to be obtained at a singularity, but
%   the joint angles within the null space are arbitrarily assigned.
% 	此方法可能在奇异点求出解
% - Joint offsets, if defined, are added to the inverse kinematics to
%   generate Q.
% 	如果定义了关节偏移，将添加到逆运动学中以生成Q
% - Joint limits are not considered in this solution.
%　 不考虑关节的范围限制
% - The 'search' option peforms a brute-force search with initial conditions
%   chosen from the entire configuration space.
% 	“search”选项形成一个强力搜索，初始条件从整个关节空间中随机选择
% - If the 'search' option is used any prismatic joint must have joint
%   limits defined.
% 	如果使用“搜索”选项，则任何移动关节都必须定义关节范围
%
% See also SerialLink.ikcon, SerialLink.ikunc, SerialLink.fkine, SerialLink.ikine6s.



% Copyright (C) 1993-2017, by Peter I. Corke
%
% This file is part of The Robotics Toolbox for MATLAB (RTB).
% 
% RTB is free software: you can redistribute it and/or modify
% it under the terms of the GNU Lesser General Public License as published by
% the Free Software Foundation, either version 3 of the License, or
% (at your option) any later version.
% 
% RTB is distributed in the hope that it will be useful,
% but WITHOUT ANY WARRANTY; without even the implied warranty of
% MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
% GNU Lesser General Public License for more details.
% 
% You should have received a copy of the GNU Leser General Public License
% along with RTB.  If not, see <http://www.gnu.org/licenses/>.
%
% http://www.petercorke.com

%TODO:
% search do a broad search from random points in configuration space
%数值解
theta_1_1 = robot.ikine(T1,'mask',[1 1 1 1 0 0])


function qt = ikine(robot, tr, varargin)
    
    n = robot.n;        	%关节变量的个数
    
    TT = SE3.check(tr);     %转换为SE3矩阵
        
    %  set default parameters for solution   默认参数设置
    opt.ilimit = 500;   	%默认迭代次数
    opt.rlimit = 100;   	%最大连续拒绝次数
    opt.slimit = 100;   	%最大尝试次数
    opt.tol = 1e-10;    	%默认迭代误差
    opt.lambda = 0.1;  		%默认步长
    opt.lambdamin = 0;  	%默认步长最小值
    opt.search = false; 	%默认关闭搜索初值
    opt.quiet = false;  	%保持安静，减少输出
    opt.verbose = false;        %输出的信息详细
    opt.mask = [1 1 1 1 1 1];   %默认六自由度
    opt.q0 = zeros(1, n);   	%初始关节形位为零位
    opt.transpose = NaN;    	%默认使用LM方法
    
    [opt,args] = tb_optparse(opt, varargin);	%输入参数传递
    
    if opt.search    				%如果为true，执行，随机选取迭代初值
        % randomised search for a starting point
        
        opt.search = false;         %关闭搜索初值
        opt.quiet = true;           %保持安静
        %args = args{2:end};
        
        for k=1:opt.slimit          %循环到最大尝试次数
            for j=1:n
                qlim = robot.links(j).qlim;     %传递机器人关节变量的范围
                if isempty(qlim)    			%是否为空集
                    if robot.links(j).isrevolute    %是否为旋转关节
                        q(j) = rand*2*pi - pi;      %产生-pi到pi的随机初值
                    else
                        error('For a prismatic joint, search requires joint limits');   %对于移动关节，需要定义关节范围
                    end
                else
                    q(j) = rand*(qlim(2)-qlim(1)) + qlim(1);    %产生关节范围内的随机初值
                end
            end
            fprintf('Trying q = %s\n', num2str(q));     %输出“尝试q的值为 ”
            
            q = robot.ikine(tr, q, args{:}, 'setopt', opt);     %以此为初值，计算结果
            if ~isempty(q)
                qt = q;									%如果不为空集，q为所求值
                return;
            end
        end
        error('no solution found, are you sure the point is reachable?');   %找不到解，你确定该点可到达？（尝试完最大尝试次数）
        qt = [];
        return
    end
    
    assert(numel(opt.mask) == 6, 'RTB:ikine:badarg', 'Mask matrix should have 6 elements');     %如果mask没有6个参数，报错
    assert(n >= numel(find(opt.mask)), 'RTB:ikine:badarg', 'Number of robot DOF must be >= the same number of 1s in the mask matrix');      %如果机器人自由度小于mask矩阵的1元素个数，报错
    W = diag(opt.mask);     %W为以mask矩阵为对角线的矩阵
    
    
    qt = zeros(length(TT), n);  % preallocate space for results   为解预分配空间
    tcount = 0;              % total iteration count    初始化总迭代次数
    rejcount = 0;            % rejected step count      初始化持续拒绝的迭代次数
    
    q = opt.q0;     %给迭代初值
    
    failed = false;                     %迭代失败的标签
    revolutes = robot.isrevolute();     %给机器人的关节构型（移动为0或旋转为1，全为旋转为[1 1 1 1 1 1]）
    
    for i=1:length(TT)                  %循环到输入的SE3的个数
        T = TT(i);                      %给其中某个SE3
        lambda = opt.lambda;            %给默认步长

        iterations = 0;                 %初始化迭代次数
        
        if opt.debug                    %是否调试程序，默认不调试，跳 if
            e = tr2delta(robot.fkine(q), T);    %给从初始零位的位姿到输入位姿的对应微分运动，d=(dx, dy, dz, dRx, dRy, dRz)
            fprintf('Initial:  |e|=%g\n', norm(W*e));
        end
        
        while true                              %开始进行迭代
            % update the count and test against iteration limit
            iterations = iterations + 1;        %计数迭代次数
            if iterations > opt.ilimit          %超过迭代最大次数
                if ~opt.quiet                   %quiet值为0，不保持安静，执行
                    warning('ikine: iteration limit %d exceeded (pose %d), final err %g', ...
                        opt.ilimit, i, nm);
                end
                failed = true;
                break                           %迭代失败，并跳出循环
            end
            
            e = tr2delta(robot.fkine(q), T);
            
            % are we there yet
            if norm(W*e) < opt.tol
                break;                          %如果小于容许误差，跳出循环
            end
            
            % compute the Jacobian
            J = jacobe(robot, q);               %给当前形位下的雅各比矩阵
            
            JtJ = J'*W*J;
            
            if ~isnan(opt.transpose)            %是否使用LM方法，进行
                % do the simple Jacobian transpose with constant gain
                dq = opt.transpose * J' * e;
            else
                % do the damped inverse Gauss-Newton with Levenberg-Marquadt
                % 用LM法做阻尼逆高斯牛顿
                dq = inv(JtJ + (lambda + opt.lambdamin) * eye(size(JtJ)) ) * J' * W * e;        %迭代公式
                
                % compute possible new value of   得到新的关节值
                qnew = q + dq';
                
                % and figure out the new error    得到新的误差值
                enew = tr2delta(robot.fkine(qnew), T);
                
                % was it a good update?
                if norm(W*enew) < norm(W*e)			%该步是否成功
                    % step is accepted		
                    if opt.debug                %是否调试程序，默认不调试，跳 if
                        fprintf('ACCEPTED: |e|=%g, |dq|=%g, lambda=%g\n', norm(W*enew), norm(dq), lambda);
                    end
                    q = qnew;
                    e = enew;					%给迭代新值
                    lambda = lambda/2;
                    rejcount = 0;               %持续拒绝的迭代次数置0
                else
                    % step is rejected, increase the damping and retry
                    % 该步被拒绝，增加阻尼并重试
                    if opt.debug                %是否调试程序，默认不调试，跳 if
                        fprintf('rejected: |e|=%g, |dq|=%g, lambda=%g\n', norm(W*enew), norm(dq), lambda);
                    end
                    lambda = lambda*2;
                    rejcount = rejcount + 1;
                    if rejcount > opt.rlimit        %超过最大拒绝次数，进行
                        if ~opt.quiet				%是否保持输出安静，默认保持，跳 else
                            warning('ikine: rejected-step limit %d exceeded (pose %d), final err %g', ...
                                opt.rlimit, i, norm(W*enew));
                        end
                        failed = true;
                        break;                      %迭代失败，跳出循环
                    end
                    continue;                       % try again   修改步长后继续尝试
                end
            end
            
            
            % wrap angles for revolute joints		将旋转关节的关节值移到-pi~pi中
            k = (q > pi) & revolutes;
            q(k) = q(k) - 2*pi;
            
            k = (q < -pi) & revolutes;
            q(k) = q(k) + 2*pi;
            
            nm = norm(W*e);
            
            
        end  % end ikine solution for this pose
        qt(i,:) = q';
        tcount = tcount + iterations;             %总共迭代次数，包括多个SE3值的情况
        if opt.verbose && ~failed                 %是否保持输出详细且迭代成功
            fprintf('%d iterations\n', iterations);
        end
        if failed
            if ~opt.quiet                         %是否失败且不保持安静
                warning('failed to converge: try a different initial value of joint coordinates');      %未能收敛，尝试不同的初值
            end
            qt = [];
        end
    end
    
    
    if opt.verbose && length(TT) > 1              %如果详细且有多个SE3值
        fprintf('TOTAL %d iterations\n', tcount);       %输出总迭代次数
    end      
end
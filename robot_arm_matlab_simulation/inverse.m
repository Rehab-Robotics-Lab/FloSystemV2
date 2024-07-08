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
%%������ˡ������޸ģ�����ĩ��λ�˾������������ؽڽ�
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
% ��������������������ɶȵĻ�����
%
% Options::
% 'ilimit',L        maximum number of iterations (default 500)      ��������
% 'rlimit',L        maximum number of consecutive step rejections (default 100)      ��������ܾ�����
% 'tol',T           final error tolerance (default 1e-10)   �����������
% 'lambda',L        initial value of lambda (default 0.1)   ����
% 'lambdamin',M     minimum allowable value of lambda (default 0)	��������Сֵ
% 'quiet'           be quiet	������ְ���
% 'verbose'         be verbose		���������ϸ
% 'mask',M          mask vector (6x1) that correspond to translation in X, Y and Z, 
%                   and rotation about X, Y and Z respectively.		mask��������ʾ���������ɶ�
% 'q0',Q            initial joint configuration (default all zeros)     �����ĳ�ʼ�ؽ���λ
% 'search'          search over all configurations      ����������λ
% 'slimit',L        maximum number of search attempts (default 100)     �������������Ŀ
% 'transpose',A     use Jacobian transpose with step size A, rather than
%                   Levenberg-Marquadt      ʹ�ò���ΪA���ſɱ�ת�ã�������LM����
%
% Trajectory operation::
%
% In all cases if T is a vector of SE3 objects (1xM) or a homogeneous
% transform sequence (4x4xM) then returns the joint coordinates
% corresponding to each of the transforms in the sequence.  Q is MxN where
% N is the number of robot joints. The initial estimate of Q for each time
% step is taken as the solution from the previous time step.
% ʹ����һ���Ľ���Ϊ��ǰ���ĳ�ʼֵ
%
% Underactuated robots::    Ƿ����������
%
% For the case where the manipulator has fewer than 6 DOF the solution
% space has more dimensions than can be spanned by the manipulator joint
% coordinates.
% Ƿ���������˽�ռ�ά���ȹؽ�����ά���ࣿ
%
% In this case we specify the 'mask' option where the mask
% vector (1x6) specifies the Cartesian DOF (in the wrist coordinate
% frame) that will be ignored in reaching a solution.  The mask vector
% has six elements that correspond to translation in X, Y and Z, and rotation
% about X, Y and Z respectively.  The value should be 0 (for ignore) or 1.
% The number of non-zero elements should equal the number of manipulator DOF.
% ʹ�á�mask��ʸ��ָ��ʧȥ�����ɶȣ����������ɶȵ��ڸ�ʸ���ķ���Ԫ�صĸ�����
%
% For example when using a 3 DOF manipulator rotation orientation might be
% unimportant in which case use the option: 'mask', [1 1 1 0 0 0].
% �ٸ����ӣ���ʹ�������ɶȻ�е��ʱ����ת������ܲ���Ҫ����Ӱ�����˶�ѧ��⣩��mask��������Ϊ[1 1 1 0 0 0]
%
% For robots with 4 or 5 DOF this method is very difficult to use since
% orientation is specified by T in world coordinates and the achievable
% orientations are a function of the tool position.
% ����4��5�����ɶȵĻ����ˣ����ַ�������ʹ��
%
% References::
% - Robotics, Vision & Control, P. Corke, Springer 2011, Section 8.4.
%
% Notes::
% - This has been completely reimplemented in RTB 9.11
% - Does NOT require MATLAB Optimization Toolbox.   ����Ҫmatlab�Ż�������
% - Solution is computed iteratively.   ���õ����ķ���
% - Implements a Levenberg-Marquadt variable step size solver.
%   ͨ��LM�䲽�������ʵ��
% - The tolerance is computed on the norm of the error between current
%   and desired tool pose.  This norm is computed from distances
%   and angles without any kind of weighting.
%   ����Ǹ��ݵ�ǰ������̬����������⣩��̬�ķ�������
% - The inverse kinematic solution is generally not unique, and
%   depends on the initial guess Q0 (defaults to 0).
%   ����ֵ��Ψһ�������ֵ�йأ���ֵQ0Ĭ��Ϊ0
% - The default value of Q0 is zero which is a poor choice for most
%   manipulators (eg. puma560, twolink) since it corresponds to a kinematic
%   singularity.
%   Q0����Ϊ[0 0 0 0 0 0]������ڲ������ˣ�puma560��twolink�����Ǻ�ѡ����Ϊ���Ӧ�˶�ѧ���
% - Such a solution is completely general, though much less efficient
%   than specific inverse kinematic solutions derived symbolically, like
%   ikine6s or ikine3.
% 	����ͨ�õĽⷨ������Ч�ʲ���
% - This approach allows a solution to be obtained at a singularity, but
%   the joint angles within the null space are arbitrarily assigned.
% 	�˷�������������������
% - Joint offsets, if defined, are added to the inverse kinematics to
%   generate Q.
% 	��������˹ؽ�ƫ�ƣ�����ӵ����˶�ѧ��������Q
% - Joint limits are not considered in this solution.
%�� �����ǹؽڵķ�Χ����
% - The 'search' option peforms a brute-force search with initial conditions
%   chosen from the entire configuration space.
% 	��search��ѡ���γ�һ��ǿ����������ʼ�����������ؽڿռ������ѡ��
% - If the 'search' option is used any prismatic joint must have joint
%   limits defined.
% 	���ʹ�á�������ѡ����κ��ƶ��ؽڶ����붨��ؽڷ�Χ
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
%��ֵ��
theta_1_1 = robot.ikine(T1,'mask',[1 1 1 1 0 0])


function qt = ikine(robot, tr, varargin)
    
    n = robot.n;        	%�ؽڱ����ĸ���
    
    TT = SE3.check(tr);     %ת��ΪSE3����
        
    %  set default parameters for solution   Ĭ�ϲ�������
    opt.ilimit = 500;   	%Ĭ�ϵ�������
    opt.rlimit = 100;   	%��������ܾ�����
    opt.slimit = 100;   	%����Դ���
    opt.tol = 1e-10;    	%Ĭ�ϵ������
    opt.lambda = 0.1;  		%Ĭ�ϲ���
    opt.lambdamin = 0;  	%Ĭ�ϲ�����Сֵ
    opt.search = false; 	%Ĭ�Ϲر�������ֵ
    opt.quiet = false;  	%���ְ������������
    opt.verbose = false;        %�������Ϣ��ϸ
    opt.mask = [1 1 1 1 1 1];   %Ĭ�������ɶ�
    opt.q0 = zeros(1, n);   	%��ʼ�ؽ���λΪ��λ
    opt.transpose = NaN;    	%Ĭ��ʹ��LM����
    
    [opt,args] = tb_optparse(opt, varargin);	%�����������
    
    if opt.search    				%���Ϊtrue��ִ�У����ѡȡ������ֵ
        % randomised search for a starting point
        
        opt.search = false;         %�ر�������ֵ
        opt.quiet = true;           %���ְ���
        %args = args{2:end};
        
        for k=1:opt.slimit          %ѭ��������Դ���
            for j=1:n
                qlim = robot.links(j).qlim;     %���ݻ����˹ؽڱ����ķ�Χ
                if isempty(qlim)    			%�Ƿ�Ϊ�ռ�
                    if robot.links(j).isrevolute    %�Ƿ�Ϊ��ת�ؽ�
                        q(j) = rand*2*pi - pi;      %����-pi��pi�������ֵ
                    else
                        error('For a prismatic joint, search requires joint limits');   %�����ƶ��ؽڣ���Ҫ����ؽڷ�Χ
                    end
                else
                    q(j) = rand*(qlim(2)-qlim(1)) + qlim(1);    %�����ؽڷ�Χ�ڵ������ֵ
                end
            end
            fprintf('Trying q = %s\n', num2str(q));     %���������q��ֵΪ ��
            
            q = robot.ikine(tr, q, args{:}, 'setopt', opt);     %�Դ�Ϊ��ֵ��������
            if ~isempty(q)
                qt = q;									%�����Ϊ�ռ���qΪ����ֵ
                return;
            end
        end
        error('no solution found, are you sure the point is reachable?');   %�Ҳ����⣬��ȷ���õ�ɵ��������������Դ�����
        qt = [];
        return
    end
    
    assert(numel(opt.mask) == 6, 'RTB:ikine:badarg', 'Mask matrix should have 6 elements');     %���maskû��6������������
    assert(n >= numel(find(opt.mask)), 'RTB:ikine:badarg', 'Number of robot DOF must be >= the same number of 1s in the mask matrix');      %������������ɶ�С��mask�����1Ԫ�ظ���������
    W = diag(opt.mask);     %WΪ��mask����Ϊ�Խ��ߵľ���
    
    
    qt = zeros(length(TT), n);  % preallocate space for results   Ϊ��Ԥ����ռ�
    tcount = 0;              % total iteration count    ��ʼ���ܵ�������
    rejcount = 0;            % rejected step count      ��ʼ�������ܾ��ĵ�������
    
    q = opt.q0;     %��������ֵ
    
    failed = false;                     %����ʧ�ܵı�ǩ
    revolutes = robot.isrevolute();     %�������˵Ĺؽڹ��ͣ��ƶ�Ϊ0����תΪ1��ȫΪ��תΪ[1 1 1 1 1 1]��
    
    for i=1:length(TT)                  %ѭ���������SE3�ĸ���
        T = TT(i);                      %������ĳ��SE3
        lambda = opt.lambda;            %��Ĭ�ϲ���

        iterations = 0;                 %��ʼ����������
        
        if opt.debug                    %�Ƿ���Գ���Ĭ�ϲ����ԣ��� if
            e = tr2delta(robot.fkine(q), T);    %���ӳ�ʼ��λ��λ�˵�����λ�˵Ķ�Ӧ΢���˶���d=(dx, dy, dz, dRx, dRy, dRz)
            fprintf('Initial:  |e|=%g\n', norm(W*e));
        end
        
        while true                              %��ʼ���е���
            % update the count and test against iteration limit
            iterations = iterations + 1;        %������������
            if iterations > opt.ilimit          %��������������
                if ~opt.quiet                   %quietֵΪ0�������ְ�����ִ��
                    warning('ikine: iteration limit %d exceeded (pose %d), final err %g', ...
                        opt.ilimit, i, nm);
                end
                failed = true;
                break                           %����ʧ�ܣ�������ѭ��
            end
            
            e = tr2delta(robot.fkine(q), T);
            
            % are we there yet
            if norm(W*e) < opt.tol
                break;                          %���С������������ѭ��
            end
            
            % compute the Jacobian
            J = jacobe(robot, q);               %����ǰ��λ�µ��Ÿ��Ⱦ���
            
            JtJ = J'*W*J;
            
            if ~isnan(opt.transpose)            %�Ƿ�ʹ��LM����������
                % do the simple Jacobian transpose with constant gain
                dq = opt.transpose * J' * e;
            else
                % do the damped inverse Gauss-Newton with Levenberg-Marquadt
                % ��LM�����������˹ţ��
                dq = inv(JtJ + (lambda + opt.lambdamin) * eye(size(JtJ)) ) * J' * W * e;        %������ʽ
                
                % compute possible new value of   �õ��µĹؽ�ֵ
                qnew = q + dq';
                
                % and figure out the new error    �õ��µ����ֵ
                enew = tr2delta(robot.fkine(qnew), T);
                
                % was it a good update?
                if norm(W*enew) < norm(W*e)			%�ò��Ƿ�ɹ�
                    % step is accepted		
                    if opt.debug                %�Ƿ���Գ���Ĭ�ϲ����ԣ��� if
                        fprintf('ACCEPTED: |e|=%g, |dq|=%g, lambda=%g\n', norm(W*enew), norm(dq), lambda);
                    end
                    q = qnew;
                    e = enew;					%��������ֵ
                    lambda = lambda/2;
                    rejcount = 0;               %�����ܾ��ĵ���������0
                else
                    % step is rejected, increase the damping and retry
                    % �ò����ܾ����������Ტ����
                    if opt.debug                %�Ƿ���Գ���Ĭ�ϲ����ԣ��� if
                        fprintf('rejected: |e|=%g, |dq|=%g, lambda=%g\n', norm(W*enew), norm(dq), lambda);
                    end
                    lambda = lambda*2;
                    rejcount = rejcount + 1;
                    if rejcount > opt.rlimit        %�������ܾ�����������
                        if ~opt.quiet				%�Ƿ񱣳����������Ĭ�ϱ��֣��� else
                            warning('ikine: rejected-step limit %d exceeded (pose %d), final err %g', ...
                                opt.rlimit, i, norm(W*enew));
                        end
                        failed = true;
                        break;                      %����ʧ�ܣ�����ѭ��
                    end
                    continue;                       % try again   �޸Ĳ������������
                end
            end
            
            
            % wrap angles for revolute joints		����ת�ؽڵĹؽ�ֵ�Ƶ�-pi~pi��
            k = (q > pi) & revolutes;
            q(k) = q(k) - 2*pi;
            
            k = (q < -pi) & revolutes;
            q(k) = q(k) + 2*pi;
            
            nm = norm(W*e);
            
            
        end  % end ikine solution for this pose
        qt(i,:) = q';
        tcount = tcount + iterations;             %�ܹ������������������SE3ֵ�����
        if opt.verbose && ~failed                 %�Ƿ񱣳������ϸ�ҵ����ɹ�
            fprintf('%d iterations\n', iterations);
        end
        if failed
            if ~opt.quiet                         %�Ƿ�ʧ���Ҳ����ְ���
                warning('failed to converge: try a different initial value of joint coordinates');      %δ�����������Բ�ͬ�ĳ�ֵ
            end
            qt = [];
        end
    end
    
    
    if opt.verbose && length(TT) > 1              %�����ϸ���ж��SE3ֵ
        fprintf('TOTAL %d iterations\n', tcount);       %����ܵ�������
    end      
end
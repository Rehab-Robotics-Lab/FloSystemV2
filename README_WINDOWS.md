# 在 Windows 上运行 FLO v2 ROS 环境

## 前提条件

### 1. 安装 Docker Desktop
- 下载：https://www.docker.com/products/docker-desktop/
- 安装后重启电脑
- 确保 Docker 正在运行（系统托盘有鲸鱼图标）

### 2. 安装 VcXsrv (Windows X Server)
- 下载：https://sourceforge.net/projects/vcxsrv/
- 安装后启动 XLaunch，配置：
  - **Multiple windows**
  - **Start no client**
  - **禁用 Native opengl**（重要！）
  - **勾选 Disable access control**（重要！）
- 保存配置到桌面，以后双击启动

### 3. 克隆/复制代码到 Windows
```powershell
# 在 PowerShell 中
cd C:\Users\YourName\Documents
git clone <your-repo-url>
cd FloSystemV2/gazebo_simulation_and_control
```

## 快速开始

### 方法1：仅可视化演示（推荐 Windows 用户）

1. **启动 VcXsrv**（双击桌面的配置文件）

2. **打开 PowerShell**（以管理员身份）
```powershell
cd C:\path\to\FloSystemV2\gazebo_simulation_and_control
.\run_docker_windows.ps1
```

3. **容器启动后，运行演示**
```bash
# 在容器内
chmod +x /catkin_ws/run_demo_in_container.sh
/catkin_ws/run_demo_in_container.sh
```

4. **RViz 窗口应该会弹出**
   - 如果没有，检查 VcXsrv 是否在运行
   - 在容器内测试：`xclock` 或 `rviz`

5. **发送测试命令**（在容器的 tmux shell 窗口）
```bash
# 切换到 shell 窗口（Ctrl+B 然后按 3）
rostopic pub /ros/mqtt/movement std_msgs/String "1"  # 右臂挥手
```

### 方法2：带硬件控制（需要 WSL2 + USB 直通）

⚠️ **警告**：Windows Docker Desktop 原生不支持 USB 设备。需要 WSL2。

#### 安装 WSL2 + usbipd

1. **启用 WSL2**
```powershell
# PowerShell（管理员）
wsl --install
wsl --set-default-version 2
# 重启电脑
```

2. **安装 Ubuntu（WSL2）**
```powershell
wsl --install -d Ubuntu-22.04
```

3. **安装 usbipd-win**
- 下载：https://github.com/dorssel/usbipd-win/releases
- 安装 MSI 包

4. **绑定 USB 设备**
```powershell
# PowerShell（管理员）
# 列出设备
usbipd list

# 绑定你的 Dynamixel U2D2（找到对应的 BUSID，例如 1-4）
usbipd bind --busid 1-4

# 附加到 WSL
usbipd attach --wsl --busid 1-4
```

5. **在 WSL2 中运行 Docker**
```bash
# 在 WSL2 Ubuntu 终端
cd /mnt/c/path/to/FloSystemV2/gazebo_simulation_and_control
./run_docker.sh  # 使用原来的 Linux 脚本
```

## 故障排查

### RViz/Gazebo 不显示
1. 确认 VcXsrv 正在运行（系统托盘有 X 图标）
2. 在容器内测试：
   ```bash
   echo $DISPLAY  # 应该显示 host.docker.internal:0
   xclock  # 简单的测试窗口
   ```
3. 重启 VcXsrv，确保禁用了"Native opengl"

### Docker 构建失败
- 确保网络连接正常
- 如果在中国，考虑使用 Docker 镜像加速：
  ```json
  // Docker Desktop -> Settings -> Docker Engine
  {
    "registry-mirrors": ["https://docker.mirrors.ustc.edu.cn"]
  }
  ```

### 容器无法启动
- 检查 Docker Desktop 是否在运行
- 确保没有端口冲突（11311, 1883）：
  ```powershell
  netstat -ano | findstr "11311"
  ```

### USB 设备在 WSL2 中找不到
```bash
# 在 WSL2 中
ls /dev/ttyUSB*  # 应该看到 /dev/ttyUSB0
# 如果没有，在 Windows PowerShell 中重新 attach:
# usbipd attach --wsl --busid <BUSID>
```

## 限制说明

### Windows Docker Desktop 的限制
- ❌ 无原生 USB 设备支持（需要 WSL2 + usbipd）
- ❌ `--network host` 无效（需显式端口映射）
- ❌ `/dev/video*` 摄像头访问受限
- ✅ X11 GUI 可用（通过 VcXsrv）
- ✅ 仿真/可视化完全支持

### 推荐使用场景
- **Windows**: 仅可视化、规划、RViz/Gazebo 演示
- **WSL2**: 完整功能（硬件 + 可视化）
- **Linux 原生**: 最佳性能（推荐用于生产）

## 网络配置（高级）

### 分布式 ROS（Windows Docker + Linux 硬件）

1. **Linux 主机运行硬件节点**
```bash
# 在 Linux 机器上
export ROS_MASTER_URI=http://192.168.1.100:11311  # Linux IP
export ROS_IP=192.168.1.100
rosrun flo_humanoid read_write_arms_node
```

2. **Windows Docker 运行 MoveIt**
```powershell
# 修改 run_docker_windows.ps1，添加环境变量：
-e ROS_MASTER_URI=http://192.168.1.100:11311 `
-e ROS_IP=172.17.0.2 `  # 容器 IP，用 docker inspect 查看
```

3. **测试连接**
```bash
# 在容器内
rostopic list  # 应该能看到 Linux 主机的话题
```

## 常用命令

### 进入运行中的容器
```powershell
docker exec -it flo_v2_container bash
```

### 查看日志
```bash
# 在容器内
roscd && cd ../log
tail -f latest/roslaunch-*.log
```

### 停止所有
```powershell
docker stop flo_v2_container
```

## 下一步

- 阅读主 README.md 了解动作编号
- 查看 `flo_core/scripts/main_controller_clean.py` 了解控制逻辑
- 使用 `rostopic pub` 手动测试动作

## 支持

如有问题，请检查：
1. Docker Desktop 日志
2. VcXsrv 日志（`%TEMP%\VcXsrv.log`）
3. 容器内 ROS 日志（`~/.ros/log/latest/`）


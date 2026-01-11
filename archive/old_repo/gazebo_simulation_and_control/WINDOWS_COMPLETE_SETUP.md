# 在一台 Windows PC 上完整运行 FLO v2（包括硬件控制）

## 总体方案：WSL2 + Docker + USB 直通

这个方案让你在 Windows 上获得**完整的 Linux 环境**，可以控制真实机器人。

---

## 第一步：安装 WSL2

### 1.1 启用 WSL2（PowerShell 管理员）

```powershell
# 启用 WSL 和虚拟机平台
wsl --install

# 如果上面命令不工作，手动启用：
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
```

**重启电脑**

### 1.2 设置 WSL2 为默认版本

```powershell
wsl --set-default-version 2
```

### 1.3 安装 Ubuntu

```powershell
# 安装 Ubuntu 22.04
wsl --install -d Ubuntu-22.04

# 首次启动会要求创建用户名和密码
```

### 1.4 验证安装

```powershell
wsl --list --verbose
# 应该看到 Ubuntu-22.04 (VERSION 2)
```

---

## 第二步：安装 Docker Desktop

### 2.1 下载并安装

- 下载：https://www.docker.com/products/docker-desktop/
- 安装时**勾选"Use WSL 2 instead of Hyper-V"**

### 2.2 配置 Docker Desktop

1. 打开 Docker Desktop
2. Settings → General → 勾选 "Use the WSL 2 based engine"
3. Settings → Resources → WSL Integration → 启用 Ubuntu-22.04
4. Apply & Restart

### 2.3 验证（在 WSL2 Ubuntu 终端）

```bash
docker --version
docker run hello-world
```

---

## 第三步：USB 设备直通（关键！）

### 3.1 安装 usbipd-win（在 Windows 上）

下载并安装：https://github.com/dorssel/usbipd-win/releases

或者用 winget：
```powershell
# PowerShell 管理员
winget install --interactive --exact dorssel.usbipd-win
```

### 3.2 在 WSL2 中安装 USB 工具

```bash
# 在 WSL2 Ubuntu 终端
sudo apt update
sudo apt install linux-tools-generic hwdata
sudo update-alternatives --install /usr/local/bin/usbip usbip /usr/lib/linux-tools/*-generic/usbip 20
```

### 3.3 连接 USB 设备

**每次插入设备后需要执行一次**

```powershell
# PowerShell 管理员

# 1. 列出所有 USB 设备
usbipd list

# 输出示例：
# BUSID  VID:PID    DEVICE
# 1-4    0403:6014  USB Serial Converter  # 这是你的 Dynamixel U2D2
# 2-3    0c45:6366  USB Camera            # 这是你的摄像头

# 2. 绑定设备（只需首次执行）
usbipd bind --busid 1-4   # Dynamixel
usbipd bind --busid 2-3   # 摄像头

# 3. 附加到 WSL2（每次插拔后需要重新执行）
usbipd attach --wsl --busid 1-4
usbipd attach --wsl --busid 2-3
```

### 3.4 验证设备在 WSL2 中可见

```bash
# 在 WSL2 Ubuntu 终端
ls /dev/ttyUSB*    # 应该看到 /dev/ttyUSB0
ls /dev/video*     # 应该看到 /dev/video0

# 检查设备权限
sudo chmod 666 /dev/ttyUSB0
sudo chmod 666 /dev/video0
```

---

## 第四步：在 WSL2 中构建和运行

### 4.1 复制代码到 WSL2

```bash
# 在 WSL2 Ubuntu 终端

# 方法1：从 Windows 文件系统访问（推荐用于开发）
cd /mnt/c/Users/YourName/Documents/FloSystemV2/gazebo_simulation_and_control

# 方法2：直接克隆到 WSL2（推荐用于运行，性能更好）
cd ~
git clone <your-repo-url> FloSystemV2
cd FloSystemV2/gazebo_simulation_and_control
```

### 4.2 安装 VcXsrv（Windows 端，用于显示 GUI）

1. 下载：https://sourceforge.net/projects/vcxsrv/
2. 启动 XLaunch，配置：
   - Multiple windows
   - Start no client
   - **禁用 Native opengl**
   - **勾选 Disable access control**
3. 保存配置到桌面

### 4.3 配置 WSL2 的 DISPLAY

```bash
# 在 WSL2 中，添加到 ~/.bashrc
echo 'export DISPLAY=$(cat /etc/resolv.conf | grep nameserver | awk "{print \$2}"):0' >> ~/.bashrc
source ~/.bashrc

# 测试
echo $DISPLAY  # 应该显示类似 172.x.x.x:0
```

### 4.4 构建 Docker 镜像

```bash
# 在 WSL2 的项目目录中
cd ~/FloSystemV2/gazebo_simulation_and_control
docker build -t flo_v2_image .
```

### 4.5 运行 Docker 容器（带 USB 设备）

创建 WSL2 专用启动脚本：

```bash
# 创建 run_docker_wsl2.sh
cat > run_docker_wsl2.sh << 'EOF'
#!/usr/bin/env bash

# 删除旧容器
docker rm -f flo_v2_container 2>/dev/null || true

# 获取 Windows 主机 IP（用于 X11）
export DISPLAY=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2}'):0

# 运行容器（带 USB 设备和 GUI 支持）
docker run -it --rm \
  --name flo_v2_container \
  --privileged \
  --network host \
  -e DISPLAY=$DISPLAY \
  -e QT_X11_NO_MITSHM=1 \
  -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
  --device=/dev/ttyUSB0:/dev/ttyUSB0 \
  --device=/dev/video0:/dev/video0 \
  flo_v2_image
EOF

chmod +x run_docker_wsl2.sh
```

### 4.6 启动容器

```bash
# 确保 VcXsrv 在 Windows 上已启动！
./run_docker_wsl2.sh
```

### 4.7 在容器内运行完整系统

```bash
# 容器启动后
source /catkin_ws/devel/setup.bash

# 测试 GUI
rviz  # 应该弹出窗口

# 运行完整演示
/catkin_ws/run_demo_in_container.sh
```

---

## 第五步：日常使用工作流

### 每次使用前（必须按顺序）：

1. **启动 VcXsrv**（Windows，双击桌面配置）
2. **连接 USB 设备**（PowerShell 管理员）：
   ```powershell
   usbipd attach --wsl --busid 1-4  # Dynamixel
   usbipd attach --wsl --busid 2-3  # 摄像头（如果需要）
   ```
3. **启动 WSL2**（PowerShell 或 Windows Terminal）：
   ```powershell
   wsl
   ```
4. **在 WSL2 中验证设备**：
   ```bash
   ls /dev/ttyUSB* /dev/video*
   sudo chmod 666 /dev/ttyUSB0 /dev/video0
   ```
5. **运行 Docker**：
   ```bash
   cd ~/FloSystemV2/gazebo_simulation_and_control
   ./run_docker_wsl2.sh
   ```

### 快捷启动脚本（可选）

创建 Windows 批处理文件 `start_flo.bat`：

```batch
@echo off
echo === Starting FLO v2 System ===

echo Step 1: Attaching USB devices...
usbipd attach --wsl --busid 1-4
timeout /t 2

echo Step 2: Starting WSL2...
wsl bash -c "cd ~/FloSystemV2/gazebo_simulation_and_control && ./run_docker_wsl2.sh"
```

---

## 故障排查

### USB 设备找不到

```bash
# 在 WSL2 中
ls /dev/ttyUSB*  # 如果为空

# 在 Windows PowerShell（管理员）重新 attach
usbipd list
usbipd attach --wsl --busid 1-4
```

### GUI 不显示

```bash
# 1. 确认 VcXsrv 在 Windows 上运行
# 2. 在 WSL2 中检查 DISPLAY
echo $DISPLAY  # 应该不为空

# 3. 测试简单窗口
xclock

# 4. 如果还是不行，手动设置 DISPLAY
export DISPLAY=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2}'):0
```

### 权限错误（/dev/ttyUSB0）

```bash
# 在 WSL2 中
sudo chmod 666 /dev/ttyUSB0
sudo usermod -a -G dialout $USER
```

### Docker 网络问题

```bash
# 如果 --network host 不工作，改用端口映射：
docker run -it \
  -p 11311:11311 \
  -p 1883:1883 \
  --device=/dev/ttyUSB0 \
  ...
```

### 性能问题

- **不要**从 `/mnt/c/` 运行（慢）
- **推荐**：将代码克隆到 WSL2 原生文件系统（`~/FloSystemV2`）

---

## 性能对比

| 方案 | GUI | 硬件 | 性能 | 难度 |
|------|-----|------|------|------|
| Windows Docker 原生 | ✅ | ❌ | ⭐⭐ | ⭐ |
| WSL2 + Docker（本方案） | ✅ | ✅ | ⭐⭐⭐⭐ | ⭐⭐ |
| Linux 双系统 | ✅ | ✅ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |

---

## 下一步

安装完成后，参考主 README.md：
- 了解动作编号和控制逻辑
- 测试 AprilTag 检测
- 运行完整的抓取演示

## 支持

如有问题：
1. 检查 WSL2 版本：`wsl --list --verbose`
2. 检查 Docker 集成：Docker Desktop → Settings → Resources → WSL Integration
3. 查看日志：`~/.ros/log/latest/`


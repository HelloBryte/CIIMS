# Campus Intelligent Inventory Management System (CIIMS)

校园智能物品管理系统

## 项目简介

CIIMS 是一个基于 PySide6 和 MySQL 的校园物品管理系统，采用 Apple 风格 UI 设计，支持人脸识别登录、物品借还管理、用户管理等功能。

## 功能特性

- 🔐 **多种登录方式**：密码登录、人脸识别登录
- 👤 **用户管理**：用户注册、角色管理（管理员/普通用户）、个人资料设置
- 📦 **物品管理**：物品添加、编辑、删除、库存管理，MySQL支持
- 📚 **借还管理**：物品借阅、归还、借阅记录查询、逾期提醒
- 🎭 **人脸识别**：人脸注册、人脸识别登录、模型自动训练、再训练（可调节模型参数）
- 🎨 **现代化 UI**：Apple 风格设计，简洁优雅的用户界面

## 快速开始

### 1. 环境要求

- Python 3.8+
- MySQL 5.7+ 或 MySQL 8.0+

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

**重要**：确保安装的是 `opencv-contrib-python` 而不是 `opencv-python`。

如果已安装 `opencv-python`，请先卸载：

```bash
pip uninstall opencv-python
pip install opencv-contrib-python==4.10.0.84
```

### 3. 配置数据库

#### 3.1 启动 MySQL

确保 MySQL 服务正在运行。

#### 3.2 创建配置文件

```bash
cp .env.example .env
```

编辑 `.env` 文件，**必须修改**数据库密码：

```env
DB_PASSWORD=你的MySQL密码  # 改为你的实际密码
```

其他配置可以保持默认。

### 4. 初始化数据库

```bash
python database/init_db.py
```

这个脚本会自动创建数据库和所有必需的表。

**默认管理员账户：**
- 用户名: `admin`
- 密码: `admin123`

**⚠️ 首次登录后请立即修改管理员密码！**

### 5. 运行应用

```bash
python main.py
```

## 使用说明

### 首次使用

1. 使用管理员账户登录（admin/admin123）
2. 在个人设置中修改管理员密码
3. 注册新用户或添加物品
4. 进行人脸注册（需要摄像头权限）

### 主要功能

- **登录窗口**: 支持密码登录、人脸识别登录、新用户注册
- **物品管理**: 添加、编辑、删除物品，查看库存
- **借还管理**: 借阅物品、归还物品、查看借阅记录
- **用户管理**: 查看用户列表、编辑用户、删除用户（仅管理员）
- **个人设置**: 修改密码、更新电话号码、更新人脸识别数据

## 常见问题

### MySQL 连接失败

- 确认 MySQL 服务正在运行
- 检查 `.env` 文件中的用户名和密码是否正确
- 测试命令行连接: `mysql -h localhost -u root -p`

### OpenCV 错误

如果遇到 `ModuleNotFoundError: No module named 'cv2.face'`：

```bash
pip uninstall opencv-python
pip install opencv-contrib-python==4.10.0.84
```

### macOS 摄像头权限

1. 打开 **系统设置** > **隐私与安全性** > **摄像头**
2. 找到你使用的应用（PyCharm、Cursor 或 Terminal）并打开开关
3. 重新运行应用

## 项目结构

```
CIIMS/
├── main.py                 # 应用程序入口
├── config.py              # 配置文件
├── requirements.txt       # Python 依赖包列表
├── database/              # 数据库相关模块
├── ui/                    # 用户界面模块
├── face_recognition/      # 人脸识别模块
├── utils/                 # 工具模块
└── scripts/               # 脚本文件
```

## 需要帮助？

如果遇到问题：
1. 检查 Python 版本是否为 3.8+
2. 检查 MySQL 版本是否为 5.7+
3. 确认所有依赖已正确安装
4. 确认 `.env` 文件配置正确
5. 查看 `logs/` 目录中的日志文件

如果还有问题，可以：
- 向我求助
- 使用 AI 工具（如 ChatGPT、Claude）询问

## 技术栈

- **GUI框架**: PySide6 (Qt for Python)
- **数据库**: MySQL
- **人脸识别**: OpenCV (opencv-contrib-python)
- **密码加密**: bcrypt

# Campus Intelligent Inventory Management System (CIIMS) / 校园智能物品管理系统

## About / 项目简介

CIIMS is a campus item management system based on PySide6 and MySQL, featuring Apple-style UI design, supporting face recognition login, item borrowing/returning management, user management, and more.

CIIMS 是一个基于 PySide6 和 MySQL 的校园物品管理系统，采用 Apple 风格 UI 设计，支持人脸识别登录、物品借还管理、用户管理等功能。

## Features / 功能特性

- 🔐 **Multiple Login Methods / 多种登录方式**: Password login, face recognition login / 密码登录、人脸识别登录
- 👤 **User Management / 用户管理**: User registration, role management (admin/regular user), profile settings / 用户注册、角色管理（管理员/普通用户）、个人资料设置
- 📦 **Item Management / 物品管理**: Add, edit, delete items, inventory management with MySQL support / 物品添加、编辑、删除、库存管理，MySQL支持
- 📚 **Borrowing Management / 借还管理**: Item borrowing, returning, borrowing record queries, overdue reminders / 物品借阅、归还、借阅记录查询、逾期提醒
- 🎭 **Face Recognition / 人脸识别**: Face registration, face recognition login, automatic model training, retraining (adjustable model parameters) / 人脸注册、人脸识别登录、模型自动训练、再训练（可调节模型参数）
- 🎨 **Modern UI / 现代化 UI**: Apple-style design, clean and elegant user interface / Apple 风格设计，简洁优雅的用户界面

## Quick Start / 快速开始

### 1. Requirements / 环境要求

- Python 3.8+
- MySQL 5.7+ or MySQL 8.0+ / MySQL 5.7+ 或 MySQL 8.0+

### 2. Install Dependencies / 安装依赖

```bash
pip install -r requirements.txt
```

**Important / 重要**: Make sure to install `opencv-contrib-python` instead of `opencv-python`. / 确保安装的是 `opencv-contrib-python` 而不是 `opencv-python`。

If you have already installed `opencv-python`, please uninstall it first: / 如果已安装 `opencv-python`，请先卸载：

```bash
pip uninstall opencv-python
pip install opencv-contrib-python==4.10.0.84
```

### 3. Configure Database / 配置数据库

#### 3.1 Start MySQL / 启动 MySQL

Make sure the MySQL service is running. / 确保 MySQL 服务正在运行。

#### 3.2 Create Configuration File / 创建配置文件

```bash
cp .env.example .env
```

Edit the `.env` file and **must modify** the database password: / 编辑 `.env` 文件，**必须修改**数据库密码：

```env
DB_PASSWORD=your_mysql_password  # Change to your actual password / 改为你的实际密码
```

Other configurations can remain default. / 其他配置可以保持默认。

### 4. Initialize Database / 初始化数据库

```bash
python database/init_db.py
```

This script will automatically create the database and all required tables. / 这个脚本会自动创建数据库和所有必需的表。

**Default Admin Account / 默认管理员账户:**
- Username / 用户名: `admin`
- Password / 密码: `admin123`

**⚠️ Please change the admin password immediately after first login! / 首次登录后请立即修改管理员密码！**

### 5. Run Application / 运行应用

```bash
python main.py
```

## Usage / 使用说明

### First Time Use / 首次使用

1. Login with admin account (admin/admin123) / 使用管理员账户登录（admin/admin123）
2. Change admin password in profile settings / 在个人设置中修改管理员密码
3. Register new users or add items / 注册新用户或添加物品
4. Perform face registration (requires camera permission) / 进行人脸注册（需要摄像头权限）

### Main Features / 主要功能

- **Login Window / 登录窗口**: Supports password login, face recognition login, new user registration / 支持密码登录、人脸识别登录、新用户注册
- **Item Management / 物品管理**: Add, edit, delete items, view inventory / 添加、编辑、删除物品，查看库存
- **Borrowing Management / 借还管理**: Borrow items, return items, view borrowing records / 借阅物品、归还物品、查看借阅记录
- **User Management / 用户管理**: View user list, edit users, delete users (admin only) / 查看用户列表、编辑用户、删除用户（仅管理员）
- **Profile Settings / 个人设置**: Change password, update phone number, update face recognition data / 修改密码、更新电话号码、更新人脸识别数据

## FAQ / 常见问题

### MySQL Connection Failed / MySQL 连接失败

- Confirm MySQL service is running / 确认 MySQL 服务正在运行
- Check if username and password in `.env` file are correct / 检查 `.env` 文件中的用户名和密码是否正确
- Test command line connection: `mysql -h localhost -u root -p` / 测试命令行连接: `mysql -h localhost -u root -p`

### OpenCV Error / OpenCV 错误

If you encounter `ModuleNotFoundError: No module named 'cv2.face'`: / 如果遇到 `ModuleNotFoundError: No module named 'cv2.face'`：

```bash
pip uninstall opencv-python
pip install opencv-contrib-python==4.10.0.84
```

### macOS Camera Permission / macOS 摄像头权限

1. Open **System Settings** > **Privacy & Security** > **Camera** / 打开 **系统设置** > **隐私与安全性** > **摄像头**
2. Find the application you're using (PyCharm, Cursor, or Terminal) and turn on the switch / 找到你使用的应用（PyCharm、Cursor 或 Terminal）并打开开关
3. Restart the application / 重新运行应用

## Project Structure / 项目结构

```
CIIMS/
├── main.py                 # Application entry point / 应用程序入口
├── config.py              # Configuration file / 配置文件
├── requirements.txt       # Python dependencies list / Python 依赖包列表
├── database/              # Database related modules / 数据库相关模块
├── ui/                    # User interface modules / 用户界面模块
├── face_recognition/      # Face recognition modules / 人脸识别模块
├── utils/                 # Utility modules / 工具模块
└── scripts/               # Script files / 脚本文件
```

## Need Help? / 需要帮助？

If you encounter problems: / 如果遇到问题：
1. Check if Python version is 3.8+ / 检查 Python 版本是否为 3.8+
2. Check if MySQL version is 5.7+ / 检查 MySQL 版本是否为 5.7+
3. Confirm all dependencies are correctly installed / 确认所有依赖已正确安装
4. Confirm `.env` file is configured correctly / 确认 `.env` 文件配置正确
5. Check log files in `logs/` directory / 查看 `logs/` 目录中的日志文件

If you still have problems, you can: / 如果还有问题，可以：
- Ask me for help / 向我求助
- Use AI tools (such as ChatGPT, Claude) to ask / 使用 AI 工具（如 ChatGPT、Claude）询问

## Tech Stack / 技术栈

- **GUI Framework / GUI框架**: PySide6 (Qt for Python)
- **Database / 数据库**: MySQL
- **Face Recognition / 人脸识别**: OpenCV (opencv-contrib-python)
- **Password Encryption / 密码加密**: bcrypt

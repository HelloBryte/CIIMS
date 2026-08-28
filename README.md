# CIIMS - Campus Intelligent Inventory Management System

## English

CIIMS is a desktop application for campus inventory management with an optional embedded AI assistant. Built with PySide6 and MySQL, it provides a modern interface for managing items, borrowing operations, and user accounts.

### Features

- 🔐 **Secure Authentication**: Password-based login with optional face recognition
- 📦 **Inventory Management**: Add, edit, and track items with stock monitoring
- 🔄 **Borrow/Return Operations**: Complete borrowing lifecycle with overdue tracking
- 👥 **User Management**: Admin controls for user accounts and permissions
- 🤖 **AI Assistant**: Optional multilingual support (English/Chinese) with intelligent query capabilities
- 🎨 **Modern UI**: Apple-inspired interface design

### AI Assistant Features (Optional)

- **Intent Classification**: Automatically routes queries to general Q&A or database operations
- **Fuzzy Search**: Semantic matching for natural language queries
- **Multilingual Support**: Responds in the same language as user input
- **SQL Generation**: Safe, validated database query generation with RBAC enforcement

### Technology Stack

- **Frontend**: PySide6 (Qt6 Python bindings)
- **Backend**: Python 3.9+
- **Database**: MySQL 8.0
- **Face Recognition**: OpenCV with LBPH algorithm (optional)
- **AI Integration**: OpenRouter-compatible API support (optional)

### Installation

1. Clone the repository
```bash
git clone https://github.com/your-username/ciims.git
cd ciims
```

2. Create virtual environment
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Configuration
```bash
# config.py already ships with safe, environment-driven defaults.
# Optionally create a .env file (see below) to override database and
# API settings without editing config.py directly.
```

5. Database setup
```bash
# Create MySQL database named 'campus_system'
python database/init_db.py
python scripts/generate_sample_items.py
```
**Note**: The database initialization creates a default admin account:
- Username: `admin`
- Password: `admin123`

Please change this password after first login for security.

6. Run the application
```bash
python main.py
```

### Configuration

`config.py` already reads every setting from an environment variable with a
sensible default, so the app runs out of the box. To override any value,
create a `.env` file in the project root (see `config.example.py` for the
full list of supported variables):
```env
# Database
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_DATABASE=campus_system

# Face recognition configuration (optional - module not bundled, see note below)
FACE_RECOGNITION_MODEL_PATH=model/trainer.yml
FACE_RECOGNITION_HAAR_CASCADE_PATH=haarcascade_frontalface_default.xml
FACE_RECOGNITION_CONFIDENCE_THRESHOLD=50
FACE_RECOGNITION_PREDICTION_THRESHOLD=70

# AI Assistant configuration (optional)
OPENROUTER_API_KEY=your_api_key_here
OPENROUTER_MODEL=deepseek/deepseek-chat
CIIMS_PROXY_URL=http://127.0.0.1:7897
```

**Note**: The face recognition capture/training module (`face_recognition/`)
is not bundled in this repository. The login, registration, and profile
screens detect its absence automatically and disable the face-recognition
UI elements; password-based authentication always works normally.

### Project Structure

```
ciims/
├── ui/                    # User interface components
│   ├── screens/          # Main application windows
│   ├── dialogs/          # Dialog windows
│   └── base/             # Base UI components and styles
├── utils/                 # Utility modules
├── database/             # Database configuration and helpers
├── scripts/              # Utility scripts (sample data generation, etc.)
├── tests/                # Unit tests (pytest, no DB required)
├── config.py             # Runtime configuration (env-driven, no secrets)
├── config.example.py     # Reference/documentation for all config options
└── main.py               # Application entry point
```

### Testing

Unit tests cover the pure-logic modules (currently the AI assistant's SQL
guardrails in `utils/assistant_data.py`) and don't require a MySQL
connection. Install the dev extras and run:
```bash
pip install -r requirements-dev.txt
pytest
```

**Note**: `face_recognition/`, `model/`, and `dataset/` are optional
directories for the (not bundled) face recognition module; they are not
part of the tracked repository structure. See the Configuration section
above.

### License

This project is licensed under the MIT License.

---

## 中文

CIIMS 是一个校园物资智能管理系统桌面应用，可选内置 AI 助手。使用 PySide6 和 MySQL 构建，提供现代化界面用于管理物资、借还操作和用户账户。

### 功能特点

- 🔐 **安全认证**：密码登录，可选人脸识别
- 📦 **物资管理**：添加、编辑、追踪物资，库存监控
- 🔄 **借还操作**：完整的借还流程，逾期追踪
- 👥 **用户管理**：管理员控制用户账户和权限
- 🤖 **AI 助手**：可选的多语言支持（中英文），智能查询
- 🎨 **现代界面**：苹果风格的界面设计

### AI 助手功能（可选）

- **意图分类**：自动路由查询到通用问答或数据库操作
- **模糊搜索**：自然语言查询的语义匹配
- **多语言支持**：根据用户输入语言回复
- **SQL 生成**：安全、经过验证的数据库查询生成，带 RBAC 权限控制

### 技术栈

- **前端**：PySide6（Qt6 Python 绑定）
- **后端**：Python 3.9+
- **数据库**：MySQL 8.0
- **人脸识别**：OpenCV LBPH 算法（可选）
- **AI 集成**：OpenRouter 兼容 API（可选）

### 安装步骤

1. 克隆仓库
```bash
git clone https://github.com/your-username/ciims.git
cd ciims
```

2. 创建虚拟环境
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

3. 安装依赖
```bash
pip install -r requirements.txt
```

4. 配置
```bash
# config.py 已内置基于环境变量的安全默认值，开箱即用。
# 如需覆盖数据库或 API 设置，可创建 .env 文件（变量说明参见英文部分的
# Configuration 小节，或直接查看 config.example.py）。
```

5. 数据库设置
```bash
# 创建名为 'campus_system' 的 MySQL 数据库
python database/init_db.py
python scripts/generate_sample_items.py
```
**注意**：数据库初始化会创建默认管理员账户：
- 用户名：`admin`
- 密码：`admin123`

首次登录后请更改密码以确保安全。

6. 运行应用
```bash
python main.py
```

### 测试

单元测试覆盖纯逻辑模块（目前为 AI 助手的 SQL 安全校验逻辑
`utils/assistant_data.py`），无需连接 MySQL 即可运行：
```bash
pip install -r requirements-dev.txt
pytest
```

### 使用说明

1. **登录**：使用密码或人脸识别进行认证
2. **仪表盘**：根据用户角色（管理员/用户）访问主要功能
3. **物资管理**：添加、编辑或删除库存物资
4. **借还**：借用和归还物资，自动追踪
5. **用户管理**：（仅管理员）管理用户账户和权限
6. **AI 助手**：点击 AI 按钮获取上下文帮助

### 许可证

本项目采用 MIT 许可证。

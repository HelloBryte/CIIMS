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
cp config.example.py config.py
# Edit config.py with your database and API settings
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

Edit `.env` file with your settings:
```env
# Database
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_DATABASE=campus_system

# AI Assistant (optional)
OPENROUTER_API_KEY=your_api_key
# Face recognition configuration
FACE_RECOGNITION_MODEL_PATH=model/trainer.yml
FACE_RECOGNITION_CASCADE_PATH=haarcascade_frontalface_default.xml
FACE_RECOGNITION_CONFIDENCE_THRESHOLD=50
FACE_RECOGNITION_PREDICTION_THRESHOLD=70
ENABLE_FACE_RECOGNITION=True

# AI Assistant configuration (optional)
OPENROUTER_API_KEY=your_api_key_here
OPENROUTER_MODEL=deepseek/deepseek-chat
PROXY_URL=http://127.0.0.1:7897
```

## Project Structure

```
ciims/
├── ui/                    # User interface components
│   ├── screens/          # Main application windows
│   ├── dialogs/          # Dialog windows
│   └── base/             # Base UI components and styles
├── utils/                 # Utility modules
├── database/             # Database configuration and helpers
├── face_recognition/     # Face recognition modules
├── scripts/              # Utility scripts
├── model/                # Face recognition model files
├── dataset/              # Face recognition training data
└── main.py              # Application entry point
```

## Usage

1. **Login**: Use password or face recognition to authenticate
2. **Dashboard**: Access main features based on user role (admin/user)
3. **Item Management**: Add, edit, or remove inventory items
4. **Borrowing**: Borrow and return items with automatic tracking
5. **User Management**: (Admin only) Manage user accounts and permissions
6. **AI Assistant**: Click the AI button for contextual help

## Face Recognition Setup (Optional)

1. Ensure camera permissions are granted
2. Register face data through the registration window
3. The system will automatically train the recognition model
4. Face recognition will be available at login

## AI Assistant

The built-in AI assistant provides:
- Context-aware help for CIIMS features
- SQL query suggestions for data analysis
- Natural language interface for database operations
- Multilingual support (English/Chinese)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

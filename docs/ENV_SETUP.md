# Environment Setup Guide

## Backend Environment Variables

Create a `.env` file in the `backend` directory with the following variables:

### Database Configuration
```
# SQLite (Development)
DATABASE_URL=sqlite:///./test.db

# PostgreSQL (Production)
# DATABASE_URL=postgresql://user:password@localhost:5432/my_personal_ai
```

### Security
```
# Generate a strong secret key:
# python -c "import secrets; print(secrets.token_urlsafe(32))"
SECRET_KEY=your-super-secret-key-here

ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

### OpenAI Configuration
```
# Get your API key from https://platform.openai.com/api-keys
OPENAI_API_KEY=sk-...

# Available models:
# - gpt-4-turbo-preview
# - gpt-4
# - gpt-3.5-turbo
OPENAI_MODEL=gpt-4-turbo-preview
```

### Application Settings
```
APP_NAME=My Personal AI
APP_VERSION=1.0.0
DEBUG=True  # Set to False in production

# Update based on your deployment URL
CORS_ORIGINS=["http://localhost:5173", "http://localhost:3000"]
```

### File Upload Settings
```
# Maximum file size in bytes (50MB default)
MAX_UPLOAD_SIZE=52428800

# Allowed file types
ALLOWED_FILE_TYPES=["pdf", "docx", "txt"]

# Directory to store uploaded files
UPLOAD_DIR=./uploads
```

### Rate Limiting
```
RATE_LIMIT_ENABLED=True
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_PERIOD=60  # seconds
```

### Logging
```
LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FILE=logs/app.log
```

### AI Model Parameters
```
# Temperature: 0.0 (deterministic) to 2.0 (random)
AI_TEMPERATURE=0.7

# Maximum tokens per response
AI_MAX_TOKENS=2000

# Top P: 0.0 to 1.0
AI_TOP_P=0.9
```

## Frontend Environment Variables

Create a `.env` file in the `frontend` directory:

```
# API endpoint (development)
VITE_API_URL=http://localhost:8000

# API endpoint (production)
# VITE_API_URL=https://your-backend-url.com
```

## Environment Variable Examples

### Development Setup

**backend/.env**
```
DATABASE_URL=sqlite:///./test.db
SECRET_KEY=dev-secret-key-change-in-production
OPENAI_API_KEY=sk-your-api-key-here
OPENAI_MODEL=gpt-3.5-turbo
DEBUG=True
CORS_ORIGINS=["http://localhost:5173", "http://localhost:3000"]
MAX_UPLOAD_SIZE=52428800
ALLOWED_FILE_TYPES=["pdf", "docx", "txt"]
UPLOAD_DIR=./uploads
RATE_LIMIT_ENABLED=True
LOG_LEVEL=DEBUG
AI_TEMPERATURE=0.7
```

**frontend/.env.local**
```
VITE_API_URL=http://localhost:8000
```

### Production Setup

**backend/.env**
```
DATABASE_URL=postgresql://user:password@prod-db.com:5432/my_personal_ai
SECRET_KEY=generate-strong-secret-key
OPENAI_API_KEY=sk-your-api-key-here
OPENAI_MODEL=gpt-4-turbo-preview
DEBUG=False
CORS_ORIGINS=["https://your-frontend-domain.com"]
MAX_UPLOAD_SIZE=52428800
ALLOWED_FILE_TYPES=["pdf", "docx", "txt"]
UPLOAD_DIR=/var/uploads
RATE_LIMIT_ENABLED=True
LOG_LEVEL=INFO
AI_TEMPERATURE=0.7
```

**frontend/.env.production**
```
VITE_API_URL=https://your-backend-domain.com
```

## How to Generate Secret Key

```bash
# Using Python
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Using OpenSSL
openssl rand -base64 32

# Using Node.js
node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"
```

## Getting OpenAI API Key

1. Go to https://platform.openai.com/account/api-keys
2. Log in with your OpenAI account
3. Click "Create new secret key"
4. Copy the key
5. Paste it in your `.env` file

## Database Setup

### SQLite (Development)
No setup needed, automatically created at `./test.db`

### PostgreSQL (Production)

```bash
# Install PostgreSQL
# macOS: brew install postgresql
# Linux: sudo apt-get install postgresql postgresql-contrib
# Windows: Download from https://www.postgresql.org/download/windows/

# Create database
creatdb my_personal_ai

# Create user
creatuser -P myuser

# Grant privileges
psql -d my_personal_ai -c "GRANT ALL PRIVILEGES ON DATABASE my_personal_ai TO myuser;"

# Update DATABASE_URL
DATABASE_URL=postgresql://myuser:password@localhost:5432/my_personal_ai
```

## Validating Configuration

```bash
# Check if .env is properly formatted
cd backend
python -c "from app.config import settings; print('Config loaded successfully')"

# Test database connection
python -c "from app.database import engine; print(engine)"

# Test OpenAI connection
python -c "import openai; openai.api_key='test'; print('OpenAI module loaded')"
```

## CORS Configuration

Update `CORS_ORIGINS` based on your deployment:

```python
# Development
CORS_ORIGINS=["http://localhost:5173", "http://localhost:3000"]

# Production
CORS_ORIGINS=[
    "https://myapp.vercel.app",
    "https://www.myapp.com",
    "https://myapp.com"
]

# Allow all (NOT recommended for production)
CORS_ORIGINS=["*"]
```

## Troubleshooting

### Environment variables not loading
- Ensure `.env` file is in the correct directory
- No spaces around `=` in variable assignments
- Restart the server after changing `.env`

### Database connection failed
- Check `DATABASE_URL` format
- Verify database server is running
- Check credentials are correct
- For PostgreSQL: ensure user has correct permissions

### OpenAI API errors
- Verify API key is valid
- Check account has credits available
- Ensure model name is correct
- Check API rate limits

### CORS errors
- Add frontend URL to `CORS_ORIGINS`
- Restart backend server
- Clear browser cache
- Check frontend API URL matches backend

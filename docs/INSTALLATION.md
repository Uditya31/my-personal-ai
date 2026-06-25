# Installation & Setup Guide

## Backend Setup

### Prerequisites
- Python 3.9+
- PostgreSQL or SQLite
- OpenAI API Key

### Installation Steps

1. **Create virtual environment:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Configure environment:**
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. **Update .env file:**
```
DATABASE_URL=sqlite:///./test.db  # or postgresql://user:password@localhost/dbname
SECRET_KEY=your-super-secret-key
OPENAI_API_KEY=your-openai-api-key
CORS_ORIGINS=["http://localhost:5173", "http://localhost:3000"]
```

5. **Run the server:**
```bash
python main.py
```

Backend will be available at `http://localhost:8000`
- API Docs: `http://localhost:8000/docs`

## Frontend Setup

### Prerequisites
- Node.js 16+
- npm or yarn

### Installation Steps

1. **Install dependencies:**
```bash
cd frontend
npm install
```

2. **Start development server:**
```bash
npm run dev
```

Frontend will be available at `http://localhost:5173`

3. **Build for production:**
```bash
npm run build
```

## Database Initialization

The database tables are automatically created when you run the FastAPI server for the first time.

## Testing the Application

1. Open `http://localhost:5173` in your browser
2. Click on "Register here" to create an account
3. Fill in the registration form and submit
4. Login with your credentials
5. Start creating conversations and chatting with the AI

## Troubleshooting

### CORS Issues
If you see CORS errors, make sure:
- Backend CORS_ORIGINS includes your frontend URL
- Frontend API_URL points to correct backend address

### Database Issues
To reset the database:
```bash
rm test.db  # For SQLite
# Then restart the server
```

### OpenAI API Issues
- Verify your API key is correct
- Check OpenAI account has available credits
- Ensure the model in .env is available to your account

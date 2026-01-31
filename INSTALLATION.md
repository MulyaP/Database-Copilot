# Installation Guide 📦

This guide will help you set up Database Copilot on your local machine.

## Prerequisites

- **Python 3.8+** - [Download Python](https://python.org/downloads/)
- **Node.js 18+** - [Download Node.js](https://nodejs.org/)
- **Git** - [Download Git](https://git-scm.com/)

## 1. Clone the Repository

```bash
git clone <repository-url>
cd Database-Copilot
```

## 2. Backend Setup

### 2.1 Navigate to Backend Directory
```bash
cd backend
```

### 2.2 Create Virtual Environment
```bash
# Windows
python -m venv dbc
dbc\Scripts\activate

# macOS/Linux
python3 -m venv dbc
source dbc/bin/activate
```

### 2.3 Install Dependencies
```bash
pip install -r requirements.txt
```

### 2.4 Environment Configuration
Create a `.env` file in the `backend` directory:

```bash
# Copy the example file
cp .env.example .env
```

Edit `.env` with your configuration:
```env
# Required: Groq API Key (Free)
GROQ_API_KEY=your_groq_api_key_here

# Required: Supabase Configuration
SUPABASE_URL=your_supabase_url
SUPABASE_ANON_KEY=your_supabase_anon_key

# Optional: OpenAI API Key (Premium features)
OPENAI_API_KEY=your_openai_api_key_here
```

### 2.5 Get API Keys

#### Groq API Key (Free & Required)
1. Visit [Groq Console](https://console.groq.com/)
2. Sign up for a free account
3. Navigate to API Keys
4. Create a new API key
5. Copy the key to your `.env` file

#### Supabase Setup (Required)
1. Visit [Supabase](https://supabase.com/)
2. Create a new project
3. Go to Settings → API
4. Copy the URL and anon key to your `.env` file
5. Create the following table in your Supabase SQL editor:

```sql
-- Create connections table
CREATE TABLE connections (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    db_name TEXT NOT NULL,
    db_provider_name TEXT NOT NULL,
    credentials JSONB NOT NULL,
    connected BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Enable Row Level Security
ALTER TABLE connections ENABLE ROW LEVEL SECURITY;

-- Create policy for users to only see their own connections
CREATE POLICY "Users can only see their own connections" ON connections
    FOR ALL USING (auth.uid() = user_id);
```

#### OpenAI API Key (Optional)
1. Visit [OpenAI Platform](https://platform.openai.com/)
2. Create an account and add billing
3. Generate an API key
4. Add to your `.env` file

### 2.6 Start Backend Server
```bash
python main.py
```

The backend will be available at `http://localhost:8000`

## 3. Frontend Setup

### 3.1 Navigate to Frontend Directory
```bash
# Open a new terminal
cd frontend/db-copilot
```

### 3.2 Install Dependencies
```bash
npm install
```

### 3.3 Start Development Server
```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

## 4. Verification

### 4.1 Check Backend
Visit `http://localhost:8000/docs` to see the API documentation.

### 4.2 Check Frontend
Visit `http://localhost:3000` to see the application.

### 4.3 Test the Application
1. Sign up for a new account
2. Create a database connection
3. Start chatting with your database!

## 5. Database Connection Setup

### Supabase Connection
1. Get your Supabase connection string from Settings → Database
2. Use the connection string format: `postgresql://[user]:[password]@[host]:[port]/[database]`

### PostgreSQL Connection
```json
{
  "host": "localhost",
  "port": "5432",
  "username": "your_username",
  "password": "your_password",
  "database": "your_database"
}
```

### MySQL Connection
```json
{
  "host": "localhost",
  "port": "3306",
  "username": "your_username",
  "password": "your_password",
  "database": "your_database"
}
```

### MongoDB Connection
```json
{
  "connection_string": "mongodb://username:password@host:port/database"
}
```

## 6. Troubleshooting

### Common Issues

#### Backend won't start
- Check if Python virtual environment is activated
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check if `.env` file exists and has required keys

#### Frontend won't start
- Check Node.js version: `node --version` (should be 18+)
- Clear npm cache: `npm cache clean --force`
- Delete node_modules and reinstall: `rm -rf node_modules && npm install`

#### Database connection fails
- Verify database credentials
- Check if database server is running
- Ensure firewall allows connections

#### API keys not working
- Verify API keys are correct and active
- Check if you have sufficient credits (for paid APIs)
- Ensure no extra spaces in `.env` file

### Getting Help

If you encounter issues:

1. Check the console logs for error messages
2. Verify all environment variables are set correctly
3. Ensure all services are running
4. Check the [GitHub Issues](link-to-issues) for similar problems

## 7. Development Mode

### Hot Reload
Both frontend and backend support hot reload:
- Backend: Automatically restarts on file changes
- Frontend: Automatically refreshes browser on file changes

### Debugging
- Backend logs are displayed in the terminal
- Frontend logs are available in browser developer tools
- API documentation is available at `http://localhost:8000/docs`

---

**🎉 You're all set! Start building amazing database interactions with AI!**
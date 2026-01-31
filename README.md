# Database Copilot 🤖

An AI-powered database assistant that helps you interact with your databases using natural language. Ask questions, run queries, and explore your data without writing SQL.

## 🚀 What It Does

Database Copilot is an intelligent database companion that:

- **Natural Language Queries**: Ask questions about your database in plain English
- **Multi-Database Support**: Connect to PostgreSQL, MySQL, Supabase, and MongoDB
- **Smart Tool Usage**: Automatically lists tables, explores schemas, and executes queries
- **Real-time Chat Interface**: Interactive chat experience with markdown formatting
- **Secure Authentication**: User management with JWT tokens
- **Connection Management**: Save and manage multiple database connections

## ✨ Current Features

### 🔐 Authentication System
- User registration and login
- JWT-based authentication
- Secure session management

### 🗄️ Database Connectivity
- **Supabase**: Full support with connection string
- **PostgreSQL**: Direct PostgreSQL connections
- **MySQL**: MySQL database support
- **MongoDB**: MongoDB connection support

### 🤖 AI Assistant
- **Groq LLaMA 3.1**: Fast, free AI model for query processing
- **OpenAI GPT**: Premium model support (when API key provided)
- **Tool Calling**: Automatic database exploration and query execution
- **Iterative Processing**: Multi-step reasoning for complex queries

### 💬 Chat Interface
- Beautiful, responsive chat UI
- Markdown rendering with syntax highlighting
- Code block formatting for SQL queries
- Table rendering for query results
- Real-time typing indicators

## 🔧 Current Development

We're actively working on:

- **Enhanced Query Optimization**: Smarter SQL generation and optimization
- **Data Visualization**: Charts and graphs for query results
- **Query History**: Save and replay previous queries
- **Export Features**: Export results to CSV, JSON, Excel
- **Advanced Analytics**: Statistical analysis and insights
- **Multi-language Support**: Support for more database types
- **Performance Monitoring**: Query execution time and optimization suggestions

## 🛠️ Tech Stack

### Backend
- **FastAPI**: Modern Python web framework
- **LangChain**: AI agent framework for tool calling
- **SQLAlchemy**: Database ORM and query execution
- **Supabase**: Authentication and data storage
- **Groq/OpenAI**: AI model providers

### Frontend
- **Next.js 14**: React framework with App Router
- **TypeScript**: Type-safe development
- **Tailwind CSS**: Utility-first styling
- **React Markdown**: Rich text rendering
- **Highlight.js**: Syntax highlighting

## 📋 Prerequisites

- Python 3.8+
- Node.js 18+
- Git

## 🚀 Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Database-Copilot
   ```

2. **Follow the installation guide**
   ```bash
   # See INSTALLATION.md for detailed setup instructions
   ```

3. **Start the application**
   ```bash
   # Backend (Terminal 1)
   cd backend
   python main.py

   # Frontend (Terminal 2)
   cd frontend/db-copilot
   npm run dev
   ```

4. **Open your browser**
   Navigate to `http://localhost:3000`

## 📖 Documentation

- [Installation Guide](INSTALLATION.md) - Detailed setup instructions
- [API Documentation](http://localhost:8000/docs) - FastAPI auto-generated docs
- [Database Setup](docs/database-setup.md) - Database configuration guide

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

If you encounter any issues or have questions:

1. Check the [Installation Guide](INSTALLATION.md)
2. Review the [API Documentation](http://localhost:8000/docs)
3. Open an issue on GitHub

---

**Made with ❤️ for developers who want to talk to their databases**
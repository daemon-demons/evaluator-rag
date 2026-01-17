# ERP Certification Assessment

A quiz application that generates multiple-choice questions using Google's Gemini AI.

## Setup

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Activate the virtual environment:
   ```bash
   source venv/bin/activate
   ```

3. Create a `.env` file with your API key:
   ```bash
   echo "GEMINI_API_KEY=your_api_key_here" > .env
   ```

4. Start the backend server:
   ```bash
   ./start_server.sh
   ```
   
   Or manually:
   ```bash
   python3 -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
   ```

   The backend will run on `http://127.0.0.1:8000`

### Frontend Setup

**Important:** You must run the frontend through a local web server, not by opening the HTML file directly (file:// protocol causes CORS errors).

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Start a local web server:
   ```bash
   ./start_frontend.sh
   ```
   
   Or manually with Python:
   ```bash
   python3 -m http.server 8080
   ```

3. Open your browser and go to:
   ```
   http://localhost:8080
   ```

## Usage

1. Enter a course name (e.g., "Python Programming", "Database Management")
2. Select your level (Beginner, Intermediate, or Expert)
3. Answer 5 multiple-choice questions
4. View your results and certification eligibility

## Troubleshooting

### "Cannot connect to backend" error

- Make sure the backend server is running on port 8000
- Check that you're opening the frontend through `http://localhost:8080` (not `file://`)
- Verify the backend is accessible: `curl http://127.0.0.1:8000/health`

### CORS errors

- Ensure you're using a local web server for the frontend (not opening the HTML file directly)
- Check that CORS middleware is enabled in the backend (it should be by default)

### API Key errors

- Make sure your `.env` file exists in the `backend` directory
- Verify the `GEMINI_API_KEY` is set correctly
- Restart the backend server after creating/modifying the `.env` file

# How to Run Backend and Frontend Separately

## Option 1: Run in Separate Terminal Windows (Recommended)

### Terminal 1 - Backend Server

1. Open a terminal window
2. Navigate to the backend directory:
   ```bash
   cd "/Users/dhineshraja/Desktop/PixDevs/ERP Learn/ERP_Learn/backend"
   ```

3. Activate the virtual environment:
   ```bash
   source venv/bin/activate
   ```

4. Start the backend server:
   ```bash
   python3 -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
   ```

5. You should see:
   ```
   INFO:     Uvicorn running on http://127.0.0.1:8000
   INFO:     Application startup complete.
   ```

6. **Keep this terminal window open** - the backend must keep running

---

### Terminal 2 - Frontend Server

1. Open a **NEW** terminal window
2. Navigate to the frontend directory:
   ```bash
   cd "/Users/dhineshraja/Desktop/PixDevs/ERP Learn/ERP_Learn/frontend"
   ```

3. Start the frontend server:
   ```bash
   python3 -m http.server 8080
   ```

4. You should see:
   ```
   Serving HTTP on :: port 8080 (http://[::]:8080/) ...
   ```

5. **Keep this terminal window open** - the frontend must keep running

---

## Option 2: Use the Individual Scripts

### Start Backend:
```bash
cd "/Users/dhineshraja/Desktop/PixDevs/ERP Learn/ERP_Learn/backend"
./start_server.sh
```

### Start Frontend (in a new terminal):
```bash
cd "/Users/dhineshraja/Desktop/PixDevs/ERP Learn/ERP_Learn/frontend"
./start_frontend.sh
```

---

## Access the Application

Once both servers are running:

1. Open your web browser
2. Go to: **http://localhost:8080**
3. You should see the quiz interface

---

## Verify Both Are Running

### Check Backend:
Open in browser: http://127.0.0.1:8000/health
Should show: `{"status":"ok","message":"Server is running"}`

### Check Frontend:
Open in browser: http://localhost:8080
Should show: The quiz interface with course name input field

---

## Troubleshooting

### "Cannot connect to backend" error:
- Make sure backend is running in Terminal 1
- Check http://127.0.0.1:8000/health works
- Make sure you're opening http://localhost:8080 (not file://)

### Input field not visible:
- Make sure you're using http://localhost:8080 (not opening HTML file directly)
- Check browser console (F12) for errors
- Try refreshing the page (Ctrl+R or Cmd+R)

### Port already in use:
- Backend (8000): Kill the process: `lsof -ti:8000 | xargs kill`
- Frontend (8080): Kill the process: `lsof -ti:8080 | xargs kill`

---

## To Stop the Servers

- **Backend**: Press `Ctrl+C` in Terminal 1
- **Frontend**: Press `Ctrl+C` in Terminal 2

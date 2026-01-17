# Quick Start - Fix Connection Error

## The Problem
You're getting "Cannot connect to server" because the **frontend server is not running**.

## The Solution - 2 Simple Steps

### Step 1: Backend (Already Running ✓)
Your backend is already running on port 8000. Keep it running!

### Step 2: Start Frontend Server (MISSING ✗)

**Open a NEW terminal window** and run:

```bash
cd "/Users/dhineshraja/Desktop/PixDevs/ERP Learn/ERP_Learn/frontend"
python3 -m http.server 8080
```

You should see:
```
Serving HTTP on :: port 8080 (http://[::]:8080/) ...
```

**Keep this terminal open!**

---

## Then Open in Browser

Once BOTH servers are running:

1. Open your browser
2. Go to: **http://localhost:8080**
3. **NOT** `file://` - it must be `http://localhost:8080`

---

## Verify Both Are Running

**Terminal 1 (Backend):**
- Should show: `Uvicorn running on http://127.0.0.1:8000`

**Terminal 2 (Frontend):**
- Should show: `Serving HTTP on port 8080`

**Browser:**
- URL should be: `http://localhost:8080`
- Should see the quiz interface with course name input

---

## Port Summary

- **Backend:** `http://127.0.0.1:8000` (API server)
- **Frontend:** `http://localhost:8080` (Web interface)

**You need BOTH running at the same time!**

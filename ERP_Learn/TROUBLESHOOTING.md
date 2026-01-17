# Troubleshooting Guide

## "Cannot connect to server" Error

### Step 1: Verify Backend is Running

Open a terminal and test:
```bash
curl http://127.0.0.1:8000/health
```

**Expected output:**
```json
{"status":"ok","message":"Server is running"}
```

If this fails, the backend is NOT running. Start it:
```bash
cd backend
source venv/bin/activate
python3 -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

---

### Step 2: Verify Frontend is Served via HTTP

**❌ WRONG:** Opening the HTML file directly (double-clicking)
- URL will be: `file:///Users/.../index.html`
- This causes CORS errors

**✅ CORRECT:** Using a web server
- URL should be: `http://localhost:8080`
- Start frontend server:
  ```bash
  cd frontend
  python3 -m http.server 8080
  ```

---

### Step 3: Check Browser Console

1. Open your browser
2. Press **F12** (or right-click → Inspect)
3. Go to **Console** tab
4. Look for error messages
5. Common errors:
   - `Failed to fetch` = Network/CORS issue
   - `CORS policy` = CORS configuration issue
   - `404 Not Found` = Wrong URL

---

### Step 4: Test Backend Connection from Browser

1. Open browser console (F12)
2. Run this command:
   ```javascript
   fetch('http://127.0.0.1:8000/health').then(r => r.json()).then(console.log)
   ```

**If this works:** Backend is reachable, issue is with the frontend code
**If this fails:** Backend is not accessible (check firewall, port, etc.)

---

### Step 5: Restart Both Servers

Sometimes a restart fixes issues:

1. **Stop backend:** Press `Ctrl+C` in backend terminal
2. **Stop frontend:** Press `Ctrl+C` in frontend terminal
3. **Restart backend:**
   ```bash
   cd backend
   source venv/bin/activate
   python3 -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
   ```
4. **Restart frontend (new terminal):**
   ```bash
   cd frontend
   python3 -m http.server 8080
   ```

---

### Step 6: Clear Browser Cache

1. Hard refresh: `Cmd+Shift+R` (Mac) or `Ctrl+Shift+R` (Windows)
2. Or clear cache: Settings → Clear browsing data

---

### Step 7: Check Port Conflicts

If ports are already in use:

**Check what's using port 8000:**
```bash
lsof -ti:8000
```

**Kill the process:**
```bash
lsof -ti:8000 | xargs kill
```

**Check what's using port 8080:**
```bash
lsof -ti:8080
```

**Kill the process:**
```bash
lsof -ti:8080 | xargs kill
```

---

## Common Issues

### Issue: "Failed to fetch"
**Cause:** Network error, CORS, or backend not running
**Solution:** 
- Verify backend is running (Step 1)
- Make sure frontend is served via HTTP (Step 2)
- Check CORS settings in backend

### Issue: CORS error in console
**Cause:** Frontend and backend origins don't match CORS policy
**Solution:** 
- Backend now allows all origins (`allow_origins=["*"]`)
- Restart backend after CORS changes
- Make sure you're using `http://localhost:8080` not `file://`

### Issue: 404 Not Found
**Cause:** Wrong URL or endpoint doesn't exist
**Solution:**
- Check the URL in `script.js` is `http://127.0.0.1:8000/generate-question`
- Verify backend is running on port 8000

### Issue: Input field not visible
**Cause:** CSS issue or page not loaded correctly
**Solution:**
- Hard refresh browser (Cmd+Shift+R)
- Check browser console for CSS errors
- Make sure you're using `http://localhost:8080`

---

## Quick Diagnostic Commands

```bash
# Test backend
curl http://127.0.0.1:8000/health

# Test backend endpoint
curl -X POST http://127.0.0.1:8000/generate-question \
  -H "Content-Type: application/json" \
  -d '{"level":"beginner","course_name":"Test"}'

# Check if ports are in use
lsof -ti:8000  # Backend
lsof -ti:8080  # Frontend
```

let level = "";
let courseName = "";
let currentQuestion = 0;
let score = 0;
let totalQuestions = 20;
let selectedAnswer = null;
let correctAnswer = null;
let answerSubmitted = false;

// Test backend connection on page load (silent check, no alert)
window.addEventListener("DOMContentLoaded", () => {
  fetch("http://127.0.0.1:8000/health")
    .then(res => res.json())
    .then(data => console.log("✓ Backend connected:", data))
    .catch(err => {
      console.warn("⚠ Backend connection test failed:", err);
      // Don't show alert on page load, only show error when actually trying to use it
    });
});

function startQuiz(selectedLevel) {
  courseName = document.getElementById("course-name").value.trim();
  
  if (!courseName) {
    alert("Please enter a course name");
    return;
  }
  
  level = selectedLevel;
  currentQuestion = 0;
  score = 0;
  selectedAnswer = null;
  correctAnswer = null;
  answerSubmitted = false;

  document.getElementById("start-screen").classList.add("hidden");
  document.getElementById("quiz-screen").classList.remove("hidden");

  document.getElementById("level-badge").innerText = `${courseName} - ${level.toUpperCase()}`;

  loadQuestion();
}

function loadQuestion() {
  // Show loading state
  document.getElementById("question").innerText = "Loading question...";
  document.getElementById("options").innerHTML = "";

  const apiUrl = "http://127.0.0.1:8000/generate-question";
  const requestBody = { 
    level: level,
    course_name: courseName
  };

  console.log("Making request to:", apiUrl);
  console.log("Request body:", requestBody);

  fetch(apiUrl, {
    method: "POST",
    headers: { 
      "Content-Type": "application/json",
      "Accept": "application/json"
    },
    body: JSON.stringify(requestBody),
    mode: "cors"  // Explicitly set CORS mode
  })
  .then(async res => {
    const contentType = res.headers.get("content-type");
    
    if (!res.ok) {
      let errorMessage = `HTTP ${res.status}: ${res.statusText}`;
      try {
        if (contentType && contentType.includes("application/json")) {
          const err = await res.json();
          errorMessage = Array.isArray(err.detail) 
            ? err.detail.map(e => e.msg || e).join(", ")
            : err.detail || errorMessage;
        } else {
          const text = await res.text();
          errorMessage = text || errorMessage;
        }
      } catch (e) {
        console.error("Error parsing error response:", e);
      }
      throw new Error(errorMessage);
    }
    
    if (!contentType || !contentType.includes("application/json")) {
      throw new Error("Response is not JSON");
    }
    
    return res.json();
  })
  .then(data => {
    if (!data.question || !data.options || !data.answer) {
      throw new Error("Invalid response format. Missing required fields.");
    }
    showQuestion(data);
  })
  .catch(error => {
    console.error("Fetch Error:", error);
    console.error("Error details:", {
      message: error.message,
      stack: error.stack,
      name: error.name
    });
    
    // Test backend connection
    fetch("http://127.0.0.1:8000/health")
      .then(res => {
        console.log("Backend health check:", res.status, res.statusText);
        return res.json();
      })
      .then(data => console.log("Backend is reachable:", data))
      .catch(healthErr => {
        console.error("Backend health check failed:", healthErr);
        console.error("This means the backend is NOT accessible from the browser");
      });
    
    let errorMsg = "Error generating question: ";
    if (error.message.includes("Failed to fetch") || error.message.includes("NetworkError") || error.name === "TypeError") {
      errorMsg += "Cannot connect to server.\n\n";
      errorMsg += "Please check:\n";
      errorMsg += "1. Backend is running on http://127.0.0.1:8000\n";
      errorMsg += "2. You're accessing the frontend via http://localhost:8080 (not file://)\n";
      errorMsg += "3. Check browser console (F12) for more details";
    } else {
      errorMsg += error.message;
    }
    
    alert(errorMsg);
    
    // Go back to start screen on error
    document.getElementById("quiz-screen").classList.add("hidden");
    document.getElementById("start-screen").classList.remove("hidden");
  });
}

function showQuestion(q) {
  document.getElementById("question").innerText = q.question;

  let optionsDiv = document.getElementById("options");
  optionsDiv.innerHTML = "";
  
  // Reset state
  selectedAnswer = null;
  correctAnswer = q.answer;
  answerSubmitted = false;
  
  // Hide next button
  document.getElementById("next-button").classList.remove("show");

  // Create option buttons
  q.options.forEach(option => {
    let btn = document.createElement("button");
    btn.innerText = option;
    btn.onclick = () => selectAnswer(option, q.answer);
    optionsDiv.appendChild(btn);
  });

  document.getElementById("progress").innerText =
    `Question ${currentQuestion + 1} of ${totalQuestions}`;

  document.getElementById("progress-fill").style.width =
    ((currentQuestion / totalQuestions) * 100) + "%";
}

function selectAnswer(selected, correct) {
  // Prevent multiple selections
  if (answerSubmitted) return;
  
  selectedAnswer = selected;
  answerSubmitted = true;
  
  // Disable all buttons
  const optionButtons = document.querySelectorAll("#options button");
  optionButtons.forEach(btn => {
    btn.disabled = true;
  });
  
  // Highlight selected answer
  optionButtons.forEach(btn => {
    if (btn.innerText === selected) {
      btn.classList.add("selected");
      if (selected === correct) {
        btn.classList.add("correct");
        score++;
      } else {
        btn.classList.add("incorrect");
        // Also highlight the correct answer
        optionButtons.forEach(correctBtn => {
          if (correctBtn.innerText === correct) {
            correctBtn.classList.add("correct");
          }
        });
      }
    }
  });
  
  // Show next button
  const nextButton = document.getElementById("next-button");
  nextButton.classList.add("show");
  
  // Update button text if last question
  if (currentQuestion + 1 >= totalQuestions) {
    nextButton.innerText = "See Results →";
  } else {
    nextButton.innerText = "Next Question →";
  }
}

function nextQuestion() {
  if (!answerSubmitted) return;
  
  currentQuestion++;

  if (currentQuestion < totalQuestions) {
    loadQuestion();
  } else {
    showResult();
  }
}

// submitAnswer function removed - now using selectAnswer and nextQuestion instead

function showResult() {
  document.getElementById("quiz-screen").classList.add("hidden");
  document.getElementById("result-screen").classList.remove("hidden");

  document.getElementById("final-score").innerText =
    `Your Score: ${score} / ${totalQuestions}`;

  document.getElementById("result-status").innerText =
    score >= 14 ? "✅ Eligible for Certification" : "❌ Not Eligible";  // 70% threshold (14/20)
}

function goHome() {
  document.getElementById("result-screen").classList.add("hidden");
  document.getElementById("start-screen").classList.remove("hidden");
}

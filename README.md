# 🧮 Virtual Calculator using Hand Gestures (OpenCV + MediaPipe)

Welcome to the **touchless future** of calculators! This project lets you interact with a floating calculator using just your **fingers and webcam**. Powered by **OpenCV** and **MediaPipe**, it's like a Snapchat filter—but useful. 😎

---

## 🎥 What It Does

🚀 **No mouse. No keyboard. Just your hands.**
This virtual calculator uses your **webcam** to detect your **hand movements** and lets you:

* Press calculator buttons by pinching (index + middle finger)
* Build and evaluate mathematical expressions
* Clear the screen with the `CLR` button
* Interact like a futuristic tech wizard 🧙‍♂️

---

## 🛠️ Technologies Used

| Library   | Purpose                              |
| --------- | ------------------------------------ |
| OpenCV    | Real-time webcam feed + drawing UI   |
| MediaPipe | Hand tracking and gesture detection  |
| NumPy     | Math & array handling (optional use) |
| Python    | The whole logic runs on it 🐍        |

---

## 🧠 How It Works

* The app detects your **index** and **middle** fingers.
* If you pinch them together, it calculates the distance.
* If the pinch is close enough (like a "click"), it detects a **button press**.
* The calculator interface is **drawn directly on the webcam feed**.

---

## 🧪 Features

* 👆 Touchless interaction
* 🔢 Functional calculator with basic operations: `+`, `-`, `*`, `/`
* ❌ "C" to clear expression
* ✅ "=" to evaluate
* 🧼 `CLR` button to clear the expression
* 🧠 Smoothed fingertips and stable pinch detection to avoid accidental clicks

---

## 🖥️ How to Run

> ⚠️ Make sure your webcam is connected.

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python app.py
```

Open [http://localhost:5000](http://localhost:5000) in a browser after starting the server.

### Render deployment

Create a Render Web Service connected to the `main` branch. Leave **Root Directory** blank and use:

```text
Build Command: pip install -r requirements.txt
Start Command: gunicorn --bind 0.0.0.0:$PORT app:app
```

In Render's **Environment Variables**, add `PYTHON_VERSION` with the value `3.12.8`. This is required because the pinned MediaPipe dependency does not support Render's default Python 3.14 runtime. No secret keys or other environment variables are required. After saving the variable, trigger a new deploy.

## Why Flask and MJPEG?

* Flask serves the calculator UI and exposes the webcam stream through a normal HTTP endpoint.
* The `/video_feed` route yields each processed OpenCV frame as a JPEG.
* Flask wraps those JPEGs in a `multipart/x-mixed-replace` response, so the browser updates the `<img>` continuously without JavaScript or a native OpenCV window.
* This keeps camera capture, hand tracking, and rendering on the server while making the result accessible from any browser on the local machine.

## 🧽 Future Upgrades

* Add scientific functions (like `sin`, `cos`, `sqrt`)
* Improve UI aesthetics with dynamic resizing
* Add sound feedback on clicks
* Voice-controlled calculator mode 🔊

---

## 🙌 Credits

Crafted by **Siva**, with caffeine, code, and curiosity.
Inspired by the future of **gesture-controlled interfaces**.

---



## 📜 License

Feel free to use, modify, and share this project for **learning and innovation**. Give credits where due. 😊

---


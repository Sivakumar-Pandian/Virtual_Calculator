# 🧮 Virtual Calculator using Hand Gestures (OpenCV + MediaPipe)

Welcome to the **touchless future** of calculators! This project lets you interact with a floating calculator using just your **fingers and webcam**. Powered by **OpenCV** and **MediaPipe**, it's like a Snapchat filter—but useful. 😎

---

## 🎥 What It Does

🚀 **No mouse. No keyboard. Just your hands.**
This virtual calculator uses your **webcam** to detect your **hand movements** and lets you:

* Press calculator buttons by pinching (index + middle finger)
* Build and evaluate mathematical expressions
* Clear the screen or close the app with a hand gesture
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
* 🔴 "Close" button to quit
* 🧠 Smart debounce to avoid accidental multiple clicks

---

## 🖥️ How to Run

> ⚠️ Make sure your webcam is connected.

```bash
pip install opencv-python mediapipe numpy
python virtual_calculator.py
```

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


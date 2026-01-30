# 🎨 Color Background Remover

A simple yet powerful **color-based background removal** tool.
With a single click, it removes areas with similar colors and exports the result as a **transparent PNG**.

> Designed especially for **pixel art**, **sprites**, **game assets**, and quick background cleanup tasks.

---

## ✨ Features

* 🖱️ **Click to Remove**
  Click on any area and all similar-colored pixels become transparent.

* ↩️ **Undo (History)**
  Made a mistake? Instantly revert your last action.

* 🔍 **Zoom (Mouse Wheel)**
  Zoom in and out for precise edits.

* ✋ **Pan (Right Click + Drag)**
  Move around the image easily when zoomed in.

* 🎚️ **Tolerance Control**
  Adjust how similar colors are detected using the tolerance slider.

* 🖼️ **Save as PNG**
  Export the result with a transparent background.

---

## 🧱 Project Structure

```
color-background-remover/
│
├─ app/
│   ├─ __init__.py
│   ├─ app.py            # Tkinter UI and application logic
│   └─ flood_fill.py     # Color-based removal algorithm
│
├─ assets/
│   └─ samples/
│       └─ input.jpg     # Sample image (optional)
│
├─ main.py               # Application entry point
├─ requirements.txt
├─ README.md
└─ .gitignore
```

---

## 🚀 Installation

### 1️⃣ Clone the repository

```bash
git clone https://github.com/your-username/color-background-remover.git
cd color-background-remover
```

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Run the application

```bash
python main.py
```

---

## 🧠 How It Works

* The app uses **OpenCV flood fill** to detect regions of similar color.
* Flood fill is applied on the **RGB channels only**.
* Matching pixels have their **alpha (transparency) channel set to 0**.
* The original image is **never modified in-place**, making Undo reliable.

---

## 🛠️ Built With

* **Python 3.10+**
* **Tkinter** (GUI)
* **OpenCV** (Image Processing)
* **NumPy**
* **Pillow (PIL)**

---

## 📌 Use Cases

* 🎮 Game development (sprite & asset cleanup)
* 🧩 Pixel art editing
* 🖼️ Quick background removal
* 🧪 Image processing learning projects

---

## 🗺️ Roadmap

* 🖌️ Brush-based removal
* 🎨 Checkerboard transparency background
* 🧠 Edge smoothing (feathering)
* 📦 EXE / Portable build
* 🧩 Sprite sheet support

---

## 🤝 Contributing

Contributions are welcome 🙌
Feel free to open an issue or submit a pull request.

---

## 📄 License

MIT License

---

> Developer note: This project is built with a balance of learning and real-world usability in mind.
> The codebase is clean, modular, and easy to extend.

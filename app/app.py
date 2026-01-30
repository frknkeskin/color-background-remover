import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
import numpy as np
from PIL import Image, ImageTk

from app.flood_fill import flood_fill_remove



class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Color Background Remover")

        # ---------------- RESİM SEÇ ----------------
        path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg")]
        )

        if not path:
            root.destroy()
            return

        # Resmi BGR formatında oku
        bgr = cv2.imread(path)
        if bgr is None:
            messagebox.showerror("Error", "Failed to load image")
            root.destroy()
            return

        # Alpha kanalı ekle (BGRA)
        h, w = bgr.shape[:2]
        self.w, self.h = w, h
        self.img_bgra = np.dstack([
            bgr,
            np.full((h, w), 255, dtype=np.uint8)
        ])

        # ---------------- STATE ----------------
        self.zoom = 1.0          # yakınlaştırma
        self.offset_x = 0        # pan x
        self.offset_y = 0        # pan y
        self.tolerance = 30      # renk toleransı
        self.history = []        # undo geçmişi

        # ---------------- UI ----------------
        self.build_ui()
        self.bind_events()
        self.fit_to_view()

    # ---------------- UI OLUŞTUR ----------------
    def build_ui(self):
        top = tk.Frame(self.root)
        top.pack(fill="x")

        # Undo butonu
        tk.Button(top, text="Undo", command=self.undo)\
            .pack(side="left", padx=5)

        # Tolerans slider
        tk.Label(top, text="Tolerance").pack(side="left")
        self.slider = tk.Scale(
            top,
            from_=0,
            to=100,
            orient="horizontal",
            command=lambda v: setattr(self, "tolerance", int(v))
        )
        self.slider.set(30)
        self.slider.pack(side="left")

        # Kaydet butonu
        tk.Button(top, text="Save as PNG", command=self.save_png)\
            .pack(side="right", padx=10)

        # Canvas
        self.canvas = tk.Canvas(self.root, bg="#333")
        self.canvas.pack(fill="both", expand=True)

    # ---------------- EVENTLER ----------------
    def bind_events(self):
        self.canvas.bind("<Button-1>", self.on_click)        # silme
        self.canvas.bind("<MouseWheel>", self.on_zoom)       # zoom
        self.canvas.bind("<ButtonPress-3>", self.pan_start)  # pan başlat
        self.canvas.bind("<B3-Motion>", self.pan_move)       # pan sürükle

    # ---------------- ÇİZ ----------------
    def render(self):
        # Güvenlik: boş image çizme
        if self.img_bgra is None or self.img_bgra.size == 0:
            return

        self.canvas.delete("all")

        # BGRA → RGBA
        rgba = cv2.cvtColor(self.img_bgra, cv2.COLOR_BGRA2RGBA)
        pil = Image.fromarray(rgba)

        # Zoom uygula
        pil = pil.resize(
            (int(self.w * self.zoom), int(self.h * self.zoom)),
            Image.NEAREST
        )

        self.tk_img = ImageTk.PhotoImage(pil)

        # Canvas’a çiz
        self.canvas.create_image(
            self.offset_x,
            self.offset_y,
            anchor="nw",
            image=self.tk_img
        )

    # ---------------- EKRANA SIĞDIR ----------------
    def fit_to_view(self):
        self.root.update_idletasks()

        cw = self.canvas.winfo_width()
        ch = self.canvas.winfo_height()

        self.zoom = min(cw / self.w, ch / self.h)
        self.offset_x = (cw - self.w * self.zoom) // 2
        self.offset_y = (ch - self.h * self.zoom) // 2

        self.render()

    # ---------------- TIKLAMA ----------------
    def on_click(self, event):
        # Canvas koordinatını resim koordinatına çevir
        ix = (event.x - self.offset_x) / self.zoom
        iy = (event.y - self.offset_y) / self.zoom

        x, y = int(ix), int(iy)

        if 0 <= x < self.w and 0 <= y < self.h:
            # Undo için kopya sakla
            self.history.append(self.img_bgra.copy())

            # Yeni image üret (inplace değil)
            new_img = flood_fill_remove(
                self.img_bgra, x, y, self.tolerance
            )

            if new_img is not None and new_img.size != 0:
                self.img_bgra = new_img
                self.render()

    # ---------------- ZOOM ----------------
    def on_zoom(self, event):
        factor = 1.1 if event.delta > 0 else 0.9
        old_zoom = self.zoom
        self.zoom = max(0.1, min(self.zoom * factor, 20))

        # Zoom merkezi mouse olsun
        mx, my = event.x, event.y
        self.offset_x = mx - (mx - self.offset_x) * (self.zoom / old_zoom)
        self.offset_y = my - (my - self.offset_y) * (self.zoom / old_zoom)

        self.render()

    # ---------------- PAN ----------------
    def pan_start(self, event):
        self.pan_x = event.x
        self.pan_y = event.y

    def pan_move(self, event):
        dx = event.x - self.pan_x
        dy = event.y - self.pan_y

        self.offset_x += dx
        self.offset_y += dy

        self.pan_x = event.x
        self.pan_y = event.y

        self.render()

    # ---------------- UNDO ----------------
    def undo(self):
        if self.history:
            self.img_bgra = self.history.pop()
            self.render()

    # ---------------- KAYDET ----------------
    def save_png(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".png",
            initialfile="Image.png",
            filetypes=[("PNG Image", "*.png")]
        )
        if path:
            cv2.imwrite(path, self.img_bgra)

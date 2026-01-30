import tkinter as tk
from app.app import App


def main():
    root = tk.Tk()
    root.geometry("1000x700")
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()

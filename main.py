# main.py

import tkinter as tk
from GUI import DICOMViewerGUI

if __name__ == "__main__":
    root = tk.Tk()
    app = DICOMViewerGUI(root)
    root.mainloop()
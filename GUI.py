# GUI.py

import tkinter as tk
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import mplcursors

from DICOMLoader import DICOMLoader, load_dicom_folder


class DICOMViewerGUI:
    """
        DICOMViewerGUI class for creating a Tkinter-based GUI for DICOM image viewing.

        Attributes:
        - root (tk.Tk): Tkinter root window.
        - load_button (tk.Button): Button for loading DICOM images.
        - canvas_frame (tk.Frame): Frame for Matplotlib canvas.
        - fig (matplotlib.figure.Figure): Matplotlib figure for displaying images.
        - axs (numpy.ndarray): Array of Matplotlib axes for different planes.
        - current_slice (int): Index of the currently displayed slice.
        - axial_aspect_ratio (float): Aspect ratio for the axial plane.
        - sagittal_aspect_ratio (float): Aspect ratio for the sagittal plane.
        - coronal_aspect_ratio (float): Aspect ratio for the coronal plane.
        - image_shape (list): Shape of the loaded 3D volume.

        Methods:
        - load_dicom_folder(): Open a file dialog to select a DICOM folder and load images.
        - display_dicom(folder_path): Display DICOM images in the GUI.
        - add_plot_to_gui(): Add Matplotlib plots to the Tkinter GUI.
        - update_plots(): Update Matplotlib plots with new images.
        - on_scroll(event): Handle the scroll event for zooming in and out.
        - set_zoom_mode(mode): Set the zoom mode for axial, sagittal, or coronal plane.
        """

    def __init__(self, source):
        """
        Initialize the DICOMViewerGUI.

        Parameters:
        - source: Tkinter root window or another source for GUI creation.
        """
        self.root = source
        self.root.title("DICOM Viewer GUI")

        window_width = 800
        window_height = 600
        screen_width = source.winfo_screenwidth()
        screen_height = source.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        self.load_button = tk.Button(self.root, text="Load DICOM Folder", command=self.load_dicom_folder, height=2,
                                     width=20)
        self.load_button.pack(pady=20)

        self.canvas_frame = tk.Frame(self.root)
        self.canvas_frame.pack(expand=True, fill="both")

        self.fig = None
        self.axs = None
        self.volume_3d = None
        self.current_slice = 0

        self.axial_aspect_ratio = None
        self.sagittal_aspect_ratio = None
        self.coronal_aspect_ratio = None

        self.image_shape = None

        self.zoom_mode = "Axial"

        self.dicom_loader = DICOMLoader()

    def load_dicom_folder(self):
        """
        Open a file dialog to select a DICOM folder and load images.
        """
        folder_path = filedialog.askdirectory(title="Select DICOM Folder")
        if folder_path:
            (self.volume_3d, self.image_shape, self.axial_aspect_ratio, self.sagittal_aspect_ratio,
             self.coronal_aspect_ratio) = load_dicom_folder(folder_path)
            self.display_dicom()

    def display_dicom(self):
        """
        Display DICOM images in the GUI.

        Parameters:
        - folder_path (str): Path to the folder containing DICOM files.
        """
        self.fig, self.axs = plt.subplots(1, 3, figsize=(15, 5))
        self.current_slice = self.image_shape[2] // 2

        self.add_plot_to_gui()

        mplcursors.cursor(hover=True)

    def add_plot_to_gui(self):
        """
        Add Matplotlib plots to the Tkinter GUI.
        """
        canvas = FigureCanvasTkAgg(self.fig, master=self.canvas_frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(expand=True, fill="both")

        axial_button = tk.Button(self.root, text="Axial", command=lambda: self.set_zoom_mode("Axial"))
        axial_button.pack(side=tk.LEFT, padx=10)

        sagittal_button = tk.Button(self.root, text="Sagittal", command=lambda: self.set_zoom_mode("Sagittal"))
        sagittal_button.pack(side=tk.LEFT, padx=10)

        coronal_button = tk.Button(self.root, text="Coronal", command=lambda: self.set_zoom_mode("Coronal"))
        coronal_button.pack(side=tk.LEFT, padx=10)

        self.fig.canvas.mpl_connect('scroll_event', self.on_scroll)

        self.update_plots()

    def update_plots(self):
        """
        Update Matplotlib plots with new images.
        """
        for ax in self.axs:
            ax.clear()

        axial_image = self.volume_3d[:, :, self.current_slice]
        sagittal_image = self.volume_3d[:, self.image_shape[1] // 2, :]
        coronal_image = self.volume_3d[self.image_shape[0] // 2, :, :].T

        self.axs[0].imshow(axial_image, cmap='gray')
        self.axs[0].set_title("Axial Plane")
        self.axs[0].set_aspect(self.axial_aspect_ratio)

        self.axs[1].imshow(sagittal_image, cmap='gray')
        self.axs[1].set_title("Sagittal Plane")
        self.axs[1].set_aspect(self.sagittal_aspect_ratio)

        self.axs[2].imshow(coronal_image, cmap='gray')
        self.axs[2].set_title("Coronal Plane")
        self.axs[2].set_aspect(self.coronal_aspect_ratio)

        self.fig.canvas.draw()

    def on_scroll(self, event):
        """
        Handle the scroll event for zooming in and out.

        Parameters:
        - event: Matplotlib scroll event.
        """
        if self.zoom_mode == "Axial":
            if event.button == 'up':
                self.current_slice = (self.current_slice + 5) % len(self.volume_3d[0, 0, :])
            elif event.button == 'down':
                self.current_slice = (self.current_slice - 5) % len(self.volume_3d[0, 0, :])
        elif self.zoom_mode == "Sagittal":
            if event.button == 'up':
                self.image_shape[1] = (self.image_shape[1] + 5) % len(self.volume_3d[0, :, 0])
            elif event.button == 'down':
                self.image_shape[1] = (self.image_shape[1] - 5) % len(self.volume_3d[0, :, 0])
        elif self.zoom_mode == "Coronal":
            if event.button == 'up':
                self.image_shape[0] = (self.image_shape[0] + 5) % len(self.volume_3d[:, 0, 0])
            elif event.button == 'down':
                self.image_shape[0] = (self.image_shape[0] - 5) % len(self.volume_3d[:, 0, 0])

        self.update_plots()

    def set_zoom_mode(self, mode):
        """
        Set the zoom mode for axial, sagittal, or coronal plane.

        Parameters:
        - mode (str): Zoom mode ('Axial', 'Sagittal', or 'Coronal').
        """
        self.zoom_mode = mode

        self.update_plots()

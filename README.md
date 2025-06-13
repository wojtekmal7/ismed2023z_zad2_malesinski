# CTViewerApp – Simple DICOM Viewer in Python

This application is a graphical DICOM viewer created in Python using `tkinter`, `matplotlib` and `pydicom`. It allows users to load and explore medical images in Axial, Sagittal, and Coronal planes interactively.

## Features

- Load DICOM images from a selected folder
- View images in 3 standard planes: Axial, Sagittal, Coronal
- Scroll through image slices in real-time (mouse wheel)
- Switch between planes using GUI buttons
- Display pixel spacing, slice thickness, and aspect ratios

## Requirements

Install the required libraries using the provided `requirements.txt`:

```bash
pip install -r requirements.txt
```

## Required versions:
matplotlib==3.3.4
mplcursors==0.5.3
pydicom==1.4.2
numpy==1.19.2

## How to Run

Simply run:
python main.py

This will open a GUI window. From there:
Click "Load DICOM Folder" and select a folder containing valid DICOM .dcm files.

Use the scroll wheel to navigate through slices (in Axial view).

Use buttons to switch between Axial, Sagittal, and Coronal planes.

## Example (in code)
To load DICOMs programmatically:
from DICOMLoader import load_dicom_folder

volume, shape, axial_ar, sagittal_ar, coronal_ar = load_dicom_folder("/path/to/folder")
## Project Structure

main.py – launches the application

GUI.py – handles the graphical user interface

DICOMLoader.py – logic for reading and processing DICOM data

requirements.txt – lists required dependencies

## Notes
Make sure the selected folder contains valid and complete DICOM series.

If the viewer doesn't display images properly, verify that files include PixelSpacing and SliceThickness.

The scroll functionality currently applies only to the Axial view.

## License
This project is intended for educational and demonstration purposes only.

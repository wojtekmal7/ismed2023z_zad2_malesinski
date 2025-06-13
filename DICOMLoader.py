# DICOMLoader.py

import os
import pydicom as dicom
import numpy as np


def load_dicom_folder(folder_path):
    """
        Load DICOM images from the specified folder and process them.

        Parameters:
        - folder_path (str): Path to the folder containing DICOM files.

        Returns:
        - volume_3d (numpy.ndarray): 3D volume containing pixel data.
        - image_shape (list): Shape of the loaded 3D volume.
        - axial_aspect_ratio (float): Aspect ratio for the axial plane.
        - sagittal_aspect_ratio (float): Aspect ratio for the sagittal plane.
        - coronal_aspect_ratio (float): Aspect ratio for the coronal plane.

        This function reads DICOM files from the specified folder, sorts them based on
        their ImagePositionPatient[2], and processes them to create a 3D volume. It computes
        pixel spacing, slice thickness, and aspect ratios for axial, sagittal, and coronal planes.

        The function prints information about pixel spacing, slice thickness, and aspect ratios.

        Example:
        volume, shape, axial_aspect, sagittal_aspect, coronal_aspect = load_dicom_folder("/path/to/dicom/folder")
        """
    ct_img = os.listdir(folder_path)
    slices = [dicom.read_file(os.path.join(folder_path, s), force=True) for s in ct_img]
    slices = sorted(slices, key=lambda x: x.ImagePositionPatient[2])

    pix_spacing = slices[0].PixelSpacing
    slices_thickness = slices[0].SliceThickness
    axial_aspect_ratio = pix_spacing[1] / pix_spacing[0]
    sagittal_aspect_ratio = pix_spacing[0] / pix_spacing[1]
    coronal_aspect_ratio = slices_thickness / pix_spacing[0]

    print("Pixel spacing:", pix_spacing)
    print("Slice Thickness:", slices_thickness)
    print("Axial Aspect Ratio:", axial_aspect_ratio)
    print("Sagittal Aspect Ratio:", sagittal_aspect_ratio)
    print("Coronal Aspect Ratio:", coronal_aspect_ratio)

    image_shape = list(slices[0].pixel_array.shape)
    image_shape.append(len(slices))
    volume_3d = np.zeros(image_shape)

    for i, s in enumerate(slices):
        array_2_d = s.pixel_array
        volume_3d[:, :, i] = array_2_d

    return volume_3d, image_shape, axial_aspect_ratio, sagittal_aspect_ratio, coronal_aspect_ratio


class DICOMLoader:
    pass

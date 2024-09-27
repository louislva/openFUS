import os
import numpy as np
import pydicom
import nibabel as nib
import pyvista as pv
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# print(dir(pv))
# exit()

class MRIViewer:
    def __init__(self, file_path):
        self.file_path = file_path
        self.image_3d = self.load_data()
    
    def load_data(self):
        if os.path.isdir(self.file_path):
            return self.load_dicom_series(self.file_path)
        elif self.file_path.endswith('.nii') or self.file_path.endswith('.nii.gz'):
            return self.load_nifti_file(self.file_path)
        else:
            raise ValueError("Unsupported file format")
    
    def load_dicom_series(self, directory):
        slices = []
        for filename in os.listdir(directory):
            if filename.endswith('.dcm'):
                ds = pydicom.dcmread(os.path.join(directory, filename))
                slices.append(ds)
        slices.sort(key=lambda x: float(x.ImagePositionPatient[2]))
        image_3d = np.stack([s.pixel_array for s in slices], axis=-1)
        return image_3d

    def load_nifti_file(self, file_path):
        nifti_img = nib.load(file_path)
        image_3d = nifti_img.get_fdata()
        return image_3d

    def display_slice(self, slice_index):
        plt.imshow(self.image_3d[:, :, slice_index], cmap='gray')
        plt.axis('off')
        plt.show()
    
    def interactive_slicing(self, dim='z'):
        max_index = self.image_3d.shape[
            'xyz'.index(dim)
        ] - 1
        slice_index = max_index // 2      

        def get_slice():
            nonlocal slice_index
            if dim == 'x':
                return self.image_3d[slice_index, :, :]
            elif dim == 'y':
                return self.image_3d[:, slice_index, :]
            elif dim == 'z':
                return self.image_3d[:, :, slice_index]
            else:
                raise ValueError("Invalid dimension")
            
        fig, ax = plt.subplots()
        plt.subplots_adjust(bottom=0.25)
        l = ax.imshow(get_slice(), cmap='gray')
        ax_slice = plt.axes([0.25, 0.1, 0.65, 0.03])
        slice_slider = Slider(ax_slice, 'Slice', 0, max_index, valinit=slice_index, valfmt='%0.0f')

        def update(val):
            nonlocal slice_index
            slice_index = int(slice_slider.val)
            plane = get_slice()
            l.set_data(plane)
            fig.canvas.draw_idle()

        slice_slider.on_changed(update)
        plt.show()

        return slice_index
    
    def visualize_3d(self, slice_x=None, slice_y=None, slice_z=None, mesh_file=None):
        if slice_x is None:
            slice_x = self.image_3d.shape[0] - 1
        if slice_y is None:
            slice_y = self.image_3d.shape[1] - 1
        if slice_z is None:
            slice_z = self.image_3d.shape[2] - 1
        
        x = np.arange(0, slice_x + 1)
        y = np.arange(0, slice_y + 1)
        z = np.arange(0, slice_z + 1)
        grid = pv.RectilinearGrid(x, y, z)
        grid.point_data["values"] = self.image_3d[:slice_x + 1, :slice_y + 1, :slice_z + 1].flatten(order="F")
        plotter = pv.Plotter()
        # opacity = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]  # Adjust opacity mapping
        # opacity = [0, 0.7, 0.73, 0.77, 0.8, 0.83, 0.86, 0.9, 0.93, 0.96, 1]  # Adjust opacity mapping
        opacity = [0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]  # Adjust opacity mapping
        plotter.add_volume(grid, cmap='viridis', opacity=opacity)
        
        # Add mesh if provided
        if mesh_file:
            mesh = pv.read(mesh_file)
            mesh = mesh.scale([0.1, 0.1, 0.1])
            plotter.add_mesh(mesh, color='white', opacity=0.5)
        
        plotter.show()

# Usage example:
# Provide the path to a directory containing DICOM files or a NIfTI file
viewer = MRIViewer('healthy-t1.nii')

# # Display a single 2D slice
# slice_index = 50  # Change this index to see different slices
# viewer.display_slice(slice_index)

# Interactive slicing with a slider
slice_x = viewer.interactive_slicing(dim='x')
slice_y = viewer.interactive_slicing(dim='y')
slice_z = viewer.interactive_slicing(dim='z')

print(slice_x, slice_y, slice_z)

# Interactive 3D volume visualization with rotation support and mesh
viewer.visualize_3d(slice_x=slice_x, slice_y=slice_y, slice_z=slice_z, mesh_file='Arge/tFUS v3.stl')
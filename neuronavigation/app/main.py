import os
import numpy as np
import pydicom
import nibabel as nib
import pyvista as pv
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from threading import Thread, Lock
import time

class ArucoTrackerThread(Thread):
    def __init__(self):
        self.position = np.zeros(3)
        self.rotation = np.zeros(3)
        self.lock = Lock()
        super().__init__()

    def get_transform(self):
        with self.lock:
            return self.position, self.rotation

    def run(self):
        while True:
            with self.lock:
                self.position, self.rotation = self.get_aruco_pos_rot()
            time.sleep(0.1)

    def get_aruco_pos_rot(self):
        return np.random.rand(3), np.random.rand(3)

class MRIViewer:
    def __init__(self, file_path):
        self.file_path = file_path
        self.image_3d = self.load_data()
        self.spacing = (1, 1, 1)
        self.image_3d, self.spacing = self.scale_image((64, 64, 64))
    
    def load_data(self):
        if os.path.isdir(self.file_path):
            return self.load_dicom_series(self.file_path)
        elif self.file_path.endswith('.nii') or self.file_path.endswith('.nii.gz'):
            return self.load_nifti_file(self.file_path)
        else:
            raise ValueError("Unsupported file format")
    
    def scale_image(self, new_shape: tuple[int, int, int]):
        """
        Scales the 3D image by the given scale factors using block averaging.

        Parameters:
            scale_factors (tuple of floats): Scaling factors for each dimension (scale_x, scale_y, scale_z).

        Returns:
            np.ndarray: The scaled 3D image.
        """

        old_shape = self.image_3d.shape
        print(f"Original shape: {old_shape}, New shape: {new_shape}")

        # Initialize the new image with zeros
        new_image = np.zeros(new_shape, dtype=self.image_3d.dtype)

        # Calculate the ratio of old to new dimensions
        ratio_x = old_shape[0] / new_shape[0]
        ratio_y = old_shape[1] / new_shape[1]
        ratio_z = old_shape[2] / new_shape[2]

        for i in range(new_shape[0]):
            for j in range(new_shape[1]):
                for k in range(new_shape[2]):
                    # Define the boundaries of the block in the original image
                    x_start = int(i * ratio_x)
                    x_end = int((i + 1) * ratio_x)
                    y_start = int(j * ratio_y)
                    y_end = int((j + 1) * ratio_y)
                    z_start = int(k * ratio_z)
                    z_end = int((k + 1) * ratio_z)

                    # Handle edge cases where the block might exceed the image dimensions
                    x_end = min(x_end, old_shape[0])
                    y_end = min(y_end, old_shape[1])
                    z_end = min(z_end, old_shape[2])

                    # Extract the block and compute the average
                    block = self.image_3d[x_start:x_end, y_start:y_end, z_start:z_end]
                    new_image[i, j, k] = block.mean()

        return new_image, (ratio_x, ratio_y, ratio_z)

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
    
    def visualize_3d(self, slice_x=None, slice_y=None, slice_z=None, mesh_file=None, tracker=None):
        if slice_x is None:
            slice_x = self.image_3d.shape[0] - 1
        if slice_y is None:
            slice_y = self.image_3d.shape[1] - 1
        if slice_z is None:
            slice_z = self.image_3d.shape[2] - 1
        
        x = np.arange(0, slice_x + 1) * self.spacing[0]
        y = np.arange(0, slice_y + 1) * self.spacing[1]
        z = np.arange(0, slice_z + 1) * self.spacing[2]
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
                
        plotter.show(interactive_update=True)

        while True:
            position, rotation = tracker.get_transform()
            print("doing", position, rotation)
            mesh.translate(position * 10, inplace=True)
            # mesh.rotate(rotation, inplace=True)
            plotter.update()        
            
            time.sleep(1)
            # plotter.close()
        

# Usage example:
# Provide the path to a directory containing DICOM files or a NIfTI file
viewer = MRIViewer('healthy-t1.nii')

# # Display a single 2D slice
# slice_index = 50  # Change this index to see different slices
# viewer.display_slice(slice_index)

# Interactive slicing with a slider
slice_x, slice_y, slice_z = None, None, None
slice_x = viewer.interactive_slicing(dim='x')
# slice_y = viewer.interactive_slicing(dim='y')
# slice_z = viewer.interactive_slicing(dim='z')

print(slice_x, slice_y, slice_z)

# Start the Aruco tracker thread
tracker = ArucoTrackerThread()
tracker.start()

print(tracker.get_transform())
print(tracker.get_transform())
time.sleep(1)
print(tracker.get_transform())

# Interactive 3D volume visualization with rotation support and mesh
viewer.visualize_3d(slice_x=slice_x, slice_y=slice_y, slice_z=slice_z, mesh_file='Arge/tFUS v3.stl', tracker=tracker)
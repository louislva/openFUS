# conda activate openfus

import os
import numpy as np
import pydicom
import nibabel as nib
import pyvista as pv
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
# from threading import Thread, Lock
import time
import cv2
import cv2.aruco as aruco
import numpy as np
# from threading import Thread
from multiprocessing import Process
import multiprocessing
from collections import deque
from scipy.stats import median_abs_deviation

# Function to filter outliers based on MAD
def filter_outliers(data, threshold=3.5):
    print()
    if len(data) == 0:
        return data
    print("data", data)
    median = np.median(data, axis=0)
    mad = median_abs_deviation(data, axis=0)
    if np.any(mad == 0):
        mad = np.where(mad == 0, 1e-6, mad)  # Prevent division by zero
    modified_z_scores = 0.6745 * (data - median) / mad
    mask = np.abs(modified_z_scores) < threshold
    return data[mask.all(axis=1)]

def aruco_tracker(shared_list):
    camera_matrix = np.load("camera_matrix.npy")
    dist_coeffs = np.load("dist_coeffs.npy")
    # Initialize the webcam
    cap = cv2.VideoCapture(0)

    # Define the ArUco dictionary
    aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_6X6_250)

    # Create ArUco parameters
    aruco_parameters = aruco.DetectorParameters()

    # ArucoDetector is a class that is used to detect ArUco markers in an image
    detector = aruco.ArucoDetector(aruco_dict, aruco_parameters)
    
    measurement = None
    last_translation = None

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
            break

        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect ArUco markers
        corners, ids, rejected = detector.detectMarkers(gray)
        
        # If markers are detected
        if ids is not None:
            # Draw detected markers
            aruco.drawDetectedMarkers(frame, corners, ids)

            # Estimate pose of each marker
            size = 0.05
            # size = 0.047
            rvecs, tvecs, _ = aruco.estimatePoseSingleMarkers(corners, size, camera_matrix, dist_coeffs)

            for i in range(len(ids)):
                tvec = np.array(tvecs[i]).round(2)
                last_translation = tvec
                rvec = np.array(rvecs[i])
                rvec_deg = np.degrees(rvec).round(0)
                if measurement is None:
                    # print(f"Marker {ids[i]} at {tvec} // {rvec_deg}")
                    new_list = tvec.tolist()[0] + rvec_deg.tolist()[0]
                    shared_list[:] = new_list                    

        # Display the resulting frame
        frame = cv2.flip(frame, 1)
        cv2.imshow('ArUco Marker Tracking', frame)

        # Break the loop if 'q' is pressed
        key = cv2.waitKey(1)
        if key == ord('q'):
            break
        elif key == ord('m'):
            measurement = last_translation
            # print(f"Measurement: {measurement}")
        elif key == ord('n'):
            measurement = None
        
        if measurement is not None:
            distance_to_measurement = (np.linalg.norm(measurement - last_translation) * 100).round(2)
            # print(f"Distance to measurement: {distance_to_measurement}cm")

    # Release the capture and close windows
    cap.release()
    cv2.destroyAllWindows()


class MRIViewer:
    def __init__(self, file_path: str):
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
        # print(f"Original shape: {old_shape}, New shape: {new_shape}")

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
    
    def visualize_3d(self, slice_x=None, slice_y=None, slice_z=None, mesh_file=None, shared_list=None):
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
        # plotter.add_volume(grid, cmap='gray', opacity=opacity)
        
        # Add mesh if provided
        if mesh_file:
            mesh = pv.read(mesh_file)
            # mesh = mesh.scale([10, 10, 10])
            # plane = pv.Plane(center=(0, 25, 25 + 4), direction=(0, 1, 0), i_size=50, j_size=50)
            # mesh = mesh.merge(plane)
            plotter.add_mesh(mesh, color='white', opacity=0.5)
                
        plotter.show(interactive_update=True)

        last_rotation = np.array([0.0, 0.0, 0.0])

        position_history = deque(maxlen=25)
        rotation_history = deque(maxlen=25)

        while True:
            position_history.append(shared_list[:3])
            rotation_history.append(shared_list[3:])

            # Position is easy to average
            filtered_position_history = filter_outliers(np.array(position_history))
            print("kept", len(filtered_position_history), "out of", len(position_history))
            rolling_average_position = np.mean(filtered_position_history, axis=0)

            # Rotation is harder to average because it loops around
            rotation_rad = np.radians(np.array(rotation_history))
            
            # However, sin & cos can easily be averaged
            sin_sum = np.sum(np.sin(rotation_rad), axis=0)
            cos_sum = np.sum(np.cos(rotation_rad), axis=0)
            
            # And then we reconstruct
            rolling_average_rotation = np.degrees(np.arctan2(sin_sum, cos_sum))
            
            position = np.array(rolling_average_position)
            rotation = np.array(rolling_average_rotation)
            print("position", position)
            print("rotation", rotation)

            mesh.translate((position * 1000) - mesh.center, inplace=True)

            # Undo the previous rotation
            if np.linalg.norm(last_rotation) != 0:
                mesh.rotate_vector(
                    vector=last_rotation / np.linalg.norm(last_rotation),
                    angle=-np.linalg.norm(last_rotation),
                    inplace=True
                )

            # Apply the new rotation
            mesh.rotate_vector(
                vector=rotation / np.linalg.norm(rotation),
                angle=np.linalg.norm(rotation),
                inplace=True
            )
            
            last_rotation = rotation

            plotter.update()
            time.sleep(1.0 / 30)
    
    def start(self):
        manager = multiprocessing.Manager()
        shared_list = manager.list([0.0] * 6)  # Initialize with a list containing six elements

        tracker_process = multiprocessing.Process(target=aruco_tracker, args=(shared_list,))
        tracker_process.start()

        slice_x, slice_y, slice_z = None, None, None
        # Interactive slicing with a slider
        # slice_x = self.interactive_slicing(dim='x')
        # slice_y = viewer.interactive_slicing(dim='y')
        # slice_z = viewer.interactive_slicing(dim='z')
        print(slice_x, slice_y, slice_z)
        self.visualize_3d(slice_x=slice_x, slice_y=slice_y, slice_z=slice_z, mesh_file='tfus-device-model.stl', shared_list=shared_list)

if __name__ == "__main__":
    # Start the Aruco tracker thread
    viewer = MRIViewer(file_path='healthy-t1.nii')
    viewer.start()

    viewer.join()

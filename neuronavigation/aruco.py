import cv2
import cv2.aruco as aruco
import numpy as np
import os

def track(camera_matrix, dist_coeffs):
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
            size = 0.0355
            # size = 0.047
            rvecs, tvecs, _ = aruco.estimatePoseSingleMarkers(corners, size, camera_matrix, dist_coeffs)

            for i in range(len(ids)):
                tvec = np.array(tvecs[i]).round(2)
                last_translation = tvec
                rvec = np.array(rvecs[i])
                rvec_deg = np.degrees(rvec).round(0)
                if measurement is None:
                    print(f"Marker {ids[i]} at {tvec} // {rvec_deg}")

        # Display the resulting frame
        frame = cv2.flip(frame, 1)
        cv2.imshow('ArUco Marker Tracking', frame)

        # Break the loop if 'q' is pressed
        key = cv2.waitKey(1)
        if key == ord('q'):
            break
        elif key == ord('m'):
            measurement = last_translation
            print(f"Measurement: {measurement}")
        elif key == ord('n'):
            measurement = None
        
        if measurement is not None:
            distance_to_measurement = (np.linalg.norm(measurement - last_translation) * 100).round(2)
            print(f"Distance to measurement: {distance_to_measurement}cm")

    # Release the capture and close windows
    cap.release()
    cv2.destroyAllWindows()

def save_markers(padding=56, size=400):
    # Save markers
    aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_6X6_250)
    os.makedirs("markers", exist_ok=True)
    for i in range(250):
        if os.path.exists(f"markers/marker_{i}.png"):
            continue
        img = aruco.generateImageMarker(aruco_dict, i, size)
        # add 56 padding each side white
        img = cv2.copyMakeBorder(img, padding, padding, padding, padding, cv2.BORDER_CONSTANT, value=[255, 255, 255])
        cv2.imwrite(f"markers/marker_{i}.png", img)

def calibrate_camera():
    H = 3
    W = 4
    # Prepare object points (0,0,0), (1,0,0), (2,0,0) ..., (6,5,0)
    objp = np.zeros((H*W,3), np.float32)
    objp[:,:2] = np.mgrid[0:W,0:H].T.reshape(-1,2)

    # Arrays to store object points and image points from all the images
    objpoints = [] # 3d point in real world space
    imgpoints = [] # 2d points in image plane

    # Capture several images of a chessboard from different angles
    cap = cv2.VideoCapture(0)
    for _ in range(1000):
        # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow('callibrations', frame)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Find the chess board corners
        ret, corners = cv2.findChessboardCorners(gray, (W,H), None)
        print("Ret, corners:", ret, corners)

        if ret:
            objpoints.append(objp)
            imgpoints.append(corners)
        
        if len(objpoints) >= 20:
            break

        # Break the loop if 'q' is pressed
        if cv2.waitKey(50) & 0xFF == ord('q'):
            break

    cap.release()

    # Calibrate the camera
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

    np.save("camera_matrix.npy", mtx)
    np.save("dist_coeffs.npy", dist)

    return mtx, dist

def main():
    save_markers(padding=0, size=512)
    # calibrate_camera()
    # camera_matrix = np.load("camera_matrix.npy")
    # dist_coeffs = np.load("dist_coeffs.npy")
    # track(camera_matrix, dist_coeffs)

if __name__ == '__main__':
    main()

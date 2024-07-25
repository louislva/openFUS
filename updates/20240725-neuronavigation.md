# Neuronavigation

### Our approach: ArUco markers + Invesalius

We're going to use [Invesalius](https://github.com/invesalius/invesalius3) neuronavigation software, and make an [ArUco](https://docs.opencv.org/4.x/d5/dae/tutorial_aruco_detection.html) integration to track it with a single webcam. Cheap, accurate, and easy to use.

We need to make hardware which has the ArUco markers on it. The points we need to track are: the ears + the device itself. With the ears especially, it's important that the ArUco markers are not occluded by slight turns of the head. Current ideas:

- Ear markers (Idea #1): ear plug + tooth pick + ArUco sign sticking out
- Ear markers (Idea #2): clamp on ear + ArUco sign attached to it
- Ear markers (Idea #3): glue a thin plastic sign-post to [a JLab sports ear bud](https://www.amazon.com/JLab-Air-Sport-Featuring-Bluetooth/dp/B09RGB47FJ?th=1)
- Device markers: 3d print a flat surface in shell + a stencil + spray paint an ArUco marker

### Other approaches you could do

- [End-to-end head 6D pose tracking](https://arxiv.org/pdf/2309.07654v1)
- Track ear keypoints from 2 views & estimate their 3d positions
    - [ViTPose](https://github.com/vitae-transformer/vitpose)
    - [X-Pose: track any keypoints](https://github.com/IDEA-Research/X-Pose)
- [End-to-end multiview pose tracking](https://www.youtube.com/watch?v=GAqhmUIr2E8)
- [Track ArUco markers placed on ears from 2 views & estimate their 3d positions with classic computer vision](https://docs.opencv.org/4.x/d5/dae/tutorial_aruco_detection.html)
- [Use Cotracker to just place tracks on ears initially and then HOLD STILL](https://co-tracker.github.io/)


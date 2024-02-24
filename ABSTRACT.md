The authors built a 3D and RGB door **DeepDoors Version 2.0 Dataset** with images from several indoor environments using a 3D Realsense camera D435. It is constituted by 3 parts, a 2D and 3D image classifcation part, a semantic segmentation part and an object detection part. Main Dataset features:

* The authors propose three different door state classifcation methods, where each one uses different types of information, and all are capable of working in real-time in low-power systems.
* The labelled dataset with RGB and depth images of ***closed***, ***open*** and ***semi-open*** doors for 2D and 3D state door classifcation.
* The dataset for 2D door segmentation with annotated doors and door frames.
* The dataset for 2D door detection properly annotated.

## Motivation

Every day, advancements in technology lead to the creation of new mobile robots equipped with superior components and software tailored for various purposes. These robots serve a multitude of functions, ranging from smart vacuum cleaners and delivery robots to security assistants and nursing aids, along with intelligent housekeeping systems. These innovations aim to alleviate the challenges people face in their daily tasks.

An essential aspect of these intelligent systems is the detection and classification of door states, which typically involve identifying whether a door is ***closed***, ***open***, or partially open (***semi-open***). This capability is crucial for ensuring the safe navigation of mobile robots within indoor spaces. As these systems often need to maneuver between rooms and interact with doors, providing them with accurate information about door states is imperative to facilitate seamless navigation.

The significance of door state classification extends beyond the realm of mobile robots and robotics. It can also find applications in assisting visually impaired individuals in safely navigating indoor environments. By providing information about the locations of doors and their current states, such technology can empower individuals with visual impairments to move between rooms with confidence and ease.

## Dataset description

The authors present three distinct methods for door state classification, each leveraging different types of information: 1) exclusively utilizing 3D data; 2) utilizing both 3D and 2D (RGB) data; and 3) relying solely on 2D (RGB) data. Their primary focus is on developing an approach suitable for low-power systems, such as single-board computers. The emphasis lies in refining door detection and state classification algorithms, independent of other aspects of robot hardware.

While many existing methods primarily concentrate on door detection without delving into state classification, some also incorporate door handle detection to facilitate robot grasping. The authors advocate for a protocol where, upon classifying the door state as ***closed***, the robot initiates a call for human assistance. If the door is detected as ***open***, the robot proceeds to traverse it effortlessly. In cases where the door is identified as ***semi-open***, the robot may either navigate around it or attempt to gently push it open.

The DeepDoors Version 2.0 Dataset comprises three main components: a section dedicated to 2D and 3D image classification, another for semantic segmentation, and a third for object detection. This dataset was curated using a portable system consisting of a Raspberry Pi 3 B+ powered by a power bank, alongside a 3D Realsense Camera (model D435). Notably, this camera boasts a wider horizontal viewing angle (86°) compared to its vertical counterpart (57°). To ensure comprehensive coverage of the door area within the images, the camera was rotated by 90°. Positioned 135 cm above the floor, the camera captured various images of doors and their surroundings, featuring diverse textures, sizes, and potential obstacles such as furniture, individuals, or other objects that partially obscure the door. The objective was to assemble a dataset that reflects real-world scenarios realistically. Additionally, to capture different perspectives of the same door, the camera's pose was adjusted accordingly. The images were sourced from diverse locations including the authors' university, public spaces, and private residences. Each image was manually captured using a portable system equipped with a Jetson Nano, and subsequently annotated using the [CVAT](https://www.cvat.ai/) tool for door segmentation, detection, and state classification.

This dataset is constituted by RGB images and corresponding depth images with a size equal to 480 × 640 pixels. The depth images are in grey-scale with pixels values between 0 and 255 and the authors used a depth scale equal to 1/16. The depth in meters is equal to depth scale * pixel value, for example, if the pixel value is equal to 32 it means that that pixel is 2 m away from the viewer (1∕16 ∗ 32 = 2). In total, this dataset has 3000 door images, 1000 samples for each class: ***open***, ***closed*** and ***semi-open*** doors. This dataset was randomly split into: 300 samples for validation, 300 for testing and 2400 for training.

<img src="https://github.com/dataset-ninja/deep-doors2/assets/120389559/e10edca8-9e7f-48f5-b279-5372dcf626ed" alt="image" width="600">

<span style="font-size: smaller; font-style: italic;">Sample images from the DeepDoors Version 2.0 dataset</span>

An advantageous aspect of the authors' dataset extends beyond its ample sample size—it offers a rich diversity of environments. The dataset comprises images sourced from various settings, including university facilities, residential interiors, countryside homes nestled amidst nature's beauty. Additionally, the dataset includes numerous blurred images to replicate real-world conditions, along with images featuring obstacles that partially obscure the doors, mirroring practical scenarios.


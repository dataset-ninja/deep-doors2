**DeepDoors Version 2.0 Dataset** is a dataset for instance segmentation, semantic segmentation, object detection, classification, and monocular depth estimation tasks. It is used in the robotics and safety industries. 

The dataset consists of 6000 images with 6142 labeled objects belonging to 1 single class (*door*).

Images in the Deep Doors v2.0 dataset have pixel-level instance segmentation annotations. Due to the nature of the instance segmentation task, it can be automatically transformed into a semantic segmentation (only one mask for every class) or object detection (bounding boxes for every object) tasks. All images are labeled (i.e. with annotations). There are 3 splits in the dataset: *train* (4800 images), *test* (600 images), and *val* (600 images). Alternatively, the dataset could be split into 3 door positions: ***close*** (2000 images), ***open*** (2000 images), and ***semi-open*** (2000 images). Additionally, images are grouped by ***im_id***. The dataset was released in 2021 by the Nova lincs, Portugal and Universidade da Beira Interior, Portugal.

<img src="https://github.com/dataset-ninja/deep-doors2/raw/main/visualizations/poster.png">

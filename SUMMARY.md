**DeepDoors Version 2.0 Dataset** is a dataset for instance segmentation, semantic segmentation, object detection, classification, and monocular depth estimation tasks. It is used in the robotics industry. 

The dataset consists of 6000 images with 6142 labeled objects belonging to 1 single class (*door*).

Images in the DeepDoors2 dataset have pixel-level instance segmentation annotations. Due to the nature of the instance segmentation task, it can be automatically transformed into a semantic segmentation (only one mask for every class) or object detection (bounding boxes for every object) tasks. All images are labeled (i.e. with annotations). There are 3 splits in the dataset: *train* (4800 images), *test* (600 images), and *val* (600 images). Alternatively, the dataset could be split into 3 door positions: ***close*** (2000 images), ***open*** (2000 images), and ***semi-open*** (2000 images). Additionally, images are grouped by ***im_id***. The dataset was released in 2021 by the <span style="font-weight: 600; color: grey; border-bottom: 1px dashed #d3d3d3;">Nova lincs, Portugal</span> and <span style="font-weight: 600; color: grey; border-bottom: 1px dashed #d3d3d3;">Universidade da Beira Interior, Portugal</span>.

<img src="https://github.com/dataset-ninja/deep-doors2/raw/main/visualizations/poster.png">

# Neural Network Training Model

## Overview

This repository contains three Jupyter notebooks showcasing the training of YOLOv8 models for traffic light and vehicle detection:
1. **Neural_Network(yolov8n).ipynb** (YOLOv8n)
2. **Neural_Network(yolov8m).ipynb** (YOLOv8m)
3. **Neural_Network(yolov8x).ipynb** (YOLOv8x)

Each notebook demonstrates the steps required to:
- Download and organise a custom traffic light dataset from Roboflow.
- Filter, label, and integrate additional classes from the COCO dataset (bicycle, car, motorcycle, bus).
- Merge all data, adjust labels, and create a configuration file (`data.yaml`).
- Train a YOLOv8 model on this combined dataset.
- Produce a final model checkpoint (`best.pt`).

All resulting model weights (`best.pt`) are renamed and stored in the **Models** directory as:
- `yolo8n.pt` for YOLOv8n  
- `yolo8m.pt` for YOLOv8m  
- `yolo8x.pt` for YOLOv8x  

## Repository Structure

```
.
├── Models
│   ├── yolo8n.pt
│   ├── yolo8m.pt
│   └── yolo8x.pt
├── Neural_Network(yolov8n).ipynb
├── Neural_Network(yolov8m).ipynb
├── Neural_Network(yolov8x).ipynb
└── README.md
```

- **Models/**: Contains final trained model weights (`.pt` files).
- **Neural_Network(yolov8n).ipynb**: Training notebook using YOLOv8n.
- **Neural_Network(yolov8m).ipynb**: Training notebook using YOLOv8m.
- **Neural_Network(yolov8x).ipynb**: Training notebook using YOLOv8x.

## Requirements

- Python 3.7+
- PyTorch (GPU support recommended)
- [Ultralytics](https://github.com/ultralytics/ultralytics) for YOLOv8
- COCO API (`pycocotools`)
- Albumentations
- OpenCV
- Matplotlib
- Pandas
- Requests
- TQDM

Installation commands are included at the beginning of each notebook:
```bash
!pip install pycocotools requests albumentations ultralytics matplotlib pandas tqdm
```

## Steps in Each Notebook

1. **Install Required Libraries**  
   Installs the necessary Python packages for YOLOv8 training, data loading, and augmentation.

2. **Import Libraries**  
   Imports modules like `torch`, `albumentations`, `requests`, `matplotlib`, etc.

3. **Prepare Dataset Directories**  
   Creates local directories for custom and COCO data.

4. **Download Custom Dataset**  
   - Downloads a custom traffic light dataset from Roboflow.
   - Extracts it into a structured folder layout: `train`, `valid`, `test`.

5. **Filter and Adjust Labels**  
   - Removes unnecessary classes (e.g., standard traffic lights) while keeping only pedestrian traffic lights (green and red).
   - Remaps class IDs to ensure consistency.

6. **Download and Filter COCO**  
   - Downloads COCO 2017 annotations, train images, and validation images.
   - Filters only the desired classes (`bicycle`, `car`, `motorcycle`, `bus`).
   - Converts COCO bounding boxes into YOLO format.

7. **Merge Datasets**  
   - Combines the filtered COCO images/labels with the custom traffic light dataset.

8. **Create `data.yaml`**  
   - Specifies paths for training, validation, and test sets.
   - Lists all class names and the number of classes (`nc`).

9. **Train the YOLOv8 Model**  
   - Selects a YOLOv8 model checkpoint (`yolov8n.pt`, `yolov8m.pt`, or `yolov8x.pt`).
   - Defines training hyperparameters (e.g., `epochs`, `batch`, `imgsz`).
   - Initiates model training.

10. **Final Model Weights**  
    - The best model weights are saved in the `Models` directory as `yolo8n.pt`, `yolo8m.pt`, or `yolo8x.pt`.

## Usage

1. **Download the Repository as a ZIP**  
   Download the repository from the repository page as a ZIP file and extract it to your desired location.

2. **Open a Notebook**  
   Open any of the three notebooks in JupyterLab, Google Colab, or any environment of your choice:
   - `Neural_Network(yolov8n).ipynb`
   - `Neural_Network(yolov8m).ipynb`
   - `Neural_Network(yolov8x).ipynb`

3. **Run the Cells**  
   Execute each cell in order. The code will:
   - Install the necessary packages.
   - Download and organise the dataset.
   - Train the YOLOv8 model.
   - Produce a final `best.pt` file in the `Models` folder.

## Results

- **Training**: Each notebook trains a YOLOv8 model (n, m, or x).  
- **Performance**: Validation metrics (mAP, precision, recall) are displayed upon training completion.  
- **Inference**: The final `best.pt` weights can be used for inference with the Ultralytics YOLO command line or within a Python script.

## References

- [Ultralytics YOLOv8 Documentation](https://docs.ultralytics.com)
- [Roboflow Dataset Management](https://roboflow.com)
- [COCO Dataset](https://cocodataset.org)

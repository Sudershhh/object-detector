# Image and Video Recognition Analysis

This project uses **AWS Rekognition** to perform **label detection** on both images and videos, displaying detected objects with confidence scores and overlaying bounding boxes using **OpenCV** for visualization.

## Features

* **Image Label Detection**: Analyze images to identify objects, scenes, and their confidence scores.
* **Video Label Detection**: Analyze videos frame-by-frame to detect and visualize objects with bounding boxes.
* **Confidence Scores**: Displays how confident AWS Rekognition is about each detected object.
* **Bounding Box Overlay**: Visualize detected labels with bounding boxes using **OpenCV**.
* **Local Saving**: Save the processed video or image with bounding boxes for offline viewing.

## Tech Stack

* **AWS Services**:
   * Amazon S3 (Storage)
   * Amazon Rekognition (Image/Video Analysis)
   * AWS SNS (Notifications for video job completion)
* **Python**
* **OpenCV** (for video/image processing)
* **Boto3** (AWS SDK for Python)

## Project Architecture

### 1. Image Analysis Workflow

1. Upload an image to an **Amazon S3 bucket**.
2. AWS Rekognition detects labels and confidence scores for the image.
3. Fetch the results using Python and **Boto3**.
4. Overlay bounding boxes on the image using **OpenCV**.
5. Display and save the processed image locally.

### 2. Video Analysis Workflow

1. Upload a video to an **Amazon S3 bucket**.
2. Start video analysis using **AWS Rekognition Video**.
3. Wait for **SNS notifications** for job completion.
4. Fetch label detection results (bounding boxes and timestamps).
5. Use **OpenCV** to overlay bounding boxes and labels on each frame.
6. Save the final video with bounding boxes locally.

## How to Run

### 1. Prerequisites

Make sure you have the following:
* **AWS CLI** configured with your access keys.
* IAM role with permissions for S3, Rekognition, and SNS.
* **Python 3.8+** installed.
* Install required libraries:

```bash
pip install boto3 opencv-python-headless
```

### 2. Set Up AWS Resources

* Create an **S3 bucket** and upload your video/image files.
* Set up an **SNS topic** to get notifications for video processing jobs.
* Update your **IAM Role ARN** and **SNS Topic ARN** in the code.

### 3. Run the Project

#### For Image Label Detection

Run the following script:

```bash
python imageRecognition.py
```

**Example Output:**
* Detected objects displayed with confidence scores.
* Processed image saved locally with bounding boxes.

#### For Video Label Detection

Run the following script:

```bash
python videoRecognition.py
```

**Example Output:**
* Labels and bounding boxes displayed on the video in real time.
* Processed video saved locally as `videoname-output.mp4`.

## Future Improvements

* Smooth object tracking across video frames using advanced tracking algorithms.
* Add support for real-time video streaming with label detection.
* Explore additional AWS Rekognition features like facial recognition or text detection.

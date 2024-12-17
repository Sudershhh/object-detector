import boto3
import cv2
import time

# Rekognition and S3 clients
rekognition = boto3.client('rekognition')
s3 = boto3.client('s3')

# Specify your S3 bucket and video
bucket_name = "image-labels-generator"
video_name = "dinner.mp4"

# Start label detection job
response = rekognition.start_label_detection(
    Video={'S3Object': {'Bucket': bucket_name, 'Name': video_name}}
)
job_id = response['JobId']
print(f"Started label detection job with ID: {job_id}")

# Wait for job completion
print("Waiting for job to complete...")
while True:
    result = rekognition.get_label_detection(JobId=job_id)
    status = result['JobStatus']
    if status == 'SUCCEEDED':
        print("Job completed successfully.")
        break
    elif status == 'FAILED':
        print("Job failed.")
        exit(1)
    time.sleep(10)

# Download the video from S3
video_path = f"./{video_name}"
s3.download_file(bucket_name, video_name, video_path)

# Extract and parse Rekognition labels
labels = result['Labels']

# Open video using OpenCV
cap = cv2.VideoCapture(video_path)
fps = int(cap.get(cv2.CAP_PROP_FPS))  # Get frames per second
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Initialize VideoWriter for saving output
output_path = f"./{video_name}-output.mp4"
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for .mp4 files
out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

# Utility function to filter labels for the current frame
def get_labels_for_frame(timestamp, labels, threshold_ms=100):
    relevant_labels = []
    for label_data in labels:
        label_timestamp = label_data['Timestamp']  # Timestamp in milliseconds
        if abs(label_timestamp - timestamp) <= threshold_ms:
            relevant_labels.append(label_data)
    return relevant_labels

# Play video, overlay labels, and save output
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Video playback complete.")
        break

    # Get current frame timestamp in milliseconds
    current_timestamp = int(cap.get(cv2.CAP_PROP_POS_MSEC))

    # Get relevant labels for this frame
    relevant_labels = get_labels_for_frame(current_timestamp, labels)

    # Overlay labels and bounding boxes on the frame
    for label_data in relevant_labels:
        label = label_data['Label']['Name']
        confidence = label_data['Label']['Confidence']
        instances = label_data['Label'].get('Instances', [])

        for instance in instances:
            bbox = instance.get('BoundingBox', {})
            if bbox:
                # Convert bbox coordinates to pixel values
                left = int(bbox['Left'] * frame_width)
                top = int(bbox['Top'] * frame_height)
                width = int(bbox['Width'] * frame_width)
                height = int(bbox['Height'] * frame_height)

                # Draw the bounding box
                cv2.rectangle(frame, (left, top), (left + width, top + height), (0, 255, 0), 2)

                # Add label and confidence as text
                text = f"{label} ({confidence:.1f}%)"
                cv2.putText(frame, text, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Write the frame to the output video
    out.write(frame)

    # Display the frame
    cv2.imshow("Video with Labels", frame)

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
out.release()
cv2.destroyAllWindows()

print(f"Labeled video saved to: {output_path}")

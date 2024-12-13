import boto3
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
from io import BytesIO

def detectLabels(photo, bucket):

    client = boto3.client('rekognition')

    response = client.detect_labels(Image={
        'S3Object':{
            'Bucket': bucket,
            'Name': photo
        }
    }, MaxLabels=10)

    print('Detected labels for ' + photo)
    print()
    for label in response['Labels']:
        print("Label:", label['Name'])
        print("Confidence:", label['Confidence'])
        print()


    s3 = boto3.resource('s3')
    object = s3.Object(bucket, photo)
    imageData = object.get()['Body'].read()
    image = Image.open(BytesIO(imageData))

    plt.imshow(image)
    ax = plt.gca()
    for label in response['Labels']:
        for instance in label.get('Instances', []):
            bbox = instance['BoundingBox']
            left = bbox['Left'] * image.width
            top = bbox['Top'] * image.height
            width = bbox['Width'] * image.width
            height = bbox['Height'] * image.height
            rect = patches.Rectangle((left, top), width, height, linewidth=1, edgecolor='r', facecolor='none')
            ax.add_patch(rect)
            label_text = label['Name'] + ' (' + str(round(label['Confidence'], 2)) + '%)'
            plt.text(left, top - 2, label_text, color='r', fontsize=8, bbox=dict(facecolor='white', alpha=0.7))
    plt.show()

    return len(response['Labels'])



def main():
    photo='food.jpg'
    bucket='image-labels-generator'
    labelsCount = detectLabels(photo, bucket)
    print("Labels Detected : ", labelsCount)


if __name__ == "__main__":
    main()
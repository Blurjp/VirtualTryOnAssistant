import os
import cv2
import uuid
import boto3
import glob
import requests
from PIL import Image
from io import BytesIO
import argparse

s3 = boto3.client('s3')
bucket_name = 'your-bucket-name'  # replace with your bucket name

def image_process(image1_url, image2_url, user_id):
    parser = argparse.ArgumentParser()
    parser.add_argument('--background', type=bool, default=True, help='Define removing background or not')
    opt = parser.parse_args()

    # download and temporarily save images
    response1 = requests.get(image1_url)
    img1 = Image.open(BytesIO(response1.content))
    img1_path = f'static/{user_id}_origin_web.jpg'
    img1.save(img1_path)

    response2 = requests.get(image2_url)
    img2 = Image.open(BytesIO(response2.content))
    img2_path = f'static/{user_id}_cloth_web.jpg'
    img2.save(img2_path)

    # Read input images
    img1=cv2.imread(img1_path)
    ori_img=cv2.resize(img1,(768,1024))
    cv2.imwrite("./origin.jpg",ori_img)

    img2=cv2.imread(img2_path)
    cloth_img=cv2.resize(img2,(768,1024))
    cv2.imwrite("./cloth.jpg",cloth_img)

    # Resize input image
    img=cv2.imread('origin.jpg')
    img=cv2.resize(img,(384,512))
    cv2.imwrite('resized_img.jpg',img)

    # Get mask of cloth
    print("Get mask of cloth\n")
    os.system("python get_cloth_mask.py")

    # Get openpose coordinate using posenet
    print("Get openpose coordinate using posenet\n")
    os.system("python posenet.py")

    # Generate semantic segmentation using Graphonomy-Master library
    print("Generate semantic segmentation using Graphonomy-Master library\n")
    os.chdir("./Graphonomy-master")
    os.system("python exp/inference/inference.py --loadmodel ./inference.pth --img_path ../resized_img.jpg --output_path ../ --output_name /resized_segmentation_img")
    os.chdir("../")

    # code continues...

    # Run HR-VITON to generate final image
    print("\nRun HR-VITON to generate final image\n")
    os.chdir("./HR-VITON-main")
    os.system("python3 test_generator.py --cuda True --test_name test1 --tocg_checkpoint mtviton.pth --gpu_ids 0 --gen_checkpoint gen.pth --datasetting unpaired --data_list t2.txt --dataroot ./test")
    os.chdir("../")

    # Add Background or Not
    l=glob.glob("./Output/*.png")

    # Add Background
    if opt.background:
        for i in l:
            img=cv2.imread(i)
            img=cv2.bitwise_and(img,img,mask=mask_img)
            img=img+back_ground
            cv2.imwrite(i,img)

    # Remove Background
    else:
        for i in l:
            img=cv2.imread(i)
            cv2.imwrite(i,img)

    # generate a unique identifier for the final image
    image_uuid = uuid.uuid4()
    final_image_path = f"./static/{user_id}_{image_uuid}.png"
    cv2.imwrite(final_image_path, img)

    # upload the final image to S3
    with open(final_image_path, 'rb') as data:
        s3.upload_fileobj(data, bucket_name, f'{user_id}_{image_uuid}.png')

    # remove the images after processing
    os.remove(img1_path)
    os.remove(img2_path)
    os.remove(final_image_path)

    # construct the final image S3 URL
    final_image_s3_url = f'https://{bucket_name}.s3.amazonaws.com/{user_id}_{image_uuid}.png'

    return final_image_s3_url

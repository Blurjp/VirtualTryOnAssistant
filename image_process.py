import os
import cv2
import uuid
import boto3
import glob
import requests
from PIL import Image
from io import BytesIO
import argparse
from utils import get_config

# Create the S3 client
config = get_config()
s3 = boto3.client('s3',
                  aws_access_key_id=config['YOUR_AWS_ACCESS_KEY_ID'],
                  aws_secret_access_key=config['YOUR_AWS_SECRET_ACCESS_KEY'],
                  region_name=config['YOUR_AWS_REGION_NAME'])

generatedImageS3Bucket = config['S3_PROFILE_IMAGE_BUCKET_NAME']

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--background', type=bool, default=True, help='Define removing background or not')
    return parser.parse_args()

def download_and_save_image(image_url, user_id, image_type):
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))
    img_path = f'static/{user_id}_{image_type}.jpg'
    img.save(img_path)
    return img_path

def resize_and_save_image(img_path, user_id, output_name, size=(768,1024)):
    img = cv2.imread(img_path)
    resized_img = cv2.resize(img, size)
    output_path = f'./{user_id}_{output_name}.jpg'
    cv2.imwrite(output_path, resized_img)
    return output_path

def execute_command(command, change_dir=None):
    if change_dir:
        os.chdir(change_dir)
    os.system(command)
    if change_dir:
        os.chdir("../")

def background_operations(opt, mask_img, back_ground):
    l = glob.glob("./Output/*.png")
    for i in l:
        img = cv2.imread(i)
        if opt.background:
            img = cv2.bitwise_and(img, img, mask=mask_img)
            img = img + back_ground
        cv2.imwrite(i, img)

def upload_to_s3(file_path, bucket_name, s3_key):
    with open(file_path, 'rb') as data:
        s3.upload_fileobj(data, bucket_name, s3_key)

def remove_files(*file_paths):
    for file_path in file_paths:
        os.remove(file_path)

def image_process(user_id, image1_url, image2_url):
    opt = parse_arguments()

    img1_path = download_and_save_image(image1_url, user_id, "origin_web")
    img2_path = download_and_save_image(image2_url, user_id, "cloth_web")

    resize_and_save_image(img1_path, user_id, "origin")
    resize_and_save_image(img2_path, user_id, "cloth")

    execute_command("python get_cloth_mask.py")
    execute_command("python posenet.py")
    execute_command("python exp/inference/inference.py --loadmodel ./inference.pth --img_path ../resized_img.jpg --output_path ../ --output_name /resized_segmentation_img", "./Graphonomy-master")

    # ... Other os.system commands can be refactored using execute_command function ...

    execute_command("python3 test_generator.py --cuda True --test_name test1 --tocg_checkpoint mtviton.pth --gpu_ids 0 --gen_checkpoint gen.pth --datasetting unpaired --data_list t2.txt --dataroot ./test", "./HR-VITON-main")

    # you might want to define mask_img and back_ground before calling this
    background_operations(opt, mask_img, back_ground)

    image_uuid = uuid.uuid4()
    final_image_path = f"./static/{user_id}_{image_uuid}.png"
    cv2.imwrite(final_image_path, img)

    s3_key = f'{user_id}_{image_uuid}.png'
    upload_to_s3(final_image_path, bucket_name, s3_key)
    remove_files(img1_path, img2_path, final_image_path)

    final_image_s3_url = f'https://{bucket_name}.s3.amazonaws.com/{s3_key}'

    return final_image_s3_url

from flask import Flask, render_template, request, redirect, url_for, jsonify
from image_process import image_process
import os

app = Flask(__name__)
#run_with_ngrok(app)

data_list = []

@app.route('/', methods=['GET', 'POST'])
def main():
    return render_template('main.html')

@app.route('/acceptImages', methods = ['GET', 'POST'])
def accept_images():
    data = request.get_json()

    user_id = data['user_id']
    profile_image_url = data['profile_image_url']
    cloth_image_url = data['cloth_image_url']

    # run main.py
    final_image_s3_url = image_process(user_id, profile_image_url, cloth_image_url)
    return jsonify({"final_image_s3_url": final_image_s3_url})

@app.route('/fileUpload', methods = ['GET', 'POST'])
def file_upload():
    if request.method == 'POST':
        f = request.files['file']
        f_src = 'static/origin_web.jpg'

        f.save(f_src)
        return render_template('fileUpload.html')

@app.route('/fileUpload_cloth', methods = ['GET', 'POST'])
def fileUpload_cloth():
    if request.method == 'POST':
        f = request.files['file']
        f_src = 'static/cloth_web.jpg'

        f.save(f_src)
        return render_template('fileUpload_cloth.html')

@app.route('/view', methods = ['GET', 'POST'])
def view():
    print("inference start")

    terminnal_command ="python main.py"
    os.system(terminnal_command)

    print("inference end")
    return render_template('view.html', data_list=data_list)

if __name__ == '__main__':
    app.run()
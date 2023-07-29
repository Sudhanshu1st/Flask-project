from flask import Flask, render_template, request, redirect, url_for
import os
import glob
import subprocess
from base64 import b64encode
from IPython.display import HTML

app = Flask(__name__)

@app.route('/')
def home():
    img_list = glob.glob1('examples/source_image', '*.png')
    img_list.sort()
    img_list = [item.split('.')[0] for item in img_list]
    return render_template('index.html', img_list=img_list)

@app.route('/process', methods=['POST'])
def process():
    img_name = request.form['image_name']
    img_path = f'examples/source_image/{img_name}.png'
    audio_path = request.files['audio']

    # Save the uploaded audio file
    audio_path.save('./uploaded_audio.wav')

    # Run SadTalker inference.py with subprocess
    subprocess.call(['python', 'inference.py', '--driven_audio', './uploaded_audio.wav',
                     '--source_image', img_path,
                     '--result_dir', './static/results', '--still', '--preprocess', 'full', '--enhancer', 'gfpgan'])

    # Find the generated mp4 file
    mp4_files = glob.glob('./static/results/*.mp4')
    if mp4_files:
        mp4_name = mp4_files[0]
    else:
        mp4_name = None

    return render_template('result.html', mp4_name=mp4_name)

if __name__ == '__main__':
    app.run(debug=True)

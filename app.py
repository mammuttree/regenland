from flask import Flask, render_template
import os

app = Flask(__name__)

# List of image filenames
images = sorted(os.listdir('static/images'))
num_images = len(images)  # Calculate the number of images

@app.route('/')
def index():
    return render_template('index.html', images=images, num_images=num_images)

if __name__ == '__main__':
    app.run(debug=True)

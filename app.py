from fastai.vision import *
import flask
from flask import Flask , request , render_template, flash, redirect, url_for #jsonify
import os
from werkzeug.utils import secure_filename
import shutil


UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = set(['png','jpg','jpeg'])


app = flask.Flask(__name__ , template_folder='templates')

app.secret_key = "abcd1234"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16*512*512

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def upload_form():
	return render_template('main.html')

@app.route('/', methods=['POST'])

def upload_image():

	remove_old_file()

	if 'file' not in request.files:
		flash('No file part')
		return redirect(request.url)
	file = request.files['file']

	if file.filename == '':
		flash('No image selected for uploading')
		return redirect(request.url)
		
	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)

		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

		template,prediction = classify_image(filename)
		flash('Image successfully uploaded and classified')

		return flask.render_template(template,name = prediction.lower(), result = prediction, filename=filename)
	else:
		flash('Allowed image types are -> png, jpg, jpeg, gif')
		return redirect(request.url)


def classify_image(filename):

	path = 'model'
	learn = load_learner(path)

	file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

	img = open_image(file_path)

	pred_class, pred_idx, outputs = learn.predict(img)

	prediction = pred_class.obj

	return "main.html",prediction

def remove_old_file():
	folder = 'static/uploads/'

	for filename in os.listdir(folder):
		file_path = os.path.join(folder, filename)
		try:
			if os.path.isfile(file_path) or os.path.islink(file_path):
				os.unlink(file_path)
			elif os.path.isdir(file_path):
				shutil.rmtree(file_path)
		except Exception as e:
			print('Failed to delete %s. Reason: %s' % (file_path, e))

@app.route('/display/<filename>')
def display_image(filename):

	return redirect(url_for('static', filename='uploads/' + filename), code=301)

if __name__ == "__main__":
    app.run()
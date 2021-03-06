
import os
from flask import Flask, request, redirect, url_for, send_from_directory, jsonify
from werkzeug.utils import secure_filename

from avahi.service import AvahiService

UPLOAD_FOLDER = '/usr/src/app/img/'
ALLOWED_EXTENSIONS = set(['txt', 'jpg', 'jpeg'])
DUMMY_SYNC_RESPONSE = {"exposure": "auto", "wb": 1234, "filename": "test.jpg"}

## Web server
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

def create_gif(sequence_id):
    wanted_filename = "/usr/src/app/output/%s.gif" % sequence_id
    all_filenames = os.listdir(UPLOAD_FOLDER)
    wanted_inputs = []
    for file in all_filenames:
        if file.split("_")[0] == sequence_id:
            wanted_inputs.append(file)
    with imageio.get_writer(wanted_filename, mode='I') as writer:
    for filename in wanted_inputs:
        image = imageio.imread(filename)
        writer.append_data(image)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@app.route('/sync')
def hello_world():
	return jsonify(DUMMY_SYNC_RESPONSE)


# MVP

# Set initial wanted filename
# Wait for button input
#	Trigger IO
#	Take own picture and store in folder
#	Wait for 3 slaves to upload their pictures
#	Gifify
#	Rotate wanted filename
#	<repeat...>

# POST MVP

# Serve sync settings
# Wait for all three slaves to sync filename

if __name__ == "__main__":
    avahiservice = AvahiService("resin webserver", "_http._tcp", 80)
    app.run(host='0.0.0.0', port=80, debug=True)

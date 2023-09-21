from speech_manipulation import playback_speed_changing, volume_changing, speech_to_txt
import os
from flask import Flask, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename

def isnum(num):
    try:
        num = float(num)
        return True
    except:
        return False


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'data'
app.config['MAX_CONTENT_LENGTH'] = 1 * 1000**3

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() == 'wav'

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            if not os.path.exists(app.config['UPLOAD_FOLDER']):
                os.mkdir(app.config['UPLOAD_FOLDER'])

            filename = 'audio.wav'
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('manipulation', name = filename))
    return ''''
    <!doctype html>
    <title>Transcribe and modification audio</title>
    <h1>Transcribe and modification audio</h1>
    <h2>Upload an audio file with the extension .wav up to 1 GB</h2>
    <h3></h3>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    </html>'
    '''


@app.route('/manipulation/<name>', methods=['GET', 'POST'])
def manipulation(name):
    if request.method == 'POST':
        index = request.form['index']
        if index == 'transcribe':
            return redirect(url_for('transcribe', name = name))
        if index == 'modification':
            return redirect(url_for('modification', name = name))
    return ''''
    <!doctype html>
    <title>Transcribe and modification audio</title>
    <h1>Transcribe or modification audio</h1>
    <form method=post enctype=multipart/form-data>
      <input type="submit" name="index" class="btn btn-dark" value="transcribe">
      <input type="submit" name="index"class="btn btn-dark" value="modification">
    </form>
    </html>'
    '''

@app.route('/transcribe/<name>')
def transcribe(name):
    text = speech_to_txt(name)
    return text


@app.route('/modification/<name>', methods=['GET', 'POST'])
def modification(name):
    if request.method == 'POST':
        cof_volume = request.form.get('volume')
        cof_speed = request.form.get('speed')

        if isnum(cof_volume) or cof_volume == '':
            if cof_volume != '':
                cof_tr = True
                cof_volume = float(cof_volume)
                volume_changing(name, cof_volume)        

        if isnum(cof_speed) or cof_speed == '':
            if cof_speed != '':
                cof_speed = float(cof_speed)
                if cof_tr:
                    name = f'Modified_{name}'
                playback_speed_changing(name, cof_speed)

        if not cof_tr:
            name = f'Modified_{name}'
        return send_from_directory(app.config['UPLOAD_FOLDER'], name, mimetype='wav',)
    
    return ''''
    <!doctype html>
    <title>Modification audio</title>
    <h1>Modification audio</h1>
    <form method=post enctype=multipart/form-data>
      <div class="slidecontainer">
      <p>Speed modifier: <span id="demo"></span></p>
      <input type="range" min="1" max="100" value="50" class="slider" id="myRange", name="speed">
      </div><br/>
      <label for="volume" class="form-label">Volume change (±dB):</label><br/>
      <input type="volume" name="volume"><br/><br/>
      <button type="submit" class="btn btn-primary">modification</button>     
    </form>
    </html>'
    '''



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

from flask import Flask, render_template, request, redirect
from werkzeug import secure_filename

# Initialize the Flask application
app = Flask(__name__)
from parse_rest.connection import register
from parse_rest.datatypes import Object, GeoPoint
from parse_rest.user import User
import os
import time
import hashlib
dir_path = os.path.dirname(os.path.abspath(__file__))

parse_credentials = {
    "application_id": "M5tnZk2K6PdF82Ra8485bG2VQwPjpeZLeL96VLPj",
    "rest_api_key": "VBGkzL4uHsOw0K1q33gHS4Qk2FWEucRHMHqT69ex",
    "master_key": "r9XwzOtLCoduZgmcU27Kc0sbexW4jWTOuBHStUFb",
}

register(parse_credentials["application_id"], parse_credentials["rest_api_key"])


class Temp(Object):
    pass

def genFilename(filename):
    filename = filename.replace(" ","")
    epoch = str(int(time.time()*100))
    filename=epoch+filename
    return filename

def genReadableFilename(filename):
    pass

@app.route('/', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Get the FileStorage instance from request
        file = request.files['file']
        name=request.form['title']
        wallet=request.form['wallet']

        filename = secure_filename(file.filename)
        md5 = hashlib.md5(file.read()).hexdigest()
        filename=genFilename(filename)
        filename="%s_%s"%(md5,filename)

        file.save(os.path.join('%s/temp/'%dir_path, filename))
        os.system("convert %s/temp/%s -quality 10 %s/temp/%s"%(dir_path,filename,dir_path,filename))
        url = 'http://orch.in/euclid/%s'%filename
        t = Temp(name=name, wallet=wallet,url=url)
        t.save()

        return redirect("/e/%s"%t.objectId)
        
    all_files = Temp.Query.all()
    return render_template('index.html',all_files=all_files)


@app.route('/e/<file_id>')
def channel(file_id):
    t = Temp.Query.get(objectId=file_id)

    return render_template('file.html',
        filename = t.name,
        url=t.url,
        wallet=t.wallet,
        type = "img")

# Run
if __name__ == '__main__':
    app.run(debug=True,host = "0.0.0.0")

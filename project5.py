from flask import *
import jwt
import os
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from datetime import datetime
import base64
from PIL import Image
from io import BytesIO
from werkzeug.utils import secure_filename


app = Flask(__name__)


SECRET_KEY = 'e6b7fb115e6442609eb851e29163674b'

app.config['UPLOAD_FOLDER'] = os.path.join('static', 'image')

if not os.path.exists(app.config['UPLOAD_FOLDER'] ):
    os.makedirs(app.config['UPLOAD_FOLDER'] )

rate_limit = Limiter( get_remote_address, app= app, default_limits=["5 per minute"])
#,storage_uri="redis://localhost:6379",
#  storage_options={"socket_connect_timeout": 30},
#  strategy="fixed-window")

@app.route('/protected', methods=['GET'])
@rate_limit.limit("5 per minute")
def protected():
    token = request.headers.get('Authorization')
    try:
        jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return jsonify({'message': 'Access granted'})
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token has expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token'}), 401


@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('homePage.html')

# Login page
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()   # a JSON request with user data
    if data['username'] == 'John' and data['password'] == 'Qwerty@54321':
        token = jwt.encode({'username': data['username']}, SECRET_KEY, algorithm='HS256')
        print(token)
        return jsonify({'token': token})
        #return render_template('homePage.html')
    

    #if request.form['username'] == 'John' and request.form['password'] == 'Qwerty@54321':
    #   session['logged_in'] = True
    #    token = jwt.encode({'username': ['username']}, SECRET_KEY, algorithm='HS256')
    #    print(token)
    #    return render_template('homePage.html')

   
    else:
        return jsonify({'message': 'Authentication failed'}), 401
    
#capture image
@app.route('/captureImage' , methods=['GET','POST'] )
def capture():
    filename =''
    image_data_url = request.form.get('image')
    if request.method == 'POST':
        image_data = base64.b64decode(image_data_url.split(',')[1])
        img = Image.open(BytesIO(image_data))
        timestamp = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        filename = f"img_{timestamp}.jpg"
        print(filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        img.save(file_path, 'jpg')
        error_message = 'Image successfully captured'
        return render_template('captureImage.html', filename=filename)
    return render_template('captureImage.html', filename=filename)


# upload image
@app.route('/upload_Image', methods=['POST'])
def upload_image():
    error_message = None
    if 'image' not in request.files:
        error_message = 'image input is required in the form'
        print(error_message)
    else:
        file = request.files['image']
        if file.filename == '':
            error_message = 'image not selected'
            print(error_message)

        elif not allowed_images(file.filename):
            error_message = 'invalid image format, allowed formats are - png, jpg, jpeg, gif only'
            print(error_message)

        else:
            filename = secure_filename(file.filename)
            if os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
                error_message = 'Image with the same name already exists.'
                print(error_message)

            else:
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                print('Image successfully uploaded')
                return redirect(url_for('image', filename=filename))
        return render_template('homePage.html', error_message=error_message)


#image name display   
@app.route('/image/<filename>')
def image(filename):
    #check if the image file exists or not in the folder
    if os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
        return render_template('image.html', filename=filename)
    else:
        return render_template('notexist.html'), 404

#image display
@app.route('/capturedimage/<filename>')
def captured(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], path=filename)

#image formats checking function
def allowed_images(filename):
    if '.' not in filename:
        return False
    allowed_extensions = ('png', 'jpg', 'jpeg', 'gif')
    return filename.rsplit('.')[-1].lower() in allowed_extensions


#if session['logged_in'] == True:
#    def get_token():
#        token = jwt.encode({'user':['username']}, SECRET_KEY, algorithm='HS256')
#        return jsonify({'token': token})



#@app.route('/logout', methods=['POST'])
#def logout():


#if __name__ == "__main__":
#    app.run(debug=True)


    



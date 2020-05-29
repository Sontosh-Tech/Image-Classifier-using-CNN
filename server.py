# -*- coding: utf-8 -*-
"""
Created on Thu May 28 22:36:14 2020

@author: Sontosh
"""
import numpy as np
#import tensorflow
#from keras.models import Sequential
#from keras.layers import Convolution2D,MaxPooling2D,Flatten,Dense
#from keras.preprocessing.image import ImageDataGenerator
from flask import Flask,request,render_template,redirect,flash,make_response
from werkzeug.utils import secure_filename
import os
from keras.models import load_model
from keras.preprocessing import image



app=Flask(__name__)
app.config['UPLOAD_FOLDER']='.\\static\\img\\'
app.config['SECRET_KEY']='secret@123'
app.config["TEMPLATE_AUTO_RELOAD"]=True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['MAX_COOKIE_SIZE']=-1


def allowed_extn(filename):
    extn = set(['png', 'jpg', 'jpeg', 'gif'])
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in extn

@app.route('/', methods=['GET','POST'])
def upload():
    if request.method=='POST':
        if 'upload' in request.form.get('action'):
            pic=request.files['pic']
            if pic.filename!='':
                if pic and allowed_extn(pic.filename):
                    pic1=secure_filename(pic.filename)
                    #target = os.path.join(app.config['UPLOAD_FOLDER'], 'img')
                    destination = '\\'.join([app.config['UPLOAD_FOLDER'], 'img.jpg'])
                    pic.save(destination)
                    r=make_response(render_template('index.html',file=pic1,flag=1))
                    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
                    r.headers["Pragma"] = "no-cache"
                    r.headers["Expires"] = "0"
                    r.headers['Cache-Control'] = 'public, max-age=0'
                    return r
                    #return render_template('index.html',file=pic1)
                else:
                    flash('Allowed image types are -> png, jpg, jpeg, gif')
                    return redirect(request.url)
            else:
                flash('No image selected for uploading')
                return redirect(request.url)
        else:
            model = load_model('model.h5')

            #target = os.path.join(app.config['UPLOAD_FOLDER'], 'img')
            destination = '\\'.join([app.config['UPLOAD_FOLDER'], 'img.jpg'])
            test_image = image.load_img(destination,target_size=(64,64))
            test_image = image.img_to_array(test_image)
            test_image = np.expand_dims(test_image, axis=0)
            prediction = model.predict(test_image)

            if prediction[0][0] == 1:
                result = 'Building'
            elif prediction[0][1]  == 1:
                result = 'Forest'
            elif prediction[0][2]  == 1:
                result = 'Glacier'
            elif prediction[0][3]  == 1:
                result = 'Mountain'
            elif prediction[0][4]  == 1:
                result = 'Sea'
            elif prediction[0][5]  == 1:
                result = 'Street'
            else:
                result = 'Something unknown'
            r = make_response(render_template('index.html', prediction='This is an image of {}'.format(result),file='img.jpg'))
            r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
            r.headers["Pragma"] = "no-cache"
            r.headers["Expires"] = "0"
            r.headers['Cache-Control'] = 'public, max-age=0'
            return r
            #return render_template('index.html', prediction='This is image of {}'.format(result),file='img.jpg')

    r = make_response(render_template('index.html'))
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r
    #return render_template('index.html')

if __name__=='__main__':
    app.run(debug=True)


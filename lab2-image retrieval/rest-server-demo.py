#!flask/bin/python
################################################################################################################################
# ------------------------------------------------------------------------------------------------------------------------------
# This file implements the REST layer. It uses flask micro framework for server implementation. Calls from front end reaches
# here as json and being branched out to each projects. Basic level of validation is also being done in this file. #
# -------------------------------------------------------------------------------------------------------------------------------
################################################################################################################################
from flask import Flask, jsonify, abort, request, make_response, url_for, redirect, render_template
from flask_httpauth import HTTPBasicAuth
from werkzeug.utils import secure_filename
import os
import shutil
import numpy as np
from search import recommend
import re
import tarfile
from datetime import datetime
from scipy import ndimage
from scipy.misc import imsave

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
from tensorflow.python.platform import gfile

app = Flask(__name__, static_url_path="")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
auth = HTTPBasicAuth()

# ==============================================================================================================================
#                                                                                                                              
#    Loading the extracted feature vectors for image retrieval                                                                 
#                                                                          						        
#                                                                                                                              
# ==============================================================================================================================
extracted_features = np.zeros((10000, 2048), dtype=np.float32)
with open('saved_features_recom.txt') as f:
    for i, line in enumerate(f):
        extracted_features[i, :] = line.split()
print("loaded extracted_features")


# ==============================================================================================================================
#                                                                                                                              
#  This function is used to do the image search/image retrieval
#                                                                                                                              
# ==============================================================================================================================
@app.route('/imgUpload', methods=['GET', 'POST'])
# def allowed_file(filename):
#    return '.' in filename and \
#           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 处理图像搜索结果并返回到前端
def upload_img():
    print("image upload")
    result = 'static/result'
    if not gfile.Exists(result):
        os.mkdir(result)
        print("创建static/result文件夹")
    shutil.rmtree(result)


    if request.method == 'POST' or request.method == 'GET':
        print(request.method)
        # check if the post request has the file part
        if 'file' not in request.files:
            print('No file part')
            return redirect(request.url)

        file = request.files['file']
        print(file.filename)
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            print('No selected file')
            return redirect(request.url)
        if file:  # and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # 将用户上传的图片save到uploads文件夹下
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            inputloc = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            # 将用户上传的图片save为static/result/uploadImg.[后缀名]

            # 进行图片搜索并将搜索出的图片save至static/result文件夹中
            recommend(inputloc, extracted_features)
            shutil.copy(os.path.join(app.config['UPLOAD_FOLDER'], filename),os.path.join('static/result','uploadImg.'+filename.split('.')[-1]))
            #file.save(os.path.join('static/result','uploadImg.'+filename.split('.')[-1]))

            os.remove(inputloc)

            # region 存储图片文件的路径
            image_path = "/result"
            image_list = [os.path.join(image_path, file) for file in os.listdir(result)
                          if not (file.startswith('.')or file.startswith('u'))]
            print("image_list:",image_list)
            # endregion

            # region 提取result图片的数字编号名称
            img_name_lists=[re.match('im(\d+).jpg',file).group(1) for file in os.listdir(result)
                           if not (file.startswith('.') or file.startswith('u'))]
            name=[i for i in img_name_lists]
            print("img_name_lists",img_name_lists)
            #endregion

            # region 提取result图片的tag
            dicts={} # 存放img-tag键值对
            tagfile_list=os.listdir('database/tags')
            for tagfile in tagfile_list:
                if len(img_name_lists)==0:
                    break

                with open("database/tags/"+tagfile,"r") as fp:
                    img_lists=fp.readlines()
                    for i in range(0,len(img_lists)):
                        img_lists[i]=img_lists[i].rstrip()

                    tmp=list(filter(lambda x:img_lists.count(x)!=0, img_name_lists))
                    for img in tmp:
                        print("img{}-----tagfile{}".format(img,tagfile))
                        dicts.setdefault(img,tagfile.split('.')[0])
                    img_name_lists=list(set(img_name_lists).difference(set(tmp)))

                    # for img in img_name_lists[::-1]:
                    #     if img_lists.count(img):
                    #         print("img{}-----tagfile{}".format(img,tagfile))
                    #         dicts.setdefault(img,tagfile.split('.')[0])
                    #         img_name_lists.remove(img)
            print(dicts)
            # endregion

            # region 构造传送的json
            length=len(dicts) #照片数量(9)
            print("共检索出{}张照片".format(length))
            images={}
            print("image_list",image_list)
            print("dict",dicts)
            images.setdefault('uploaded',os.path.join('/result','uploadImg.'+filename.split('.')[-1]))
            k=0
            for i in range(length):
                if name[i] in dicts.keys():
                    print("image{}:[{},{}]".format(k,image_list[i],dicts[name[i]]))
                    images.setdefault('image'+str(k),[image_list[i],dicts[name[i]]])
                    k+=1
            # endregion
            print(images)
            return jsonify(images)


# ==============================================================================================================================
#                                                                                                                              
#                                           Main function                                                        	            #						     									       
#  				                                                                                                
# ==============================================================================================================================
@app.route("/")
def main():
    return render_template("mainPage.html")


if __name__ == '__main__':
    app.run(debug=True, host='localhost')

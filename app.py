from flask import Flask,render_template,request,session
import pickle
import numpy as np
import csv
import pandas as pd
from flask_mysqldb import MySQL
modeldtc=pickle.load(open('desision.pkl','rb'))
modelrfc=pickle.load(open('randomforest.pkl','rb'))
app = Flask(__name__)
app.secret_key="supersecrectkey"
@app.route('/')
def hello_world():
    return render_template("home.html")



@app.route('/predict',methods=['POST'])
def make_prediction():
    
    input_features=[float(x) for x in request.form.values()]
    features_values=[np.array(input_features)]
    features_names=['age','sex','cp','terstbps','chol','fbs','restecg','thalach','exang','oldpeak','slope','ca','thal']
    age1=request.form['age']
    sex1=request.form['sex']
    cp1=request.form['cp']
    terstbps1=request.form['trestbps']
    chol1=request.form['chol']
    fbs1=request.form['fbs']
    restecg1=request.form['restecg']
    thalach1=request.form['thalach']
    exang1=request.form['exang']
    oldpeak1=request.form['oldpeak']
    slope1=request.form['slope']
    ca1=request.form['ca']
    thal1=request.form['thal']
    

    #arr=np.array([[age,sex,cp,terstbps,chol,fbs,restecg,thalach,exang,oldpeak,slope,ca,thal]])
    df = pd.DataFrame(features_values, columns=features_names)
   
    pred=modelrfc.predict(df);

    return render_template("after.html",data=pred,data1=age1,data2=sex1,data3=cp1,data4=terstbps1,data5=chol1,data6=fbs1,data7=restecg1,data8=thalach1,data9=exang1,data10=oldpeak1,data11=slope1,data12=ca1,data13=thal1)


@app.route('/login',methods=['GET','POST'])
def load_dashboard():
    if('user' in session and session['user']=="admin"):
        return render_template("index.html")
    if request.method=='POST':
        #redirect to admin Panel
        username=request.form.get('uname')
        password=request.form.get('upass')
        if username=="admin" and password=="admin":
            session['user']=username
            return render_template("index.html");
        return render_template("admin.html")
    return render_template("admin.html")

@app.route('/loaddata')
def load_data():
    if('user' in session and session['user']=="admin"):
        return render_template("load.html")
    return render_template("load.html")

@app.route('/adminpage')
def load_Admin():
    if('user' in session and session['user']=="admin"):
        return render_template("index.html")
    return render_template("index.html")



@app.route('/chart')
def load_chart():
    values = [30.6, 90.5,90.6 , 80,60.3]
    labels = ['decision tree', 'random forest classifier', 'k neighbors classifier', 'support vector machine','logistic regression']
    colors = ['#ff0000','#0000ff','#ffffe0','#008000','#FFA500',]
    return render_template('chart.html', values=values, labels=labels, colors=colors)






@app.route('/logout')
def logout_to_home():
    session.pop('user',None)
    return render_template("home.html")



if __name__ == "__main__":
    app.run(debug=True)
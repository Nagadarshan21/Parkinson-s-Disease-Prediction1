from flask import *
import pandas as pd
import pickle
import numpy as np
from xgboost import XGBClassifier

app = Flask(__name__)

#load model
model = pickle.load(open('model.pkl', 'rb'))

@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/upload')
def upload():
    return render_template('upload.html')

@app.route('/preview', methods=['POST'])
def preview():
    if request.method == 'POST':
        dataset = request.files['datasetfile']
        df = pd.read_csv(dataset,encoding = 'unicode_escape')
        df.set_index('Id', inplace=True)
        return render_template("preview.html",df_view = df)	

@app.route('/prediction')
def prediction():
    return render_template('prediction.html')

@app.route('/predict',methods=['POST'])
def predict():
    int_feature = [x for x in request.form.values()]
    
    final_features = [np.array(int_feature, dtype=object)]
    
    result=model.predict(final_features)
    
    if result == 1:
        result = "Abnormal"
    else:
        result = 'Normal'
	
    return render_template('prediction.html', prediction_text= result)

@app.route('/performance')
def performance():
    return render_template('performance.html')

@app.route('/chart')
def chart():
    return render_template('chart.html')

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template, url_for, request
# import config
import sys

from .utils import pred_tags

app = Flask(__name__)

# Config options - Make sure you created a 'config.py' file.
#app.config.from_object('config')
app.config.from_pyfile('config.py')
# To get one variable, tape app.config['MY_VARIABLE']

@app.route('/',methods=["POST","GET"])
def index():
    #print('This is standard output', file=sys.stdout)
    # if request.method == 'GET':
        # return f"The URL /data is accessed directly. Try going to '/form' to submit form"
    if request.method == 'POST':
        form_data = request.form['question'] #request.form('question')
        print('form_data = '+form_data, file=sys.stdout)
        data_result = pred_tags(form_data)[0]
        for res in data_result:
            print('data_result_i = '+res, file=sys.stdout)
        
        # myDict = {data_result[i]: data_result[i] for i in range(0, len(data_result), 1)}
        
        return render_template('result.html', data_result = data_result)
    else:
        return render_template('index.html')
    # return "Hello world !"

@app.route('/result')
def result():

        # print('This is standard output', file=sys.stdout)
        # print(form_data)
        return render_template('result.html')
 
    # response = request.form
    # print(response)
    # return render_template('result.html')

# if __name__ == "__main__":
    # app.run()
    
    
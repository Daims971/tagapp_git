from flask import Flask, render_template, url_for, request
# import config
import sys


app = Flask(__name__)

# Config options - Make sure you created a 'config.py' file.
#app.config.from_object('config')
app.config.from_pyfile('config.py')
# To get one variable, tape app.config['MY_VARIABLE']

@app.route('/',methods=["POST"])
def index():
    #print('This is standard output', file=sys.stdout)
    # if request.method == 'GET':
        # return f"The URL /data is accessed directly. Try going to '/form' to submit form"
    if request.method == 'POST':
        form_data = request.form('question')
        data_result = form_data
        
        return render_template('result.html', data_result)
    else:
        return render_template('index.html')
    # return "Hello world !"

@app.route('/result')
def result():

        print('This is standard output', file=sys.stdout)
        print(form_data)
        return render_template('result.html')
 
    # response = request.form
    # print(response)
    # return render_template('result.html')

# if __name__ == "__main__":
    # app.run()
    
    
#task1-create flask project

from flask import Flask #importing flask
app=Flask(__name__)#create constructor
@app.route('/')
def hello_world(): #function
    return "Hello World!"

if __name__=='__main__':
    app.run()

from flask import Flask , render_template , request
app= Flask(__name__)
import getPredictions
from getPredictions import getPredictions
import connection
from connection import finalAlgorithm
# from connection import companyAlreadyPresent

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/', methods=["GET","POST"])
def companyName():
    companyName = request.form["companyName"]
    print(companyName)
    finalAlgorithm(companyName)
    return "kam ho raha hai"

app.run(debug= True)

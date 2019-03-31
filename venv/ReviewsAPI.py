from AmazonReviews import AmazonReview
from flask import Flask,redirect,url_for,request,render_template
from MongoDBUtil import MongoPersist
import sys
app = Flask(__name__)

@app.route('/review',methods=['POST'])
def login():
    if request.method == 'POST':
        reviewurl = request.form['reviewUrl']
        review = AmazonReview()
        result = 'Successfully loaded review content into Database'
        try:
             review.reviewWrap(reviewurl)
        except Exception as e:
           result='Not able to process you request.Please try after sometime.'
        return render_template("status.html", result=result)



@app.route('/reviewstore/<name>')
def reviewstore(name):
    return name



@app.route('/reviewSearch')
def reviewsearch():
    if request.method == 'GET':
        query = request.args.get('personName')
        result = "query results found"
        m = MongoPersist()
        try:
            result = m.searchMongodb(query)
        except:
            result = 'Not able to process you request.Please try after sometime.'
        return render_template("searchResults.html", result=result)
        #return str(result)

if __name__ == '__main__':
    app.run(debug= True)

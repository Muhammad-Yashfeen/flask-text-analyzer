from flask import Flask, render_template, request, Response
from bson.json_util import dumps
import os
import pymongo
from datetime import datetime
from bson.objectid import ObjectId
mongodb_uri = 'mongodb+srv://yashfeenaliskills_db_user:YaAK1234@python.lk5ulld.mongodb.net/?appName=python'
client = pymongo.MongoClient(mongodb_uri)
db = client['Text_Analyzer']
analyses = db.analyses
feedbacks = db.feedbacks

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

def analyze_text(text):
    char_count = len(text)
    lst = text.split()
    word_count = len(lst)
    dct = {}
    for word in lst:
        if word in dct:
            dct[word] += 1
        else:
            dct[word] = 1
    tup_dct = dct.items()
    sorted_words = sorted(tup_dct, key = lambda x : x[1], reverse =True)
    most_frequent_word = sorted_words[0][0]
    unique_words = set(lst)
    variety = (len(unique_words) / len(lst)) * 100
    analysis = {'text' : text, 'word_count' : word_count, 'character_count' : char_count, 'most_frequent_word' : most_frequent_word, 'word_variety' : variety, 'created_at' : datetime.now(), 'sorted_words' : sorted_words}
    return analysis
@app.route('/')
def home():
    techs = ['HTML', 'CSS', 'Python', 'Flask', 'MongoDB', 'PyMongo', 'REST API']
    name = '30 Days Of Python Programming'
    return render_template('home.html', techs=techs, name=name, title='Home')

@app.route('/about')
def about():
    name = '30 Days Of Python Programming'
    return render_template('about.html', name=name, title='About us')

@app.route('/post', methods= ['GET','POST'])
def post():
    name = 'Text Analyzer'
    if request.method == 'GET':
         return render_template('post.html', name = name, title = name)
    if request.method =='POST':
        content = request.form['content']
        if not content.strip():
            message = 'Please enter some text to analyze.'
            return render_template('post.html', name=name, title = name, message = message)
        analysis = analyze_text(content)
        word_count = analysis['word_count']
        char_count = analysis['character_count']
        most_frequent_word = analysis['most_frequent_word']
        variety = analysis['word_variety']
        sorted_words = analysis['sorted_words']
        analyses.insert_one(analysis)
        return render_template('result.html', char_count = char_count, word_count = word_count, most_frequent_word = most_frequent_word, variety = variety, sorted_words = sorted_words)

@app.route('/history')
def history():
    analysis_list = analyses.find()
    return render_template('history.html', analyses = analysis_list)

@app.route('/feedback', methods= ['GET','POST'])
def feedback():
    name = 'Feedback'
    if request.method == 'GET':
        feedback_list = feedbacks.find()
        return render_template('feedback.html', name = name, feedbacks = feedback_list)
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        feedback = request.form['feedback']
        if not name.strip() or not email.strip() or not feedback.strip():
            message = 'Please fill in all required fields.'
            feedback_list = feedbacks.find()
            return render_template('feedback.html', message=message, feedbacks = feedback_list) 
        full_feedback = {'name' : name, 'email' : email, 'feedback': feedback, 'created_at' : datetime.now()}
        feedbacks.insert_one(full_feedback)
        feedback_list = feedbacks.find()
        return render_template('feedback.html', name = name, email = email, feedback = feedback, feedbacks = feedback_list)
@app.route('/api/v1.0/analyses', methods = ['GET'])
def get_analyses():
    analysis_list = analyses.find()
    return Response(dumps(analysis_list), mimetype ='application/json')
@app.route('/api/v1.0/analyses/<analysis_id>', methods = ['GET'])
def get_analysis(analysis_id):
    analysis = analyses.find_one({'_id' : ObjectId(analysis_id)})
    return Response(dumps(analysis), mimetype = 'application/json')
@app.route('/api/v1.0/analyses', methods = ['POST'])
def send_analyses():
    data = request.get_json()
    text = data['text'] 
    if not text.strip():
        return Response('Please enter some text.', mimetype = 'text/plain')
    analysis = analyze_text(text)
    analyses.insert_one(analysis)
    return Response('Text successfully sent', mimetype ='text/plain')
@app.route('/api/v1.0/analyses/<analysis_id>', methods = ['PUT'])
def update_analysis(analysis_id):
    content = request.get_json()
    text = content['text']
    if not text.strip():
        return Response('Please enter some text.', mimetype='text/plain')
    analysis = analyze_text(text)
    query = {'_id' : ObjectId(analysis_id)}
    analyses.update_one(query, {'$set' : analysis})
    return Response('Text updated successfully!', mimetype = 'text/plain')
@app.route('/api/v1.0/analyses/<analysis_id>', methods = ['DELETE'])
def delete_analysis(analysis_id):
    analyses.delete_one({'_id' : ObjectId(analysis_id)})
    return Response('Text deleted successfully!', mimetype = 'text/plain')
@app.route('/api/v1.0/analyses', methods = ['DELETE'])
def delete_all_analysis():
    analyses.delete_many({})
    return Response('All Analysis successfully deleted', mimetype = 'text/plain')
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
from flask import Flask, render_template, request
import os
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
@app.route('/')
def home():
    techs = ['HTML', 'CSS', 'Flask', 'Python']
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
        char_count = len(content)
        word_count = len(content.split())
        lst = content.split()
        dct = {}
        for word in lst:
            if word in dct:
                dct[word] += 1
            else:
                dct[word] = 1
        tup_dct = dct.items()
        sorted_words = sorted(tup_dct, key= lambda x : x[1], reverse = True)
        most_frequent_word = sorted_words[0][0]
        setis = set(lst)
        variety = (len(setis) / len(lst)) * 100
        return render_template('result.html', char_count = char_count, word_count = word_count, most_frequent_word = most_frequent_word, variety = variety, sorted_words = sorted_words)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
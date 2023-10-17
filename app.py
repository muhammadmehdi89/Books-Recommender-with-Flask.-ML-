from flask import Flask,render_template,request
import pickle
import numpy as np

popular_df = pickle.load(open('popular.pk2','rb'))
pt = pickle.load(open('pt.pkl','rb'))
books = pickle.load(open('books1.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))
avg_rating = pickle.load(open('avg_rating.pkl','rb'))
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('home.html',
                           book_name = popular_df['Book-Title'].values,
                           author = popular_df['Book-Author'].values,
                           image = popular_df['Image-URL-M'].values,
                           ratings = popular_df['avg-rating'].values,
                           publisher = popular_df['Publisher'].values,
                           year = popular_df['Year-Of-Publication'].values)
@app.route('/recommender')
def recommend():
    
    return render_template('recommender.html')
@app.route('/recommender_books',methods=['post'])
def recommend_2():
    try:
        user_input = request.form.get('user_input')
        index = np.where(pt.index == user_input)[0][0]
        sim_books = similarity[index].argsort()[similarity[0].size-15:][::-1]

        data=[]
        for i in sim_books:
            item = []
            temp_df = books[books['Book-Title']==pt.index[i]]
            temp_df1 = avg_rating[avg_rating['Book-Title']==pt.index[i]]
            item.extend(temp_df.drop_duplicates('Book-Title')['Book-Title'].values)
            item.extend(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values)
            item.extend(temp_df1.drop_duplicates('Book-Title')['avg-rating'].values)
            item.extend(temp_df.drop_duplicates('Book-Title')['Book-Author'].values)
            item.extend(temp_df.drop_duplicates('Book-Title')['Publisher'].values)
            item.extend(temp_df.drop_duplicates('Book-Title')['Year-Of-Publication'].values)

            data.append(item)

        return render_template('recommender.html',data=data)
    except Exception as e:
        print(f"An error occurred: {e}")
        return render_template('recommender.html',data=[])

@app.route('/contact')
def contact():
    
    return render_template('contact.html')

if __name__=='__main__':
    app.run(debug=True)
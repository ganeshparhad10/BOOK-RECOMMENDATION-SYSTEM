
from flask import Flask, render_template, request
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

app = Flask(__name__)

# Load the datasets
books = pd.read_csv('books.csv')
users = pd.read_csv('users.csv')
ratings = pd.read_csv('ratings.csv')

# Handle missing values
books['Book-Title'] = books['Book-Title'].fillna('')
books['Book-Author'] = books['Book-Author'].fillna('')

# Content-Based Filtering
tfidf_vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf_vectorizer.fit_transform(books['Book-Title'] + ' ' + books['Book-Author'])

# Function to recommend books based on user input
def recommend_books(user_input):
    # Vectorize the user input
    user_tfidf = tfidf_vectorizer.transform([user_input])

    # Compute cosine similarities
    cosine_similarities = linear_kernel(user_tfidf, tfidf_matrix)

    # Get book indices based on similarity scores
    book_indices = cosine_similarities.argsort()[0][::-1]

    # Get top 5 recommended books
    recommended_books = books.loc[book_indices[:5], 'Book-Title'].tolist()
    return recommended_books

# Define routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def get_recommendation():
    user_input = request.form.get('book_input')
    recommended_books = recommend_books(user_input)
    return render_template('index.html', user_input=user_input, recommended_books=recommended_books)

if __name__ == '__main__':
    app.run(debug=True)


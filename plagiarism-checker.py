from flask import Flask, request, render_template
import re
import math

app = Flask(__name__)

@app.route("/")
def loadPage():
    return render_template('index.html', query="")

@app.route("/", methods=['POST'])
def cosineSimilarity():
    try:
        inputQuery = request.form['query']
        lowercaseQuery = inputQuery.lower()

        # Function to process text
        def process_text(text):
            word_list = re.sub(r'[^\w\s]', '', text).split()  # Remove punctuation
            return word_list

        # Compute cosine similarity
        def compute_cosine_similarity(query, database):
            dot_product = sum(a*b for a, b in zip(query, database))
            query_vector_magnitude = math.sqrt(sum(a**2 for a in query))
            database_vector_magnitude = math.sqrt(sum(b**2 for b in database))
            similarity = (dot_product / (query_vector_magnitude * database_vector_magnitude)) * 100
            return similarity

        query_word_list = process_text(lowercaseQuery)

        # Create universal set of unique words
        universal_set_of_unique_words = set()

        for word in query_word_list:
            universal_set_of_unique_words.add(word)

        # Load database text
        with open("database.txt", "r") as file:
            database_text = file.read().lower()

        database_word_list = process_text(database_text)

        for word in database_word_list:
            universal_set_of_unique_words.add(word)

        # Compute TF (Term Frequency) for query and database
        query_tf = [query_word_list.count(word) for word in universal_set_of_unique_words]
        database_tf = [database_word_list.count(word) for word in universal_set_of_unique_words]

        match_percentage = compute_cosine_similarity(query_tf, database_tf)

        output = "Input query text matches %0.02f%% with database." % match_percentage

        return render_template('index.html', query=inputQuery, output=output)
    except Exception as e:
        output = "Please Enter Valid Data"
        return render_template('index.html', query=inputQuery, output=output)

if __name__ == "__main__":
    app.run()

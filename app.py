import streamlit as st
import pickle
import pandas as pd
import requests 

# Function to fetch movie poster
def fetch_poster(movie_id):
    try:
        response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=935b19e32e5aecbb21ef2c792bc65df0&language=en-US")
        data = response.json()
        if response.status_code == 200 and data.get('poster_path'):
            return "https://image.tmdb.org/t/p/original" + data['poster_path']
        else:
            st.error(f"Error fetching poster for movie ID {movie_id}: {data.get('status_message', 'Unknown error')}")
            return "https://via.placeholder.com/200x300.png?text=No+Image"
    except Exception as e:
        st.error(f"Error fetching poster: {e}")
        return "https://via.placeholder.com/200x300.png?text=No+Image"

# Load the movie data
movies_dict = pickle.load(open('movies.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

# Set the title of the Streamlit app
st.title('Movie Recommender System')

# Create a selectbox for movie titles
option = st.selectbox('Select a Movie:', movies['title'].values)

# Add custom CSS to style the button
st.markdown("""
    <style>
    .stButton button {
        background-color: red;
        color: white; /* Text color */
        border: none;
    }
    .stButton button:hover {
        background-color: darkred; /* Button background color on hover */
        color: lightgreen; /* Text color on hover */
    }
    .recommendation-header {
        font-size: 14px; /* Smaller font size for movie titles */
    }
    </style>
""", unsafe_allow_html=True)

# Load the similarity data
similarity = pickle.load(open('similarity.pkl', 'rb'))

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distance = similarity[movie_index]
    movies_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id  # Assuming movie_id is stored in your DataFrame
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_posters

# Display the selected movie recommendations when the button is pressed
if st.button("Recommend"):
    names, posters = recommend(option)
    st.write(f"Here are some movies based on {option}!")

    cols = st.columns(len(names))  # Create columns based on the number of recommendations
    for col, name, poster in zip(cols, names, posters):
        with col:
            st.image(poster, caption=name, use_column_width=True)

import streamlit as st
import pandas as pd
import pickle
import requests
import time
def fetch_poster(movie_id,retries=3):
    headers = {
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIxN2E4NzA2ZDFiYzIwYTdkZDEyNWRmZWM0MjNhMzY2NCIsIm5iZiI6MTc2MjI3MTkwMC4wNjQ5OTk4LCJzdWIiOiI2OTBhMjI5Y2VmZDAwYjU2ZWFjOTZiNDEiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.CUgDfROoy6RLh2s2-SeJur0bxyjXPBVJRhihyEIKlK4",  # Replace with your actual token
        "accept": "application/json"
    }

    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            poster_path = data.get('poster_path')
            print(f"Poster path: {poster_path}")

            if poster_path:
                return f"https://image.tmdb.org/t/p/w500{poster_path}"
            else:
                print("Poster path is None or empty")
                return "https://via.placeholder.com/500x750?text=No+Image"


        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed for movie_id {movie_id}: {e}")
            time.sleep(2 * (attempt + 1))  # exponential backoff
    return "https://via.placeholder.com/500x750?text=No+Image"


def recommend(movie):
    movie_index=movies[movies['title']==movie].index[0]
    distances=similarity[movie_index]
    movies_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]

    recommended_movies=[]
    recommended_movies_posters=[]
    for i in movies_list:
        movie_id=movies.iloc[i[0]].movie_id
        #fetch poster from api
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
        time.sleep(0.5)
    return recommended_movies,recommended_movies_posters


movies_dict=pickle.load(open('movie_dict.pkl','rb'))
movies=pd.DataFrame(movies_dict)

similarity=pickle.load(open('similarity.pkl','rb'))
st.title('Movie Recommender System')
selected_movie_name=st.selectbox("Enter Movie Name",
    movies['title'].values)
if st.button('Recommend'):
    name,posters=recommend(selected_movie_name)

    col1,col2,col3,col4,col5=st.columns(5)
    with col1:
        st.text(name[0])
        st.image(posters[0])
    with col2:
        st.text(name[1])
        st.image(posters[1])
    with col3:
        st.text(name[2])
        st.image(posters[2])
    with col4:
        st.text(name[3])
        st.image(posters[3])
    with col5:
        st.text(name[4])
        st.image(posters[4])
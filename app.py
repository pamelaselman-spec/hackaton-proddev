import streamlit as st
import pandas as pd

# --- Cargar datasets ---
df_books   = pd.read_csv("data/books.csv", encoding='ISO-8859-1', on_bad_lines='skip',sep=';')
df_ratings = pd.read_csv("data/ratings.csv", encoding='ISO-8859-1', on_bad_lines='skip',sep=';')
df_users   = pd.read_csv("data/users.csv", encoding='ISO-8859-1', on_bad_lines='skip',sep=';')

# --- Integración básica ---
df_books_ratings = pd.merge(df_ratings, df_books, on="ISBN", how="inner")
df_full = pd.merge(df_books_ratings, df_users, on="User-ID", how="inner")
# --- Funciones de búsqueda ---
def get_top_books(n=10):
    return (df_full.groupby("Book-Title")["Book-Rating"]
            .mean()
            .sort_values(ascending=False)
            .head(n))

def get_books_by_author(author):
    return df_books[df_books["Book-Author"].str.contains(author, case=False, na=False)]["Book-Title"].unique()

def get_books_by_year(year):
    return df_books[df_books["Year-Of-Publication"] == year]["Book-Title"].unique()

def get_book_recommendation_stats(title):
    # Filtrar el libro por título
    libro = df_full[df_full['Book-Title'].str.contains(title, case=False, na=False)]
    
    if libro.empty:
        return f"No se encontró el libro '{title}' en el dataset."
    
    # Calcular métricas
    promedio = libro['Book-Rating'].mean()
    cantidad = libro['Book-Rating'].count()
    maximo = libro['Book-Rating'].max()
    minimo = libro['Book-Rating'].min()
    
    return {
        "Título": title,
        "Número de recomendaciones": cantidad,
        "Promedio de rating": round(promedio, 2),
        "Rating mínimo": minimo,
        "Rating máximo": maximo
    }

# --- Interfaz Streamlit ---
st.title("Chatbot de Libros 📚")

option = st.selectbox(
    "¿Qué quieres consultar?",
    ("Top libros mejor valorados", "Buscar por autor", "Buscar por año")
)

if option == "Top libros mejor valorados":
    n = st.slider("Número de libros", 5, 20, 10)
    st.write(get_top_books(n))

elif option == "Buscar por autor":
    author = st.text_input("Nombre del autor:")
    if author:
        st.write(get_books_by_author(author))

elif option == "Buscar por año":
    year = st.number_input("Año de publicación:", min_value=1900, max_value=2025, step=1)
    if year:
        st.write(get_books_by_year(year))

elif option == "Analizar recomendación de un libro":
    book_title = st.text_input("Título del libro:")
    if book_title:
        stats = get_book_recommendation_stats(book_title)
        st.write(stats)
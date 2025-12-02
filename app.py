import streamlit as st
import pandas as pd
import ollama

# Cargar datasets
df_books = pd.read_csv("books.csv", encoding="latin-1")
df_ratings = pd.read_csv("ratings.csv", encoding="latin-1")
df_users = pd.read_csv("users.csv", encoding="latin-1")
df_full = pd.merge(pd.merge(df_ratings, df_books, on="ISBN"), df_users, on="User-ID")

def get_top_books(n=5):
    return (df_full.groupby("Book-Title")["Book-Rating"]
            .mean()
            .sort_values(ascending=False)
            .head(n)
            .reset_index())

st.title("Chatbot de Libros con Ollama 📚")

user_input = st.text_input("Hazme una pregunta:")

if user_input:
    # Ollama interpreta la intención
    response = ollama.chat(
        model="llama2",
        messages=[{"role": "user", "content": user_input}]
    )
    st.write("🤖 Ollama dice:")
    st.write(response["message"]["content"])

    # Ejemplo de lógica conectada al dataset
    if "mejor valorados" in user_input.lower():
        st.write(get_top_books(5))
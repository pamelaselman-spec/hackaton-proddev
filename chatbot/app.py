import pandas as pd
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
import requests
import os
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/assets", StaticFiles(directory="assets"), name="assets")


OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")

# --- Load datasets ---
try:
    df_books   = pd.read_csv("data/books.csv", encoding="ISO-8859-1", sep=";", on_bad_lines="skip")
    df_ratings = pd.read_csv("data/ratings.csv", encoding="ISO-8859-1", sep=";", on_bad_lines="skip")
    df_users   = pd.read_csv("data/users.csv", encoding="ISO-8859-1", sep=";", on_bad_lines="skip")

    # Ensure correct types
    df_books["ISBN"] = df_books["ISBN"].astype(str)
    df_books["Book-Title"] = df_books["Book-Title"].astype(str)
    df_books["Book-Author"] = df_books["Book-Author"].astype(str)
    df_books["Publisher"] = df_books["Publisher"].astype(str)
    df_books["Year-Of-Publication"] = df_books["Year-Of-Publication"].astype(str)

    df_ratings["ISBN"] = df_ratings["ISBN"].astype(str)
    df_ratings["User-ID"] = df_ratings["User-ID"].astype(int)
    df_ratings["Book-Rating"] = df_ratings["Book-Rating"].astype(int)

    df_users["User-ID"] = df_users["User-ID"].astype(int)

except Exception as e:
    raise RuntimeError(f"Error loading datasets: {e}")

@app.get("/")
def root():
    return FileResponse("index.html")

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_input = data.get("message", "").lower()

    context = ""

    # --- Detect intent and extract keywords ---
    if "author" in user_input or "written by" in user_input or "by" in user_input:
        tokens = user_input.split("by")
        search_term = tokens[-1].strip() if len(tokens) > 1 else user_input
        related = df_books[df_books["Book-Author"].str.lower().str.contains(search_term, na=False)].head(10)
        if not related.empty:
            context = "\n".join([
                f"- **{row['Book-Title']}** by *{row['Book-Author']}*"
                for _, row in related.iterrows()
            ])

    elif "publisher" in user_input:
        tokens = user_input.split("publisher")
        search_term = tokens[-1].strip() if len(tokens) > 1 else user_input
        related = df_books[df_books["Publisher"].str.lower().str.contains(search_term, na=False)].head(10)
        if not related.empty:
            context = "\n".join([
                f"- **{row['Book-Title']}** (*{row['Publisher']}*)"
                for _, row in related.iterrows()
            ])

    elif "year" in user_input or "published" in user_input:
        tokens = user_input.split()
        years = [t for t in tokens if t.isdigit()]
        if years:
            related = df_books[df_books["Year-Of-Publication"].str.contains(years[0], na=False)].head(10)
            if not related.empty:
                context = "\n".join([
                    f"- **{row['Book-Title']}** ({row['Year-Of-Publication']})"
                    for _, row in related.iterrows()
                ])

    elif "rating" in user_input or "score" in user_input or "top" in user_input:
        merged = df_ratings.merge(df_books, on="ISBN")
        top_books = merged.groupby("Book-Title")["Book-Rating"].mean().sort_values(ascending=False).head(10)
        context = "\n".join([
            f"- **{title}** (average rating: {rating:.2f})"
            for title, rating in top_books.items()
        ])

    elif "title" in user_input or "book" in user_input:
        tokens = user_input.split()
        search_term = None
        if "with" in tokens:
            idx = tokens.index("with")
            if idx + 1 < len(tokens):
                search_term = tokens[idx + 1]
        elif "title" in tokens:
            idx = tokens.index("title")
            if idx + 1 < len(tokens):
                search_term = tokens[idx + 1]
        else:
            search_term = tokens[-1]

        if search_term:
            related = df_books[df_books["Book-Title"].str.lower().str.contains(search_term, na=False)].head(10)
            if not related.empty:
                context = "\n".join([
                    f"- **{row['Book-Title']}** by *{row['Book-Author']}*"
                    for _, row in related.iterrows()
                ])

    if not context:
        context = "No matches found. Try specifying title, author, publisher, year or rating."

    # --- Prompt for Ollama ---
    prompt = f"User asked: {data.get('message', '')}\n\nContext from dataset:\n{context}"

    response = requests.post(
        f"{OLLAMA_HOST}/api/generate",
        json={"model": "llama2", "prompt": prompt}
    )

    reply_json = response.json()
    bot_reply = reply_json.get("response", "No response generated.")

    return {
        "reply": bot_reply,
        "context": context
    }
import requests
import pandas as pd
import nltk
from nltk.corpus import stopwords
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

nltk.download('stopwords')
# Define the GraphQL endpoint
url = 'https://api.hardcover.app/v1/graphql'  # Replace with your actual GraphQL endpoint

# Define the GraphQL query
query = """
query Test {
  me {
    username
  }
  books(
    where: {title: {_like: "Harry Potter"}, subtitle: {_eq: "The Creature Vault"}}
  ) {
    description
    book_category_id
    title
    subtitle
  }
}

"""

# Set up the headers, assuming authorization might be needed
headers = {
    'Content-Type': 'application/json',
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ2ZXJzaW9uIjoiNiIsImlkIjoyMjYxNCwibG9nZ2VkSW4iOnRydWUsInN1YiI6IjIyNjE0IiwiaWF0IjoxNzMzMDI3ODA4LCJleHAiOjE3NjQ0Nzc3MDgsImh0dHBzOi8vaGFzdXJhLmlvL2p3dC9jbGFpbXMiOnsieC1oYXN1cmEtYWxsb3dlZC1yb2xlcyI6WyJ1c2VyIl0sIngtaGFzdXJhLWRlZmF1bHQtcm9sZSI6InVzZXIiLCJ4LWhhc3VyYS1yb2xlIjoidXNlciIsIlgtaGFzdXJhLXVzZXItaWQiOiIyMjYxNCJ9fQ.IRlB1Pvw-zrybAWrKsWy9mB-ZzEIyBFBdYA9kZMzg3M"  # Ajoutez cette ligne si un token est requis
}

# Make the request
response = requests.post(url, json={'query': query}, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()
    
    # Extract the books' descriptions and categories
    books = data['data']['books']
    
    if books:
        print("Books found similar to 'Harry Potter':")
        for book in books:
            description = book['description']
            category_id = book['book_category_id']
            print(f"Description: {description}\nCategory ID: {category_id}\n")
    else:
        print("No books found matching 'Harry Potter'.")
else:
    print(f"Error: {response.status_code}")
    print(response.text)


#----

query2 = """
query GetBooksByCategory($category_id: Int!) {
  books(
    where: {book_category_id: {_eq: $category_id }, description: {_is_null: false}}
    limit: 50
  ) {
    title
    subtitle
    description
  }
}


"""
category_id = 1
variables = {
    "category_id": category_id
}
response = requests.post(url, json={'query': query2, 'variables': variables}, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()
    
    # Extraire les livres dans la même catégorie
    books_in_category = data['data']['books']
    
    # Vérifier si des livres sont trouvés
    if books_in_category:
        # Créer une liste de dictionnaires pour les livres
        books_data = [{
            'Title': book['title'],
            'Subtitle': book['subtitle'],
            'Description': book['description']
        } for book in books_in_category]
        
        # Créer un DataFrame Pandas à partir des données des livres
        df_books = pd.DataFrame(books_data)
        
        df_books['Description'] = df_books['Description'].str.lower()
        
        # Charger la liste des stopwords en anglais
        stop_words = set(stopwords.words('english'))
        
        # Fonction pour supprimer les stopwords
        def remove_stopwords(text):
            words = text.split()
            filtered_words = [word for word in words if word not in stop_words]
            return ' '.join(filtered_words)
        
        # Appliquer la fonction pour nettoyer la colonne 'Description'
        df_books['Description'] = df_books['Description'].apply(remove_stopwords)
        
        # Afficher le DataFrame
        print(f"\nLivres dans la catégorie ID {category_id} :")
        print(df_books)
    else:
        print("Aucun livre trouvé dans cette catégorie.")
else:
    print(f"Erreur lors de la requête: {response.status_code}")
    print(response.text)
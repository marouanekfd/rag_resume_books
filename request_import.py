import requests

# Définir l'URL de l'API
url = "https://api.hardcover.app/v1/graphql"  # Remplacez avec l'URL exacte si elle diffère

# La requête GraphQL
query = """
query Test {
  me {
    username
  }
  books(where: {title: {_like: "Harry Potter"}}) {
    list_books {
      id
    }
    description
  }
}
"""

# En-têtes de la requête (ajoutez un token si nécessaire)
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ2ZXJzaW9uIjoiNiIsImlkIjoyMjYxNCwibG9nZ2VkSW4iOnRydWUsInN1YiI6IjIyNjE0IiwiaWF0IjoxNzMzMDI3ODA4LCJleHAiOjE3NjQ0Nzc3MDgsImh0dHBzOi8vaGFzdXJhLmlvL2p3dC9jbGFpbXMiOnsieC1oYXN1cmEtYWxsb3dlZC1yb2xlcyI6WyJ1c2VyIl0sIngtaGFzdXJhLWRlZmF1bHQtcm9sZSI6InVzZXIiLCJ4LWhhc3VyYS1yb2xlIjoidXNlciIsIlgtaGFzdXJhLXVzZXItaWQiOiIyMjYxNCJ9fQ.IRlB1Pvw-zrybAWrKsWy9mB-ZzEIyBFBdYA9kZMzg3M"  # Ajoutez cette ligne si un token est requis
}

# Envoyer la requête
response = requests.post(url, json={"query": query}, headers=headers)

# Afficher les résultats
if response.status_code == 200:
    data = response.json()
    print(data)
else:
    print(f"Error: {response.status_code}, {response.text}")

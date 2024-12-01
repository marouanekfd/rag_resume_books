import requests

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
    limit: 10
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
    print(data)
    # Extract the books' descriptions and categories
    books = data['data']['books']
    
    if books:
        print("Books found similar to 'Harry Potter':")
        for book in books:
            description = book['description']
            title = book['title']
            subtitle = book['subtitle']
            print(f"Title: {title}\nSubtitle: {subtitle}\nDescription: {description}\n")
    else:
        print("No books found matching 'Harry Potter'.")
else:
    print(f"Error: {response.status_code}")
    print(response.text)

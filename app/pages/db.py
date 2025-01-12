import streamlit as st
from pymongo import MongoClient

# MongoDB connection setup
def connect_to_mongodb():
    try:
        # Replace with your MongoDB connection string
        client = MongoClient("mongodb+srv://chanaveer7:itTfV9syXU2NaqIx@cluster0.6iy7n.mongodb.net/")
        db = client["email"]  # Replace <dbname> with your database name
        collection = db["summary"]  # Replace <collection_name> with your collection name
        return collection
    except Exception as e:
        st.error(f"Error connecting to MongoDB: {e}")
        return None

# Streamlit app
st.title("Streamlit and MongoDB Integration")

collection = connect_to_mongodb()

if collection:
    # Insert data into MongoDB
    name = st.text_input("Enter your name")
    age = st.number_input("Enter your age", min_value=0, step=1)

    if st.button("Save to Database"):
        data = {"name": name, "age": age}
        collection.insert_one(data)
        st.success("Data saved successfully!")

    # Retrieve and display data
    if st.button("Show Data"):
        data = list(collection.find())
        for entry in data:
            st.write(f"Name: {entry['name']}, Age: {entry['age']}")
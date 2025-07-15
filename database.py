import logging
from pymongo import MongoClient
from config import MONGO_URI  # Ensure this exists and is correct
import urllib.parse
from bson import ObjectId  # For MongoDB ObjectId queries

# Configure Logging
logging.basicConfig(level=logging.INFO)

try:
    # Escape special characters in username & password
    if "your_username" in MONGO_URI or "your_password" in MONGO_URI:
        raise ValueError("❌ Replace 'your_username' and 'your_password' in config.py")

    # Connect to MongoDB
    client = MongoClient(MONGO_URI)
    db = client["project_submission"]  # Database name
    projects_collection = db["projects"]  # Collection name
    faculty_collection = db["faculty"]  # ✅ Added Faculty Collection
    reviews_collection = db["reviews"]  # ✅ Collection to store feedback/reviews

    logging.info("✅ Connected to MongoDB successfully!")

except Exception as e:
    logging.error(f"❌ MongoDB Connection Failed: {e}")
    db = None
    projects_collection = None
    faculty_collection = None  # ✅ Handle faculty collection properly

# Function to Get Database (Prevents `None` Errors)
def get_db():
    if db is None:
        raise ConnectionError("❌ Database connection not established!")
    return db

# Function to Get Projects Collection
def get_projects_collection():
    if projects_collection is None:
        raise ConnectionError("❌ Projects collection not available!")
    return projects_collection

# ✅ Function to Get Faculty Collection
def get_faculty_collection():
    if faculty_collection is None:
        raise ConnectionError("❌ Faculty collection not available!")
    return faculty_collection

# ✅ Function to Get Reviews Collection
def get_reviews_collection():
    if reviews_collection is None:
        raise ConnectionError("❌ Reviews collection not available!")
    return reviews_collection

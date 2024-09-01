from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mysql.connector
from mysql.connector import Error

app = FastAPI()

# MySQL connection settings
db_config = {
    'host': '127.0.0.1',
    'user': 'root',  # Replace with your MySQL username
    'password': '',  # Replace with your MySQL password
    'database': 'test'  # Replace with your database name
}

# Define Pydantic model for input validation
class User(BaseModel):
    name: str
    email: str
    # class Config:
    #     extra = "allow" 
        # Allow extra fields

# Function to insert a new user into the database
def add_user_to_db(user: User):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        cursor.execute("INSERT INTO crud (name, email) VALUES (%s, %s)", (user.name, user.email))
        connection.commit()
        return cursor.lastrowid  # Return the ID of the newly created user
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

@app.post("/crud", status_code=201)
async def create_user(user: User):
    print("DATAAA",user)  # Print the user data to the console for debugging
    user_id = add_user_to_db(user)
    return {"message": "User created successfully", "user_id": user_id}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)

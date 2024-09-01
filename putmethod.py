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
class UserUpdate(BaseModel):
    id: int  # Include the ID in the request body
    name: str
    email: str

# Function to update an existing user in the database
def update_user_in_db(user: UserUpdate):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Build the update query
        update_query = "UPDATE crud SET name = %s, email = %s WHERE id = %s"
        cursor.execute(update_query, (user.name, user.email, user.id))
        connection.commit()

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="User not found")

        return {"message": "User updated successfully"}
    
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# PUT endpoint to update a user using the ID from the request body
@app.put("/crud")
async def update_user(user: UserUpdate):
    result = update_user_in_db(user)
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)

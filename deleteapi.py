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
class UserDelete(BaseModel):
    id: int  # Include the ID in the request body

# Function to delete an existing user in the database
def delete_user_from_db(user_id: int):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Delete the user based on ID
        delete_query = "DELETE FROM crud WHERE id = %s"
        cursor.execute(delete_query, (user_id,))
        connection.commit()

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="User not found")

        return {"message": "User deleted successfully"}
    
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# DELETE endpoint to delete a user using the ID from the request body
@app.delete("/crud")
async def delete_user(user: UserDelete):
    result = delete_user_from_db(user.id)
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)

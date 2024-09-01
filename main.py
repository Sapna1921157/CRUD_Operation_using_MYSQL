from fastapi import FastAPI, HTTPException
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

# Function to establish a connection to MySQL and fetch data
def get_users_from_db():
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM crud")
        crud = cursor.fetchall()
        return crud
    except Error as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

@app.get("/crud")
async def read_users():
    users = get_users_from_db()
    if not users:
        raise HTTPException(status_code=404, detail="No users found")
    return users

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)

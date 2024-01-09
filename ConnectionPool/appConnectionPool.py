from pymongo import MongoClient
from time import time
from flask import Flask, request, jsonify
import queue

app = Flask(__name__)
maxsize = 5
connection_pool = queue.Queue(maxsize=maxsize)
db_name = 'chat_db'
collection_name = 'users'
user_id_column = 'userId'
for _ in range(maxsize):
    connection = MongoClient('mongodb://localhost:27017/')
    connection_pool.put(connection)

@app.route('/heartbeat', methods=['POST'])
def heartbeat():
    try:
        connection = connection_pool.get()  # Wait for an available connection
        db = connection[db_name]
        collection = db[collection_name]
        user_id = request.json.get(user_id_column)
        current_time = int(time())
        result = collection.update_one(
            {user_id_column : user_id},
            {'$set' : {'latestHeartbeat': current_time}},
            upsert = True
        )
        connection_pool.put(connection)
        if result.modified_count > 0 or result.upserted_id:
            return jsonify({'success':1})
        else:
            return jsonify({'success':0})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)

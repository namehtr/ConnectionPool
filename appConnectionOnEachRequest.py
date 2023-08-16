from pymongo import MongoClient
from time import time
from flask import Flask, request, jsonify

app = Flask(__name__)



@app.route('/heartbeat', methods=['POST'])
def heartbeat():
    try:
        mongo_client = MongoClient("mongodb://localhost:27017/")
        db = mongo_client['chat_db']
        collection = db['users']
        user_id = request.json.get('userId')
        current_time = int(time())
        result = collection.update_one(
            {'userId' : user_id},
            {'$set' : {'latestHeartbeat': current_time}},
            upsert = True
        )
        if result.modified_count > 0 or result.upserted_id:
            return jsonify({'success':1})
        else:
            return jsonify({'success':0})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
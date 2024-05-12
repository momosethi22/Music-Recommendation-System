from flask import Flask, jsonify, send_from_directory
from flask_socketio import SocketIO
from kafka import KafkaProducer, KafkaConsumer
import json
from joblib import load
from threading import Thread

app = Flask(__name__, static_folder='static')
socketio = SocketIO(app)
tracks = [
    {"id": 2, "filename": "2.mp3", "folder": "000"},
    {"id": 3, "filename": "3.mp3", "folder": "000"},
       {"id": 5, "filename": "5.mp3", "folder": "000"}
]
# Load the model data
model_data = load('kmeans_model1.joblib')
kmeans_model = model_data['model']
cluster_labels = model_data['labels']

# Setup Kafka producer
producer = KafkaProducer(bootstrap_servers=['localhost:9092'], value_serializer=lambda x: json.dumps(x).encode('utf-8'))

@app.route('/play/<int:track_id>', methods=['POST'])
def play_track(track_id):
    print(f"Sending track ID to Kafka: {track_id}")
    producer.send('track_played_topic', {'track_id': track_id})
    print("Track play event sent")
    return jsonify({'status': 'Track play event sent'})

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/tracks')
def get_tracks():
    return jsonify(tracks)

@app.route('/media/momo/UBUNTU 23_1/sample_3/<folder>/<filename>')
def stream_audio(folder, filename):
    return send_from_directory(f'/media/momo/UBUNTU 23_1/sample_3/{folder}', filename)

import pymongo

# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["audio_features1"]
collection = db["tracks1"]

track_ids = [doc["track_id"] for doc in collection.find({}, {"track_id": 1})]

def get_recommendations(track_id):
    # Find the index of the track_id in the track_ids list  
    track_index = track_ids.index(track_id)
    # Get the cluster label for the corresponding track
    track_cluster = cluster_labels[track_index]
    # Find all track IDs in the same cluster, excluding the current track
    similar_track_ids = [track_ids[i] for i, label in enumerate(cluster_labels) if label == track_cluster and i != track_index]
    print(len(similar_track_ids))  # Count the number of similar items
    return similar_track_ids

def kafka_consumer():
    try:
        consumer = KafkaConsumer(
            'track_played_topic',
            bootstrap_servers=['localhost:9092'],
            auto_offset_reset='earliest',
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )
        for message in consumer:
            track_id = message.value['track_id']
            recommendations = get_recommendations(track_id)
            socketio.emit('new_recommendations', {'track_id': track_id, 'recommendations': recommendations[0:10]})
            print(f"Processed track {track_id} and sent recommendations.")
            print(recommendations)
    except Exception as e:
        print(f"Error in Kafka consumer thread: {e}")


# Run Kafka consumer in a background thread
Thread(target=kafka_consumer).start()

if __name__ == '__main__':
    socketio.run(app, debug=True)




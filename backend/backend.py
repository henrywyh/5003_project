from flask import Flask, request, jsonify
import findspark
import os 
spark_home = os.environ.get('SPARK_HOME', None)
findspark.init(spark_home)
from pyspark.sql import SparkSession
from mllib.ml_model import MLModel
from stream.connector import SparkStreamingWrapper
from stream.transformer import Receiver
import threading
import signal

# Create a Flask app
app = Flask(__name__)
# Create a SparkSession
spark = SparkSession.builder.appName('myApp').getOrCreate()

# Create a Spark Streaming 
wrapper = SparkStreamingWrapper('teenagers')
streaming_thread = threading.Thread(target=wrapper.start, args=(15,))
streaming_thread.start()

# Create a Kafka receiver
receiver = Receiver(spark,'reddit_titles', 'machine_learning')
receiver_thread = threading.Thread(target=receiver.start)
receiver_thread.start()

ml_model = MLModel(spark,'models/lr_model','machine_learning')
ml_thread = threading.Thread(target=ml_model.start)
ml_thread.start()

# Define a function to stop all threads gracefully
def stop_threads(signum, frame):
    print('Stopping threads...')
    for thread in threading.enumerate():
        if thread is not threading.current_thread():
            thread.stop()
    print('All threads stopped.')
    exit(0)
# Register the signal handler
signal.signal(signal.SIGINT, stop_threads)

# Define an API endpoint
@app.route('/depressed', methods=['POST'])
def depressed():
    # Get the input arguments from the request
    text = request.json['text']

    # Call the Spark function with the input arguments
    result = ml_model.predict(text)
    
    # Return the result as a JSON response
    return jsonify(result)

# Define an API endpoint
@app.route('/get_stream_result', methods=['GET'])
def get_stream_result():
    # Call the Spark function with the input arguments
    result = ml_model.get_results()
    
    # Return the result as a JSON response
    return jsonify(result)

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
    
# example of calling the API
# curl -X POST -H "Content-Type: application/json" -d '{"text":"I am so depressed"}' http://localhost:5000/depressed
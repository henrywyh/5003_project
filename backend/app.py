from flask import Flask, request, jsonify
import findspark
import os 
spark_home = os.environ.get('SPARK_HOME', None)
findspark.init(spark_home)
from pyspark.sql import SparkSession
from mllib.ml_model import MLModel
from stream.connector import SparkStreamingWrapper
from stream.transformer import Receiver
from utils import FlaskThread
import signal

def create_app():
    # Create a Flask app
    app = Flask('myApp')

    # Create a SparkSession
    spark = SparkSession.builder.appName('myApp').getOrCreate()

    # Create a Spark Streaming 
    wrapper = SparkStreamingWrapper('teenagers')
    # Create a Kafka receiver
    receiver = Receiver(spark,'reddit_titles', 'machine_learning')
    ml_model = MLModel(spark,'models/lr_model','machine_learning')
    
    streaming_thread = FlaskThread(target=wrapper.start, args=(15,))
    receiver_thread = FlaskThread(target=receiver.start)
    ml_thread = FlaskThread(target=ml_model.start)

    # Define a function to stop all threads gracefully
    def stop_threads(signum, frame):
        print('Stopping threads...')
        wrapper.stop()
        print ('Wrapper stopped')
        receiver.stop()
        print ('Receiver stopped')
        ml_model.stop()
        print ('MLModel stopped')
        streaming_thread.stop_and_join()
        receiver_thread.stop_and_join()
        ml_thread.stop_and_join()    
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
    return app

# Run the Flask app
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True,threaded=True)
    
# example of calling the API
# curl -X POST -H "Content-Type: application/json" -d '{"text":"I am so depressed"}' http://localhost:5000/depressed
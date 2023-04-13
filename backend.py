from flask import Flask, request, jsonify
import findspark
import os 
spark_home = os.environ.get('SPARK_HOME', None)
findspark.init(spark_home)
from pyspark.sql import SparkSession
from src.ml_model import MLModel

# Create a Flask app
app = Flask(__name__)
# Create a SparkSession
spark = SparkSession.builder.appName('myApp').getOrCreate()
ml_model = MLModel('models/lr_model',spark)


# Define an API endpoint
@app.route('/depressed', methods=['POST'])
def depressed():
    # Get the input arguments from the request
    text = request.json['text']

    # Call the Spark function with the input arguments
    result = ml_model.predict(text)
    
    # Return the result as a JSON response
    return jsonify(result)

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
    
# example of calling the API
# curl -X POST -H "Content-Type: application/json" -d '{"text":"I am so depressed"}' http://localhost:5000/depressed
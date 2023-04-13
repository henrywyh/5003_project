
import findspark
import os 
spark_home = os.environ.get('SPARK_HOME', None)
findspark.init(spark_home)

from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.ml.feature import Tokenizer, StopWordsRemover, CountVectorizer, IDF
from pyspark.ml.feature import StringIndexer
from pyspark.ml.classification import LogisticRegression
from pyspark.ml import PipelineModel
from pyspark.ml.evaluation import MulticlassClassificationEvaluator

class MLModel(object):
    def __init__(self,path,spark):
        self.model = PipelineModel.load(path)
        self.spark = spark

    def predict(self, text):
        # Create a Spark DataFrame from the input text
        df = self.spark.createDataFrame([(text,)], ['text'])
        # Predict the sentiment
        result = self.model.transform(df)
        # Return the prediction
        return result.first().prediction
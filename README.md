# 5003 Project
1. Clone the repository
2. Create a data folder in the training directory and put the data files in it
3. go to training/ml_training.ipynb and run the cells to create the ml model

4. install the requirements.txt
```
pip install -r requirements.txt
```
5. Run Kafka
```
cd kafka_2.13-3.4.0
bin/zookeeper-server-start.sh config/zookeeper.properties
bin/kafka-server-start.sh config/server.properties
```
6. Run the port
```
nc -lk 9999
```
7. Run the flask app
```
cd backend
python backend.py
```
8. Run the streamlit app
```
cd frontend
streamlit run Home.py
```

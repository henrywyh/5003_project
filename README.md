# 5003 Project
1. Clone the repository
2. Create a data folder in the root directory and put the data files in it
3. go to ml_training.ipynb and run the cells to create the ml model

4. install the requirements.txt
```
pip install -r requirements.txt
```

5. Run the flask app
```
python app.py
```
6. Test the post enpoint
```
curl -X POST -H "Content-Type: application/json" -d \
'{"text":"I am so depressed"}' http://localhost:5000/depressed
```
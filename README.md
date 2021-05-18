# AI Basket Analysis

We are looking to answer the following question:

Does this basket of items fit larger purchasing patterns?



## Developing

Start Docker container

```
docker run -p 6379:6379 redislabs/redismod:edge
```

Setup Environment

```
python -m venv venv
source venv/bin/active
pip install -r requirements.txt
python3 app.py
```

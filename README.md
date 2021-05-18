# AI Basket Analysis

We are looking to answer the following question:

Does this basket of items fit larger purchasing patterns?


## Running

```
docker-compose up
```

Access the demo through your [browser](http://localhost:8080)

1) Select a user to act as
2) View the user profile
3) Click on the cart tab and add new items and score
4) Select a different user and experiment with baskets

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

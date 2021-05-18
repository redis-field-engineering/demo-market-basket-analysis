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

### Scoring

The scores vary between 0 and 1.

A score closer to 1 indicates that the basket of items by category is more likely to mirror broader purchasing patterns.

For example given the user profile "splurgenarrow" :

If they add Wireless this is a higly likely basket with a score of 0.99989

But they add Major_Appliances then it will be an unlikely baske with a score of 0.00417

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

## Data sources

The data was pulled from [Amazon reviews datasets](https://s3.amazonaws.com/amazon-reviews-pds/readme.html) and the model was trained using reviews with verified purchases
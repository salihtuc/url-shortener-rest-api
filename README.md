# url-shortener-rest-api
This simple REST API is a basic approach for shortening URL problem. <br>

Let's say you have a URL with 1000 characters. When you call this service endpoint,
it will shorten it to 26 characters (without the server name). <br>

**Example**: <br><br>
**Before**: https://github.com/salihtuc/url-shortener-rest-api/blob/main/main.py

**After**: https://github.com/QTddpDCkefLkb6m6i6pC8R

And if you want to extend the shortened URL to 1000 character again (or redirect it)
you should just call another endpoint and extend it.

The service's all endpoints are working with **URLRequest** model:

```
{
    "url": "http://...."
}
```

## Usage
After the download, change your directory to the repository folder.

Then, following command can be used for running the Rest API:

```
uvicorn main:app --reload
```

In addition to that, if you just run the main.py file, it works too:
```
python main.py
```

Please note that, you should consider installing the required libraries
before running:

```
python -m pip install -r requirements.txt
```

## Endpoints
### POST /shorten
It accepts a _URLRequest_ model and shorten it after checking the URL in it.

It returns the shortened URL in _URLRequest_ format.

**Algorithm**
- Check if the _URLRequest_ sent or not.
- Get the URL in _URLRequest_ and check it wheter it is malformed or not. (via validators)
- Parse the URL with **_urlparse_** (from urllib.parse)
- Shorten the path using **_shortuuid_** (The uuid guaranteed the url's uniqueness)
- Create the final URL (Original url's scheme and server + shortened url)
- Store the URL in database (MongoDB in our case. key/value database like Redis is ideal.
    - Original URL is the key (**_src_**), Shortened URL is the value (**_tgt_**).
- Return the shortened URL in _URLRequest_ format.

### GET /extend
It accepts a _URLRequest_ model which contains a URL that shortened before.

It returns the original URL in _URLRequest_ format.

If it isn't shortened by our service (i.e. if there is no record in database) the output code is 404 
with an error message.

**Algorithm**
- Check if the _URLRequest_ sent or not.
- Get the URL in _URLRequest_ and check it wheter it is malformed or not. (via validators)
- Look for the URL in database. (Where value (**_tgt_**) is the input URL.)
    - If not exists, return 404.
- Return key (src) of the record in _URLRequest_ format.

### GET /extend/go
It accepts a _URLRequest_ model which contains a URL that shortened before.

It **redirects** to the original URL. <br>
_(**NOTE**: The approach is same with the /extend except the last step.)_

**Algorithm**
- Check if the _URLRequest_ sent or not.
- Get the URL in _URLRequest_ and check it wheter it is malformed or not. (via validators)
- Look for the URL in database. (Where value (tgt) is the input URL.)
    - If not exists, return 404.
- Redirects to the key (**_src_**) of the record in _URLRequest_ format.


## Technology Stack
This REST API is created using **FastAPI** in **Python**. As the database, I used
**MongoDB Atlas** (because of the free cloud tier).

In Python code, **shortuuid** used for shorten operation (it helps the uniqueness)
and **validator** used for URL checks.
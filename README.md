# url-shortener-rest-api
This simple REST API is a basic approach for shortening URL problem. <br>

Let's say you have a URL with 1000 characters. When you call this service endpoint,
it will shorten it to 26 characters (without the server name). <br>

And if you want to extend the shortened URL to 1000 character again (or redirect it)
you should just call another endpoint and extend it.

The service's all endpoints are working with URLRequest model:

```
{
    "url": "http://...."
}
```

## Endpoints
### POST /shorten
It accepts a URLRequest model and shorten it after checking the URL in it.

**Algorithm**
- Check if the URLRequest sent or not.
- Get the URL in URLRequest and check it wheter it is malformed or not. (via validators)
- Parse the URL with urlparse (from urllib.parse)
- Shorten the path using shortuuid (The uuid guaranteed the url's uniqueness)
- Create the final path (Original url's scheme and server + shortened url)
- Store the URL in database (MongoDB in our case. key/value database like Redis is ideal.)
- Return the shortened URL in URLRequest format.




from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from urllib.parse import urlparse, urlunparse
import validators
import shortuuid
import uvicorn
from pymongo import MongoClient


class URLRequest(BaseModel):
    url: str


app = FastAPI()

# Default connection parameters for MongoDB connection.
dbname = "url-shortener"
username = "dbwriter"
password = "<pass>"

conn_string = "mongodb+srv://{}:{}@cluster0.w7zml.mongodb.net/{}?retryWrites=true&w=majority".format(username, password,
                                                                                                     dbname)
print(conn_string)

client = MongoClient(conn_string)


db = client[dbname]

col_dict = db["urls"]


@app.post("/shorten")
async def shorten_url(url_request: URLRequest):

    """This function is using for shorten the given url.
        Note that, it encodes the url to 22 characters."""

    if url_request is None:
        err_msg = "Cannot get the input url from the client."
        raise HTTPException(status_code=400, detail={"error": err_msg})

    # Validate the url
    if not validators.url(url_request.url):
        err_msg = "This URL is malformed: " + url_request.url
        raise HTTPException(status_code=406, detail={"error": err_msg})

    # Parse the url
    parsed_url = urlparse(url_request.url)
    short_path = shortuuid.uuid(name=parsed_url.path)

    final_path = parsed_url.scheme + '://' + parsed_url.netloc + '/' + short_path

    col_dict.insert_one({"src": url_request.url, "tgt": final_path})

    return {"url": final_path}


@app.get("/extend")
async def extend_url(url_request: URLRequest):
    """It gets the url and search it in database in order to find whether it encoded before or not.
        If it encoded before, returns the key (url); else 404."""

    if url_request is None:
        err_msg = "Cannot get the input url from the client."
        raise HTTPException(status_code=400, detail={"error": err_msg})

    # Validate the url
    if not validators.url(url_request.url):
        err_msg = "This URL is malformed: " + url_request.url
        raise HTTPException(status_code=406, detail={"error": err_msg})

    # Search the url is encoded or not
    f = col_dict.find_one(filter={"tgt": url_request.url})

    # If cannot find it in database, return 404
    if not f:
        err_msg = "This url is not shorten before."
        raise HTTPException(status_code=404, detail={"error": err_msg})

    # Return the original url
    return {"url": f['src']}


@app.get("/extend/go")
async def extend_url(url_request: URLRequest):
    """It gets the url and search it in database in order to find whether it encoded before or not.
        If it encoded before, redirects to the key (url); else 404."""

    if url_request is None:
        err_msg = "Cannot get the input url from the client."
        raise HTTPException(status_code=400, detail={"error": err_msg})

    # Validate the url
    if not validators.url(url_request.url):
        err_msg = "This URL is malformed: " + url_request.url
        raise HTTPException(status_code=406, detail={"error": err_msg})

    # Search the url is encoded or not
    f = col_dict.find_one(filter={"tgt": url_request.url})

    # If cannot find it in database, return 404
    if not f:
        err_msg = "This url is not shorten before."
        raise HTTPException(status_code=404, detail={"error": err_msg})

    # Redirects to original url
    return RedirectResponse(f['src'])


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

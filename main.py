from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from urllib.parse import urlparse, urlunparse
import validators
import shortuuid


class URLRequest(BaseModel):
    url: str


app = FastAPI()


@app.get("/")
async def shorten_url(url_request: URLRequest):
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

    return {"url": final_path}


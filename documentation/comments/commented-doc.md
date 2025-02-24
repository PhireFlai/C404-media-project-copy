# URL: ://service/api/authors/{AUTHOR_SERIAL}/commented
## When the API endpoint should be used
It should be used when you want to get all the comments made by `AUTHOR_SERIAL`, or when you want to post a comment object

## How the API endpoint should be used
Send a GET request to the URL, or send a POST request with a Body, which is composed of a comment object, to the URL. For the GET, the response is a paginated comments object.

## Why the API endpoint should or should not be used
It should be used when you want to see all of the comments made by a specific author, or create a comment using your `AUTHOR_SERIAL`. It can be used for remote and local requests.


## Example Request
GET http://nodeaaaa/api/authors/111/commented

## Response
```
{
    "type": "comments",
    "items": [
        {
            "type": "comment",
            "author": {
                "type": "author",
                "id": "http://nodeaaaa/api/authors/111",
                "displayName": "Greg Johnson",
                "github": "http://github.com/gjohnson",
                "profileImage": "https://i.imgur.com/k7XVwpB.jpeg"
            },
            "comment": "Great post!",
            "contentType": "text/markdown",
            "published": "2025-02-24T13:07:04+00:00",
            "id": "http://nodeaaaa/api/authors/111/commented/130",
            "post": "http://nodebbbb/api/authors/222/posts/249"
        },
        {
            "type": "comment",
            "author": {
                "type": "author",
                "id": "http://nodeaaaa/api/authors/111",
                "displayName": "Greg Johnson",
                "github": "http://github.com/gjohnson",
                "profileImage": "https://i.imgur.com/k7XVwpB.jpeg"
            },
            "comment": "So cool!",
            "contentType": "text/markdown",
            "published": "2025-02-24T13:07:04+00:00",
            "id": "http://nodeaaaa/api/authors/111/commented/131",
            "post": "http://nodebbbb/api/authors/222/posts/250"
        }
    ]
}
```

## Example Request
GET http://nodeaaaa/api/authors/111/commented/?page=1

## Response
```
{
    "type": "comments",
    "page_number": 1,
    "count": 2,
    "items": [
        {
            "type": "comment",
            "author": {
                "type": "author",
                "id": "http://nodeaaaa/api/authors/111",
                "displayName": "Greg Johnson",
                "github": "http://github.com/gjohnson",
                "profileImage": "https://i.imgur.com/k7XVwpB.jpeg"
            },
            "comment": "Great post!",
            "contentType": "text/markdown",
            "published": "2025-02-24T13:07:04+00:00",
            "id": "http://nodeaaaa/api/authors/111/commented/130",
            "post": "http://nodebbbb/api/authors/222/posts/249"
        },
        {
            "type": "comment",
            "author": {
                "type": "author",
                "id": "http://nodeaaaa/api/authors/111",
                "displayName": "Greg Johnson",
                "github": "http://github.com/gjohnson",
                "profileImage": "https://i.imgur.com/k7XVwpB.jpeg"
            },
            "comment": "So cool!",
            "contentType": "text/markdown",
            "published": "2025-02-24T13:07:04+00:00",
            "id": "http://nodeaaaa/api/authors/111/commented/131",
            "post": "http://nodebbbb/api/authors/222/posts/250"
        }
    ]
}
```
## Example Request
POST http://nodeaaaa/api/authors/111/commented/
```
{
    "type": "comment",
    "author": {
        "type": "author",
        "id": "http://nodeaaaa/api/authors/111",
        "displayName": "Greg Johnson",
        "github": "http://github.com/gjohnson",
        "profileImage": "https://i.imgur.com/k7XVwpB.jpeg"
    },
    "comment": "Great post!",
    "contentType": "text/markdown",
    "published": "2025-02-24T13:07:04+00:00",
    "id": "http://nodeaaaa/api/authors/111/commented/130",
    "post": "http://nodebbbb/api/authors/222/posts/249"
}
```

## Response
```
{
    "type": "comment",
    "author": {
        "type": "author",
        "id": "http://nodeaaaa/api/authors/111",
        "displayName": "Greg Johnson",
        "github": "http://github.com/gjohnson",
        "profileImage": "https://i.imgur.com/k7XVwpB.jpeg"
    },
    "comment": "Great post!",
    "contentType": "text/markdown",
    "published": "2025-02-24T13:07:04+00:00",
    "id": "http://nodeaaaa/api/authors/111/commented/130",
    "post": "http://nodebbbb/api/authors/222/posts/249"
}
```

# URL: ://service/api/authors/{AUTHOR_FQID}/commented
## When the API endpoint should be used
This endpoint should be used when you want to retrieve all comments posted by author identified by `AUTHOR_SERIAL`

## How the API endpoint should be used
Send a GET request to the URL. The response is a comments object.

## Why the API endpoint should or should not be used
This endpoint can only be used for local requests. It should be used when you want to see all comments made by a specific author that the local node knows about.

## Example 
GET http://nodeaaaa/api/authors/111/commented

## Response
```
{
    "type": "comments",
    "items": [
        {
            "type": "comment",
            "author": {
                "type": "author",
                "id": "http://nodeaaaa/api/authors/111",
                "displayName": "Greg Johnson",
                "github": "http://github.com/gjohnson",
                "profileImage": "https://i.imgur.com/k7XVwpB.jpeg"
            },
            "comment": "Great post!",
            "contentType": "text/markdown",
            "published": "2025-02-24T13:07:04+00:00",
            "id": "http://nodeaaaa/api/authors/111/commented/130",
            "post": "http://nodebbbb/api/authors/222/posts/249"
        },
        {
            "type": "comment",
            "author": {
                "type": "author",
                "id": "http://nodeaaaa/api/authors/111",
                "displayName": "Greg Johnson",
                "github": "http://github.com/gjohnson",
                "profileImage": "https://i.imgur.com/k7XVwpB.jpeg"
            },
            "comment": "So cool!",
            "contentType": "text/markdown",
            "published": "2025-02-24T13:07:04+00:00",
            "id": "http://nodeaaaa/api/authors/111/commented/131",
            "post": "http://nodebbbb/api/authors/222/posts/250"
        }
    ]
}
```

## URL: ://service/api/authors/{AUTHOR_SERIAL}/commented/{COMMENT_SERIAL}
## When the API endpoint should be used
This endpoint should be used when you want to retrieve a specific comment identified by `COMMENT_SERIAL`

## How the API endpoint should be used
Send a GET request to the URL. The response is a comment object.

## Why the API endpoint should or should not be used
This endpoint can be used for both local and remote requests to get the specific comment.

## Example 
GET http://nodeaaaa/api/authors/111/commented/130

## Response

```
{
    "type":"comment",
    "author":{
        "type":"author",
        "id":"http://nodeaaaa/api/authors/111",
        "page":"http://nodeaaaa/authors/greg",
        "host":"http://nodeaaaa/api/",
        "displayName":"Greg Johnson",
        "github": "http://github.com/gjohnson",
        "profileImage": "https://i.imgur.com/k7XVwpB.jpeg"
    },
    "comment":"Sick Olde English",
    "contentType":"text/markdown",
    // ISO 8601 TIMESTAMP
    "published":"2015-03-09T13:07:04+00:00",
    // ID of the Comment
    "id": "http://nodeaaaa/api/authors/111/commented/130",
    "post": "http://nodebbbb/api/authors/222/posts/249",
}
```

## URL: ://service/api/commented/{COMMENT_FQID}
## When the API endpoint should be used
This endpoint should be used when you want to retrieve a specific comment identified by `COMMENT_SERIAL`

## How the API endpoint should be used
Send a GET request to the URL. The response is a comment object.

## Why the API endpoint should or should not be used
This endpoint can be used only for local requests to get the specific comment.

## Example 
GET http://nodebbbb/api/commented/http%3A%2F%2Fnodeaaaa%2Fapi%2Fauthors%2F111%2Fcommented%2F130

## Response
```
{
    "type":"comment",
    "author":{
        "type":"author",
        "id":"http://nodeaaaa/api/authors/111",
        "page":"http://nodeaaaa/authors/greg",
        "host":"http://nodeaaaa/api/",
        "displayName":"Greg Johnson",
        "github": "http://github.com/gjohnson",
        "profileImage": "https://i.imgur.com/k7XVwpB.jpeg"
    },
    "comment":"Sick Olde English",
    "contentType":"text/markdown",
    // ISO 8601 TIMESTAMP
    "published":"2015-03-09T13:07:04+00:00",
    // ID of the Comment
    "id": "http://nodeaaaa/api/authors/111/commented/130",
    "post": "http://nodebbbb/api/authors/222/posts/249",
}
```
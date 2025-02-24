# URL: ://service/api/authors/{AUTHOR_SERIAL}/inbox
## When the API endpoint should be used
It should be used when you want to make a comment on a post by `AUTHOR_SERIAL`

## How the API endpoint should be used
Need to send a Body, which is composed of a comment object, to the aforementioned URL

## Why the API endpoint should or should not be used
It should be used when you need to add a comment to a specific author's post. 
It should only be used for remote. It shouldn't be used for local.


## Example 1 - Request
POST http://nodebbbb/api/authors/222/inbox
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

## Example 2 - Response
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

### Breakdown
type: "comment"
- Type: String
- Purpose: Indicates that this object is a comment.

author:
- Type: Object
- Purpose: Contains information about the author of the comment.
- Composed of
    - type: "author"
        - Type: String
        - Purpose: Indicates that this object is an author.
    - id: "http://nodeaaaa/api/authors/111"
        - Type: String (URL)
        - Purpose: The unique identifier of the author.
    - displayName: "Greg Johnson"
        - Type: String
        - Purpose: The display name of the author.
    - github: "http://github.com/gjohnson"
        - Type: String (URL)
        - Purpose: The GitHub profile URL of the author.
    - profileImage: "https://i.imgur.com/k7XVwpB.jpeg"
        - Type: String (URL)
        - Purpose: The profile image URL of the author.
comment: "Great post!"
- Type: String
- Purpose: The content of the comment.

contentType: "text/markdown"
- Type: String
- Purpose: The format of the comment content.

published: "2025-02-24T13:07:04+00:00"
- Type: String (ISO 8601 Timestamp)
- Purpose: The timestamp when the comment was published.

id: "http://nodeaaaa/api/authors/111/commented/130"
- Type: String (URL)
- Purpose: The unique identifier of the comment.

post: "http://nodebbbb/api/authors/222/posts/249"
- Type: String (URL)
- Purpose: The URL of the post to which the comment is being added.



# URL: ://service/api/authors/{AUTHOR_SERIAL}/posts/{POST_SERIAL}/comments
## When the API endpoint should be used
This endpoint should be used when you want to retrieve the comments on a specific post authored by `AUTHOR_SERIAL`.

## How the API endpoint should be used
Send a GET request to the aforementioned URL. The response will contain a "comments" object.

## Why the API endpoint should or should not be used
This endpoint can be used for both local and remote requests to get the comments on a post.

## Example 1 - Request
GET ://service/api/authors/222/posts/249/comments

## Example 2 - Response
Response body is a "comments" object made up of comments
Comment type and purpose breakdown is above
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
                "id": "http://nodeaaaa/api/authors/112",
                "displayName": "Jane Doe",
                "github": "http://github.com/janedoe",
                "profileImage": "https://i.imgur.com/k7XVwpB.jpeg"
            },
            "comment": "Interesting perspective!",
            "contentType": "text/markdown",
            "published": "2025-02-24T14:07:04+00:00",
            "id": "http://nodeaaaa/api/authors/112/commented/131",
            "post": "http://nodebbbb/api/authors/223/posts/250"
        }
    ]
}
```

# URL: ://service/api/posts/{POST_FQID}/comments
## When the API endpoint should be used
This endpoint should be used when you want to retrieve the comments on a specific post that our server knows about.

## How the API endpoint should be used
Send a GET request to the aforementioned URL. The response will contain a "comments" object.

## Why the API endpoint should or should not be used
This endpoint can be used for both local and remote requests to get the comments on a post that our server is aware of.

## Example 1 - Request
GET ://service/api/posts/12345/comments

## Example 2 - Response
Response body is a "comments" object made up of comments
Comment type and purpose breakdown is above

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
                "id": "http://nodeaaaa/api/authors/112",
                "displayName": "Jane Doe",
                "github": "http://github.com/janedoe",
                "profileImage": "https://i.imgur.com/k7XVwpB.jpeg"
            },
            "comment": "Interesting perspective!",
            "contentType": "text/markdown",
            "published": "2025-02-24T14:07:04+00:00",
            "id": "http://nodeaaaa/api/authors/112/commented/131",
            "post": "http://nodebbbb/api/authors/223/posts/250"
        }
    ]
}
```

# URL: ://service/api/authors/{AUTHOR_SERIAL}/post/{POST_SERIAL}/comment/{REMOTE_COMMENT_FQID}
## When the API endpoint should be used
This endpoint should be used when you want to retrieve a specific comment identified by `REMOTE_COMMENT_FQID` on a post authored by `AUTHOR_SERIAL`.

## How the API endpoint should be used
Send a GET request to the aforementioned URL. The response will contain a "comment" object.

## Why the API endpoint should or should not be used
This endpoint can be used for both local and remote requests to get a specific comment on a post. Emphasis on specific,
as it shouldn't be used to get multiple comments as that is covered by a different endpoint.

GET [local, remote] get the comment
Example: 

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

Every JSON field in both request and response
- Has a type
- Has an example value
- Has an explanation of its purpose (when to use it)

## Example 1 - Request
GET http://nodebbbb/api/authors/222/posts/249/comments/http%3A%2F%2Fnodeaaaa%2Fapi%2Fauthors%2F111%2Fcommented%2F130

## Example 2 - Response
Response body is a comment object
Comment type and purpose breakdown is above

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

# Additional notes
Currently does not have likes, since our project has not implemented them yet
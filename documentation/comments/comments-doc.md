# When the API endpoint should be used
# How the API endpoint should be used
# Why the API endpoint should or should not be used





# URL: ://service/api/authors/{AUTHOR_SERIAL}/inbox
POST [remote]: comment on a post by AUTHOR_SERIAL
Body is a comment object

Every JSON field in both request and response
- Has a type
- Has an example value
- Has an explanation of its purpose (when to use it)

## Example 1
## Example 2


# URL: ://service/api/authors/{AUTHOR_SERIAL}/posts/{POST_SERIAL}/comments
GET [local, remote]: the comments on the post
Body is a "comments" object

Every JSON field in both request and response
- Has a type
- Has an example value
- Has an explanation of its purpose (when to use it)

## Example 1
## Example 2


# URL: ://service/api/posts/{POST_FQID}/comments
GET [local, remote]: the comments on the post (that our server knows about)
Body is a "comments" object

Every JSON field in both request and response
- Has a type
- Has an example value
- Has an explanation of its purpose (when to use it)

## Example 1
## Example 2

# URL: ://service/api/authors/{AUTHOR_SERIAL}/post/{POST_SERIAL}/comment/{REMOTE_COMMENT_FQID}
GET [local, remote] get the comment
Example: GET http://nodebbbb/api/authors/222/posts/249/comments/http%3A%2F%2Fnodeaaaa%2Fapi%2Fauthors%2F111%2Fcommented%2F130:
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

## Example 1
## Example 2


# Additional notes

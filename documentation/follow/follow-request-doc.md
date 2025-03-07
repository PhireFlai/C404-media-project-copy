# URL: ://service/api/authors/{AUTHOR_SERIAL}/inbox
## When the API endpoint should be used
It should be used when you want to send a follow request to `AUTHOR_SERIAL`

## How the API endpoint should be used
Need to send a Body, which is composed of a follow request object, to the aforementioned URL

## Why the API endpoint should or should not be used
It should be used when you want to follow a specific author.
It should only be used for remote. It shouldn't be used for local.

## Example 1: Request
POST http://nodebbbb/api/authors/222/inbox
```
{
    "type": "follow",      
    "summary":"Greg wants to follow Lara",
    "actor":{
        "type":"author",
        "id":"http://nodeaaaa/api/authors/111",
        "host":"http://nodeaaaa/api/",
        "displayName":"Greg Johnson",
        "github": "http://github.com/gjohnson",
        "profileImage": "https://i.imgur.com/k7XVwpB.jpeg",
        // URL of the user's HTML profile page
        "page": "http://nodeaaaa/authors/greg"
    },
    "object":{
        "type":"author",
        "id":"http://nodebbbb/api/authors/222",
        "host":"http://nodebbbb/api/",
        "displayName":"Lara Croft",
        // URL of the user's HTML profile page
        "page":"http://nodebbbb/authors/222",
        "github": "http://github.com/laracroft",
        "profileImage": "http://nodebbbb/api/authors/222/posts/217/image"
    }
}
```

## Example 2: Response
```
{
    "type": "follow",      
    "summary":"Greg wants to follow Lara",
    "actor":{
        "type":"author",
        "id":"http://nodeaaaa/api/authors/111",
        "host":"http://nodeaaaa/api/",
        "displayName":"Greg Johnson",
        "github": "http://github.com/gjohnson",
        "profileImage": "https://i.imgur.com/k7XVwpB.jpeg",
        // URL of the user's HTML profile page
        "page": "http://nodeaaaa/authors/greg"
    },
    "object":{
        "type":"author",
        "id":"http://nodebbbb/api/authors/222",
        "host":"http://nodebbbb/api/",
        "displayName":"Lara Croft",
        // URL of the user's HTML profile page
        "page":"http://nodebbbb/authors/222",
        "github": "http://github.com/laracroft",
        "profileImage": "http://nodebbbb/api/authors/222/posts/217/image"
    }
}
```
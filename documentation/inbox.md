# Outgoing
## Cyan sending a remote node a follow request
So, we have the actor, you have the object. We're sending all of our user's info, and just sending the id/fqid of your user back to you in the object since you'll already have the rest

We do have a few extra fields that we're using to keep track of things on our side, but all of the project documentation defined fields are present.

Incoming post type: follow
Incoming post data: 
{'summary': 'cyan_primaryuser wants to follow cyan2_user1', 
    'actor': {'id': 'http://[2605:fd00:4:1001:f816:3eff:fe50:bc21]/api/authors/86f5a339-03d3-4ff3-9d26-de924b1ebb2e/', 'username': 'cyan_primaryuser', 'profile_picture': '/media/profile_pictures/default.png', 'followers': ['http://[2605:fd00:4:1001:f816:3eff:fe50:bc21]/api/authors/a4c2dfdf-99dc-4b31-ad68-8678ba286f3e/'], 'following': [], 'friends': [], 'remote_fqid': None, 'displayName': 'cyan_primaryuser', 'github': None, 'host': '86f5a339-03d3-4ff3-9d26-de924b1ebb2e', 'page': 'http://[2605:fd00:4:1001:f816:3eff:fe50:bc21]/86f5a339-03d3-4ff3-9d26-de924b1ebb2e', 'profileImage': '/media/profile_pictures/default.png', 'type': 'author', 'github_etag': None}, 
    'object': {'id': 'http://[2605:fd00:4:1001:f816:3eff:fe50:bc21]/api/authors/0b3cf0a1-f2b1-4e2d-ba13-5071f8fd0e90/', 'username': 'cyan2_user1', 'profile_picture': '/media/profile_pictures/default.png', 'followers': [], 'following': [], 'friends': [], 'remote_fqid': 'http://[2605:fd00:4:1001:f816:3eff:fe31:b37b]/api/authors/0b3cf0a1-f2b1-4e2d-ba13-5071f8fd0e90/', 'displayName': None, 'github': None, 'host': None, 'page': None, 'profileImage': None, 'type': 'author', 'github_etag': None}, 
    'type': 'follow'
}

## Cyan sending a post
Sending post
URL: http://[2605:fd00:4:1001:f816:3eff:fe50:bc21]/api/authors/86f5a339-03d3-4ff3-9d26-de924b1ebb2e/inbox/
Headers: {'Content-Type': 'application/json'}
Payload: 
{'id': 'http://[2605:fd00:4:1001:f816:3eff:fe50:bc21]//posts/http://[2605:fd00:4:1001:f816:3eff:fe31:b37b]:8000/api/authors/0b3cf0a1-f2b1-4e2d-ba13-5071f8fd0e90/posts/e0187a42-fb4e-4c91-bcaa-a91c8d76b3e1/', 
'author': 
    {'id': 'http://[2605:fd00:4:1001:f816:3eff:fe31:b37b]/api/authors/0b3cf0a1-f2b1-4e2d-ba13-5071f8fd0e90/', 
        'username': 'cyan2_user1', 'profile_picture': '/media/profile_pictures/default.png', 'followers': ['http://[2605:fd00:4:1001:f816:3eff:fe31:b37b]/api/authors/86f5a339-03d3-4ff3-9d26-de924b1ebb2e/'], 'following': [], 'friends': [], 'remote_fqid': None, 'displayName': 'cyan2_user1', 'github': None, 'host': '0b3cf0a1-f2b1-4e2d-ba13-5071f8fd0e90', 'page': 'http://[2605:fd00:4:1001:f816:3eff:fe31:b37b]/0b3cf0a1-f2b1-4e2d-ba13-5071f8fd0e90', 'profileImage': '/media/profile_pictures/default.png', 'type': 'author', 'github_etag': None
    }, 
    'title': 'Other cyan node public post', 'content': 'See this?', 'image': None, 'formatted_content': '<p>See this?</p>', 'created_at': '2025-03-30T21:17:43.900318Z', 'published': '2025-03-30T21:17:43.905550Z', 'visibility': 'public', 'like_count': 0, 'type': 'post', 'remote_fqid': 'http://[2605:fd00:4:1001:f816:3eff:fe31:b37b]:8000/api/authors/0b3cf0a1-f2b1-4e2d-ba13-5071f8fd0e90/posts/e0187a42-fb4e-4c91-bcaa-a91c8d76b3e1/', 'comments': [], 'description': 'Other cyan node public post', 'page': 'http://[2605:fd00:4:1001:f816:3eff:fe31:b37b]/0b3cf0a1-f2b1-4e2d-ba13-5071f8fd0e90', 'contentType': 'text/plain'
}
## Cyan sending a comment
Inbox url: http://[2605:fd00:4:1001:f816:3eff:fe50:bc21]/api/authors/86f5a339-03d3-4ff3-9d26-de924b1ebb2e/inbox/
Payload:
{
    'id': 'http://[2605:fd00:4:1001:f816:3eff:fe50:bc21]:8000/api/authors/0b3cf0a1-f2b1-4e2d-ba13-5071f8fd0e90/posts/e0187a42-fb4e-4c91-bcaa-a91c8d76b3e1/comments/754b1940-1502-4b38-a7e2-907a69048e6c/', 'author': {'id': 'http://[2605:fd00:4:1001:f816:3eff:fe50:bc21]/api/authors/0b3cf0a1-f2b1-4e2d-ba13-5071f8fd0e90/', 'username': 'cyan2_user1', 'profile_picture': '/media/profile_pictures/default.png', 'followers': ['http://[2605:fd00:4:1001:f816:3eff:fe50:bc21]/api/authors/86f5a339-03d3-4ff3-9d26-de924b1ebb2e/'], 'following': [], 'friends': [], 'remote_fqid': 'http://[2605:fd00:4:1001:f816:3eff:fe31:b37b]/api/authors/0b3cf0a1-f2b1-4e2d-ba13-5071f8fd0e90/', 'displayName': None, 'github': None, 'host': None, 'page': None, 'profileImage': None, 'type': 'author', 'github_etag': None}, 
    'comment': 'New comment', 'post': 'http://[2605:fd00:4:1001:f816:3eff:fe50:bc21]:8000/api/authors/0b3cf0a1-f2b1-4e2d-ba13-5071f8fd0e90/posts/e0187a42-fb4e-4c91-bcaa-a91c8d76b3e1/', 
    'created_at': '2025-03-30T21:21:00.822987Z', 'like_count': 0, 'type': 'comment', 'contentType': 'text/markdown', 'published': '2025-03-30T21:21:00.967926Z'
}
# Incoming
## Cyan getting a request for its authors
Pass the basic auth
http://[2605:fd00:4:1001:f816:3eff:fe50:bc21]/api/authors/

Response:
[
    {
        "id": "http://[2605:fd00:4:1001:f816:3eff:fe50:bc21]/api/authors/6d9c4836-a312-4083-bc0b-c6028428282c/",
        "username": "admin",
        "profile_picture": "http://[2605:fd00:4:1001:f816:3eff:fe50:bc21]/media/profile_pictures/default.png",
        "followers": [],
        "following": [],
        "friends": [],
        "remote_fqid": null,
        "displayName": null,
        "github": null,
        "host": null,
        "page": null,
        "profileImage": null,
        "type": "author",
        "github_etag": null
    },
    {
        "id": "http://[2605:fd00:4:1001:f816:3eff:fe50:bc21]/api/authors/a4c2dfdf-99dc-4b31-ad68-8678ba286f3e/",
        "username": "cyan_guestuser",
        "profile_picture": "http://[2605:fd00:4:1001:f816:3eff:fe50:bc21]/media/profile_pictures/default.png",
        "followers": [],
        "following": [
            "http://[2605:fd00:4:1001:f816:3eff:fe50:bc21]/api/authors/86f5a339-03d3-4ff3-9d26-de924b1ebb2e/"
        ],
        "friends": [],
        "remote_fqid": null,
        "displayName": "cyan_guestuser",
        "github": null,
        "host": "a4c2dfdf-99dc-4b31-ad68-8678ba286f3e",
        "page": "http://[2605:fd00:4:1001:f816:3eff:fe50:bc21]/a4c2dfdf-99dc-4b31-ad68-8678ba286f3e",
        "profileImage": "/media/profile_pictures/default.png",
        "type": "author",
        "github_etag": null
    },
    {
        "id": "http://[2605:fd00:4:1001:f816:3eff:fe50:bc21]/api/authors/86f5a339-03d3-4ff3-9d26-de924b1ebb2e/",
        "username": "cyan_primaryuser",
        "profile_picture": "http://[2605:fd00:4:1001:f816:3eff:fe50:bc21]/media/profile_pictures/default.png",
        "followers": [
            "http://[2605:fd00:4:1001:f816:3eff:fe50:bc21]/api/authors/a4c2dfdf-99dc-4b31-ad68-8678ba286f3e/"
        ],
        "following": [
            "http://[2605:fd00:4:1001:f816:3eff:fe50:bc21]/api/authors/0b3cf0a1-f2b1-4e2d-ba13-5071f8fd0e90/"
        ],
        "friends": [],
        "remote_fqid": null,
        "displayName": "cyan_primaryuser",
        "github": null,
        "host": "86f5a339-03d3-4ff3-9d26-de924b1ebb2e",
        "page": "http://[2605:fd00:4:1001:f816:3eff:fe50:bc21]/86f5a339-03d3-4ff3-9d26-de924b1ebb2e",
        "profileImage": "/media/profile_pictures/default.png",
        "type": "author",
        "github_etag": null
    }
]

## Cyan getting a follow request
Obviously, this just matches the outgoing request that we make, since the follow_request object should be standardized.
Incoming post type: follow
Incoming post data: 
{'summary': 'cyan_primaryuser wants to follow cyan2_user1', 
    'actor': {'id': 'http://[2605:fd00:4:1001:f816:3eff:fe50:bc21]/api/authors/86f5a339-03d3-4ff3-9d26-de924b1ebb2e/', 'username': 'cyan_primaryuser', 'profile_picture': '/media/profile_pictures/default.png', 'followers': ['http://[2605:fd00:4:1001:f816:3eff:fe50:bc21]/api/authors/a4c2dfdf-99dc-4b31-ad68-8678ba286f3e/'], 'following': [], 'friends': [], 'remote_fqid': None, 'displayName': 'cyan_primaryuser', 'github': None, 'host': '86f5a339-03d3-4ff3-9d26-de924b1ebb2e', 'page': 'http://[2605:fd00:4:1001:f816:3eff:fe50:bc21]/86f5a339-03d3-4ff3-9d26-de924b1ebb2e', 'profileImage': '/media/profile_pictures/default.png', 'type': 'author', 'github_etag': None}, 
    'object': {'id': 'http://[2605:fd00:4:1001:f816:3eff:fe50:bc21]/api/authors/0b3cf0a1-f2b1-4e2d-ba13-5071f8fd0e90/', 'username': 'cyan2_user1', 'profile_picture': '/media/profile_pictures/default.png', 'followers': [], 'following': [], 'friends': [], 'remote_fqid': 'http://[2605:fd00:4:1001:f816:3eff:fe31:b37b]/api/authors/0b3cf0a1-f2b1-4e2d-ba13-5071f8fd0e90/', 'displayName': None, 'github': None, 'host': None, 'page': None, 'profileImage': None, 'type': 'author', 'github_etag': None}, 'type': 'follow'
}

## Cyan getting posts
Incoming post type: post
Incoming post data: 
{'id': 'http://[2605:fd00:4:1001:f816:3eff:fe50:bc21]//posts/http://[2605:fd00:4:1001:f816:3eff:fe31:b37b]:8000/api/authors/0b3cf0a1-f2b1-4e2d-ba13-5071f8fd0e90/posts/e0187a42-fb4e-4c91-bcaa-a91c8d76b3e1/', 
'author': {
    'id': 'http://[2605:fd00:4:1001:f816:3eff:fe31:b37b]/api/authors/0b3cf0a1-f2b1-4e2d-ba13-5071f8fd0e90/', 'username': 'cyan2_user1', 'profile_picture': '/media/profile_pictures/default.png', 'followers': ['http://[2605:fd00:4:1001:f816:3eff:fe31:b37b]/api/authors/86f5a339-03d3-4ff3-9d26-de924b1ebb2e/'], 'following': [], 'friends': [], 'remote_fqid': None, 'displayName': 'cyan2_user1', 'github': None, 'host': '0b3cf0a1-f2b1-4e2d-ba13-5071f8fd0e90', 'page': 'http://[2605:fd00:4:1001:f816:3eff:fe31:b37b]/0b3cf0a1-f2b1-4e2d-ba13-5071f8fd0e90', 'profileImage': '/media/profile_pictures/default.png', 'type': 'author', 'github_etag': None
}, 
'title': 'Other cyan node public post', 
'content': 'See this?', 
'image': None, 
'formatted_content': '<p>See this?</p>', 'created_at': '2025-03-30T21:17:43.900318Z', 
'published': '2025-03-30T21:17:43.905550Z', 
'visibility': 'public', 'like_count': 0, 
'type': 'post', 
'remote_fqid': 'http://[2605:fd00:4:1001:f816:3eff:fe31:b37b]:8000/api/authors/0b3cf0a1-f2b1-4e2d-ba13-5071f8fd0e90/posts/e0187a42-fb4e-4c91-bcaa-a91c8d76b3e1/', 
'comments': [], 
'description': 'Other cyan node public post', 
'page': 'http://[2605:fd00:4:1001:f816:3eff:fe31:b37b]/0b3cf0a1-f2b1-4e2d-ba13-5071f8fd0e90', 
'contentType': 'text/plain'
}

## Cyan getting comments
Same object as what was sent above
Processing comment: 
{'id': 'http://[2605:fd00:4:1001:f816:3eff:fe31:b37b]:8000/api/authors/0b3cf0a1-f2b1-4e2d-ba13-5071f8fd0e90/posts/e0187a42-fb4e-4c91-bcaa-a91c8d76b3e1/comments/754b1940-1502-4b38-a7e2-907a69048e6c/', 'author': {'id': 'http://[2605:fd00:4:1001:f816:3eff:fe31:b37b]/api/authors/0b3cf0a1-f2b1-4e2d-ba13-5071f8fd0e90/', 'username': 'cyan2_user1', 'profile_picture': '/media/profile_pictures/default.png', 'followers': ['http://[2605:fd00:4:1001:f816:3eff:fe31:b37b]/api/authors/86f5a339-03d3-4ff3-9d26-de924b1ebb2e/'], 'following': [], 'friends': [], 'remote_fqid': None, 'displayName': 'cyan2_user1', 'github': None, 'host': '0b3cf0a1-f2b1-4e2d-ba13-5071f8fd0e90', 'page': 'http://[2605:fd00:4:1001:f816:3eff:fe31:b37b]/0b3cf0a1-f2b1-4e2d-ba13-5071f8fd0e90', 'profileImage': '/media/profile_pictures/default.png', 'type': 'author', 'github_etag': None}, 'comment': 'New comment', 'post': 'http://[2605:fd00:4:1001:f816:3eff:fe31:b37b]:8000/api/authors/0b3cf0a1-f2b1-4e2d-ba13-5071f8fd0e90/posts/e0187a42-fb4e-4c91-bcaa-a91c8d76b3e1/', 'created_at': '2025-03-30T21:21:00.822987Z', 'like_count': 0, 'type': 'comment', 'contentType': 'text/markdown', 'published': '2025-03-30T21:21:00.823920Z', 'remote_fqid': 'http://[2605:fd00:4:1001:f816:3eff:fe31:b37b]:8000/api/authors/0b3cf0a1-f2b1-4e2d-ba13-5071f8fd0e90/posts/e0187a42-fb4e-4c91-bcaa-a91c8d76b3e1/comments/754b1940-1502-4b38-a7e2-907a69048e6c/'
}


# Outside of project documentation scope
So, the documentation doesn't talk about what it should like to send confirmation of accept vs declining of a follow request, or the case of unfollowing a user or choosing a follower to remove. We've expanded our inbox api to handle additional types in these cases, but we don't necessarily expect that people have handling for this. Unfortunate project design, but that's the lot we've been given.

## Accept follow request
For interacting with follow requests, there will already be a user and remote user involved and known, based on the follow request object, so we just send the minimal data to the remote inbox for it to identify and operate on the follow request, which is basically the ids (UUID) of each user. We can also handle FQIDs incoming for this

Remote sends post to our inbox
URL: http://[2605:fd00:4:1001:f816:3eff:fe50:bc21]/api/authors/86f5a339-03d3-4ff3-9d26-de924b1ebb2e/inbox/
Headers: {'Content-Type': 'application/json'}
Payload: {'type': 'accept_follow', 
            'summary': "cyan_primaryuser's follow request to cyan2_user1 was accepted", 'actor': {'id': '86f5a339-03d3-4ff3-9d26-de924b1ebb2e', 'username': 'cyan_primaryuser', 'remote_fqid': 'http://[2605:fd00:4:1001:f816:3eff:fe31:b37b]/authors/0b3cf0a1-f2b1-4e2d-ba13-5071f8fd0e90/'}, 
            'object': {'id': '0b3cf0a1-f2b1-4e2d-ba13-5071f8fd0e90', 'username': 'cyan2_user1', 'remote_fqid': None}
        }


We receive the same
Accepting follow request
{'type': 'accept_follow', 'summary': "cyan_primaryuser's follow request to cyan2_user1 was accepted", 'actor': {'id': '86f5a339-03d3-4ff3-9d26-de924b1ebb2e', 'username': 'cyan_primaryuser', 'remote_fqid': 'http://[2605:fd00:4:1001:f816:3eff:fe31:b37b]/authors/0b3cf0a1-f2b1-4e2d-ba13-5071f8fd0e90/'}, 'object': {'id': '0b3cf0a1-f2b1-4e2d-ba13-5071f8fd0e90', 'username': 'cyan2_user1', 'remote_fqid': None}}

## Reject follow request
Same goes for rejecting
Deleting follow request
{'type': 'decline_follow', 'summary': "cyan_primaryuser's follow request to cyan2_user1 was rejected", 'actor': {'id': '86f5a339-03d3-4ff3-9d26-de924b1ebb2e', 'username': 'cyan_primaryuser', 'remote_fqid': 'http://[2605:fd00:4:1001:f816:3eff:fe31:b37b]/authors/0b3cf0a1-f2b1-4e2d-ba13-5071f8fd0e90/'}, 'object': {'id': '0b3cf0a1-f2b1-4e2d-ba13-5071f8fd0e90', 'username': 'cyan2_user1', 'remote_fqid': None}}
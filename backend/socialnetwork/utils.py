import requests
from urllib.parse import unquote, urlparse
from django.utils.timezone import now
from socialnetwork.models import Post
import logging
import urllib.request
from rest_framework.response import Response
from rest_framework import status
logger = logging.getLogger(__name__)

GITHUB_API_URL = "https://api.github.com/users/{}/events"

def get_github_username(github_url):
    """Extract GitHub username from a profile URL."""
    if github_url:
        path = urlparse(github_url).path.strip("/")
        return path.split("/")[0]  # Extract username
    return None

def fetch_github_events(user):
    """Fetch GitHub public events, respecting API rate limits."""
    username = get_github_username(user.github)
    if not username:
        print(f"Invalid GitHub URL for user {user.username}")
        return None

    url = GITHUB_API_URL.format(username)
    headers = {}

    if user.github_etag:
        headers["If-None-Match"] = user.github_etag  # Use stored ETag

    response = requests.get(url, headers=headers)

    if response.status_code == 304:
        # No new events
        print(f"No new events for {username}.")
        return None

    if response.status_code == 200:
        # Store new ETag in the database
        new_etag = response.headers.get("ETag")
        if new_etag:
            user.github_etag = new_etag
            user.save(update_fields=["github_etag"])  # Save without touching other fields
        return response.json()

    logger.error(f"GitHub API error: {response.status_code} - {response.text}")
    return None

def create_github_posts(user):
    """Fetch GitHub events and create posts."""
    events = fetch_github_events(user)
    if not events:
        return  # No new events

    for event in events:
        event_time = event.get("created_at")
        event_type = event.get("type")
        event_repo = event.get("repo", {}).get("name", "Unknown Repository")
        event_url = event.get("repo", {}).get("url", "")

        # Construct post title
        title = f"GitHub Activity: {event_type}"

        # Construct post content
        content = f"New GitHub activity: {event_type} on {event_repo} at {event_time}. Find at {event_url}"

        # Check if a post with the same content and timestamp already exists
        if Post.objects.filter(author=user, content=content).exists():
            continue  # Skip duplicates

        # Create a new post
        Post.objects.create(
            author=user,
            title=title,
            content=content,
            visibility=Post.PUBLIC
        )
        logger.info(f"Created post for {user.username}: {content}")

    logger.info(f"GitHub posts updated for {user.username}")



def forward_get_request(request, encoded_url):
    """
    Decodes an encoded URL, validates its format, and forwards the GET request to the decoded URL.
    
    Parameters:
        request: The Django request object.
        encoded_url: The URL-encoded string (e.g., 'http%3A%2F%2Fexample-node-2%2Fauthors%2F<uuid>')
    
    Returns:
        A DRF Response containing either the remote response data or an error message.
    """
    # Decode the URL
    decoded_url = unquote(encoded_url)

    # Optionally, check if the request should be processed locally based on the hostname.
    # For now, we forward regardless.
    try:
        remote_response = requests.get(decoded_url)
    except requests.RequestException as e:
        logger.error(f"Failed to forward request to {e}")
        return Response({'error': 'Failed to forward request ' + decoded_url}, status=status.HTTP_502_BAD_GATEWAY)
    
    # Attempt to return JSON data if available; fallback to plain text
    try:
        data = remote_response.json()
    except ValueError:
        data = remote_response.text
    
    return Response(data, status=remote_response.status_code)

def get_local_ip():
    try:
        # Use a third-party service like ipify
        with urllib.request.urlopen('https://api.ipify.org', timeout=5) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        return f"Error: {str(e)}"
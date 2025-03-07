from django.core.management.base import BaseCommand
from socialnetwork.models import User
from socialnetwork.utils import create_github_posts

class Command(BaseCommand):
    help = "Fetch GitHub activity for all users with a GitHub URL and create posts"

    def handle(self, *args, **kwargs):
        users = User.objects.exclude(github__isnull=True).exclude(github="")

        if not users.exists():
            self.stdout.write(self.style.WARNING("No users with GitHub URLs found."))
            return

        for user in users:
            try:
                create_github_posts(user)
                self.stdout.write(self.style.SUCCESS(f"Updated GitHub posts for {user.username}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Failed to update {user.username}: {e}"))

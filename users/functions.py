import random
import string
from .models import AcessCode

def generate_unique_code():
    """Generate a unique 10-character code associated with a specific role."""
    while True:
        # Generate a random alphanumeric string of length 10
        random_code = ''.join(random.choices(string.ascii_letters + string.digits, k=10))

        if not AcessCode.objects.filter(code=random_code).exists():
            return random_code

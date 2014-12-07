from django.utils.crypto import salted_hmac


def idhash(id):
    """Generate a short hash of an object ID (for URL verification)."""
    return salted_hmac('wonderment-idhash', id).hexdigest()[:10]

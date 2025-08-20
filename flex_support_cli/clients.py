from twilio.rest import Client
from twilio.base.exceptions import TwilioException


# --- Helper Functions ---
def _build_session(): ...
    # optional: configure requests session with retries, timeouts

# --- Twilio Client Factory ---
def get_twilio_client(username=None, password=None):
    """Create and return a Twilio REST client."""
    if not username or not password:
        raise ValueError("Username and password must be provided.")
    return Client(username, password)

# --- Convenience Wrappers (optional) ---
def fetch_paginated(resource_fn, **kwargs): ...
    # generic pagination helper that yields all items

def with_retries(callable_fn, *args, **kwargs): ...
    # wrap SDK calls with retry/backoff logic
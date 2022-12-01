class QueryParameterValidationError(Exception):
    """Query parameters are invalid or incorrectly formatted."""
    
    msg = (
        "The request contains query parameters that are invalid or "
        "incorrectly formatted."
    )

class MinimumAppVersionError(Exception):
    """User's mobile app does not meet minimum version."""
    
    msg = (
        "The Oura user's mobile app does not meet the minimum app version "
        "requirement to support sharing the requested data type. The Oura user "
        "must update their mobile app to enable API access for the requested "
        "data type."
    )

class RequestRateLimitExceeded(Exception):
    """API rate is limited to 500 requests in a 5 minute period."""
    
    msg = (
        "The API is rate limited to 5000 requests in a 5 minute period. You will "
        "receive a 429 error code if you exceed this limit. Contact us if you "
        "expect your usage to exceed this limit."
    )

class InternalServerError(Exception):
    """Internal Oura Api server error."""

    msg = ("Interal Oura Api server error.")
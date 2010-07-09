"""
Rules for PHAs, AccessTokens, ReqTokens
"""

from smart.views import *

def grant(principal, permset):
    """
    grant the permissions of an account to this permset
    """

    permset.grant(request_token, None)
    permset.grant(session_create, None)
    permset.grant(get_rdf_store, None)
    permset.grant(post_rdf_store, None)
    permset.grant(put_rdf_store, None)
    permset.grant(delete_rdf_store, None)
    
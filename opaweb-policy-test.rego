package opaweb.authz_test

import data.opaweb.authz

test_get_authenticated_allowed {
    input := {
        "method": "GET",
        "path": ["api", "users"],
        "authenticated": true
    }
    allow := allow with input
    allow == true
}

test_get_unauthenticated_denied {
    input := {
        "method": "GET",
        "path": ["api", "users"],
        "authenticated": false
    }
    allow := allow with input
    allow == false
}

test_post_admin_allowed {
    input := {
        "method": "POST",
        "path": ["api", "users"],
        "role": "admin"
    }
    allow := allow with input
    allow == true
}

test_post_non_admin_denied {
    input := {
        "method": "POST",
        "path": ["api", "users"],
        "role": "user"
    }
    allow := allow with input
    allow == false
}

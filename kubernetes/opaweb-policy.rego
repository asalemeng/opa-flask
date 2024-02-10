package opaweb.authz

default allow = false

allow {
    input.method == "GET"
    input.path == ["api", "users"]
    input.authenticated == true
}

allow {
    input.method == "POST"
    input.path == ["api", "users"]
    input.role == "admin"
}
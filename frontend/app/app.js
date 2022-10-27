// JSON вернет мне {'Status': 'OK}

function logout() {
    document.cookie = "name=access_token; expires=-1"
    location.reload()
}
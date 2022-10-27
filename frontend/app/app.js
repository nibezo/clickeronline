// JSON вернет мне {'Status': 'OK}

function logout() {
    document.cookie = "name=access_token;max-age=0"
    location.reload()
}
// JSON вернет мне {'Status': 'OK}

function logout() {
    document.cookie = "token=access_token;max-age=0"
    location.reload()
}
// JSON вернет мне {'Status': 'OK}

function logout() {
    document.cookie = "token=access_token;max-age=-1000000000000000000000000"
    location.reload()
}
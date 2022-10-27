// JSON вернет мне {'Status': 'OK}

async function logout() {
    const response = await fetch("/logout", {
        method: "POST",
        headers: { "Accept": "application/json", "Content-Type": "application/json" },
        body: JSON.stringify({
        })
    });
    // document.cookie = "name=access_token; expires=-1"
    location.reload()
}
async function add() {
    const response = await fetch("/click", {
        method: "POST",
        headers: { "Accept": "application/json", "Content-Type": "application/json" },
        body: JSON.stringify({
        })
    });
    console.log('OK')
}

async function logout() {
    const response = await fetch("/logout", {
        method: "POST",
        headers: { "Accept": "application/json", "Content-Type": "application/json" },
        body: JSON.stringify({
        })
    });
    location.reload()
}
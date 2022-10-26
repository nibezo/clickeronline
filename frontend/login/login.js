async function send(){
    // getting user's password and login
    const username = document.getElementById("username").value
    const password = document.getElementById("password").value
    
    // отправляем запрос
    const response = await fetch("/signin", {
    method: "POST",
    headers: { "Accept": "application/json", "Content-Type": "application/json" },
    body: JSON.stringify({ 
        username: username,
        password: password
    })
});
    if (response.ok) {
        const data = await response.json()
        document.getElementById("message").textContent = data.message
    } else
    console.log(response)
}
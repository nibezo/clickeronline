function enterKeyPressed(event) {
    if (event.keyCode == 13) {
        send()
    }
 }

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
        location.reload();
    } else
    console.log(response)
}
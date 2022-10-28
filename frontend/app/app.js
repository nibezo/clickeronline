const data = 'http://127.0.0.1:8000/profile'
let clickCount = 0

document.addEventListener("DOMContentLoaded", getData);

async function getData() {
    const xhr = new XMLHttpRequest()
    xhr.open('GET', data, true)
    xhr.responseType = 'json'
    xhr.onload = () => {
        console.log(xhr.response)
        clickCount = xhr.response['money']
        document.getElementById('score').innerHTML = `${clickCount}$`
    }
    xhr.send()
    console.log(xhr)
}


async function add() {
    const response = await fetch("/click", {
        method: "POST",
        headers: { "Accept": "application/json", "Content-Type": "application/json" },
    });
    console.log('OK')
    clickCount++
    document.getElementById('score').innerHTML = `${clickCount}$`
    console.log(clickCount)

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
document.addEventListener("DOMContentLoaded", scorePrepare);
const data = 'http://127.0.0.1:8000/profile'

async function getData() {
    const xhr = new XMLHttpRequest()
    xhr.open('GET', data, true)
    xhr.responseType = 'json'
    xhr.onload = () => {
        console.log(xhr.response)
    }
    xhr.send()
    console.log(xhr)
}


async function add() {
    const response = await fetch("/click", {
        method: "GET",
        headers: { "Accept": "application/json", "Content-Type": "application/json" },
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
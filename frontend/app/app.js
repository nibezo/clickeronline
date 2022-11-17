const userData = 'http://127.0.0.1:8000/profile'
const getLeaderboardData = 'http://127.0.0.1:8000/leaderboard'
const buyAMeme = 'http://127.0.0.1:8000/buymeme'
let clickCount = 0
let userName = ''

document.addEventListener("DOMContentLoaded", getData);
document.addEventListener("DOMContentLoaded", getLeaderboard);

async function getData() {
    const xhr = new XMLHttpRequest()
    xhr.open('GET', userData, true)
    xhr.responseType = 'json'
    xhr.onload = () => {
        console.log(xhr.response)
        clickCount = xhr.response['money']
        userName = xhr.response['username']
        console.log(userName)
        document.getElementById('score').innerHTML = `${clickCount}$`
        document.getElementById('nickname').innerHTML = userName
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

async function getLeaderboard () {
    const xhr = new XMLHttpRequest()
    xhr.open('GET', getLeaderboardData, true)
    xhr.responseType = 'json'
    xhr.onload = () => {
        console.log(xhr.response['1'])
        if (document.getElementById('gamers'))
        for (id in xhr.response) {
            document.getElementById('gamers').innerHTML += `
                <p clsss="user">
                    <span class="id">${id}.</span>
                    <span class="username">${xhr.response[id]['username']} - </span>
                    <span class="money"><b>${xhr.response[id]['money']}$</b></span>
                </p>
            `
        }
    }
    xhr.send()
    console.log(xhr)
}

async function buyMeme() {
    const xhr = new XMLHttpRequest()
    xhr.open('GET', buyAMeme, true)
    xhr.responseType = 'json'
    xhr.onload = () => {
        if (xhr.response['Status'] === 'OK') {
            console.log(clickCount)
            getData() 
            let memeNum = getRandomIntInRange(1, 425)
            document.getElementById('meme').innerHTML = `<img src="https://veshok.com/dw/files/Memy/%D0%9C%D0%B5%D0%BC%20(${memeNum}).jpg" width="300px" onerror="javascript: buyMeme()">`
        }
    }
    xhr.send()
}

function getRandomIntInRange(from, to) {
    let x = Math.random()+from;
    return Math.floor(Math.random() * to);
  }
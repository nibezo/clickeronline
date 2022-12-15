const userData = '/profile';
const getLeaderboardData = '/leaderboard';
const buyAMeme = '/buymeme';
const king = '/king';
const wipe = '/wipe';
const boost = '/boost';
let clickCount = 0;
let userName = '';
let currentKing = '';
let colors = [
  '#FBF8CC',
  '#FDE4CF',
  '#FFCFD2',
  '#F1C0E8',
  '#CFBAF0',
  '#A3C4F3',
  '#8EECF5',
  '#98F5E1',
  '#B9FBC0',
  '#606c38',
  '#bde0fe',
  '#fca311',
  '#faedcd',
  '#e85d04',
  '#99d98c',
  '#f5cac3',
  '#d62828',
  '#b8c0ff',
  '#06d6a0',
  '#f15bb5',
  '#936639',
  '#e56b6f',
  '#023e7d',
  '#577590',
  '#b5179e',
  '#ff4d6d',
  '#ff4d6d',
  '#ff595e',
  '#ccff33',
];

document.addEventListener('DOMContentLoaded', getData);
document.addEventListener('DOMContentLoaded', getLeaderboard);

async function getData() {
  const xhr = new XMLHttpRequest();
  xhr.open('GET', userData, true);
  xhr.responseType = 'json';
  xhr.onload = () => {
    clickCount = xhr.response['money'];
    userName = xhr.response['username'];
    currentKing = xhr.response['king'];
    document.getElementById('score').innerHTML = `${clickCount}$`;
    document.getElementById('nickname').innerHTML = userName;
    document.getElementById('king-name').innerHTML = `<b>${currentKing} 😎</b>`;
  };
  xhr.send();
}

async function add() {
  const response = await fetch('/click', {
    method: 'GET',
    headers: { Accept: 'application/json', 'Content-Type': 'application/json' },
  });
  console.log('OK');
  clickCount++;
  document.getElementById('score').innerHTML = `${clickCount}$`;
  if (clickCount % 10 === 0) {
    let color = getRandomColor();
    let body = document.getElementsByTagName('body');
    body[0].style.backgroundColor = color;
  }
}

async function logout() {
  const response = await fetch('/logout', {
    method: 'POST',
    headers: { Accept: 'application/json', 'Content-Type': 'application/json' },
    body: JSON.stringify({}),
  });
  location.reload();
}

function getLeaderboard() {
  const xhr = new XMLHttpRequest();
  xhr.open('GET', getLeaderboardData, true);
  xhr.responseType = 'json';
  let idCounter = 0;
  xhr.onload = () => {
    if (document.getElementById('gamers')) {
      for (id in xhr.response) {
        document.getElementById('gamers').innerHTML += `
                <p clsss="user">
                    <span class="id" id="gamer${idCounter}">${id}. ${xhr.response[id]['username']} - </span>
                    <span class="money"><b>${xhr.response[id]['money']}$</b></span>
                </p>
            `;
        idCounter += 1;
      }
    }
  };
  xhr.send();
}

async function buyMeme() {
  const xhr = new XMLHttpRequest();
  xhr.open('GET', buyAMeme, true);
  xhr.responseType = 'json';
  xhr.onload = () => {
    if (xhr.response['Status'] === 'OK') {
      getData();
      let memeNum = getRandomIntInRange(1, 425);
      document.getElementById(
        'meme'
      ).innerHTML = `<img src="https://veshok.com/dw/files/Memy/%D0%9C%D0%B5%D0%BC%20(${memeNum}).jpg" width="300px" onerror="javascript: buyMeme()">`;
    }
  };
  xhr.send();
}

function getRandomIntInRange(from, to) {
  let bad = [
    291, 315, 317, 319, 321, 323, 325, 327, 329, 331, 333, 335, 337, 339, 341,
    343, 345, 347, 349, 351, 353, 355, 357, 359, 361, 363, 365, 314, 318, 322,
    326, 330, 334, 338, 342, 346, 350, 354, 358, 362, 366, 320, 328, 336, 344,
    352, 360, 316, 332, 348, 364, 340, 324, 356,
  ];
  let result = Math.random() + from;
  result = Math.floor(Math.random() * to);
  while (bad.includes(result)) {
    result = Math.floor(Math.random() * to);
  }
  return result;
}

function getRandomColor() {
  return colors[Math.floor(Math.random() * colors.length)];
}

function beKing() {
  let currentKing = document.getElementById('king-name').innerText.split(' ')[0];
  let currentPlayer = document.getElementById('nickname').innerText;
  if (currentPlayer !== currentKing) {
    console.log(currentPlayer)
    const xhr = new XMLHttpRequest();
    xhr.open('GET', '/king', true);
    xhr.send();
    location.reload();
  } else if (clickCount < 3000) {
    alert(`Ты имеешь мало денег, накопи еще ${3000-clickCount}`)
  } else {
    alert('Ты уже король 😎')
  }
  
    
}

function wipeAll() {
  const xhr = new XMLHttpRequest();
  xhr.open('GET', '/wipe', true);
  xhr.onload = () => {
    if (xhr.response === '{"Status":"OK"}') {
      location.reload();
    } else if (clickCount < 1000000) {
      alert(`Мало денег для покупки вайпа! Накопи еще ${1000000-clickCount}$ и сделай вайп на сервере для всех игроков!`)
    }
  }
  xhr.send();
}
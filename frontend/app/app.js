// JSON вернет мне {'Status': 'OK}

document.addEventListener("DOMContentLoaded", getUserInfo);

function getUserInfo() {
    const options = {
        hostname: 'ru.hexlet.io',
        path: 'my',
        method: 'GET', // default
      }
      const req = http.request(options, res => {
        console.log(res.statusCode);
      });
      req.end();
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
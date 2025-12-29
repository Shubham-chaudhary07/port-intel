async function loadData() {
    const res = await fetch("/api/data");
    const data = await res.json();

    document.getElementById("total").innerText = data.total;

    let sev = document.getElementById("severity");
    sev.innerHTML = "";
    for (let key in data.severity) {
        sev.innerHTML += `<li>${key}: ${data.severity[key]}</li>`;
    }

    let ips = document.getElementById("ips");
    ips.innerHTML = "";
    data.top_ips.forEach(ip => {
        ips.innerHTML += `<li>${ip[0]} → ${ip[1]} attempts</li>`;
    });
}

setInterval(loadData, 3000);
loadData();

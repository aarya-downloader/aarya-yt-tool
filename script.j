async function startDownload(type) {
    const url = document.getElementById('video-url').value;
    const statusText = document.getElementById('status-text');
    const buttons = document.querySelectorAll('.dl-btn');
    
    if(!url) {
        alert("Pehle YouTube link paste karein!");
        return;
    }
    
    // Sab buttons lock kar do aur loading dikhao
    buttons.forEach(btn => btn.disabled = true);
    statusText.innerText = "PROCESSING YOUR REQUEST... PLEASE WAIT ⚡";
    statusText.style.color = "#ff0055"; // Neon Red
    
    try {
        const response = await fetch('/api/get-link', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url: url, type: type })
        });
        
        const data = await response.json();
        
        if(data.error) {
            alert("Error: " + data.error);
        } else {
            // Nayi tab me file kholo ya download karo
            window.location.href = data.download_url;
            statusText.innerText = "SUCCESS! FILE IS READY 🔥";
            statusText.style.color = "#00ffcc"; // Neon Cyan
        }
    } catch (error) {
        alert("Kuch gadbad ho gayi!");
        statusText.innerText = "";
    }
    
    // 3 second baad buttons wapas normal kar do
    setTimeout(() => {
        buttons.forEach(btn => btn.disabled = false);
        statusText.innerText = "";
    }, 3000);
}

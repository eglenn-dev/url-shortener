const host = 'http://127.0.0.1:5510';
const urlForm = document.querySelector('#url-form');
const statsForm = document.querySelector('#stats-form');
const urlArea = document.querySelector('#urlArea');
const statsArea = document.querySelector('#statsArea');

urlForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    const url = document.querySelector('#url').value;
    console.log("URL ", url);
    const response = await fetch('/api/shorten', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url: url }),
    });
    const data = await response.json();
    if (data.error) {
        console.error(data.error);
    } else {
        const shortUrl = data.shortUrl;
        const shortUrlInput = document.createElement('input');
        shortUrlInput.className = 'url-input';
        shortUrlInput.type = 'text';
        shortUrlInput.value = `${host}/${shortUrl}`;
        shortUrlInput.readOnly = true;

        const copyButton = document.createElement('button');
        copyButton.className = 'submit-button';
        copyButton.textContent = 'Copy';
        copyButton.addEventListener('click', () => {
            navigator.clipboard.writeText(`${host}/${shortUrl}`)
                .then(() => {
                    copyButton.textContent = 'Copied!';
                    setTimeout(() => {
                        copyButton.textContent = 'Copy';
                    }, 1500);
                })
                .catch(err => {
                    console.error('Failed to copy: ', err);
                });
        });

        urlArea.innerHTML = '';
        urlArea.appendChild(shortUrlInput);
        urlArea.appendChild(copyButton);
    }
});

statsForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    let shortUrl = document.querySelector('#shortUrl').value;
    shortUrl = shortUrl.split('/').pop();
    console.log('Short URL: ', shortUrl);
    const response = await fetch('/api/stats', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ shortUrl: shortUrl }),
    });

    const data = await response.json();
    if (data.error) {
        console.error(data.error);
    } else {
        const stats = data.stats;
        const statsDisplay = document.createElement('div');
        statsDisplay.className = 'stats-display';
        statsDisplay.innerHTML = `
                    <p>Original URL: <a href="${stats.originalUrl}" target="_blank">${stats.originalUrl}</a></p>
                    <p>Short URL: <a href="${shortUrl}" target="_blank">${shortUrl}</a></p>
                    <p>Click Count: ${stats.clickCount}</p>
                `;
        statsArea.innerHTML = '';
        statsArea.appendChild(statsDisplay);
    }
});
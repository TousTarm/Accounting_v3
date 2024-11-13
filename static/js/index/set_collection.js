function setCollection(collectionName) {
    fetch('/set_collection', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ collection_name: collectionName })
    })
    .then(response => {
        if (response.redirected) {
            window.location.href = response.url;
        } else {
            return response.json();
        }
    })
    .catch(error => console.error('Error:', error));
}

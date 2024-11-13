function updateStats() {
    const query = new URLSearchParams(window.location.search);
    fetch(`/get_stats?${query}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            const stats = data.stats;
            stats.forEach(stat => {
                const [type, total] = stat;
                let statElement = document.getElementById(type);

                if (!statElement) {
                    console.warn(`Element with ID "${type}" not found.`);
                    statElement = document.createElement("div");
                    statElement.id = type;
                    document.getElementById("stats-container").appendChild(statElement);
                }

                statElement.innerHTML = total;
            });
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
        });
}

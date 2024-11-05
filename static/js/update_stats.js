function updateStats() {
    fetch('/get_stats')
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

                // If the stat element doesn't exist, log an error or create it
                if (!statElement) {
                    console.warn(`Element with ID "${type}" not found.`);
                    // Optionally, create and insert the missing element
                    statElement = document.createElement("div");
                    statElement.id = type;
                    document.getElementById("stats-container").appendChild(statElement);
                }

                // Update the element's content
                statElement.innerHTML = total;
            });
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
        });
}

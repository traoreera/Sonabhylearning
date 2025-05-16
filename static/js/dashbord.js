
async function updateChart(chart, url) {
    try {
        const res = await fetch(url);
        const json = await res.json();

    
        chart.data.labels = json['data'];
        chart.data.datasets[0].data = json["error"];
        chart.update();
    } catch (err) {
        console.error(`Erreur pour ${url}:`, err);
    }
}

const chart1 = new Chart(document.getElementById('chart1').getContext('2d'), {
    type: 'line',
    data: {
        labels: [],
        datasets: [{
            label: 'Erreurs calcule du Modèle SGD Regression LLm',
            data: [],
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            borderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 1
        }]
    }
});

const chart2 = new Chart(document.getElementById('chart2').getContext('2d'), {
    type: 'line',
    data: {
        labels: [],
        datasets: [{
            label: 'Erreurs calcule du Modèle Lineare Reggression',
            data: [],
            backgroundColor: 'rgba(153, 102, 255, 0.2)',
            borderColor: 'rgba(153, 102, 255, 1)',
            borderWidth: 1
        }]
    }
});

const chart3 = new Chart(document.getElementById('chart3').getContext('2d'), {
    type: 'line',
    data: {
        labels: [],
        datasets: [{
            label: 'Erreurs calcule du Modèle Keras multi features',
            data: [],
            backgroundColor: 'rgba(255, 159, 64, 0.2)',
            borderColor: 'rgba(255, 159, 64, 1)',
            borderWidth: 1
        }]
    }
});

const chart4 = new Chart(document.getElementById('chart4').getContext('2d'), {
    type: 'line',
    data: {
        labels: [],
        datasets: [{
            label: 'Erreurs calcule du model Keras NeuralNetworks',
            data: [],
            backgroundColor: 'rgba(255, 99, 132, 0.2)',
            borderColor: 'rgba(255, 99, 132, 1)',
            borderWidth: 1
        }]
    }
});

// Lancer l’update toutes les 6000ms
setInterval(() => {
    updateChart(chart1, '/models/rdgmodel');
    updateChart(chart2, '/models/lrmodel');
    updateChart(chart3, '/models/kerasmodel');
    updateChart(chart4, '/models/kerasmodelM');
}, 9000);

// Lancer immédiatement une première fois
updateChart(chart1, '/models/rdgmodel');
updateChart(chart2, '/models/lrmodel');
updateChart(chart3, '/models/kerasmodel');
updateChart(chart4, '/models/kerasmodelM');

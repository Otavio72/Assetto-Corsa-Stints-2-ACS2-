
const container = document.getElementById("chart-data");

const lapsA = JSON.parse(container.dataset.lapsA);
const lapsB = JSON.parse(container.dataset.lapsB);

const labels = lapsA.map(l => l.lap);

new Chart(document.getElementById('lapChart'), {
    type: 'line',
    data: {
        labels: labels,
        datasets: [
            {
                label: 'Stint A',
                data: lapsA.map(l => l.time),
                borderColor: 'blue',
                tension: 0.3
            },
            {
                label: 'Stint B',
                data: lapsB.map(l => l.time),
                borderColor: 'red',
                tension: 0.3
            }
        ]
    }
});

console.log(container.dataset.lapsA);
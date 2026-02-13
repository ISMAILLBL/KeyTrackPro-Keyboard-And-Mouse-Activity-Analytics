// Keyboard Usage by Day of the Week Chart
const keyPressesByDay = JSON.parse('{{ key_presses_by_day|escapejs }}');
const daysOfWeek = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
let data = daysOfWeek.map(day => keyPressesByDay[day] || 0);

const ctx = document.getElementById('keyboardUsageChart').getContext('2d');
const chart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: daysOfWeek,
        datasets: [{
            label: 'Key Presses',
            data: data,
            backgroundColor: 'rgba(75, 192, 192, 0.6)', // More vibrant color
            borderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 2, // Thicker border
            borderRadius: 5, // Rounded bars
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false, // Allow custom height and width
        scales: {
            y: {
                beginAtZero: true,
                title: {
                    display: true,
                    text: 'Number of Key Presses',
                    font: {
                        size: 14,
                        weight: 'bold',
                    }
                },
                grid: {
                    color: '#e0e0e0', // Light grid lines
                }
            },
            x: {
                title: {
                    display: true,
                    text: 'Day of the Week',
                    font: {
                        size: 14,
                        weight: 'bold',
                    }
                },
                grid: {
                    display: false, // Hide vertical grid lines
                }
            }
        },
        plugins: {
            legend: {
                display: false, // Hide the legend
            }
        }
    }
});

// Filter Event Listener
document.getElementById('monthFilter').addEventListener('change', updateChart);

// Function to update the chart based on filters
function updateChart() {
    const month = document.getElementById('monthFilter').value;

    // Simulate fetching new data based on filters (replace with actual API call)
    const newData = daysOfWeek.map(day => {
        // Replace this with logic to fetch data for the selected month
        return Math.floor(Math.random() * 100); // Random data for demonstration
    });

    // Update the chart
    chart.data.datasets[0].data = newData;
    chart.update();
}

// Keyboard Heatmap
const keyPressCounts = JSON.parse('{{ key_press_counts|escapejs }}');

function updateKeyColor(keyElement, count) {
    const intensity = Math.min(count / 200, 1);
    const red = Math.floor(255 * intensity);
    const green = Math.floor(255 * (1 - intensity));
    keyElement.style.backgroundColor = `rgb(${red}, ${green}, 0)`;

    // Update the tooltip text
    const tooltip = keyElement.querySelector('.tooltip');
    tooltip.textContent = `Clicks: ${count}`;
}

document.querySelectorAll('.key').forEach(keyElement => {
    const key = keyElement.getAttribute('data-key');
    const count = keyPressCounts[key] || 0;
    updateKeyColor(keyElement, count);
});
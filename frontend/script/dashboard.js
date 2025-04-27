/*************************************************
 * Handle charts on Dashboard                    *
 *************************************************/
const kcalChart = document.getElementById('myChart').getContext('2d');
const weightChart = document.getElementById('weightChart').getContext('2d');
const timeChart = document.getElementById('bubbleChart').getContext('2d');

// Kcal Burned in the Last 7 Days
const myKcalChart = new Chart(kcalChart, {
    type: 'bar',
    data: {
        labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
        datasets: [{
            label: 'Kcal (hundreds)',
            data: [1, 5, 12, 19, 3, 5, 0],
            borderWidth: 1
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            y: {
                beginAtZero: true,
                title: {
                    display: true,
                    text: "Kcal (hundreds)"
                }
            }
        },
        plugins: {
            title: {
                display: true,
                text: 'Kcal Burned in the Last 7 Days',
                align: 'start',
                padding: {
                    top: 10,
                    bottom: 30
                },
                font: {
                    size: 18
                }
            },
            legend: {
                display: false,
                position: 'top'
            }
        }
    }
});

// Weight Changes Over the Past 12 Weeks
const myWeight = {
    labels: [
        "1", "2", "3", "4",
        "5", "6", "7", "8",
        "9", "10", "11", "12"
    ],
    datasets: [{
        label: "Weight (kg)",
        data: [70, 69.5, 69, 70, 70.5, 71.2, 68.8, 67.5, 67, 66.8, 66.5, 66],
        fill: false,
        borderColor: "blue",
        tension: 0.3,
        pointBackgroundColor: "blue",
        pointBorderColor: "#fff",
        pointHoverBackgroundColor: "#fff",
        pointHoverBorderColor: "blue"
    }]
};
const myWeightChart = new Chart(weightChart, {
    type: 'line',
    data: myWeight,
    options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            y: {
                beginAtZero: false,
                title: {
                    display: true,
                    text: "Weight (kg)"
                }
            },
            x: {
                title: {
                    display: true,
                    text: "Week"
                }
            }
        },
        plugins: {
            title: {
                display: true,
                text: 'Weight Changes Over the Past 12 Weeks',
                align: 'start',
                padding: {
                    top: 10,
                    bottom: 30
                },
                font: {
                    size: 18
                }
            },
            legend: {
                display: false,
                position: 'top'
            },
            tooltip: {
                displayColors: false,
                callbacks: {
                    title: function () {
                        return '';
                    },
                    label: function (context) {
                        let week = context.label;
                        let weight = context.parsed.y;
                        return `Week ${week}: ${weight}kg`;
                    }
                }
            }
        }
    }
});

// Exercise minutes in the last 100 days
const data = Array.from({length: 100}, (_, i) => {
    const minutes = Math.floor(Math.random() * 120) + 30; // 30-150 phút
    return {
        x: i + 1,
        y: minutes,
        r: minutes / 15  // bán kính tỉ lệ theo số phút (15 phút ~ 1px)
    };
});
const bubbleChart = new Chart(timeChart, {
    type: 'bubble',
    data: {
        datasets: [{
            label: 'Giờ tập luyện',
            data: data,
            backgroundColor: 'rgba(54, 162, 235, 0.5)',
            borderColor: 'rgba(54, 162, 235, 1)',
            borderWidth: 1
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                display: false
            },
            tooltip: {
                displayColors: false,
                callbacks: {
                    label: function(context) {
                        const x = context.raw.x;
                        const y = context.raw.y;
                        return `Day ${x}: ${y} minutes`;
                    }
                }
            },
            title: {
                display: true,
                text: 'Exercise minutes in the last 100 days',
                align: 'start',
                padding: {
                    top: 10,
                    bottom: 30
                },
                font: {
                    size: 18
                }
            },
        },
        scales: {
            x: {
                title: {
                    display: true,
                    text: 'Day'
                },
                min: 0,
                max: 100,
                ticks: {
                    stepSize: 10
                }
            },
            y: {
                title: {
                    display: true,
                    text: 'Minutes'
                },
                min: 0,
                max: 180
            }
        }
    }
});

$(document).ready(function () {
    Chart.register(ChartDataLabels);

    let ctx = document.getElementById('myChart');

    let myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['2019', '2020', '2021', '2022', '2023', '2024'],
            datasets: [{
                label: 'Total Number of Inspected devices By James',
                data: [8160, 1000, 9741, 7913, 13860, 3500],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false, // This allows the chart to fill the container
            layout: {
                padding: 56,
            },
            scales: {
                x: {
                    stacked: true
                },
                y: {
                    min: 0,
                    suggestedMax: 10000,
                    stacked: true,
                    beginAtZero: true
                }
            },
            plugins: {
                datalabels: {
                    font: {
                        size: 14
                    },
                    textAlign: 'center',
                }
            }
        }
    });

    // // Handle the tab switch event in Bootstrap
    // $('button[data-bs-toggle="tab"]').on('shown.bs.tab', function (e) {
    //     // Check if the tab containing the chart is now visible
    //     if ($(e.target).attr('href') === '#nav-devices-inspected-per-technician-tab') {
    //         myChart.resize();  // Trigger resize when the tab is shown
    //     }
    // });

    // Optional: To dynamically resize the chart on window resize
    window.addEventListener('resize', () => {
        myChart.resize();
    });

    let ctx2 = document.getElementById("myChart2");
    let myChart2 = new Chart(ctx2, {
        type: 'bar',
        data: {
            labels: ['2019', '2020', '2021', '2022', '2023', '2024'],
            datasets: [{
                label: 'Total Number of Inspected devices By All Lab Technicians',
                data: [15007, 10000, 13500, 23000, 19910, 3500],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false, // This allows the chart to fill the container
            layout: {
                padding: 56,
            },
            scales: {
                x: {
                    stacked: true
                },
                y: {
                    stacked: true,
                    beginAtZero: true
                }
            },
            plugins: {
                datalabels: {
                    font: {
                        size: 14
                    },
                    textAlign: 'center',
                }
            }
        }
    });

    // Optional: To dynamically resize the chart on window resize
    window.addEventListener('resize', () => {
        myChart2.resize();
    });

    $('button[data-bs-toggle="tab"]').on('shown.bs.tab', function (e) {
        if ($(e.target).attr('href') === '#nav-number-of-devices-inspected') {
            myChart2.resize();  // Trigger resize for the second chart when its tab is shown
        }
    });

    // Chart#3 Number of Inspected Devices per Technician
    let ctx3 = document.getElementById("myChart3");
    let myChart3 = new Chart(ctx3, {
        type: 'bar',
        data: {
            labels: ['Sarah', 'James', 'Robert', 'Michael', 'Adam', 'David'],
            datasets: [{
                label: 'Total Number of Inspected Devices Per Technician',
                data: [1507, 1000, 1350, 2000, 1990, 350],
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(255, 159, 64, 0.2)',
                    'rgba(255, 205, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(153, 102, 255, 0.2)'
                ],
                borderColor: [
                    'rgb(255, 99, 132)',
                    'rgb(255, 159, 64)',
                    'rgb(255, 205, 86)',
                    'rgb(75, 192, 192)',
                    'rgb(54, 162, 235)',
                    'rgb(153, 102, 255)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false, // This allows the chart to fill the container
            layout: {
                padding: 56,
            },
            scales: {
                x: {
                    stacked: true
                },
                y: {
                    stacked: true,
                    beginAtZero: true
                }
            },
            plugins: {
                datalabels: {
                    font: {
                        size: 14
                    },
                    textAlign: 'center',
                }
            }
        }
    });

    // Optional: To dynamically resize the chart on window resize
    window.addEventListener('resize', () => {
        myChart3.resize();
    });

    $('button[data-bs-toggle="tab"]').on('shown.bs.tab', function (e) {
        if ($(e.target).attr('href') === '#nav-number-of-inspected-devices-per-technician') {
            myChart3.resize();  // Trigger resize for the second chart when its tab is shown
        }
    });

    // Chart#4 Refurbishing Costs
    let ctx4 = document.getElementById("myChart4");
    let myChart4 = new Chart(ctx4, {
        type: 'line',
        data: {
            labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
            datasets: [{
                label: 'Refurbishing Costs',
                data: [65, 59, 80, 81, 56, 55, 40],
                fill: false,
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1,
                pointStyle: 'circle',
                pointRadius: 10,
                pointHoverRadius: 15,
                pointBorderColor: 'rgb(0, 0, 0)',
            }],
        },
        options: {
            responsive: true,
            maintainAspectRatio: false, // This allows the chart to fill the container
            layout: {
                padding: 56,
            },
            scales: {
                y: {
                    min: 0,
                    suggestedMax: 100,       // make sure max is of multiple of ****
                }
            },
            plugins: {
                title: {
                    display: true,
                    text: 'Refurbished Costs',
                },
                legend: {
                    labels: {
                        usePointStyle: true,
                    }
                },
                datalabels: {
                    font: {
                        size: 16,
                        weight: "bold"
                    },
                    textAlign: 'center',
                    align: 'top',
                    color: "black"
                }
            }
        }
    });

    $('button[data-bs-toggle="tab"]').on('shown.bs.tab', function (e) {
        if ($(e.target).attr('href') === '#nav-refurbishing-costs') {
            myChart4.resize();  // Resize the chart when the tab is shown
        }
    });

});
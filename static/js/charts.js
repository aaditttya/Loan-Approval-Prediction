document.addEventListener("DOMContentLoaded", function () {

    const approvalDataElement = document.getElementById(
        "approval-chart-data"
    );

    const riskDataElement = document.getElementById(
        "risk-chart-data"
    );

    const dailyDataElement = document.getElementById(
        "daily-chart-data"
    );


    // ------------------------------
    // Approval Chart
    // ------------------------------

    if (approvalDataElement) {

        const approvalChartData = JSON.parse(
            approvalDataElement.textContent
        );

        const approvalCanvas = document.getElementById(
            "approvalChart"
        );

        if (approvalCanvas) {

            new Chart(approvalCanvas, {

                type: "doughnut",

                data: {

                    labels: [
                        "Approved",
                        "Rejected"
                    ],

                    datasets: [
                        {
                            data: [
                                approvalChartData.approved,
                                approvalChartData.rejected
                            ],

                            backgroundColor: [
                                "#22c55e",
                                "#ef4444"
                            ],

                            borderWidth: 0,
                            hoverOffset: 12
                        }
                    ]
                },

                options: {

                    responsive: true,
                    maintainAspectRatio: false,
                    cutout: "68%",

                    plugins: {

                        legend: {
                            position: "bottom"
                        }
                    }
                }
            });
        }
    }


    // ------------------------------
    // Risk Chart
    // ------------------------------

    if (riskDataElement) {

        const riskChartData = JSON.parse(
            riskDataElement.textContent
        );

        const riskCanvas = document.getElementById(
            "riskChart"
        );

        if (riskCanvas) {

            new Chart(riskCanvas, {

                type: "bar",

                data: {

                    labels: [
                        "Low Risk",
                        "Medium Risk",
                        "High Risk"
                    ],

                    datasets: [
                        {
                            label: "Applications",

                            data: [
                                riskChartData.low,
                                riskChartData.medium,
                                riskChartData.high
                            ],

                            backgroundColor: [
                                "#22c55e",
                                "#facc15",
                                "#ef4444"
                            ],

                            borderRadius: 10,
                            borderSkipped: false
                        }
                    ]
                },

                options: {

                    responsive: true,
                    maintainAspectRatio: false,

                    plugins: {

                        legend: {
                            display: false
                        }
                    },

                    scales: {

                        y: {
                            beginAtZero: true,

                            ticks: {
                                precision: 0,
                                stepSize: 1
                            }
                        }
                    }
                }
            });
        }
    }


    // ------------------------------
    // Daily Chart
    // ------------------------------

    if (dailyDataElement) {

        const dailyChartData = JSON.parse(
            dailyDataElement.textContent
        );

        const dailyCanvas = document.getElementById(
            "dailyChart"
        );

        if (dailyCanvas) {

            new Chart(dailyCanvas, {

                type: "line",

                data: {

                    labels: dailyChartData.labels,

                    datasets: [
                        {
                            label: "Predictions",

                            data: dailyChartData.counts,

                            borderColor: "#2563eb",

                            backgroundColor:
                                "rgba(37, 99, 235, 0.15)",

                            fill: true,
                            tension: 0.4,
                            pointRadius: 5,
                            pointHoverRadius: 7
                        }
                    ]
                },

                options: {

                    responsive: true,
                    maintainAspectRatio: false,

                    plugins: {

                        legend: {
                            display: false
                        }
                    },

                    scales: {

                        y: {
                            beginAtZero: true,

                            ticks: {
                                precision: 0,
                                stepSize: 1
                            }
                        }
                    }
                }
            });
        }
    }

});
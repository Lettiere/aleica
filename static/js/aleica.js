document.querySelector("[data-toggle-sidebar]")?.addEventListener("click", () => {
    document.body.classList.toggle("sidebar-open");
});

function makeChart(id, type, labels, values) {
    const el = document.getElementById(id);
    if (!el) return;
    new Chart(el, {
        type,
        data: {
            labels,
            datasets: [{
                data: values,
                backgroundColor: ["#1769ff", "#20b486", "#f5b942", "#e44848", "#00a6d6", "#071b33"],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            plugins: { legend: { position: "bottom" } },
            scales: type === "bar" ? { y: { beginAtZero: true } } : {}
        }
    });
}

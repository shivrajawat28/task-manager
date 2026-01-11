// ===============================
// Progress Bar Fill
// ===============================
document.addEventListener("DOMContentLoaded", function () {

    const bar = document.querySelector(".progress-bar-fill");

    if (bar) {
        const progress = bar.getAttribute("data-progress");

        if (progress !== null) {
            bar.style.width = progress + "%";
        }
    }

    // ===============================
    // Auto focus task input
    // ===============================
    const taskInput = document.getElementById("taskInput");
    if (taskInput) {
        taskInput.focus();
    }

    // ===============================
    // Confirm before deleting task
    // ===============================
    const deleteForms = document.querySelectorAll(".delete-form");

    deleteForms.forEach(form => {
        form.addEventListener("submit", function (e) {
            const confirmDelete = confirm("Are you sure you want to delete this task?");
            if (!confirmDelete) {
                e.preventDefault();
            }
        });
    });

});

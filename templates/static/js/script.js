document.addEventListener("DOMContentLoaded", () => {
    const sidebar = document.querySelector(".sidebar");
    const toggleButton = document.createElement("button");

    toggleButton.classList.add("menu-toggle");
    toggleButton.innerHTML = "☰";
    document.body.appendChild(toggleButton);

    toggleButton.addEventListener("click", () => {
        sidebar.classList.toggle("open");
    });
});

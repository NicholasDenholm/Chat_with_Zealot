// themeToggle.js
function toggleTheme() {
    const current = document.documentElement.getAttribute("data-theme");
    const next = current === "dark" ? "light" : "dark";
    document.documentElement.setAttribute("data-theme", next);
}

// Set default theme
document.addEventListener("DOMContentLoaded", () => {
    document.documentElement.setAttribute("data-theme", "light");
    
    const themeToggleBtn = document.getElementById("themeToggleBtn");
    if (themeToggleBtn) {
        themeToggleBtn.addEventListener("click", toggleTheme);
    }
});

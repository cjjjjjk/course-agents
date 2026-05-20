(function () {
  const toggle = document.querySelector("[data-toggle-nav]");
  const sidebar = document.querySelector("[data-sidebar]");
  const search = document.querySelector("[data-search]");

  if (toggle && sidebar) {
    toggle.addEventListener("click", () => {
      sidebar.classList.toggle("is-open");
    });
  }

  if (search) {
    search.addEventListener("input", () => {
      const value = search.value.trim().toLowerCase();
      document.querySelectorAll(".lesson-link").forEach((link) => {
        const text = link.textContent.toLowerCase();
        link.classList.toggle("hidden", value.length > 0 && !text.includes(value));
      });
    });
  }
})();

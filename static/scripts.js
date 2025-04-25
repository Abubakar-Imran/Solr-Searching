document.addEventListener("DOMContentLoaded", () => {
  const searchInput = document.getElementById("search-input");
  const suggestionsList = document.getElementById("autocomplete-suggestions");
  const searchForm = document.getElementById("search-form");

  searchInput.addEventListener("input", async () => {
    const query = searchInput.value;

    if (query.length > 2) {
      const response = await fetch(`/autocomplete?query=${encodeURIComponent(query)}`);
      const suggestions = await response.json();

      if (suggestions.length > 0) {
        suggestionsList.innerHTML = "";
        suggestions.forEach((suggestion) => {
          const li = document.createElement("li");
          li.classList.add("list-group-item");
          li.textContent = suggestion.title;
          li.addEventListener("click", () => {
            searchInput.value = suggestion.title;
            suggestionsList.style.display = "none";
            searchForm.submit(); // 👉 Trigger the form submission
          });
          suggestionsList.appendChild(li);
        });
        suggestionsList.style.display = "block";
      } else {
        suggestionsList.style.display = "none";
      }
    } else {
      suggestionsList.style.display = "none";
    }
  });

  document.addEventListener("click", (event) => {
    if (!event.target.closest("#autocomplete-suggestions")) {
      suggestionsList.style.display = "none";
    }
  });
});

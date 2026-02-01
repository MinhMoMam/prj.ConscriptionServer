function autocomplete(container, arr) {
  const inp = container.querySelector(".auto-input");
  const btn = container.querySelector(".auto-btn");

  function renderList(val = "") {
    closeAllLists();

    const list = document.createElement("DIV");
    list.className = "autocomplete-items";
    container.appendChild(list);

    arr.forEach(item => {
      if (!val || item.toUpperCase().startsWith(val.toUpperCase()) || val === "") {
        const div = document.createElement("DIV");
        div.textContent = item;

        div.addEventListener("click", () => {
          inp.value = item;
          closeAllLists();
        });

        list.appendChild(div);
      }
    });
  }

  inp.addEventListener("input", () => renderList(inp.value));

  btn.addEventListener("click", e => {
    e.stopPropagation();
    renderList("");
  });

  document.addEventListener("click", e => {
    if (!container.contains(e.target)) closeAllLists();
  });

  function closeAllLists() {
    document.querySelectorAll(".autocomplete-items")
      .forEach(el => el.remove());
  }
}


/*execute a function when someone clicks in the document:*/
document.addEventListener("click", function (e) {
    closeAllLists(e.target);
});
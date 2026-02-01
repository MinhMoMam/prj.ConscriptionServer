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
          inp.dispatchEvent(new Event("input", { bubbles: true }))
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

  /*execute a function when someone clicks in the document:*/
  document.addEventListener("click", function (e) {
      closeAllLists(e.target);
  });
}


function autocompleteWithDependency(communeSelect, provinceSelect, COMMUNE_BY_DISTRICT) {
  const inp = communeSelect.querySelector(".auto-input");
  const btn = communeSelect.querySelector(".auto-btn");
  selectedProvince = this.value;
  if (selectedProvince in COMMUNE_BY_DISTRICT)
  {
    arr = COMMUNE_BY_DISTRICT[selectedProvince]
  }
  else
  {
    arr = []
  }
  
  function renderList(val = "") {
    closeAllLists();

    const list = document.createElement("DIV");
    list.className = "autocomplete-items";
    communeSelect.appendChild(list);

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

  provinceSelect.addEventListener("input", function () {
      selectedProvince = this.value;
      if (selectedProvince in COMMUNE_BY_DISTRICT)
      {
        arr = COMMUNE_BY_DISTRICT[selectedProvince]
      }
      else
      {
        arr = []
      }

      if (!selectedProvince) return;

      if (!val || item.toUpperCase().startsWith(val.toUpperCase()) || val === "") {
        const div = document.createElement("DIV");
        div.textContent = item;

        div.addEventListener("click", () => {
          inp.value = item;
          closeAllLists();
        });

        list.appendChild(div);
      }

      communeSelect.disabled = false;
  });

  inp.addEventListener("input", () => renderList(inp.value));

  btn.addEventListener("click", e => {
    e.stopPropagation();
    renderList("");
  });

  document.addEventListener("click", e => {
    if (!communeSelect.contains(e.target)) closeAllLists();
  });

  function closeAllLists() {
    document.querySelectorAll(".autocomplete-items")
      .forEach(el => el.remove());
  }

  /*execute a function when someone clicks in the document:*/
  document.addEventListener("click", function (e) {
      closeAllLists(e.target);
  });
}





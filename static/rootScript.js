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


  function showToast(message, duration = 3000) {
    const toast = document.getElementById("toast");
    toast.innerText = message;
    toast.classList.add("show");

    setTimeout(() => {
      toast.classList.remove("show");
    }, duration);
  }

  async function saveDatabase() {
    try {
      const response = await fetch("/SaveDatabase", {
        method: "GET"
      });

      const data = await response.json();  // FastAPI response

      showToast(data.message);  // show it in toast
    }
    catch (error) {
      showToast("Error connecting to server ❌");
    }
  }

  async function exportData() {
    let Hovaten = document.getElementsByName("Hovaten")[0].value;
    let Namsinh = document.getElementsByName("Namsinh")[0].value;
    let Thuongtruap = document.getElementsByName("Thuongtruap")[0].value;
    let request = "/ExportInformation?Hovaten="+ Hovaten + "&Namsinh=" + Namsinh+ "&Thuongtruap=" + Thuongtruap;
    try {
      const response = await fetch(request, {
        method: "GET"
      });

      if (!response.ok) {
        showToast("Export failed ❌");
        return;
      }

      const blob = await response.blob();

      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      let disposition = response.headers.get("content-disposition");
      let filename = "export.docx";

      if (disposition && disposition.includes("filename*=")) {
        filename = disposition.split("filename*=")[1].split("''")[1];
        filename = decodeURIComponent(filename);
      }
      a.download = filename;   // filename
      document.body.appendChild(a);
      a.click();

      a.remove();
      window.URL.revokeObjectURL(url);

      showToast("Export success ✅");
    }
    catch (error) {
      showToast("Error connecting to server ❌");
    }
  }

  async function filterData() {
    let request = "/filterData"
    try {
      const response = await fetch(request, {
        method: "GET"
      });

      if (!response.ok) {
        showToast("Failed ❌");
        return;
      }

      const blob = await response.blob();

      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      let disposition = response.headers.get("content-disposition");
      let filename = "FilterData.xlsx";

      if (disposition && disposition.includes("filename*=")) {
        filename = disposition.split("filename*=")[1].split("''")[1];
        filename = decodeURIComponent(filename);
      }
      a.download = filename;   // filename
      document.body.appendChild(a);
      a.click();

      a.remove();
      window.URL.revokeObjectURL(url);

      showToast("Export success ✅");
    }
    catch (error) {
      showToast("Error connecting to server ❌");
    }
  }

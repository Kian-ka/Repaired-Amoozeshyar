document.addEventListener("DOMContentLoaded", function () {
  // sidebar
  const sidebar = document.querySelector(".sidebar_container");
  const sidebarBtn = document.querySelector(".sidebar_toggle_btn");
  const sidebarBackdrop = document.querySelector(".backdrop");

  sidebarBtn.addEventListener("click", function () {
    sidebar.classList.toggle("sidebar_active");
    sidebarBackdrop.classList.toggle("backdrop_active");
  });

  // sidebar backdrop
  sidebarBackdrop.addEventListener("click", function () {
    sidebar.classList.remove("sidebar_active");
    sidebarBackdrop.classList.remove("backdrop_active");
  });

  // Accordion
  let acc = document.getElementsByClassName("accordion");
  let accHeaders = document.getElementsByClassName("accordion_header");
  for (let i = 0; i < acc.length; i++) {
    accHeaders[i].addEventListener("click", function (e) {

      // Check if the clicked element is the header itself, not its children
      if (e.target === acc[i] || acc[i].contains(e.target)) {
        acc[i].classList.toggle("accordion_active");
      }

      if (!sidebar.classList.contains("sidebar_active")) {
        sidebar.classList.add("sidebar_active");
        sidebarBackdrop.classList.add("backdrop_active");
      }
    });
  }
});

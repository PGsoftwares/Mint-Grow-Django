document.addEventListener("DOMContentLoaded", function () {
    const filterButtons = document.querySelectorAll(".filter-btn");
    const productCards = document.querySelectorAll(".product-card");
    const categoryCards = document.querySelectorAll(
        "[data-category-link]"
    );

    function filterProducts(category) {
        filterButtons.forEach(function (button) {
            button.classList.toggle(
                "active",
                button.dataset.filter === category
            );
        });

        productCards.forEach(function (card) {
            const productCategory = card.dataset.category;

            const shouldShow =
                category === "all" ||
                productCategory === category;

            card.classList.toggle(
                "hidden",
                !shouldShow
            );
        });
    }

    filterButtons.forEach(function (button) {
        button.addEventListener("click", function () {
            const category = button.dataset.filter;

            filterProducts(category);
        });
    });

    categoryCards.forEach(function (categoryCard) {
        categoryCard.addEventListener("click", function () {
            const category =
                categoryCard.dataset.categoryLink;

            filterProducts(category);
        });
    });
});


document.addEventListener("DOMContentLoaded", function () {
    // Mobile navigation
    const menuButton = document.getElementById("menuButton");
    const navMenu = document.getElementById("navMenu");
    const navLinks = document.querySelectorAll(".nav-menu a");

    if (menuButton && navMenu) {
        menuButton.addEventListener("click", function () {
            const isOpen = navMenu.classList.toggle("active");

            menuButton.textContent = isOpen ? "✕" : "☰";

            menuButton.setAttribute(
                "aria-expanded",
                isOpen ? "true" : "false"
            );
        });

        navLinks.forEach(function (link) {
            link.addEventListener("click", function () {
                navMenu.classList.remove("active");
                menuButton.textContent = "☰";
                menuButton.setAttribute("aria-expanded", "false");
            });
        });
    }

    // Product filtering
    const filterButtons = document.querySelectorAll(".filter-btn");
    const productCards = document.querySelectorAll(".product-card");
    const categoryLinks = document.querySelectorAll(
        "[data-category-link]"
    );

    function filterProducts(category) {
        filterButtons.forEach(function (button) {
            button.classList.toggle(
                "active",
                button.dataset.filter === category
            );
        });

        productCards.forEach(function (card) {
            const shouldShow =
                category === "all" ||
                card.dataset.category === category;

            card.classList.toggle("hidden", !shouldShow);
        });
    }

    filterButtons.forEach(function (button) {
        button.addEventListener("click", function () {
            filterProducts(button.dataset.filter);
        });
    });

    categoryLinks.forEach(function (categoryLink) {
        categoryLink.addEventListener("click", function () {
            filterProducts(
                categoryLink.dataset.categoryLink
            );
        });
    });
});
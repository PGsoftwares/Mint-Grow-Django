document.addEventListener("DOMContentLoaded", function () {

    /*
    =====================================================
    MOBILE NAVIGATION
    =====================================================
    */

    const menuButton = document.getElementById("menuButton");
    const navMenu = document.getElementById("navMenu");

    if (menuButton && navMenu) {

        const navLinks = navMenu.querySelectorAll("a");

        menuButton.addEventListener("click", function () {

            const isOpen =
                navMenu.classList.toggle("active");

            menuButton.textContent =
                isOpen ? "✕" : "☰";

            menuButton.setAttribute(
                "aria-expanded",
                isOpen ? "true" : "false"
            );

        });


        navLinks.forEach(function (link) {

            link.addEventListener("click", function () {

                navMenu.classList.remove("active");

                menuButton.textContent = "☰";

                menuButton.setAttribute(
                    "aria-expanded",
                    "false"
                );

            });

        });

    }


    /*
    =====================================================
    PRODUCT TABLE
    =====================================================
    */

    const tableBody =
        document.getElementById("productTableBody");

    const searchInput =
        document.getElementById("productSearch");

    const categoryFilter =
        document.getElementById("categoryFilter");

    const perPageSelect =
        document.getElementById("productPerPage");

    const pagination =
        document.getElementById("productPagination");

    const tableInfo =
        document.getElementById("productTableInfo");

    const sortableHeaders =
        document.querySelectorAll(
            ".home-product-table th.sortable"
        );


    /*
    Stop only if product table doesn't exist.
    */

    if (!tableBody) {
        return;
    }


    const allRows = Array.from(
        tableBody.querySelectorAll(
            ".product-table-row"
        )
    );


    let filteredRows = [...allRows];

    let currentPage = 1;

    let perPage = perPageSelect
        ? parseInt(perPageSelect.value, 10)
        : 10;

    let currentSort = null;

    let currentDirection = "asc";


    /*
    =====================================================
    GET PRODUCT NAME
    =====================================================
    */

    function getProductName(row) {

        const element =
            row.querySelector(
                ".home-product-name"
            );

        if (!element) {
            return "";
        }

        return element.textContent
            .trim()
            .toLowerCase();

    }


    /*
    =====================================================
    GET CATEGORY
    =====================================================
    */

    function getCategory(row) {

        return (
            row.dataset.category || ""
        )
            .trim()
            .toLowerCase();

    }


    /*
    =====================================================
    GET PRICE
    =====================================================
    */

    function getPrice(row) {

        const value =
            parseFloat(
                row.dataset.price
            );

        return Number.isNaN(value)
            ? 0
            : value;

    }


    /*
    =====================================================
    SEARCH + CATEGORY FILTER
    =====================================================
    */

    function applyFilters() {

        const searchTerm =
            searchInput
                ? searchInput.value
                    .trim()
                    .toLowerCase()
                : "";


        const selectedCategory =
            categoryFilter
                ? categoryFilter.value
                    .trim()
                    .toLowerCase()
                : "all";


        filteredRows =
            allRows.filter(function (row) {

                const productName =
                    getProductName(row);

                const category =
                    getCategory(row);


                const matchesSearch =
                    searchTerm === "" ||
                    productName.includes(
                        searchTerm
                    );


                const matchesCategory =
                    selectedCategory === "all" ||
                    selectedCategory === "" ||
                    category === selectedCategory;


                return (
                    matchesSearch &&
                    matchesCategory
                );

            });


        currentPage = 1;


        if (currentSort) {

            sortRows();

        } else {

            renderTable();

        }

    }


    /*
    =====================================================
    SORT TABLE
    =====================================================
    */

    function sortRows() {

        filteredRows.sort(
            function (a, b) {

                let valueA;
                let valueB;


                /*
                PRODUCT NAME
                */

                if (
                    currentSort === "name"
                ) {

                    valueA =
                        getProductName(a);

                    valueB =
                        getProductName(b);


                    return currentDirection === "asc"
                        ? valueA.localeCompare(valueB)
                        : valueB.localeCompare(valueA);

                }


                /*
                CATEGORY
                */

                if (
                    currentSort === "category"
                ) {

                    valueA =
                        getCategory(a);

                    valueB =
                        getCategory(b);


                    return currentDirection === "asc"
                        ? valueA.localeCompare(valueB)
                        : valueB.localeCompare(valueA);

                }


                /*
                PRICE
                */

                if (
                    currentSort === "price"
                ) {

                    valueA =
                        getPrice(a);

                    valueB =
                        getPrice(b);


                    return currentDirection === "asc"
                        ? valueA - valueB
                        : valueB - valueA;

                }


                return 0;

            }
        );


        renderTable();

    }


    /*
    =====================================================
    SORT HEADER CLICK
    =====================================================
    */

    sortableHeaders.forEach(
        function (header) {

            header.addEventListener(
                "click",
                function () {

                    const sortType =
                        header.dataset.sort;


                    if (
                        currentSort ===
                        sortType
                    ) {

                        currentDirection =
                            currentDirection === "asc"
                                ? "desc"
                                : "asc";

                    } else {

                        currentSort =
                            sortType;

                        currentDirection =
                            "asc";

                    }


                    currentPage = 1;


                    updateSortIcons();


                    sortRows();

                }
            );

        }
    );


    /*
    =====================================================
    SORT ICONS
    =====================================================
    */

    function updateSortIcons() {

        sortableHeaders.forEach(
            function (header) {

                const icon =
                    header.querySelector(
                        ".sort-icon"
                    );


                if (!icon) {
                    return;
                }


                if (
                    header.dataset.sort ===
                    currentSort
                ) {

                    icon.textContent =
                        currentDirection === "asc"
                            ? "↑"
                            : "↓";

                } else {

                    icon.textContent =
                        "↕";

                }

            }
        );

    }


    /*
    =====================================================
    RENDER TABLE
    =====================================================
    */

    function renderTable() {

        /*
        Hide all rows first
        */

        allRows.forEach(
            function (row) {

                row.style.display =
                    "none";

            }
        );


        const totalRows =
            filteredRows.length;


        const totalPages =
            Math.ceil(
                totalRows /
                perPage
            );


        /*
        Fix current page
        */

        if (
            totalPages > 0 &&
            currentPage > totalPages
        ) {

            currentPage =
                totalPages;

        }


        if (
            totalPages === 0
        ) {

            currentPage = 1;

        }


        const start =
            (currentPage - 1) *
            perPage;


        const end =
            start + perPage;


        const rowsToShow =
            filteredRows.slice(
                start,
                end
            );


        /*
        Reorder DOM according to sorting
        */

        filteredRows.forEach(
            function (row) {

                tableBody.appendChild(
                    row
                );

            }
        );


        /*
        Show current page
        */

        rowsToShow.forEach(
            function (row) {

                row.style.display =
                    "";

            }
        );


        updateInfo(
            totalRows,
            start,
            rowsToShow.length
        );


        renderPagination(
            totalPages
        );

    }


    /*
    =====================================================
    TABLE INFORMATION
    =====================================================
    */

    function updateInfo(
        totalRows,
        start,
        visibleRows
    ) {

        if (!tableInfo) {
            return;
        }


        if (
            totalRows === 0
        ) {

            tableInfo.textContent =
                "No products found";

            return;

        }


        const first =
            start + 1;

        const last =
            start + visibleRows;


        tableInfo.textContent =
            `Showing ${first} to ${last} of ${totalRows} products`;

    }


    /*
    =====================================================
    PAGINATION
    =====================================================
    */

    function renderPagination(
        totalPages
    ) {

        if (!pagination) {
            return;
        }


        pagination.innerHTML =
            "";


        if (
            totalPages <= 1
        ) {

            return;

        }


        /*
        PREVIOUS
        */

        const previousButton =
            document.createElement(
                "button"
            );


        previousButton.type =
            "button";

        previousButton.textContent =
            "‹";

        previousButton.disabled =
            currentPage === 1;


        previousButton.addEventListener(
            "click",
            function () {

                if (
                    currentPage > 1
                ) {

                    currentPage--;

                    renderTable();

                }

            }
        );


        pagination.appendChild(
            previousButton
        );


        /*
        PAGE NUMBERS
        */

        for (
            let page = 1;
            page <= totalPages;
            page++
        ) {

            const pageButton =
                document.createElement(
                    "button"
                );


            pageButton.type =
                "button";

            pageButton.textContent =
                page;


            if (
                page ===
                currentPage
            ) {

                pageButton.classList.add(
                    "active"
                );

            }


            pageButton.addEventListener(
                "click",
                function () {

                    currentPage =
                        page;

                    renderTable();

                }
            );


            pagination.appendChild(
                pageButton
            );

        }


        /*
        NEXT
        */

        const nextButton =
            document.createElement(
                "button"
            );


        nextButton.type =
            "button";

        nextButton.textContent =
            "›";

        nextButton.disabled =
            currentPage ===
            totalPages;


        nextButton.addEventListener(
            "click",
            function () {

                if (
                    currentPage <
                    totalPages
                ) {

                    currentPage++;

                    renderTable();

                }

            }
        );


        pagination.appendChild(
            nextButton
        );

    }


    /*
    =====================================================
    EVENTS
    =====================================================
    */

    if (searchInput) {

        searchInput.addEventListener(
            "input",
            applyFilters
        );

    }


    if (categoryFilter) {

        categoryFilter.addEventListener(
            "change",
            applyFilters
        );

    }


    if (perPageSelect) {

        perPageSelect.addEventListener(
            "change",
            function () {

                perPage =
                    parseInt(
                        this.value,
                        10
                    );


                currentPage = 1;


                renderTable();

            }
        );

    }


    /*
    =====================================================
    INITIAL TABLE
    =====================================================
    */

    applyFilters();

});
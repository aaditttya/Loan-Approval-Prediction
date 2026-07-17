document.addEventListener("DOMContentLoaded", function () {
    const menuButton = document.getElementById("menuButton");
    const navLinks = document.querySelector(".nav-links");
    const currentYear = document.getElementById("currentYear");

    // Automatically update footer year
    if (currentYear) {
        currentYear.textContent = new Date().getFullYear();
    }

    // Mobile navigation
    if (menuButton && navLinks) {
        menuButton.addEventListener("click", function () {
            navLinks.classList.toggle("active");

            const icon = menuButton.querySelector("i");

            if (!icon) {
                return;
            }

            if (navLinks.classList.contains("active")) {
                icon.classList.remove("fa-bars");
                icon.classList.add("fa-xmark");
            } else {
                icon.classList.remove("fa-xmark");
                icon.classList.add("fa-bars");
            }
        });

        // Close mobile menu after clicking a link
        navLinks.querySelectorAll("a").forEach(function (link) {
            link.addEventListener("click", function () {
                navLinks.classList.remove("active");

                const icon = menuButton.querySelector("i");

                if (!icon) {
                    return;
                }

                icon.classList.remove("fa-xmark");
                icon.classList.add("fa-bars");
            });
        });
    }

    // Scroll prediction result into view
    const resultCard = document.querySelector(".result-card");
    const serverErrorCard = document.querySelector(".server-error-card");

    const messageCard = resultCard || serverErrorCard;

    if (messageCard) {
        setTimeout(function () {
            messageCard.scrollIntoView({
                behavior: "smooth",
                block: "center"
            });
        }, 300);
    }
    /*
    ==========================================
    Phase 3 - Statistics Counter Animation
    ==========================================
    */

    const statCards = document.querySelectorAll(".reveal-card");
    const statNumbers = document.querySelectorAll(".stat-number");

    function animateCounter(element) {
        const target = Number(element.dataset.target);
        const suffix = element.dataset.suffix || "";
        const duration = 1600;
        const startTime = performance.now();

        function updateCounter(currentTime) {
            const elapsedTime = currentTime - startTime;
            const progress = Math.min(elapsedTime / duration, 1);

            const currentValue = Math.floor(target * progress);

            element.textContent =
                currentValue.toLocaleString("en-IN") + suffix;

            if (progress < 1) {
                requestAnimationFrame(updateCounter);
            } else {
                element.textContent =
                    target.toLocaleString("en-IN") + suffix;
            }
        }

        requestAnimationFrame(updateCounter);
    }

    const statsSection = document.querySelector(".stats-section");

    if (statsSection) {
        const statsObserver = new IntersectionObserver(
            function (entries, observer) {
                entries.forEach(function (entry) {
                    if (!entry.isIntersecting) {
                        return;
                    }

                    statCards.forEach(function (card, index) {
                        setTimeout(function () {
                            card.classList.add("active");
                        }, index * 150);
                    });

                    statNumbers.forEach(function (number) {
                        animateCounter(number);
                    });

                    observer.unobserve(entry.target);
                });
            },
            {
                threshold: 0.25
            }
        );

        statsObserver.observe(statsSection);
    }
        /*
    ==========================================
    Phase 3 - Dark / Light Theme
    ==========================================
    */

    const themeToggle = document.getElementById("themeToggle");

    function updateThemeIcon() {
        if (!themeToggle) {
            return;
        }

        const icon = themeToggle.querySelector("i");

        if (!icon) {
            return;
        }

        const darkModeEnabled =
            document.body.classList.contains("dark-theme");

        if (darkModeEnabled) {
            icon.classList.remove("fa-moon");
            icon.classList.add("fa-sun");

            themeToggle.setAttribute(
                "aria-label",
                "Switch to light theme"
            );
        } else {
            icon.classList.remove("fa-sun");
            icon.classList.add("fa-moon");

            themeToggle.setAttribute(
                "aria-label",
                "Switch to dark theme"
            );
        }
    }

    const savedTheme = localStorage.getItem("loanwise-theme");

    if (savedTheme === "dark") {
        document.body.classList.add("dark-theme");
    }

    updateThemeIcon();

    if (themeToggle) {
        themeToggle.addEventListener("click", function () {
            document.body.classList.toggle("dark-theme");

            const currentTheme =
                document.body.classList.contains("dark-theme")
                    ? "dark"
                    : "light";

            localStorage.setItem(
                "loanwise-theme",
                currentTheme
            );

            updateThemeIcon();
        });
    }
        /*
    ==========================================
    Phase 3 - Section Reveal Animation
    ==========================================
    */

    const revealSections =
        document.querySelectorAll(".reveal-section");

    if (revealSections.length > 0) {
        const revealObserver = new IntersectionObserver(
            function (entries, observer) {
                entries.forEach(function (entry) {
                    if (!entry.isIntersecting) {
                        return;
                    }

                    entry.target.classList.add("active");
                    observer.unobserve(entry.target);
                });
            },
            {
                threshold: 0.12
            }
        );

        revealSections.forEach(function (section) {
            revealObserver.observe(section);
        });
    }

    /*
    ==========================================
    Phase 3 - Button Ripple Effect
    ==========================================
    */

    const rippleButtons =
        document.querySelectorAll(".ripple-button");

    rippleButtons.forEach(function (button) {
        button.addEventListener("click", function (event) {
            const oldRipple =
                button.querySelector(".ripple-effect");

            if (oldRipple) {
                oldRipple.remove();
            }

            const ripple = document.createElement("span");
            const buttonRectangle =
                button.getBoundingClientRect();

            const rippleSize = Math.max(
                buttonRectangle.width,
                buttonRectangle.height
            );

            const rippleX =
                event.clientX -
                buttonRectangle.left -
                rippleSize / 2;

            const rippleY =
                event.clientY -
                buttonRectangle.top -
                rippleSize / 2;

            ripple.classList.add("ripple-effect");

            ripple.style.width = rippleSize + "px";
            ripple.style.height = rippleSize + "px";
            ripple.style.left = rippleX + "px";
            ripple.style.top = rippleY + "px";

            button.appendChild(ripple);

            setTimeout(function () {
                ripple.remove();
            }, 700);
        });
    });
        /*
    ==========================================
    Phase 3 - Confidence Ring Animation
    ==========================================
    */

    const confidenceMeter =
        document.querySelector(".confidence-meter");

    if (confidenceMeter) {
        const confidenceRing =
            confidenceMeter.querySelector(".confidence-ring");

        const rawConfidence = Number(
            confidenceMeter.dataset.confidence
        );

        const safeConfidence = Math.min(
            Math.max(rawConfidence, 0),
            100
        );

        const targetAngle = safeConfidence * 3.6;

        if (confidenceRing) {
            requestAnimationFrame(function () {
                setTimeout(function () {
                    confidenceRing.style.setProperty(
                        "--confidence-angle",
                        targetAngle + "deg"
                    );
                }, 250);
            });
        }
    }
        /*
    ==========================================
    Phase 4 - History Search, Filter and Sort
    ==========================================
    */

    const historySearch =
        document.getElementById("historySearch");

    const historySort =
        document.getElementById("historySort");

    const historyRows =
        Array.from(document.querySelectorAll(".history-row"));

    const filterButtons =
        document.querySelectorAll(".history-filter-button");

    const visibleRecordCount =
        document.getElementById("visibleRecordCount");

    let activeHistoryFilter = "all";

    function updateHistoryTable() {
        const searchValue = historySearch
            ? historySearch.value.trim().toLowerCase()
            : "";

        let visibleRows = historyRows.filter(function (row) {
            const rowText = row.textContent.toLowerCase();
            const rowStatus = row.dataset.status || "";

            const matchesSearch =
                rowText.includes(searchValue);

            const matchesFilter =
                activeHistoryFilter === "all" ||
                rowStatus === activeHistoryFilter;

            return matchesSearch && matchesFilter;
        });

        historyRows.forEach(function (row) {
            row.style.display = "none";
        });

        if (historySort) {
            visibleRows.sort(function (rowA, rowB) {
                const dateA = new Date(rowA.dataset.date);
                const dateB = new Date(rowB.dataset.date);

                if (historySort.value === "oldest") {
                    return dateA - dateB;
                }

                return dateB - dateA;
            });
        }

        const tableBody = document.querySelector(
            ".history-table tbody"
        );

        visibleRows.forEach(function (row) {
            row.style.display = "";
            tableBody.appendChild(row);
        });

        if (visibleRecordCount) {
            visibleRecordCount.textContent =
                visibleRows.length;
        }
    }

    if (historySearch) {
        historySearch.addEventListener(
            "input",
            updateHistoryTable
        );
    }

    if (historySort) {
        historySort.addEventListener(
            "change",
            updateHistoryTable
        );
    }

    filterButtons.forEach(function (button) {
        button.addEventListener("click", function () {
            filterButtons.forEach(function (item) {
                item.classList.remove("active");
            });

            button.classList.add("active");

            activeHistoryFilter =
                button.dataset.filter || "all";

            updateHistoryTable();
        });
    });

    if (historyRows.length > 0) {
        updateHistoryTable();
    }
 });
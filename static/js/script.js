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
});
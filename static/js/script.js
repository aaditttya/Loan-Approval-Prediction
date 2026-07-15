document.addEventListener("DOMContentLoaded", function () {
    const loanForm = document.getElementById("loanForm");
    const predictButton = document.getElementById("predictButton");
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

            if (icon) {
                if (navLinks.classList.contains("active")) {
                    icon.classList.remove("fa-bars");
                    icon.classList.add("fa-xmark");
                } else {
                    icon.classList.remove("fa-xmark");
                    icon.classList.add("fa-bars");
                }
            }
        });

        // Close mobile menu after clicking a navigation link
        navLinks.querySelectorAll("a").forEach(function (link) {
            link.addEventListener("click", function () {
                navLinks.classList.remove("active");

                const icon = menuButton.querySelector("i");

                if (icon) {
                    icon.classList.remove("fa-xmark");
                    icon.classList.add("fa-bars");
                }
            });
        });
    }

    // Form validation and submit loading animation
    if (loanForm && predictButton) {
        loanForm.addEventListener("submit", function (event) {
            // Check all HTML required fields
            if (!loanForm.checkValidity()) {
                event.preventDefault();
                loanForm.reportValidity();
                return;
            }

            const applicantIncomeInput =
                document.getElementById("applicantIncome");

            const coapplicantIncomeInput =
                document.getElementById("coapplicantIncome");

            const loanAmountInput =
                document.getElementById("loanAmount");

            if (
                !applicantIncomeInput ||
                !coapplicantIncomeInput ||
                !loanAmountInput
            ) {
                event.preventDefault();
                alert("Some required form fields are missing.");
                return;
            }

            const applicantIncome = Number(applicantIncomeInput.value);
            const coapplicantIncome = Number(
                coapplicantIncomeInput.value
            );
            const loanAmount = Number(loanAmountInput.value);

            // Validate numeric values
            if (
                Number.isNaN(applicantIncome) ||
                Number.isNaN(coapplicantIncome) ||
                Number.isNaN(loanAmount)
            ) {
                event.preventDefault();
                alert("Please enter valid numeric values.");
                return;
            }

            // Income validation
            if (applicantIncome < 0 || coapplicantIncome < 0) {
                event.preventDefault();
                alert("Income cannot be negative.");
                return;
            }

            // Loan amount validation
            if (loanAmount <= 0) {
                event.preventDefault();
                alert("Please enter a valid loan amount.");
                return;
            }

            // Prevent multiple form submissions
            predictButton.disabled = true;
            predictButton.classList.add("loading");
        });
    }

    // Scroll prediction result into view
    const resultCard = document.querySelector(".result-card");

    if (resultCard) {
        setTimeout(function () {
            resultCard.scrollIntoView({
                behavior: "smooth",
                block: "center"
            });
        }, 300);
    }
});
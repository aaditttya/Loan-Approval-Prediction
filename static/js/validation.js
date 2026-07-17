document.addEventListener("DOMContentLoaded", function () {
    const loanForm = document.getElementById("loanForm");
    const predictButton = document.getElementById("predictButton");

    if (!loanForm || !predictButton) {
        return;
    }

    const buttonText = predictButton.querySelector(".button-text");
    const buttonLoader = predictButton.querySelector(".button-loader");
    const buttonIcon = predictButton.querySelector("i");

    let formIsSubmitting = false;

    /*
    ==========================================
    Helper: Show validation error
    ==========================================
    */

    function showError(field, message) {
        const formGroup = field.closest(".form-group");

        if (!formGroup) {
            return;
        }

        field.classList.add("input-error");

        let errorMessage = formGroup.querySelector(".error-message");

        if (!errorMessage) {
            errorMessage = document.createElement("small");
            errorMessage.classList.add("error-message");
            formGroup.appendChild(errorMessage);
        }

        errorMessage.textContent = message;
    }

    /*
    ==========================================
    Helper: Remove validation error
    ==========================================
    */

    function clearError(field) {
        const formGroup = field.closest(".form-group");

        field.classList.remove("input-error");

        if (!formGroup) {
            return;
        }

        const errorMessage = formGroup.querySelector(".error-message");

        if (errorMessage) {
            errorMessage.remove();
        }
    }

    /*
    ==========================================
    Helper: Clear all errors
    ==========================================
    */

    function clearAllErrors() {
        const fields = loanForm.querySelectorAll("input, select");

        fields.forEach(function (field) {
            clearError(field);
        });

        const consentGroup = loanForm.querySelector(".form-consent");

        if (consentGroup) {
            consentGroup.classList.remove("consent-error");

            const consentError =
                consentGroup.querySelector(".consent-error-message");

            if (consentError) {
                consentError.remove();
            }
        }
    }

    /*
    ==========================================
    Validate required field
    ==========================================
    */

    function validateRequiredField(field) {
        const value = field.value.trim();

        if (value === "") {
            showError(field, "This field is required.");
            return false;
        }

        clearError(field);
        return true;
    }

    /*
    ==========================================
    Validate applicant income
    ==========================================
    */

    function validateApplicantIncome() {
        const field = document.getElementById("applicantIncome");

        if (!field) {
            return true;
        }

        if (!validateRequiredField(field)) {
            return false;
        }

        const income = Number(field.value);

        if (Number.isNaN(income)) {
            showError(field, "Please enter a valid income.");
            return false;
        }

        if (income < 0) {
            showError(field, "Applicant income cannot be negative.");
            return false;
        }

        if (income === 0) {
            showError(field, "Applicant income must be greater than zero.");
            return false;
        }

        clearError(field);
        return true;
    }

    /*
    ==========================================
    Validate co-applicant income
    ==========================================
    */

    function validateCoapplicantIncome() {
        const field = document.getElementById("coapplicantIncome");

        if (!field) {
            return true;
        }

        if (!validateRequiredField(field)) {
            return false;
        }

        const income = Number(field.value);

        if (Number.isNaN(income)) {
            showError(field, "Please enter a valid income.");
            return false;
        }

        if (income < 0) {
            showError(field, "Co-applicant income cannot be negative.");
            return false;
        }

        clearError(field);
        return true;
    }

    /*
    ==========================================
    Validate loan amount
    ==========================================
    */

    function validateLoanAmount() {
        const field = document.getElementById("loanAmount");

        if (!field) {
            return true;
        }

        if (!validateRequiredField(field)) {
            return false;
        }

        const loanAmount = Number(field.value);

        if (Number.isNaN(loanAmount)) {
            showError(field, "Please enter a valid loan amount.");
            return false;
        }

        if (loanAmount <= 0) {
            showError(field, "Loan amount must be greater than zero.");
            return false;
        }

        if (loanAmount < 1000) {
            showError(
                field,
                "Loan amount should be at least ₹1,000."
            );

            return false;
        }

        clearError(field);
        return true;
    }

    /*
    ==========================================
    Validate consent checkbox
    ==========================================
    */

    function validateConsent() {
        const consent = document.getElementById("consent");
        const consentGroup = loanForm.querySelector(".form-consent");

        if (!consent || !consentGroup) {
            return true;
        }

        const previousError =
            consentGroup.querySelector(".consent-error-message");

        if (previousError) {
            previousError.remove();
        }

        consentGroup.classList.remove("consent-error");

        if (!consent.checked) {
            consentGroup.classList.add("consent-error");

            const errorMessage = document.createElement("small");

            errorMessage.classList.add("consent-error-message");
            errorMessage.textContent =
                "Please confirm that the information is accurate.";

            consentGroup.appendChild(errorMessage);

            return false;
        }

        return true;
    }

    /*
    ==========================================
    Validate complete form
    ==========================================
    */

    function validateForm() {
        clearAllErrors();

        let isValid = true;

        const requiredFields = loanForm.querySelectorAll(
            "input[required]:not([type='checkbox']), select[required]"
        );

        requiredFields.forEach(function (field) {
            if (!validateRequiredField(field)) {
                isValid = false;
            }
        });

        if (!validateApplicantIncome()) {
            isValid = false;
        }

        if (!validateCoapplicantIncome()) {
            isValid = false;
        }

        if (!validateLoanAmount()) {
            isValid = false;
        }

        if (!validateConsent()) {
            isValid = false;
        }

        return isValid;
    }

    /*
    ==========================================
    Loading state
    ==========================================
    */

    function startLoading() {
        formIsSubmitting = true;

        predictButton.disabled = true;
        predictButton.classList.add("loading");

        if (buttonText) {
            buttonText.textContent = "Analyzing Application...";
        }

        if (buttonLoader) {
            buttonLoader.style.display = "block";
        }

        if (buttonIcon) {
            buttonIcon.style.display = "none";
        }
    }

    /*
    ==========================================
    Reset loading state
    ==========================================
    */

    function stopLoading() {
        formIsSubmitting = false;

        predictButton.disabled = false;
        predictButton.classList.remove("loading");

        if (buttonText) {
            buttonText.textContent = "Predict Loan Eligibility";
        }

        if (buttonLoader) {
            buttonLoader.style.display = "none";
        }

        if (buttonIcon) {
            buttonIcon.style.display = "inline-block";
        }
    }

    /*
    ==========================================
    Real-time field validation
    ==========================================
    */

    const allFields = loanForm.querySelectorAll(
        "input:not([type='checkbox']), select"
    );

    allFields.forEach(function (field) {
        field.addEventListener("input", function () {
            clearError(field);
        });

        field.addEventListener("change", function () {
            clearError(field);
        });

        field.addEventListener("blur", function () {
            if (field.hasAttribute("required")) {
                validateRequiredField(field);
            }

            if (field.id === "applicantIncome") {
                validateApplicantIncome();
            }

            if (field.id === "coapplicantIncome") {
                validateCoapplicantIncome();
            }

            if (field.id === "loanAmount") {
                validateLoanAmount();
            }
        });
    });

    const consent = document.getElementById("consent");

    if (consent) {
        consent.addEventListener("change", function () {
            validateConsent();
        });
    }

    /*
    ==========================================
    Form submission
    ==========================================
    */

    loanForm.addEventListener("submit", function (event) {
        if (formIsSubmitting) {
            event.preventDefault();
            return;
        }

        const formIsValid = validateForm();

        if (!formIsValid) {
            event.preventDefault();

            const firstInvalidField = loanForm.querySelector(
                ".input-error"
            );

            if (firstInvalidField) {
                firstInvalidField.scrollIntoView({
                    behavior: "smooth",
                    block: "center"
                });

                setTimeout(function () {
                    firstInvalidField.focus();
                }, 400);
            }

            return;
        }

        startLoading();
    });

    /*
    ==========================================
    Browser back-button handling
    ==========================================
    */

    window.addEventListener("pageshow", function () {
        stopLoading();
    });
});
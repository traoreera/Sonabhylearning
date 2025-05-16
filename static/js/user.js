const submitButton = document.getElementById("submit-button");
submitButton.disabled = true;
// Fonction pour vérifier la force du mot de passe
function checkPasswordStrength(password) {
    const strengthBar = document.getElementById("strength-bar");
    const passRegEx = {
        "weak": /^(?=.*[a-z]).{6,}$/, // Faible : au moins 6 caractères, une minuscule
        "medium": /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$/, // Moyen : au moins 8 caractères, une minuscule, une majuscule et un chiffre
        "strong": /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&]).{8,}$/ // Fort : au moins 8 caractères, une minuscule, une majuscule, un chiffre et un caractère spécial
    };
    if (passRegEx.strong.test(password)) {
        strengthBar.innerHTML = "Fort";
        strengthBar.style.color = "green";
    } else if (passRegEx.medium.test(password)) {
        strengthBar.innerHTML = "Moyen";
        strengthBar.style.color = "orange";
        submitButton.disabled = true;
    } else if (passRegEx.weak.test(password)) {
        strengthBar.innerHTML = "Faible";
        submitButton.disabled = true;
        strengthBar.style.color = "red";
    } else {
        strengthBar.innerHTML = "Très faible";
        submitButton.disabled = true;
        strengthBar.style.color = "gray";
    }
}
// Fonction pour vérifier que les mots de passe correspondent
function checkPasswordsMatch() {
    const password = document.getElementById("password").value;
    const confirmPassword = document.getElementById("confirm_password").value;
    const submitButton = document.getElementById("submit-button");
    const passwordMatchMessage = document.getElementById("password-match-message");
    if (password === confirmPassword) {
        passwordMatchMessage.textContent = "Les mots de passe correspondent.";
        passwordMatchMessage.style.color = "green";
        submitButton.disabled = false;
    } else {
        passwordMatchMessage.textContent = "Les mots de passe ne correspondent pas.";
        passwordMatchMessage.style.color = "red";
        submitButton.disabled = true;
    }
}
// Ajouter un écouteur d'événement pour chaque champ
window.onload = function() {
    const passwordField = document.getElementById("password");
    const confirmPasswordField = document.getElementById("confirm_password");
    passwordField.addEventListener("input", function() {
        checkPasswordStrength(passwordField.value); // Vérifier la force du mot de passe à chaque saisie
    });
    confirmPasswordField.addEventListener("input", checkPasswordsMatch); // Vérifier si les mots de passe correspondent à chaque saisie
};
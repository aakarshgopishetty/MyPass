document.addEventListener('DOMContentLoaded', function() {
    const passwordInput = document.getElementById('passwordInput');
    const checkBtn = document.getElementById('checkBtn');
    const strengthFeedback = document.getElementById('strengthFeedback');
    const strengthLabel = document.getElementById('strengthLabel');
    const suggestions = document.getElementById('suggestions');
    const showPasswordBtn = document.getElementById("showPasswordBtn");

    showPasswordBtn.addEventListener('click', function() {
        const isPassword = passwordInput.type === 'password';
        passwordInput.type = isPassword ? 'text' : 'password';
        showPasswordBtn.textContent = isPassword ? '🐵' : '🙈';
    });

    checkBtn.addEventListener('click', function() {
        checkPasswordStrength();
    });

    function checkPasswordStrength() {
        const password = passwordInput.value;

        if (!password) {
            strengthFeedback.style.display = 'none';
            return;
        }

        let strength = 0;
        let feedbackSuggestions = [];

        if (password.length >= 8) strength++; 
        else feedbackSuggestions.push("Password should be at least 8 characters long.");

        if (/[A-Z]/.test(password)) strength++;
        else feedbackSuggestions.push("Add uppercase letters (A-Z).");

        if (/[a-z]/.test(password)) strength++;
        else feedbackSuggestions.push("Add lowercase letters (a-z).");

        if (/\d/.test(password)) strength++;
        else feedbackSuggestions.push("Add numbers (0-9).");

        if (/[\W_]/.test(password)) strength++;
        else feedbackSuggestions.push("Add special characters (!@#$%^&*...).");

        let strengthLabelText = "";
        switch (strength) {
            case 0:
            case 1:
                strengthLabelText = "Very Weak";
                strengthLabel.style.color = "#ff0000";
                break;
            case 2:
                strengthLabelText = "Weak";
                strengthLabel.style.color = "#ff8c00";
                break;
            case 3:
                strengthLabelText = "Fair";
                strengthLabel.style.color = "#ffd700";
                break;
            case 4:
                strengthLabelText = "Good";
                strengthLabel.style.color = "#9acd32";
                break;
            case 5:
                strengthLabelText = "Strong";
                strengthLabel.style.color = "#008000";
                break;
        }

        strengthLabel.textContent = strengthLabelText;

        if (feedbackSuggestions.length > 0) {
            suggestions.innerHTML = feedbackSuggestions.join('<br>');
        } else if (strength < 4) {
            suggestions.innerHTML = "Try adding more characters, numbers, or special symbols.";
        } else {
            suggestions.innerHTML = "Great password!";
        }

        strengthFeedback.style.display = 'block';
    }
});
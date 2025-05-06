// static/js/main.js
// Additional JavaScript functionality

document.addEventListener('DOMContentLoaded', function() {
    // Password strength meter
    const passwordField = document.querySelector('input[name="password"]');
    const confirmField = document.querySelector('input[name="confirm_password"]');
    
    if (passwordField && confirmField) {
        // Simple password validation
        const validatePassword = () => {
            if (passwordField.value !== confirmField.value) {
                confirmField.setCustomValidity("Passwords don't match");
            } else {
                confirmField.setCustomValidity('');
            }
        };
        
        passwordField.addEventListener('change', validatePassword);
        confirmField.addEventListener('keyup', validatePassword);
    }
    
    // Auto dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert:not(.alert-danger)');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            setTimeout(() => {
                alert.style.display = 'none';
            }, 500);
        }, 5000);
    });
    
    // Add animation to cards
    const cards = document.querySelectorAll('.card');
    if (cards.length) {
        cards.forEach((card, index) => {
            card.style.animationDelay = `${index * 0.1}s`;
            card.classList.add('animate-on-scroll');
        });
    }
});

// Function to show loading spinner when forms are submitted
function showLoading() {
    const submitButtons = document.querySelectorAll('button[type="submit"]');
    
    submitButtons.forEach(button => {
        button.addEventListener('click', function() {
            const form = this.closest('form');
            if (form && form.checkValidity()) {
                this.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Loading...';
                this.disabled = true;
            }
        });
    });
}

// Initialize functions
showLoading();
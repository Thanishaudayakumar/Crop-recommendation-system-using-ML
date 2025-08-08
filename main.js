// Main JavaScript file for Crop Recommendation System

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all components
    initializeFormValidation();
    initializeAnimations();
    initializeTooltips();
    initializeNavigation();
    
    console.log('Crop Recommendation System loaded successfully');
});

// Form Validation
function initializeFormValidation() {
    const form = document.querySelector('.prediction-form');
    if (!form) return;
    
    const inputs = form.querySelectorAll('input[required]');
    const submitBtn = form.querySelector('button[type="submit"]');
    
    // Real-time validation
    inputs.forEach(input => {
        input.addEventListener('input', function() {
            validateInput(this);
            updateSubmitButton(form, submitBtn);
        });
        
        input.addEventListener('blur', function() {
            validateInput(this);
        });
    });
    
    // Form submission
    form.addEventListener('submit', function(e) {
        let isValid = true;
        
        inputs.forEach(input => {
            if (!validateInput(input)) {
                isValid = false;
            }
        });
        
        if (!isValid) {
            e.preventDefault();
            showNotification('Please correct the highlighted fields', 'error');
            return;
        }
        
        // Show loading state
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Processing...';
        
        // Add loading overlay
        showLoadingOverlay();
    });
}

function validateInput(input) {
    const value = parseFloat(input.value);
    const min = parseFloat(input.getAttribute('min'));
    const max = parseFloat(input.getAttribute('max'));
    const name = input.getAttribute('name');
    
    // Remove existing validation classes
    input.classList.remove('is-valid', 'is-invalid');
    
    // Remove existing feedback
    const existingFeedback = input.parentNode.querySelector('.invalid-feedback');
    if (existingFeedback) {
        existingFeedback.remove();
    }
    
    // Check if empty
    if (!input.value.trim()) {
        input.classList.add('is-invalid');
        addValidationFeedback(input, `${getFieldDisplayName(name)} is required`);
        return false;
    }
    
    // Check if valid number
    if (isNaN(value)) {
        input.classList.add('is-invalid');
        addValidationFeedback(input, 'Please enter a valid number');
        return false;
    }
    
    // Check range
    if (value < min || value > max) {
        input.classList.add('is-invalid');
        addValidationFeedback(input, `${getFieldDisplayName(name)} must be between ${min} and ${max}`);
        return false;
    }
    
    // Additional specific validations
    if (!validateSpecificField(name, value)) {
        input.classList.add('is-invalid');
        addValidationFeedback(input, getSpecificValidationMessage(name, value));
        return false;
    }
    
    input.classList.add('is-valid');
    return true;
}

function validateSpecificField(fieldName, value) {
    switch(fieldName) {
        case 'ph':
            // pH should typically be between 4-9 for most crops
            return value >= 4 && value <= 9;
        case 'temperature':
            // Temperature should be reasonable for crop growth
            return value >= 10 && value <= 45;
        case 'humidity':
            // Humidity should be realistic
            return value >= 20 && value <= 100;
        default:
            return true;
    }
}

function getSpecificValidationMessage(fieldName, value) {
    switch(fieldName) {
        case 'ph':
            return 'pH should typically be between 4 and 9 for optimal crop growth';
        case 'temperature':
            return 'Temperature should be between 10°C and 45°C for crop cultivation';
        case 'humidity':
            return 'Humidity should be between 20% and 100%';
        default:
            return 'Invalid value';
    }
}

function addValidationFeedback(input, message) {
    const feedback = document.createElement('div');
    feedback.className = 'invalid-feedback';
    feedback.textContent = message;
    input.parentNode.appendChild(feedback);
}

function getFieldDisplayName(fieldName) {
    const displayNames = {
        'nitrogen': 'Nitrogen',
        'phosphorus': 'Phosphorus',
        'potassium': 'Potassium',
        'temperature': 'Temperature',
        'humidity': 'Humidity',
        'ph': 'pH',
        'rainfall': 'Rainfall'
    };
    return displayNames[fieldName] || fieldName;
}

function updateSubmitButton(form, button) {
    const inputs = form.querySelectorAll('input[required]');
    let allValid = true;
    
    inputs.forEach(input => {
        if (input.classList.contains('is-invalid') || !input.value.trim()) {
            allValid = false;
        }
    });
    
    button.disabled = !allValid;
}

// Animations
function initializeAnimations() {
    // Animate elements on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
            }
        });
    }, observerOptions);
    
    // Observe elements for animation
    document.querySelectorAll('.feature-card, .parameter-group').forEach(el => {
        observer.observe(el);
    });
    
    // Add CSS for animations
    if (!document.querySelector('#dynamic-animations')) {
        const style = document.createElement('style');
        style.id = 'dynamic-animations';
        style.textContent = `
            .feature-card, .parameter-group {
                opacity: 0;
                transform: translateY(30px);
                transition: all 0.6s ease-out;
            }
            .feature-card.animate-in, .parameter-group.animate-in {
                opacity: 1;
                transform: translateY(0);
            }
        `;
        document.head.appendChild(style);
    }
}

// Tooltips
function initializeTooltips() {
    // Add tooltips to form inputs
    const tooltips = {
        nitrogen: 'Nitrogen content in soil (mg/kg). Essential for leaf growth and chlorophyll production.',
        phosphorus: 'Phosphorus content in soil (mg/kg). Important for root development and flowering.',
        potassium: 'Potassium content in soil (mg/kg). Helps with water regulation and disease resistance.',
        temperature: 'Average temperature in Celsius. Critical for crop growth and development.',
        humidity: 'Relative humidity percentage. Affects water uptake and disease susceptibility.',
        ph: 'Soil pH level (0-14). Determines nutrient availability to plants.',
        rainfall: 'Annual rainfall in millimeters. Essential for crop water requirements.'
    };
    
    Object.keys(tooltips).forEach(fieldName => {
        const input = document.getElementById(fieldName);
        if (input) {
            input.setAttribute('title', tooltips[fieldName]);
            input.setAttribute('data-bs-toggle', 'tooltip');
            input.setAttribute('data-bs-placement', 'top');
        }
    });
    
    // Initialize Bootstrap tooltips
    if (typeof bootstrap !== 'undefined') {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
}

// Navigation
function initializeNavigation() {
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Navbar background on scroll
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        window.addEventListener('scroll', function() {
            if (window.scrollY > 50) {
                navbar.style.background = 'rgba(255, 255, 255, 0.95)';
                navbar.style.backdropFilter = 'blur(20px)';
            } else {
                navbar.style.background = 'rgba(255, 255, 255, 0.1)';
                navbar.style.backdropFilter = 'blur(10px)';
            }
        });
    }
}

// Utility Functions
function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `alert alert-${type === 'error' ? 'danger' : type} alert-dismissible fade show`;
    notification.innerHTML = `
        <i class="fas fa-${getNotificationIcon(type)} me-2"></i>
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    // Add to flash messages container or create one
    let container = document.querySelector('.flash-messages');
    if (!container) {
        container = document.createElement('div');
        container.className = 'flash-messages';
        document.body.appendChild(container);
    }
    
    container.appendChild(notification);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 5000);
}

function getNotificationIcon(type) {
    const icons = {
        success: 'check-circle',
        error: 'exclamation-triangle',
        warning: 'exclamation-circle',
        info: 'info-circle'
    };
    return icons[type] || 'info-circle';
}

function showLoadingOverlay() {
    const overlay = document.createElement('div');
    overlay.id = 'loading-overlay';
    overlay.innerHTML = `
        <div class="loading-content">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
            <p class="mt-3 text-primary fw-bold">Analyzing your data...</p>
        </div>
    `;
    
    // Add styles
    overlay.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(255, 255, 255, 0.9);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 9999;
        backdrop-filter: blur(5px);
    `;
    
    document.body.appendChild(overlay);
}

function hideLoadingOverlay() {
    const overlay = document.getElementById('loading-overlay');
    if (overlay) {
        overlay.remove();
    }
}

// Input formatting helpers
function formatInputValue(input, value) {
    const fieldName = input.getAttribute('name');
    
    switch(fieldName) {
        case 'ph':
            return Math.round(value * 10) / 10; // 1 decimal place
        case 'temperature':
        case 'humidity':
        case 'rainfall':
            return Math.round(value * 10) / 10; // 1 decimal place
        default:
            return Math.round(value); // No decimal places for nutrients
    }
}

// Auto-complete suggestions (can be expanded with real data)
function addAutoCompleteSuggestions() {
    const suggestions = {
        nitrogen: [40, 60, 80, 100, 120],
        phosphorus: [20, 40, 60, 80, 100],
        potassium: [20, 40, 60, 80, 100],
        temperature: [20, 25, 30, 35],
        humidity: [50, 60, 70, 80, 90],
        ph: [5.5, 6.0, 6.5, 7.0, 7.5],
        rainfall: [50, 100, 150, 200, 250]
    };
    
    Object.keys(suggestions).forEach(fieldName => {
        const input = document.getElementById(fieldName);
        if (input) {
            const datalist = document.createElement('datalist');
            datalist.id = `${fieldName}-suggestions`;
            
            suggestions[fieldName].forEach(value => {
                const option = document.createElement('option');
                option.value = value;
                datalist.appendChild(option);
            });
            
            input.setAttribute('list', datalist.id);
            input.parentNode.appendChild(datalist);
        }
    });
}

// Initialize auto-complete when DOM is ready
document.addEventListener('DOMContentLoaded', addAutoCompleteSuggestions);

// Export functions for testing
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        validateInput,
        formatInputValue,
        showNotification,
        hideLoadingOverlay
    };
}

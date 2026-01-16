// Health Assessment System - Interactive JavaScript

document.addEventListener('DOMContentLoaded', function() {
    initializeSliders();
    initializeFormValidation();
    initializeFormSubmission();
    initializeGenderDependentFields();
});

// Initialize slider-input synchronization
function initializeSliders() {
    const sliderPairs = [
        { slider: 'age-slider', input: 'age' },
        { slider: 'height-slider', input: 'height' },
        { slider: 'weight-slider', input: 'weight' },
        { slider: 'systolic-slider', input: 'systolic_bp' },
        { slider: 'diastolic-slider', input: 'diastolic_bp' },
        { slider: 'resting-hr-slider', input: 'resting_heart_rate' },
        { slider: 'max-hr-slider', input: 'max_heart_rate' },
        { slider: 'glucose-slider', input: 'glucose' },
        { slider: 'cholesterol-slider', input: 'cholesterol' },
        { slider: 'ldl-slider', input: 'ldl' },
        { slider: 'hdl-slider', input: 'hdl' },
        { slider: 'triglycerides-slider', input: 'triglycerides' },
        { slider: 'insulin-slider', input: 'insulin' },
        { slider: 'sleep-slider', input: 'sleep_hours' },
        { slider: 'vegetable-slider', input: 'vegetable_consumption_frequency' },
        { slider: 'meals-slider', input: 'num_main_meals' },
        { slider: 'water-slider', input: 'daily_water_consumption' },
        { slider: 'pregnancy-slider', input: 'pregnancies' }
    ];

    sliderPairs.forEach(pair => {
        const slider = document.getElementById(pair.slider);
        const input = document.getElementById(pair.input);
        
        if (slider && input) {
            // Update input when slider changes
            slider.addEventListener('input', function() {
                input.value = this.value;
                validateInput(input);
                updateHealthIndicators();
            });
            
            // Update slider when input changes
            input.addEventListener('input', function() {
                if (this.value >= slider.min && this.value <= slider.max) {
                    slider.value = this.value;
                }
                validateInput(this);
                updateHealthIndicators();
            });
            
            // Initialize slider position
            if (input.value) {
                slider.value = input.value;
            } else {
                input.value = slider.value;
            }
        }
    });
}

// Form validation
function initializeFormValidation() {
    const form = document.getElementById('healthForm');
    const inputs = form.querySelectorAll('input, select');
    
    inputs.forEach(input => {
        input.addEventListener('blur', function() {
            validateInput(this);
        });
        
        input.addEventListener('input', function() {
            clearValidationError(this);
        });
    });
}

function validateInput(input) {
    const value = input.value.trim();
    const inputType = input.type;
    const required = input.hasAttribute('required');
    
    // Clear previous validation
    clearValidationError(input);
    
    // Check required fields
    if (required && !value) {
        showValidationError(input, 'This field is required');
        return false;
    }
    
    // Validate numeric inputs
    if (inputType === 'number' && value) {
        const num = parseFloat(value);
        const min = parseFloat(input.min);
        const max = parseFloat(input.max);
        
        if (isNaN(num)) {
            showValidationError(input, 'Please enter a valid number');
            return false;
        }
        
        if (min !== undefined && num < min) {
            showValidationError(input, `Value must be at least ${min}`);
            return false;
        }
        
        if (max !== undefined && num > max) {
            showValidationError(input, `Value must be no more than ${max}`);
            return false;
        }
        
        // Specific health validations
        if (input.name === 'systolic_bp' && value) {
            const systolic = parseFloat(value);
            const diastolic = parseFloat(document.getElementById('diastolic_bp').value);
            if (diastolic && systolic <= diastolic) {
                showValidationError(input, 'Systolic pressure should be higher than diastolic');
                return false;
            }
        }
        
        if (input.name === 'diastolic_bp' && value) {
            const diastolic = parseFloat(value);
            const systolic = parseFloat(document.getElementById('systolic_bp').value);
            if (systolic && diastolic >= systolic) {
                showValidationError(input, 'Diastolic pressure should be lower than systolic');
                return false;
            }
        }
    }
    
    return true;
}

function showValidationError(input, message) {
    input.classList.add('error');
    
    // Remove existing error message
    const existingError = input.parentNode.querySelector('.error-message');
    if (existingError) {
        existingError.remove();
    }
    
    // Add new error message
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.textContent = message;
    errorDiv.style.color = 'var(--danger-color)';
    errorDiv.style.fontSize = '0.8rem';
    errorDiv.style.marginTop = '0.25rem';
    
    input.parentNode.appendChild(errorDiv);
}

function clearValidationError(input) {
    input.classList.remove('error');
    const errorMessage = input.parentNode.querySelector('.error-message');
    if (errorMessage) {
        errorMessage.remove();
    }
}

// Gender-dependent fields
function initializeGenderDependentFields() {
    const genderSelect = document.getElementById('gender');
    const pregnancySection = document.getElementById('pregnancy-section');
    
    if (genderSelect && pregnancySection) {
        genderSelect.addEventListener('change', function() {
            if (this.value === 'Female') {
                pregnancySection.style.display = 'block';
            } else {
                pregnancySection.style.display = 'none';
                document.getElementById('pregnancies').value = '';
            }
        });
    }
}

// Form submission
function initializeFormSubmission() {
    const form = document.getElementById('healthForm');
    
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        if (validateForm()) {
            submitHealthAssessment();
        }
    });
}

function validateForm() {
    const form = document.getElementById('healthForm');
    const requiredInputs = form.querySelectorAll('input[required], select[required]');
    let isValid = true;
    
    requiredInputs.forEach(input => {
        if (!validateInput(input)) {
            isValid = false;
        }
    });
    
    if (!isValid) {
        showNotification('Please correct the errors in the form before submitting.', 'error');
        // Scroll to first error
        const firstError = form.querySelector('.error');
        if (firstError) {
            firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
    }
    
    return isValid;
}

function submitHealthAssessment() {
    const form = document.getElementById('healthForm');
    const formData = new FormData(form);
    const data = {};
    
    // Convert FormData to regular object
    for (let [key, value] of formData.entries()) {
        data[key] = value;
    }
    
    // Show loading modal
    showLoadingModal();
    
    // Simulate progress steps
    simulateProgressSteps();
    
    // Submit to backend
    fetch('/api/assess', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        hideLoadingModal();
        
        console.log('Assessment result received:', result); // Debug log
        
        if (result.success && result.report) {
            // Store result in sessionStorage and redirect
            console.log('Storing result in sessionStorage:', result.report); // Debug log
            sessionStorage.setItem('healthAssessmentResult', JSON.stringify(result.report));
            
            // Verify storage
            const stored = sessionStorage.getItem('healthAssessmentResult');
            console.log('Verification - stored data:', stored); // Debug log
            
            window.location.href = '/results';
        } else {
            console.error('Assessment failed:', result); // Debug log
            showNotification('Assessment failed: ' + (result.error || 'No results received'), 'error');
        }
    })
    .catch(error => {
        hideLoadingModal();
        console.error('Error:', error);
        showNotification('An error occurred during assessment. Please try again.', 'error');
    });
}

// Loading modal functions
function showLoadingModal() {
    const modal = document.getElementById('loadingModal');
    modal.style.display = 'flex';
    document.body.style.overflow = 'hidden';
}

function hideLoadingModal() {
    const modal = document.getElementById('loadingModal');
    modal.style.display = 'none';
    document.body.style.overflow = 'auto';
}

function simulateProgressSteps() {
    const steps = document.querySelectorAll('.progress-steps .step');
    let currentStep = 0;
    
    const interval = setInterval(() => {
        if (currentStep < steps.length) {
            steps[currentStep].classList.add('active');
            currentStep++;
        } else {
            clearInterval(interval);
        }
    }, 800);
}

// Health indicators (visual feedback)
function updateHealthIndicators() {
    const age = parseFloat(document.getElementById('age').value) || 0;
    const weight = parseFloat(document.getElementById('weight').value) || 0;
    const height = parseFloat(document.getElementById('height').value) || 0;
    const systolic = parseFloat(document.getElementById('systolic_bp').value) || 0;
    const glucose = parseFloat(document.getElementById('glucose').value) || 0;
    
    // Calculate BMI if height and weight are available
    if (height > 0 && weight > 0) {
        const heightM = height / 100;
        const bmi = weight / (heightM * heightM);
        updateBMIIndicator(bmi);
    }
    
    // Update BP indicator
    if (systolic > 0) {
        updateBPIndicator(systolic);
    }
    
    // Update glucose indicator
    if (glucose > 0) {
        updateGlucoseIndicator(glucose);
    }
}

function updateBMIIndicator(bmi) {
    // Could add visual BMI indicator here
    console.log('BMI:', bmi.toFixed(1));
}

function updateBPIndicator(systolic) {
    // Could add visual BP indicator here
    console.log('Systolic BP:', systolic);
}

function updateGlucoseIndicator(glucose) {
    // Could add visual glucose indicator here
    console.log('Glucose:', glucose);
}

// Notification system
function showNotification(message, type = 'info') {
    // Remove existing notifications
    const existingNotifications = document.querySelectorAll('.notification');
    existingNotifications.forEach(n => n.remove());
    
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <i class="fas ${getNotificationIcon(type)}"></i>
            <span>${message}</span>
            <button class="notification-close" onclick="this.parentElement.parentElement.remove()">
                <i class="fas fa-times"></i>
            </button>
        </div>
    `;
    
    // Add styles
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${getNotificationColor(type)};
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        box-shadow: var(--shadow-lg);
        z-index: 1001;
        max-width: 400px;
        animation: slideInRight 0.3s ease;
    `;
    
    document.body.appendChild(notification);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 5000);
}

function getNotificationIcon(type) {
    switch (type) {
        case 'success': return 'fa-check-circle';
        case 'error': return 'fa-exclamation-circle';
        case 'warning': return 'fa-exclamation-triangle';
        default: return 'fa-info-circle';
    }
}

function getNotificationColor(type) {
    switch (type) {
        case 'success': return 'var(--success-color)';
        case 'error': return 'var(--danger-color)';
        case 'warning': return 'var(--warning-color)';
        default: return 'var(--primary-color)';
    }
}

// Form reset function
function resetForm() {
    const form = document.getElementById('healthForm');
    form.reset();
    
    // Reset sliders to default values
    const sliders = form.querySelectorAll('.slider');
    sliders.forEach(slider => {
        const input = document.getElementById(slider.id.replace('-slider', ''));
        if (input) {
            slider.value = slider.defaultValue || slider.min;
            input.value = slider.value;
        }
    });
    
    // Clear all validation errors
    const errorInputs = form.querySelectorAll('.error');
    errorInputs.forEach(input => clearValidationError(input));
    
    // Hide pregnancy section
    const pregnancySection = document.getElementById('pregnancy-section');
    if (pregnancySection) {
        pregnancySection.style.display = 'none';
    }
    
    showNotification('Form has been reset', 'info');
}

// Sample data function (for demo)
function loadSampleData() {
    const sampleData = {
        age: 52,
        gender: 'Male',
        height: 178,
        weight: 92,
        systolic_bp: 142,
        diastolic_bp: 92,
        glucose: 126,
        cholesterol: 245,
        ldl: 155,
        hdl: 42,
        triglycerides: 195,
        resting_heart_rate: 78,
        max_heart_rate: 145,
        smoking_status: 'Former',
        alcohol_intake: 'Moderate',
        physical_activity: 'Low',
        sleep_hours: 5.5,
        stress_level: 'High',
        salt_intake: 'High'
    };
    
    // Fill form with sample data
    Object.keys(sampleData).forEach(key => {
        const element = document.getElementById(key);
        if (element) {
            element.value = sampleData[key];
            
            // Update corresponding slider
            const slider = document.getElementById(key + '-slider');
            if (slider) {
                slider.value = sampleData[key];
            }
        }
    });
    
    updateHealthIndicators();
    showNotification('Sample data loaded successfully', 'success');
}

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + Enter to submit form
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        e.preventDefault();
        const submitBtn = document.querySelector('.submit-btn');
        if (submitBtn) {
            submitBtn.click();
        }
    }
    
    // Escape to close modal
    if (e.key === 'Escape') {
        const modal = document.getElementById('loadingModal');
        if (modal && modal.style.display === 'flex') {
            hideLoadingModal();
        }
    }
});

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    .notification-content {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    .notification-close {
        background: none;
        border: none;
        color: white;
        cursor: pointer;
        padding: 4px;
        border-radius: 4px;
        margin-left: auto;
    }
    
    .notification-close:hover {
        background: rgba(255, 255, 255, 0.2);
    }
    
    .error {
        border-color: var(--danger-color) !important;
        box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.1) !important;
    }
`;
document.head.appendChild(style);
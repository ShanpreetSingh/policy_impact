// Add these new functions
function showLoading(element) {
    element.disabled = true;
    element.innerHTML = `<span class="loading-spinner"></span> ${element.textContent}`;
}

function hideLoading(element, originalText) {
    element.disabled = false;
    element.textContent = originalText;
}

function validateForm(formData) {
    const errors = {};
    
    if (!formData.state) errors.state = 'Please select a state';
    if (!formData.scheme) errors.scheme = 'Please select a scheme';
    if (!formData.year || formData.year < 2000 || formData.year > 2030) {
        errors.year = 'Please enter a valid year (2000-2030)';
    }
    if (!formData.beneficiaries || formData.beneficiaries < 1) {
        errors.beneficiaries = 'Please enter a valid number of beneficiaries';
    }
    
    return errors;
}

// Enhanced form submission handler
async function handleFormSubmit(e) {
    e.preventDefault();
    const form = e.target;
    const submitBtn = form.querySelector('button[type="submit"]');
    const originalBtnText = submitBtn.textContent;
    
    const formData = {
        state: form.querySelector('#formState').value,
        scheme: form.querySelector('#formScheme').value,
        year: form.querySelector('#formYear').value,
        beneficiaries: form.querySelector('#formBeneficiaries').value
    };
    
    // Clear previous errors
    document.querySelectorAll('.form-error').forEach(el => el.remove());
    document.querySelectorAll('.is-invalid').forEach(el => el.classList.remove('is-invalid'));
    
    // Validate
    const errors = validateForm(formData);
    if (Object.keys(errors).length > 0) {
        Object.entries(errors).forEach(([field, message]) => {
            const input = form.querySelector(`#form${field.charAt(0).toUpperCase() + field.slice(1)}`);
            input.classList.add('is-invalid');
            const errorEl = document.createElement('div');
            errorEl.className = 'form-error';
            errorEl.textContent = message;
            input.parentNode.appendChild(errorEl);
        });
        return;
    }
    
    try {
        showLoading(submitBtn);
        
        const response = await fetch('/api/data/add/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(formData)
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.message || 'Submission failed');
        }
        
        showMessage('Data added successfully!', 'success');
        form.reset();
        await refreshCharts();
    } catch (error) {
        showMessage(error.message, 'error');
        console.error('Submission error:', error);
    } finally {
        hideLoading(submitBtn, originalBtnText);
    }
}

// Update your setupForm function
function setupForm() {
    document.getElementById('dataForm').addEventListener('submit', handleFormSubmit);
}
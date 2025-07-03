/**
 * CT Scanner Preinstallation System - Main JavaScript
 * Handles global functionality, utilities, and common interactions
 */

// Global configuration
const CONFIG = {
    DEBUG: false,
    API_BASE_URL: '/api',
    REFRESH_INTERVAL: 30000, // 30 seconds
    TOAST_DURATION: 5000, // 5 seconds
    ANIMATION_DURATION: 300,
    
    // CT Scanner specific constants
    SCANNER_MODELS: {
        NEUVIZ_ACE: 'NeuViz ACE (16-slice)',
        NEUVIZ_ACE_SP: 'NeuViz ACE SP (32-slice)',
        GE_OPTIMA: 'GE Optima CT660',
        SIEMENS_SOMATOM: 'Siemens SOMATOM X.cite',
        PHILIPS_INCISIVE: 'Philips Incisive CT',
        CANON_AQUILION: 'Canon Aquilion Prime SP',
        GE_REVOLUTION: 'GE Revolution EVO'
    },
    
    // Compliance thresholds
    COMPLIANCE: {
        EXCELLENT: 90,
        GOOD: 75,
        ACCEPTABLE: 60,
        POOR: 0
    }
};

// Global utilities
const Utils = {
    /**
     * Format currency values
     */
    formatCurrency: function(amount, currency = 'USD') {
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: currency,
            minimumFractionDigits: 0,
            maximumFractionDigits: 0
        }).format(amount);
    },

    /**
     * Format numbers with commas
     */
    formatNumber: function(number) {
        return new Intl.NumberFormat('en-US').format(number);
    },

    /**
     * Format dates
     */
    formatDate: function(date, options = {}) {
        const defaultOptions = {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
        };
        return new Intl.DateTimeFormat('en-US', { ...defaultOptions, ...options }).format(new Date(date));
    },

    /**
     * Format relative time
     */
    formatRelativeTime: function(date) {
        const now = new Date();
        const targetDate = new Date(date);
        const diffInSeconds = Math.floor((now - targetDate) / 1000);
        
        if (diffInSeconds < 60) return 'Just now';
        if (diffInSeconds < 3600) return `${Math.floor(diffInSeconds / 60)} minutes ago`;
        if (diffInSeconds < 86400) return `${Math.floor(diffInSeconds / 3600)} hours ago`;
        if (diffInSeconds < 604800) return `${Math.floor(diffInSeconds / 86400)} days ago`;
        
        return this.formatDate(date);
    },

    /**
     * Debounce function calls
     */
    debounce: function(func, wait, immediate) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                timeout = null;
                if (!immediate) func.apply(this, args);
            };
            const callNow = immediate && !timeout;
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
            if (callNow) func.apply(this, args);
        };
    },

    /**
     * Generate unique ID
     */
    generateId: function() {
        return Date.now().toString(36) + Math.random().toString(36).substr(2);
    },

    /**
     * Deep clone object
     */
    deepClone: function(obj) {
        return JSON.parse(JSON.stringify(obj));
    },

    /**
     * Check if element is in viewport
     */
    isInViewport: function(element) {
        const rect = element.getBoundingClientRect();
        return (
            rect.top >= 0 &&
            rect.left >= 0 &&
            rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
            rect.right <= (window.innerWidth || document.documentElement.clientWidth)
        );
    },

    /**
     * Smooth scroll to element
     */
    scrollToElement: function(element, offset = 0) {
        const targetPosition = element.offsetTop - offset;
        window.scrollTo({
            top: targetPosition,
            behavior: 'smooth'
        });
    },

    /**
     * Local storage helpers
     */
    storage: {
        set: function(key, value) {
            try {
                localStorage.setItem(key, JSON.stringify(value));
                return true;
            } catch (e) {
                console.warn('LocalStorage not available:', e);
                return false;
            }
        },
        
        get: function(key, defaultValue = null) {
            try {
                const item = localStorage.getItem(key);
                return item ? JSON.parse(item) : defaultValue;
            } catch (e) {
                console.warn('Error reading from localStorage:', e);
                return defaultValue;
            }
        },
        
        remove: function(key) {
            try {
                localStorage.removeItem(key);
                return true;
            } catch (e) {
                console.warn('Error removing from localStorage:', e);
                return false;
            }
        }
    }
};

// API utility functions
const API = {
    /**
     * Make API requests with error handling
     */
    request: async function(endpoint, options = {}) {
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            },
            credentials: 'same-origin'
        };

        const config = { ...defaultOptions, ...options };
        
        try {
            const response = await fetch(`${CONFIG.API_BASE_URL}${endpoint}`, config);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const contentType = response.headers.get('content-type');
            if (contentType && contentType.includes('application/json')) {
                return await response.json();
            }
            
            return await response.text();
        } catch (error) {
            console.error('API request failed:', error);
            throw error;
        }
    },

    /**
     * GET request
     */
    get: function(endpoint) {
        return this.request(endpoint, { method: 'GET' });
    },

    /**
     * POST request
     */
    post: function(endpoint, data) {
        return this.request(endpoint, {
            method: 'POST',
            body: JSON.stringify(data)
        });
    },

    /**
     * PUT request
     */
    put: function(endpoint, data) {
        return this.request(endpoint, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    },

    /**
     * DELETE request
     */
    delete: function(endpoint) {
        return this.request(endpoint, { method: 'DELETE' });
    }
};

// Toast notification system
const Toast = {
    container: null,

    init: function() {
        if (!this.container) {
            this.container = document.createElement('div');
            this.container.className = 'toast-container position-fixed top-0 end-0 p-3';
            this.container.style.zIndex = '9999';
            document.body.appendChild(this.container);
        }
    },

    show: function(message, type = 'info', duration = CONFIG.TOAST_DURATION) {
        this.init();

        const toast = document.createElement('div');
        toast.className = `toast show align-items-center text-white bg-${type} border-0`;
        toast.setAttribute('role', 'alert');
        toast.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">
                    <i class="fas fa-${this.getIcon(type)} me-2"></i>
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        `;

        this.container.appendChild(toast);

        // Auto-remove after duration
        setTimeout(() => {
            if (toast.parentNode) {
                toast.remove();
            }
        }, duration);

        // Add click to dismiss
        const closeButton = toast.querySelector('.btn-close');
        if (closeButton) {
            closeButton.addEventListener('click', () => {
                toast.remove();
            });
        }

        return toast;
    },

    getIcon: function(type) {
        const icons = {
            'success': 'check-circle',
            'danger': 'exclamation-triangle',
            'warning': 'exclamation-circle',
            'info': 'info-circle'
        };
        return icons[type] || 'info-circle';
    },

    success: function(message, duration) {
        return this.show(message, 'success', duration);
    },

    error: function(message, duration) {
        return this.show(message, 'danger', duration);
    },

    warning: function(message, duration) {
        return this.show(message, 'warning', duration);
    },

    info: function(message, duration) {
        return this.show(message, 'info', duration);
    }
};

// Loading indicator
const Loading = {
    show: function(message = 'Loading...') {
        let overlay = document.getElementById('loadingOverlay');
        if (!overlay) {
            overlay = document.createElement('div');
            overlay.id = 'loadingOverlay';
            overlay.className = 'position-fixed top-0 start-0 w-100 h-100 d-flex align-items-center justify-content-center';
            overlay.style.cssText = 'background: rgba(255,255,255,0.9); z-index: 9998; backdrop-filter: blur(2px);';
            overlay.innerHTML = `
                <div class="text-center">
                    <div class="spinner-border text-primary mb-3" style="width: 3rem; height: 3rem;">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                    <div class="h5">${message}</div>
                </div>
            `;
            document.body.appendChild(overlay);
        }
        return overlay;
    },

    hide: function() {
        const overlay = document.getElementById('loadingOverlay');
        if (overlay) {
            overlay.remove();
        }
    },

    /**
     * Show loading during async operation
     */
    during: async function(asyncOperation, message = 'Loading...') {
        this.show(message);
        try {
            const result = await asyncOperation;
            return result;
        } finally {
            this.hide();
        }
    }
};

// Form validation utilities
const FormValidator = {
    rules: {
        required: (value) => value.trim() !== '',
        email: (value) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value),
        phone: (value) => /^[\+]?[1-9][\d]{0,15}$/.test(value.replace(/\s/g, '')),
        number: (value) => !isNaN(value) && isFinite(value),
        minLength: (value, min) => value.length >= min,
        maxLength: (value, max) => value.length <= max,
        pattern: (value, pattern) => new RegExp(pattern).test(value),
        
        // CT Scanner specific validations
        dimension: (value) => {
            const num = parseFloat(value);
            return num >= 0 && num <= 50; // Reasonable room dimension limits
        },
        
        compliance: (value) => {
            const num = parseFloat(value);
            return num >= 0 && num <= 100;
        }
    },

    validate: function(form) {
        const errors = {};
        const elements = form.querySelectorAll('[data-validation]');

        elements.forEach(element => {
            const rules = JSON.parse(element.getAttribute('data-validation'));
            const value = element.value;
            const fieldName = element.name || element.id;

            for (const [ruleName, ruleValue] of Object.entries(rules)) {
                if (this.rules[ruleName]) {
                    const isValid = typeof ruleValue === 'boolean' 
                        ? this.rules[ruleName](value)
                        : this.rules[ruleName](value, ruleValue);

                    if (!isValid) {
                        if (!errors[fieldName]) errors[fieldName] = [];
                        errors[fieldName].push(this.getErrorMessage(ruleName, ruleValue));
                        element.classList.add('is-invalid');
                        break;
                    } else {
                        element.classList.remove('is-invalid');
                        element.classList.add('is-valid');
                    }
                }
            }
        });

        return {
            isValid: Object.keys(errors).length === 0,
            errors: errors
        };
    },

    getErrorMessage: function(rule, value) {
        const messages = {
            required: 'This field is required',
            email: 'Please enter a valid email address',
            phone: 'Please enter a valid phone number',
            number: 'Please enter a valid number',
            minLength: `Minimum length is ${value} characters`,
            maxLength: `Maximum length is ${value} characters`,
            dimension: 'Please enter a valid dimension (0-50m)',
            compliance: 'Please enter a value between 0-100%'
        };
        return messages[rule] || 'Invalid value';
    },

    showErrors: function(errors) {
        // Clear previous errors
        document.querySelectorAll('.invalid-feedback').forEach(el => el.remove());

        Object.entries(errors).forEach(([fieldName, fieldErrors]) => {
            const field = document.querySelector(`[name="${fieldName}"], #${fieldName}`);
            if (field) {
                fieldErrors.forEach(error => {
                    const errorDiv = document.createElement('div');
                    errorDiv.className = 'invalid-feedback d-block';
                    errorDiv.textContent = error;
                    field.parentNode.appendChild(errorDiv);
                });
            }
        });
    }
};

// Data management for CT Scanner specifications
const ScannerData = {
    specifications: {},

    init: function() {
        // Load scanner specifications if available
        this.loadSpecifications();
    },

    loadSpecifications: async function() {
        try {
            const specs = await API.get('/scanner-specifications');
            this.specifications = specs;
        } catch (error) {
            console.warn('Could not load scanner specifications:', error);
        }
    },

    getSpecification: function(model) {
        return this.specifications[model] || null;
    },

    isNeuViz: function(model) {
        return model && model.toLowerCase().includes('neuviz');
    },

    getComplianceLevel: function(score) {
        if (score >= CONFIG.COMPLIANCE.EXCELLENT) return 'excellent';
        if (score >= CONFIG.COMPLIANCE.GOOD) return 'good';
        if (score >= CONFIG.COMPLIANCE.ACCEPTABLE) return 'acceptable';
        return 'poor';
    },

    getComplianceColor: function(score) {
        const level = this.getComplianceLevel(score);
        const colors = {
            excellent: 'success',
            good: 'info',
            acceptable: 'warning',
            poor: 'danger'
        };
        return colors[level];
    }
};

// Real-time updates manager
const UpdateManager = {
    intervals: {},

    start: function(key, callback, interval = CONFIG.REFRESH_INTERVAL) {
        this.stop(key); // Clear existing interval
        this.intervals[key] = setInterval(callback, interval);
    },

    stop: function(key) {
        if (this.intervals[key]) {
            clearInterval(this.intervals[key]);
            delete this.intervals[key];
        }
    },

    stopAll: function() {
        Object.keys(this.intervals).forEach(key => this.stop(key));
    }
};

// Event manager for custom events
const EventManager = {
    events: {},

    on: function(event, callback) {
        if (!this.events[event]) {
            this.events[event] = [];
        }
        this.events[event].push(callback);
    },

    off: function(event, callback) {
        if (this.events[event]) {
            this.events[event] = this.events[event].filter(cb => cb !== callback);
        }
    },

    emit: function(event, data) {
        if (this.events[event]) {
            this.events[event].forEach(callback => callback(data));
        }
    }
};

// Initialize everything when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    // Initialize global components
    ScannerData.init();
    
    // Initialize Bootstrap tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize Bootstrap popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Global form validation
    document.querySelectorAll('form[data-validate]').forEach(form => {
        form.addEventListener('submit', function(e) {
            const validation = FormValidator.validate(this);
            if (!validation.isValid) {
                e.preventDefault();
                FormValidator.showErrors(validation.errors);
                Toast.error('Please correct the errors in the form');
            }
        });
    });

    // Global AJAX form handling
    document.querySelectorAll('form[data-ajax]').forEach(form => {
        form.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const data = Object.fromEntries(formData);
            const action = this.action || window.location.pathname;
            const method = this.method || 'POST';

            try {
                Loading.show('Processing...');
                const result = await API.request(action, {
                    method: method,
                    body: JSON.stringify(data)
                });

                if (result.success) {
                    Toast.success(result.message || 'Operation completed successfully');
                    if (result.redirect) {
                        window.location.href = result.redirect;
                    }
                } else {
                    Toast.error(result.message || 'Operation failed');
                }
            } catch (error) {
                Toast.error('An error occurred. Please try again.');
                console.error('Form submission error:', error);
            } finally {
                Loading.hide();
            }
        });
    });

    // Auto-save forms
    document.querySelectorAll('form[data-autosave]').forEach(form => {
        const saveKey = form.getAttribute('data-autosave');
        
        // Load saved data
        const savedData = Utils.storage.get(saveKey);
        if (savedData) {
            Object.entries(savedData).forEach(([name, value]) => {
                const field = form.querySelector(`[name="${name}"]`);
                if (field) {
                    field.value = value;
                }
            });
        }

        // Save on change
        form.addEventListener('input', Utils.debounce(function() {
            const formData = new FormData(this);
            const data = Object.fromEntries(formData);
            Utils.storage.set(saveKey, data);
        }, 1000));
    });

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                Utils.scrollToElement(target, 80);
            }
        });
    });

    // Auto-refresh indicators
    document.querySelectorAll('[data-auto-refresh]').forEach(element => {
        const interval = parseInt(element.getAttribute('data-auto-refresh')) || CONFIG.REFRESH_INTERVAL;
        const endpoint = element.getAttribute('data-endpoint');
        
        if (endpoint) {
            UpdateManager.start(`refresh-${Utils.generateId()}`, async () => {
                try {
                    const data = await API.get(endpoint);
                    element.innerHTML = data.html || data;
                } catch (error) {
                    console.error('Auto-refresh failed:', error);
                }
            }, interval);
        }
    });

    // Print functionality
    document.querySelectorAll('[data-print]').forEach(button => {
        button.addEventListener('click', function() {
            const target = this.getAttribute('data-print');
            if (target === 'page') {
                window.print();
            } else {
                const element = document.querySelector(target);
                if (element) {
                    const printWindow = window.open('', '_blank');
                    printWindow.document.write(`
                        <html>
                            <head>
                                <title>Print</title>
                                <link href="/static/css/main.css" rel="stylesheet">
                                <style>
                                    body { margin: 20px; }
                                    .no-print { display: none !important; }
                                </style>
                            </head>
                            <body>${element.innerHTML}</body>
                        </html>
                    `);
                    printWindow.document.close();
                    setTimeout(() => {
                        printWindow.print();
                        printWindow.close();
                    }, 500);
                }
            }
        });
    });

    // Global error handling
    window.addEventListener('error', function(e) {
        if (CONFIG.DEBUG) {
            console.error('Global error:', e.error);
        }
        // Optionally send to logging service
    });

    // Global unhandled promise rejection handling
    window.addEventListener('unhandledrejection', function(e) {
        if (CONFIG.DEBUG) {
            console.error('Unhandled promise rejection:', e.reason);
        }
        // Optionally send to logging service
    });

    // Page visibility change handling
    document.addEventListener('visibilitychange', function() {
        if (document.hidden) {
            // Page is hidden, pause updates
            UpdateManager.stopAll();
        } else {
            // Page is visible, resume updates
            // Restart auto-refresh intervals
            document.querySelectorAll('[data-auto-refresh]').forEach(element => {
                const interval = parseInt(element.getAttribute('data-auto-refresh')) || CONFIG.REFRESH_INTERVAL;
                const endpoint = element.getAttribute('data-endpoint');
                
                if (endpoint) {
                    UpdateManager.start(`refresh-${Utils.generateId()}`, async () => {
                        try {
                            const data = await API.get(endpoint);
                            element.innerHTML = data.html || data;
                        } catch (error) {
                            console.error('Auto-refresh failed:', error);
                        }
                    }, interval);
                }
            });
        }
    });

    // Emit page ready event
    EventManager.emit('pageReady', {
        timestamp: new Date(),
        pathname: window.location.pathname
    });
});

// Clean up on page unload
window.addEventListener('beforeunload', function() {
    UpdateManager.stopAll();
});

// Export globals for use in other scripts
window.CTScanner = {
    CONFIG,
    Utils,
    API,
    Toast,
    Loading,
    FormValidator,
    ScannerData,
    UpdateManager,
    EventManager
};

// Log initialization
if (CONFIG.DEBUG) {
    console.log('CT Scanner Preinstallation System initialized', {
        version: '1.0.0',
        timestamp: new Date(),
        config: CONFIG
    });
}
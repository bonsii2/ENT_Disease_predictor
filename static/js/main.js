/**
 * Global Main JavaScript for Navbar, Mobile Menu, and General UI Validation
 */

document.addEventListener('DOMContentLoaded', () => {
    // 1. Mobile Menu Hamburger Toggle
    const hamburgerBtn = document.getElementById('hamburgerBtn');
    const navMenu = document.getElementById('navMenu');

    if (hamburgerBtn && navMenu) {
        hamburgerBtn.addEventListener('click', () => {
            navMenu.classList.toggle('active');
            hamburgerBtn.classList.toggle('open');
        });
    }

    // 2. Active Page Navigation Link Highlighting
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        const linkPath = link.getAttribute('href');
        if (currentPath === linkPath || (currentPath === '/' && linkPath === '/')) {
            link.classList.add('active');
        } else if (currentPath.startsWith(linkPath) && linkPath !== '/') {
            link.classList.add('active');
        }
    });

    // 3. Contact Form Client-Side Validation
    const contactForm = document.getElementById('contactForm');
    const contactAlert = document.getElementById('contactAlert');

    if (contactForm) {
        contactForm.addEventListener('submit', (e) => {
            e.preventDefault();
            
            const nameInput = document.getElementById('contactName');
            const emailInput = document.getElementById('contactEmail');
            const subjectInput = document.getElementById('contactSubject');
            const messageInput = document.getElementById('contactMessage');
            
            // Basic Client Validation
            if (!nameInput.value.trim() || !emailInput.value.trim() || !messageInput.value.trim()) {
                showContactAlert('Please fill in all required fields (Name, Email, and Message).', 'danger');
                return;
            }
            
            // Simple Email Pattern Check
            const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailPattern.test(emailInput.value.trim())) {
                showContactAlert('Please enter a valid email address.', 'danger');
                return;
            }

            // Success feedback
            showContactAlert('Thank you for contacting us! Your message has been sent successfully.', 'success');
            contactForm.reset();
        });
    }

    function showContactAlert(message, type) {
        if (!contactAlert) return;
        contactAlert.textContent = message;
        contactAlert.style.display = 'block';
        if (type === 'success') {
            contactAlert.style.background = '#d1fae5';
            contactAlert.style.color = '#065f46';
            contactAlert.style.borderColor = '#34d399';
        } else {
            contactAlert.style.background = '#fee2e2';
            contactAlert.style.color = '#991b1b';
            contactAlert.style.borderColor = '#f87171';
        }
    }
});

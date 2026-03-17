$(document).ready(function() {
    // Theme Switcher Logic
    const themeToggle = $('#themeToggle');
    const themeIcon = themeToggle.find('i');
    
    const updateThemeIcon = (theme) => {
        if (theme === 'dark') {
            themeIcon.removeClass('fa-moon').addClass('fa-sun');
        } else {
            themeIcon.removeClass('fa-sun').addClass('fa-moon');
        }
    };

    // Initial icon state
    const currentTheme = document.documentElement.getAttribute('data-bs-theme') || 'light';
    updateThemeIcon(currentTheme);

    themeToggle.on('click', function(e) {
        e.preventDefault();
        const currentDataTheme = document.documentElement.getAttribute('data-bs-theme') || 'light';
        const newTheme = currentDataTheme === 'dark' ? 'light' : 'dark';
        
        document.documentElement.setAttribute('data-bs-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        updateThemeIcon(newTheme);
    });

    // Form Validation Logic
    $('#feedbackForm').on('submit', function(e) {
        let isValid = true;
        
        // Clear previous validation states
        $('.form-control, .form-select, .form-check-input').removeClass('is-invalid');
        
        // Validation logic
        const name = $('#name').val().trim();
        if (name === '') {
            $('#name').addClass('is-invalid');
            isValid = false;
        }
        
        const email = $('#email').val().trim();
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (email === '' || !emailRegex.test(email)) {
            $('#email').addClass('is-invalid');
            isValid = false;
        }
        
        const message = $('#message').val().trim();
        if (message.length < 20) {
            $('#message').addClass('is-invalid');
            isValid = false;
        }
        
        if (!isValid) {
            e.preventDefault();
            const toastEl = document.getElementById('validationToast');
            if (toastEl) {
                const toast = new bootstrap.Toast(toastEl);
                toast.show();
            }
            
            // Subtle card shake
            const card = $(this).closest('.card');
            card.addClass('shake');
            setTimeout(() => card.removeClass('shake'), 400);
        }
    });

    // Admin Page: Mark Resolved via AJAX
    $(document).on('click', '.mark-resolved-btn', function() {
        const btn = $(this);
        const id = btn.data('id');
        
        btn.prop('disabled', true).html('<span class="spinner-border spinner-border-sm me-2"></span>Updating...');
        
        $.ajax({
            url: '/update-status',
            type: 'POST',
            data: { id: id },
            success: function(response) {
                if (response.success) {
                    const badge = $('#status-badge-' + id);
                    
                    badge.fadeOut(200, function() {
                        $(this).removeClass('bg-warning text-dark')
                               .addClass('bg-success text-white')
                               .text('Resolved')
                               .fadeIn(200);
                    });
                    
                    btn.fadeOut(200, function() {
                        $(this).removeClass('btn-outline-success')
                               .addClass('btn-success disabled')
                               .text('Resolved')
                               .fadeIn(200);
                    });
                    
                    const toastEl = document.getElementById('statusToast');
                    if (toastEl) {
                        const toast = new bootstrap.Toast(toastEl);
                        toast.show();
                    }
                } else {
                    alert('Error: ' + response.message);
                    btn.prop('disabled', false).text('Mark Resolved');
                }
            },
            error: function() {
                alert('An error occurred while updating status.');
                btn.prop('disabled', false).text('Mark Resolved');
            }
        });
    });

    // Admin Page: View Details Modal logic
    $(document).on('click', '.view-details-btn', function() {
        const btn = $(this);
        const name = btn.data('name');
        const email = btn.data('email');
        const dept = btn.data('dept');
        const cat = btn.data('cat');
        const msg = btn.data('msg');
        const date = btn.data('date');
        const status = btn.data('status');
        
        // Populate modal
        $('#modal-name').text(name);
        $('#modal-email').text(email);
        $('#modal-dept').text(dept);
        $('#modal-cat').text(cat);
        $('#modal-msg').text(msg);
        $('#modal-date').text(date);
        $('#modal-status').text(status);
        $('#modal-avatar span').text(name.substring(0, 1).toUpperCase());
        
        // Handle badge colors in modal
        if (cat === 'Complaint') {
            $('#modal-cat').removeClass('bg-info text-info').addClass('bg-danger text-danger bg-opacity-10');
        } else {
            $('#modal-cat').removeClass('bg-danger text-danger bg-opacity-10').addClass('bg-info text-info');
        }
        
        if (status === 'Pending') {
            $('#modal-status').removeClass('bg-success text-white').addClass('bg-warning text-dark');
        } else {
            $('#modal-status').removeClass('bg-warning text-dark').addClass('bg-success text-white');
        }
        
        // Show modal
        const myModal = new bootstrap.Modal(document.getElementById('detailsModal'));
        myModal.show();
    });
});

$(document).ready(function() {
    // Form Validation Logic
    $('#feedbackForm').on('submit', function(e) {
        let isValid = true;
        
        // Clear previous validation states
        $('.form-control, .form-select, .form-check-input').removeClass('is-invalid');
        
        // 1. Name validation
        const name = $('#name').val().trim();
        if (name === '') {
            $('#name').addClass('is-invalid');
            isValid = false;
        }
        
        // 2. Email validation
        const email = $('#email').val().trim();
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (email === '' || !emailRegex.test(email)) {
            $('#email').addClass('is-invalid');
            isValid = false;
        }
        
        // 3. Department validation
        const department = $('#department').val();
        if (department === '') {
            $('#department').addClass('is-invalid');
            isValid = false;
        }
        
        // 4. Category validation
        if (!$('input[name="category"]:checked').val()) {
            $('input[name="category"]').addClass('is-invalid');
            isValid = false;
        }
        
        // 5. Message validation (min 20 chars)
        const message = $('#message').val().trim();
        if (message.length < 20) {
            $('#message').addClass('is-invalid');
            isValid = false;
        }
        
        if (!isValid) {
            e.preventDefault(); // Stop submission
            
            // Show toast error
            const toastEl = document.getElementById('validationToast');
            if (toastEl) {
                const toast = new bootstrap.Toast(toastEl);
                toast.show();
            }
            
            // Shake effect for the form
            $('#feedbackForm').closest('.card').animate({ left: '-10px' }, 50)
                .animate({ left: '10px' }, 50)
                .animate({ left: '-10px' }, 50)
                .animate({ left: '10px' }, 50)
                .animate({ left: '0px' }, 50);
        }
    });

    // Remove is-invalid class on input change
    $('.form-control, .form-select').on('input change', function() {
        $(this).removeClass('is-invalid');
    });
    
    $('input[type="radio"]').on('change', function() {
        $('input[name="' + $(this).attr('name') + '"]').removeClass('is-invalid');
    });

    // Admin Page: Mark Resolved via AJAX
    $('.mark-resolved-btn').on('click', function() {
        const btn = $(this);
        const id = btn.data('id');
        
        // Prepare to send AJAX request
        btn.prop('disabled', true).text('Updating...');
        
        $.ajax({
            url: '/update-status',
            type: 'POST',
            data: { id: id },
            success: function(response) {
                if (response.success) {
                    // Update UI on success
                    const badge = $('#status-badge-' + id);
                    
                    // Fade out, update content and classes, fade in
                    badge.fadeOut(200, function() {
                        $(this).removeClass('bg-warning text-dark')
                               .addClass('bg-success')
                               .text('Resolved')
                               .fadeIn(200);
                    });
                    
                    // Update button
                    btn.fadeOut(200, function() {
                        $(this).removeClass('btn-outline-success')
                               .addClass('btn-success disabled')
                               .text('Resolved')
                               .off('click')
                               .fadeIn(200);
                    });
                    
                    // Show success toast
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
});

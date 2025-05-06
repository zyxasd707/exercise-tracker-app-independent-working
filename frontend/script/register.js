/*************************************************************
 * Handle register form                                      *
 *************************************************************/
$(function () {
    $('#register-form').on('submit', function (e) {
        e.preventDefault();
        const $error = $('#registration-error');
        const $success = $('#registration-success');
        const formData = new FormData(this);

        const $button = $('#register-button');
        const $spinner = $('#register-spinner');
        const $buttonText = $('#register-text');
        
        // Password confirmation check
        const password = $('#password').val();
        const confirmPassword = $('#confirm-password').val();
        
        if (password !== confirmPassword) {
            $error.text('Passwords do not match!').removeClass('d-none');
            return;
        }
        
        $error.addClass('d-none');
        $success.addClass('d-none');
        $button.prop('disabled', true);
        $spinner.removeClass('d-none');
        $buttonText.addClass('d-none');
        
        fetch('/register', {
            method: 'POST',
            body: formData
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // If registration is successful, show success message and redirect
                    $success.removeClass('d-none');
                    setTimeout(() => {
                        $button.prop('disabled', false);
                        $spinner.addClass('d-none');
                        $buttonText.removeClass('d-none');
                        window.location.href = '/login';
                    }, 2000);
                } else {
                    // If registration fails, show the error message
                    $error.text(data.message || 'Registration failed!').removeClass('d-none');
                    $button.prop('disabled', false);
                    $spinner.addClass('d-none');
                    $buttonText.removeClass('d-none');
                }
            })
            .catch(error => {
                // Handle any errors that occur during the fetch
                $error.text('Error occurred during registration').removeClass('d-none');
                $button.prop('disabled', false);
                $spinner.addClass('d-none');
                $buttonText.removeClass('d-none');
                console.error(error);
            });
    });
});
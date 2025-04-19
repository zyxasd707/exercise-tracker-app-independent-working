/*************************************************************
 * Handle login form                                         *
 *************************************************************/
$(function () {
    $('#login-form').on('submit', function (e) {
        e.preventDefault();
        const $failure = $('#unsuccessful-login');
        const $success = $('#successful-login');
        const formData = new FormData(this);
        $failure.addClass('d-none');
        $success.addClass('d-none');
        
        fetch('/login', {
            method: 'POST',
            body: formData
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // If login is successful, redirect to the dashboard
                    $success.removeClass('d-none');
                } else {
                    // If login fails, show the error message
                    $failure.removeClass('d-none');
                }
            })
            .catch(error => {
                // Handle any errors that occur during the fetch
                $failure.text('Error occurred');
                console.error(error);
            });
    });
})

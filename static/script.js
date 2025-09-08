document.addEventListener('DOMContentLoaded', function() {
    var userBtn = document.getElementById('user-btn');
    var dropdown = document.getElementById('user-dropdown');
    if (userBtn && dropdown) {
        userBtn.addEventListener('click', function(e) {
            dropdown.classList.toggle('show');
            e.stopPropagation();
        });
        document.addEventListener('click', function(e) {
            if (!e.target.closest('#user-btn')) {
                dropdown.classList.remove('show');
            }
        });
    }
});
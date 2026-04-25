// main.js — students will add JavaScript here as features are built

// Video Modal functionality
(function() {
    const modal = document.getElementById('videoModal');
    const openBtn = document.getElementById('openVideoBtn');
    const closeBtn = document.getElementById('closeModalBtn');
    const iframe = document.getElementById('youtubeFrame');

    if (!modal || !openBtn) return;

    const videoUrl = 'https://www.youtube.com/embed/dQw4w9WgXcQ?autoplay=1';

    openBtn.addEventListener('click', function() {
        iframe.src = videoUrl;
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
    });

    function closeModal() {
        iframe.src = '';
        modal.classList.remove('active');
        document.body.style.overflow = '';
    }

    closeBtn.addEventListener('click', closeModal);

    modal.addEventListener('click', function(e) {
        if (e.target === modal) {
            closeModal();
        }
    });

    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && modal.classList.contains('active')) {
            closeModal();
        }
    });
})();

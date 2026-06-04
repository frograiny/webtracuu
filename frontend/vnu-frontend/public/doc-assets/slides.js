document.addEventListener('DOMContentLoaded', () => {
  const slides = document.querySelectorAll('.slide');
  const totalSlides = slides.length;
  let currentSlideIndex = 0;
  
  // Navigation elements
  const prevBtn = document.getElementById('prev-btn');
  const nextBtn = document.getElementById('next-btn');
  const playBtn = document.getElementById('play-btn');
  const fullscreenBtn = document.getElementById('fullscreen-btn');
  const dropdown = document.getElementById('slides-dropdown');
  const progressBar = document.getElementById('progress-bar');
  const timerBar = document.getElementById('timer-bar');
  
  // Auto-play settings
  let autoPlayInterval = null;
  let autoPlayDuration = 8000; // 8 seconds per slide
  let autoPlayStartTime = 0;
  let autoPlayRemainingTime = 8000;
  let isPlaying = false;
  let timerAnimation = null;

  // Initialize
  function init() {
    // Populate dropdown
    dropdown.innerHTML = '';
    slides.forEach((slide, idx) => {
      const title = slide.querySelector('.slide-title')?.textContent || `Slide ${idx + 1}`;
      const option = document.createElement('option');
      option.value = idx;
      option.textContent = `${idx + 1}. ${title}`;
      dropdown.appendChild(option);
    });

    updateSlides();
    setupEventListeners();
  }

  // Update Slides visual state
  function updateSlides() {
    slides.forEach((slide, idx) => {
      slide.classList.remove('active', 'past', 'future');
      if (idx === currentSlideIndex) {
        slide.classList.add('active');
      } else if (idx < currentSlideIndex) {
        slide.classList.add('past');
      } else {
        slide.classList.add('future');
      }
    });

    // Update controls
    prevBtn.disabled = currentSlideIndex === 0;
    nextBtn.disabled = currentSlideIndex === totalSlides - 1;
    dropdown.value = currentSlideIndex;
    
    // Update progress bar
    const progressPercent = ((currentSlideIndex + 1) / totalSlides) * 100;
    progressBar.style.width = `${progressPercent}%`;

    // Reset timer bar on change
    if (isPlaying) {
      startTimer();
    } else {
      timerBar.style.width = '0%';
    }
  }

  // Slide Navigation
  function goToSlide(index) {
    if (index >= 0 && index < totalSlides && index !== currentSlideIndex) {
      currentSlideIndex = index;
      updateSlides();
    }
  }

  function nextSlide() {
    if (currentSlideIndex < totalSlides - 1) {
      goToSlide(currentSlideIndex + 1);
    } else if (isPlaying) {
      // Loop back to start if playing and reached the end
      goToSlide(0);
    }
  }

  function prevSlide() {
    if (currentSlideIndex > 0) {
      goToSlide(currentSlideIndex - 1);
    }
  }

  // Auto-play Timer Logic
  function startTimer() {
    cancelAnimationFrame(timerAnimation);
    autoPlayStartTime = performance.now();
    
    function animateTimer(now) {
      const elapsed = now - autoPlayStartTime;
      const progress = Math.min((elapsed / autoPlayDuration) * 100, 100);
      timerBar.style.width = `${progress}%`;
      
      if (elapsed >= autoPlayDuration) {
        nextSlide();
      } else {
        timerAnimation = requestAnimationFrame(animateTimer);
      }
    }
    
    timerAnimation = requestAnimationFrame(animateTimer);
  }

  function stopTimer() {
    cancelAnimationFrame(timerAnimation);
    timerBar.style.width = '0%';
  }

  function togglePlay() {
    isPlaying = !isPlaying;
    if (isPlaying) {
      playBtn.innerHTML = '&#10074;&#10074;'; // Pause icon
      playBtn.title = "Tạm dừng tự chạy";
      startTimer();
    } else {
      playBtn.innerHTML = '&#9658;'; // Play icon
      playBtn.title = "Tự động chạy (8s)";
      stopTimer();
    }
  }

  // Fullscreen implementation
  function toggleFullscreen() {
    if (!document.fullscreenElement) {
      document.documentElement.requestFullscreen().catch(err => {
        console.error(`Error attempting to enable full-screen mode: ${err.message}`);
      });
    } else {
      document.exitFullscreen();
    }
  }

  // Monitor fullscreen change to update icon
  document.addEventListener('fullscreenchange', () => {
    if (document.fullscreenElement) {
      fullscreenBtn.innerHTML = '&#10066;'; // Exit fullscreen icon
      fullscreenBtn.title = "Thoát toàn màn hình (F)";
    } else {
      fullscreenBtn.innerHTML = '&#10064;'; // Fullscreen icon
      fullscreenBtn.title = "Xem toàn màn hình (F)";
    }
  });

  // Event Listeners Setup
  function setupEventListeners() {
    // Navigation Buttons
    prevBtn.addEventListener('click', () => {
      prevSlide();
      if (isPlaying) stopTimer(); // Pause autoplay on manual control
    });
    nextBtn.addEventListener('click', () => {
      nextSlide();
      if (isPlaying) stopTimer();
    });
    playBtn.addEventListener('click', togglePlay);
    fullscreenBtn.addEventListener('click', toggleFullscreen);

    // Dropdown change
    dropdown.addEventListener('change', (e) => {
      goToSlide(parseInt(e.target.value, 10));
      if (isPlaying) stopTimer();
    });

    // Keyboard bindings
    document.addEventListener('keydown', (e) => {
      switch (e.key) {
        case 'ArrowRight':
        case 'ArrowDown':
        case ' ': // Space
        case 'PageDown':
          e.preventDefault();
          nextSlide();
          if (isPlaying) stopTimer();
          break;
        case 'ArrowLeft':
        case 'ArrowUp':
        case 'PageUp':
          e.preventDefault();
          prevSlide();
          if (isPlaying) stopTimer();
          break;
        case 'Home':
          e.preventDefault();
          goToSlide(0);
          if (isPlaying) stopTimer();
          break;
        case 'End':
          e.preventDefault();
          goToSlide(totalSlides - 1);
          if (isPlaying) stopTimer();
          break;
        case 'f':
        case 'F':
          e.preventDefault();
          toggleFullscreen();
          break;
      }
    });

    // Touch Swipe handling
    let touchStartX = 0;
    let touchStartY = 0;
    
    document.addEventListener('touchstart', (e) => {
      touchStartX = e.changedTouches[0].screenX;
      touchStartY = e.changedTouches[0].screenY;
    }, { passive: true });

    document.addEventListener('touchend', (e) => {
      const touchEndX = e.changedTouches[0].screenX;
      const touchEndY = e.changedTouches[0].screenY;
      
      const diffX = touchEndX - touchStartX;
      const diffY = touchEndY - touchStartY;
      
      // Filter out small accidental gestures
      if (Math.abs(diffX) > Math.abs(diffY) && Math.abs(diffX) > 60) {
        if (diffX > 0) {
          prevSlide();
        } else {
          nextSlide();
        }
        if (isPlaying) stopTimer();
      }
    }, { passive: true });
  }

  // Run init
  init();
});

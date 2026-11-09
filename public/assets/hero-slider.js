const slider = document.querySelector('.hero-slider');
const slides = [...slider.querySelectorAll('.hero-slide')];
const controls = slider.querySelector('.hero-controls');
const counter = controls.querySelector('.hero-counter');
const announcement = controls.querySelector('.hero-announcement');
let active = 0;

function moveSlide(step) {
  slides[active].hidden = true;
  active = (active + step + slides.length) % slides.length;
  const slide = slides[active];
  if (slide.dataset.slideImage) {
    slide.style.setProperty('--slide-image', `url("/assets/${slide.dataset.slideImage}")`);
  }
  slide.hidden = false;
  counter.textContent = `${active + 1} / ${slides.length}`;
  announcement.textContent = `Slide ${active + 1} of ${slides.length}: ${slide.dataset.slideTitle}`;
}

for (const button of controls.querySelectorAll('[data-slide-step]')) {
  button.addEventListener('click', () => moveSlide(Number(button.dataset.slideStep)));
}
controls.addEventListener('keydown', (event) => {
  if (event.key !== 'ArrowLeft' && event.key !== 'ArrowRight') return;
  event.preventDefault();
  moveSlide(event.key === 'ArrowRight' ? 1 : -1);
});
controls.hidden = false;
slider.classList.add('has-controls');

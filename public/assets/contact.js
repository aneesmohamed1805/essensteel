const quoteForm = document.querySelector('#quote-form');

quoteForm.addEventListener('submit', (event) => {
  event.preventDefault();
  const details = [...new FormData(quoteForm)]
    .filter(([, value]) => value.trim())
    .map(([label, value]) => `${label}: ${value.trim()}`)
    .join('\r\n\r\n');
  const subject = encodeURIComponent('Essen Steel quote enquiry');
  window.location.href = `mailto:sales@essensteel.com?subject=${subject}&body=${encodeURIComponent(details)}`;
});

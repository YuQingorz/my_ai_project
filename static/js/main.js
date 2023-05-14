particlesJS.load("particles-js", "/static/particles.json", function () {
  console.log("callback - particles.js config loaded");
});

document.addEventListener('DOMContentLoaded', function () {
  const polygonCanvas = document.querySelector('.particles-canvas-el');
  if (polygonCanvas) {
    polygonCanvas.style.position = 'absolute';
    polygonCanvas.style.bottom = '0';
    polygonCanvas.style.zIndex = '-2';
  }
});

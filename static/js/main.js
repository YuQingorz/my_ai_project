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

document.addEventListener('DOMContentLoaded', function () {
    const pattern = Trianglify({
        width: window.innerWidth,
        height: window.innerHeight / 2, // 将高度设置为窗口高度的一半
    });
    const patternDiv = document.getElementById('trianglify-pattern');
    if (patternDiv) {
        patternDiv.style.backgroundImage = `url(${pattern.png()})`;
    }
});

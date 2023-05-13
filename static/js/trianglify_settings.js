document.addEventListener("DOMContentLoaded", function () {
  var pattern = Trianglify({
    width: window.innerWidth,
    height: window.innerHeight,
    cell_size: 80,
    variance: 0.75,
    x_colors: ["#34495e", "#3498db", "#9b59b6", "#2ecc71", "#e74c3c"],
    y_colors: "match_x",
  });

  document.body.appendChild(pattern.canvas());
});

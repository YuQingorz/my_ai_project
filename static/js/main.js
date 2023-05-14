particlesJS.load("particles-js", "/static/particles.json", function () {
  console.log("callback - particles.js config loaded");
});

.navbar {
  background-color: #34495e;
}

.navbar a {
  color: white;
  text-decoration: none;
  transition: all 0.3s;
}

.navbar a:hover {
  color: #3498db;
  text-decoration: underline;
}

.content-block {
  background-color: #f1f1f1;
  padding: 20px;
  margin-bottom: 20px;
  border-radius: 5px;
}

.content-block h2 {
  margin-top: 0;
  font-size: 24px;
  color: #34495e;
}

.content-block p {
  margin-bottom: 0;
  font-size: 16px;
}

.content-block img {
  max-width: 100%;
  height: auto;
  display: block;
  margin: 10px 0;
}

.button {
  background-color: #34495e;
  color: white;
  text-decoration: none;
  padding: 12px 20px;
  border-radius: 5px;
  font-size: 16px;
  display: inline-block;
  transition: all 0.3s;
}

.button:hover {
  background-color: #3498db;
}

input[type="text"],
select {
  width: 100%;
  padding: 12px 20px;
  margin-bottom: 20px;
  border-radius: 5px;
  border: 1px solid #ccc;
  display: inline-block;
  box-sizing: border-box;
}

input[type="submit"] {
  background-color: #34495e;
  color: white;
  padding: 12px 20px;
  border-radius: 5px;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.3s;
}

input[type="submit"]:hover {
  background-color: #3498db;
}

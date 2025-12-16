async function upload() {
  const fileInput = document.getElementById("fileInput");
  const file = fileInput.files[0];

  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch("https://YOUR_BACKEND_URL/run", {
    method: "POST",
    body: formData
  });

  const data = await res.json();
  document.getElementById("result").textContent =
    JSON.stringify(data, null, 2);
}

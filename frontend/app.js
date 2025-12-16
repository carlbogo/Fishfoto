const BACKEND_URL = "https://YOUR_BACKEND_URL/run";

function showPreview() {
  const fileInput = document.getElementById("fileInput");
  const preview = document.getElementById("previewImage");
  const container = document.getElementById("previewContainer");

  const file = fileInput.files[0];
  if (!file) return;

  preview.src = URL.createObjectURL(file);
  container.classList.remove("hidden");
}

async function upload() {
  const fileInput = document.getElementById("fileInput");
  const file = fileInput.files[0];

  const errorEl = document.getElementById("error");
  const btn = document.getElementById("runBtn");
  const resultBox = document.getElementById("resultBox");
  const resultPre = document.getElementById("result");
  const badge = document.getElementById("badge");

  errorEl.classList.add("hidden");
  resultBox.classList.add("hidden");

  if (!file) {
    errorEl.textContent = "Please select an image first.";
    errorEl.classList.remove("hidden");
    return;
  }

  btn.disabled = true;
  btn.textContent = "Running...";

  const formData = new FormData();
  formData.append("file", file);

  try {
    const res = await fetch(BACKEND_URL, {
      method: "POST",
      body: formData
    });

    if (!res.ok) {
      throw new Error("Backend error");
    }

    const data = await res.json();

    // Badge
    badge.textContent = `${data.predicted_class} (${Math.round(data.confidence * 100)}%)`;
    badge.className = "badge " + data.predicted_class;

    resultPre.textContent = JSON.stringify(data, null, 2);
    resultBox.classList.remove("hidden");

  } catch (err) {
    errorEl.textContent = "Failed to run pipeline.";
    errorEl.classList.remove("hidden");
  } finally {
    btn.disabled = false;
    btn.textContent = "Run pipeline";
  }
}

const BACKEND_URL = "/api/process";   // NGINX server

function showPreview() {
  const fileInput = document.getElementById("fileInput");
  const preview = document.getElementById("previewImage");
  const container = document.getElementById("previewContainer");
  const resultBox = document.getElementById("resultBox");
  const errorEl = document.getElementById("error");

  const file = fileInput.files[0];
  if (!file) return;

  // Update preview
  preview.src = URL.createObjectURL(file);
  container.classList.remove("hidden");

  // 🔹 CLEAR OLD RESULTS
  resultBox.classList.add("hidden");
  errorEl.classList.add("hidden");
}


async function upload() {
  const fileInput = document.getElementById("fileInput");
  const file = fileInput.files[0];

  const errorEl = document.getElementById("error");
  const btn = document.getElementById("runBtn");
  const resultBox = document.getElementById("resultBox");

  const totalEl = document.getElementById("totalCount");
  const kiluEl = document.getElementById("kiluCount");
  const raimEl = document.getElementById("raimCount");
  const resultImg = document.getElementById("resultImage");

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
      body: formData,
    });

    if (!res.ok) {
      throw new Error(`Backend error: ${res.status}`);
    }

    const data = await res.json();

    // ✅ Correct response keys
    totalEl.textContent = data.total_fish;
    kiluEl.textContent = data.num_kilu;
    raimEl.textContent = data.num_raim;

    if (data.image_base64) {
      resultImg.src = "data:image/png;base64," + data.image_base64;
    }

    resultBox.classList.remove("hidden");

  } catch (err) {
    console.error("Pipeline error:", err);
    errorEl.textContent = "Failed to run pipeline.";
    errorEl.classList.remove("hidden");
  } finally {
    btn.disabled = false;
    btn.textContent = "Run pipeline";
  }
}

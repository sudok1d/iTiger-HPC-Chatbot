async function getBotResponse(text, imageFile) {
  const form = new FormData();
  form.append("message", text);
  if (imageFile) {
    form.append("image", imageFile);
  }

  const res = await fetch("http://localhost:7860/chat", {
    method: "POST",
    body: form
  });

  const data = await res.json();
  return data.response;
}

async function sendMessage() {
  const input = document.getElementById("userInput");
  const imgInput = document.getElementById("imageInput");

  const text = input.value.trim();
  const imageFile = imgInput.files[0];

  if (!text && !imageFile) return;

  addMessage(text || "[Image sent]", "user");
  input.value = "";
  imgInput.value = "";

  const reply = await getBotResponse(text, imageFile);
  addMessage(reply, "bot");
}

function addMessage(text, sender) {
  const box = document.getElementById("chatbox");
  const div = document.createElement("div");
  div.className = "message " + sender;
  div.textContent = text;
  box.appendChild(div);
  box.scrollTop = box.scrollHeight;
}

document.addEventListener("DOMContentLoaded", () => {
  const input = document.getElementById("userInput");
  input.addEventListener("keyup", event => {
    if (event.key === "Enter") sendMessage();
  });
});

// function addMessage(text, sender) {
//     const box = document.getElementById("chatbox");
//     const div = document.createElement("div");
//     div.className = "message " + sender;
//     div.textContent = text;
//     box.appendChild(div);
//     box.scrollTop = box.scrollHeight;
//   }
  
//   function sendMessage() {
//     const input = document.getElementById("userInput");
//     const text = input.value.trim();
//     if (!text) return;
  
//     addMessage(text, "user");
//     input.value = "";
  
//     const reply = getBotResponse(text);
//     addMessage(reply, "bot");
//   }
  
// //   function getBotResponse(text) {
// //     text = text.toLowerCase();
  
// //     if (text.includes("proposal"))
// //       return "A strong proposal explains the motivation, gap, methods, and expected results.";
  
// //     if (text.includes("vision") || text.includes("vlm"))
// //       return "Vision-language models combine image encoders with language models. You could explore instruction tuning or multimodal alignment.";
  
// //     return "Tell me more about what you want to build.";
// //   }

async function getBotResponse(text) {
    // simulate a fake backend delay
    await new Promise(r => setTimeout(r, 300));
    return "Test reply: " + text;
  }
  
  async function sendMessage() {
    const input = document.getElementById("userInput");
    const text = input.value.trim();
    if (!text) return;
  
    addMessage(text, "user");
    input.value = "";
  
    const reply = await getBotResponse(text); 
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
  
    input.addEventListener("keyup", function(event) {
      if (event.key === "Enter") {
        sendMessage();
      }
    });
  });
  
  
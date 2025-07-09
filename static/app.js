function sendMessage() {
    const input = document.getElementById("user-input");
    const message = input.value.trim();
    const chatBox = document.getElementById("chat-box");

    if (!message) return;

    // Display user message
    chatBox.innerHTML += `<p><strong>You:</strong> ${message}</p>`;

    fetch('/ask', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ query:message })
    })
    .then(response => response.json())
    .then(data => {
        // Display bot response
        chatBox.innerHTML += `<p><strong>Bot:</strong> ${data.answer}</p>`;
        chatBox.scrollTop = chatBox.scrollHeight;
    })
    .catch(error => {
        console.error('Error getting response:', error);
        chatBox.innerHTML += `<p style="color:red;"><strong>Error:</strong> Unable to get response from server.</p>`;
    });

    input.value = "";
    }

function clearChat() {
    const chatBox = document.getElementById("chat-box");
    chatBox.innerHTML = '';
}
      


document.addEventListener("DOMContentLoaded", () => {

    function uploadPDF() {
        const fileInput = document.getElementById('pdf-upload');
        const file = fileInput.files[0];

        if (!file) {
            alert("Please select a PDF file.");
            return;
        }

        const formData = new FormData();
        formData.append('file', file);

        fetch('/pdf', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            console.log("Upload successful:", data);
        })
        .catch(error => {
            console.error('Error uploading PDF:', error);
            alert('An error occurred while uploading the PDF.');
        });
    }


    document.getElementById("user-input").addEventListener("keydown", function(event) {
        if (event.key === "Enter" && !event.shiftKey) {
            event.preventDefault();
            sendMessage();
        }
    });

    // Drop tone
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('pdf-upload');
    const fileNameSpan = document.getElementById('selected-filename');
    dropZone.addEventListener('click', () => fileInput.click());

    // File selection
    fileInput.addEventListener('change', () => {
        const file = fileInput.files[0];
        fileNameSpan.textContent = file ? file.name : "No file selected.";

        if (file && file.type === "application/pdf") {
            uploadPDF();
        } else {
            alert("Please select a valid PDF file.");
        }
    });

    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('dragover');
    });

    dropZone.addEventListener('dragleave', () => {
        dropZone.classList.remove('dragover');
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('dragover');

        const file = e.dataTransfer.files[0];
        if (file && file.type === "application/pdf") {
            fileInput.files = e.dataTransfer.files;
            fileNameSpan.textContent = file.name;
            uploadPDF();
        } else {
            alert("Please drop a valid PDF file.");
        }
    });
});

const input = document.getElementById('input_prompt');
const button = document.getElementById('submit_button');
const messagesDiv = document.getElementById('messages');

let FILE_ID = ""
let curr_chat_id = chat_id

const file = document.getElementById("pdf_upload")
function update_file_status(status, error=null) {
    if (status) {
    appendMessage(`Uploaded ${file.files[0].name}`, 'file_uploaded')
    }
    else {
    window.alert(error)
    }
}
file.addEventListener("change", async () => {
        if (!file.files.length) {
        window.alert("No files selected")
        return ;
        }

        if (file.files.length > 1) {
        window.alert("You can upload only a single file at once")
        return ;
        }
        
        const form_data = new FormData()
        form_data.append("file", file.files[0])
        form_data.append("chatID", chat_id)
        
        try {

            const response = await fetch(`/upload_pdf`, {
                "method" : "POST",
                "body" : form_data
            })

            const json = await response.json()

            update_file_status(true, null)
            FILE_ID = json.filename
            // return json.filename
            
        }
        catch (error) {
            update_file_status(false, "Something went wrong while uploading PDF.")
        }
        
})
function appendMessage(text, sender) {
    const msg = document.createElement('div');
    msg.classList.add('message', sender);
if (sender === 'bot') {
    msg.innerHTML = `<pre>${text}</pre>`; // Render HTML for bot
}
if (sender === "file_uploaded") {
    msg.innerHTML = text
}
else {
    msg.innerHTML  = text; // Keep user input safe
}
    messagesDiv.appendChild(msg);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

button.addEventListener('click', async event => {
    event.preventDefault()
    
    const userText = input.value.trim();
    if (!userText) return;
    
    appendMessage(userText, 'user');
    input.value = '';
    
    try {
    const response = await fetch(`/generate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ data: userText, id : FILE_ID, chatID : chat_id})
    });
    const result = await response.json();
    appendMessage(result.llm_response, 'bot');
    } catch (err) {
    appendMessage('Error connecting to server.', 'bot');
    }
});

input.addEventListener('keypress', (e) => {
if (e.key === 'Enter') {
    button.click();
}
});



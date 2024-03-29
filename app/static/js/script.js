document.addEventListener('DOMContentLoaded', handleFileUpload);

function handleFileUpload() {
    const fileInput = document.getElementById('fileInput');
    const uploadButton = document.getElementById('uploadButton');
    fileInput.addEventListener('change', function(event){
        var files = event.target.files;
        if (files.length === 0) {
            alert('Please select a file first.');
            return;
        }
        const formData = new FormData();
        for (var i = 0; i < files.length; i++) {
            var file = files[i];
            formData.append('files[]', file, file.name);
        }
        console.log(formData)

        var serverMessage = document.createElement('div');
        serverMessage.classList.add('chat-message', 'server-response', 'learning-from-file');
        serverMessage.textContent = "Learning from files";
        document.getElementById('chatContent').appendChild(serverMessage);
        var chatContent = document.getElementById('chatContent');
        chatContent.scrollTop = chatContent.scrollHeight;

        fetch('/create-embedding', {
            method: 'POST',
            body: formData,
        })
        .then(response => response.text())
        .then(data => {
            console.log(JSON.parse(data).message)
            serverMessage.textContent = JSON.parse(data).message;
        })
        .catch(error => {
            serverMessage.textContent = "I couldn't learn from this file";
        })
        .finally(() => {
            serverMessage.classList.remove('learning-from-file');
        });
    });
}


document.addEventListener('DOMContentLoaded', function() {
    const sendButton = document.getElementById('sendButton');
    const chatInput = document.getElementById('chatInput');
    const chatContent = document.getElementById('chatContent');

    chatInput.addEventListener('keydown', function(event){
        if(event.key=='Enter'){
            event.preventDefault();
            askQuestion();
        }
    })

    sendButton.addEventListener('click', ()=>{
        askQuestion();
    });

    function askQuestion(){
        const query = chatInput.value.trim();
        if (query === '') {
            alert('Please enter a query.');
            return;
        }
        addMessageToChat('user-message', query);
        const requestBody = JSON.stringify({ query: query });

        var serverMessage = document.createElement('div');
        serverMessage.classList.add('chat-message', 'server-response', 'learning-from-file');
        serverMessage.textContent = "Let me think!";
        document.getElementById('chatContent').appendChild(serverMessage);
        var chatContent = document.getElementById('chatContent');
        chatContent.scrollTop = chatContent.scrollHeight;

        fetch('/run-query', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: requestBody
        })
        .then(response => response.json())
        .then(data => {
            if (data && data.message) {
                console.log(data)
                serverMessage.textContent = data.message;
                const sources = data.sources
                for (const [source, pages] of Object.entries(sources)) {
                    const sourceDiv = createSourceDiv(source, pages);
                    serverMessage.appendChild(sourceDiv);
                }
            } else {
                addMessageToChat('server-response', 'No results found or invalid response format.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            addMessageToChat('server-response', 'Error fetching results.');
        })
        .finally(()=>{
            serverMessage.classList.remove('learning-from-file');
        });

        chatInput.value = '';
    }

    function addMessageToChat(className, text) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `chat-message ${className}`;
        messageDiv.textContent = text;
        chatContent.appendChild(messageDiv);
        chatContent.scrollTop = chatContent.scrollHeight; // Scroll to the bottom
    }
});


// Function to create a div for each source
function createSourceDiv(source, pages) {
    const div = document.createElement('div');
    div.className = 'source-info';
    let content;
    if(pages){
        content = `<i>${source}: P. ${pages}</i>`
    }else{
        content = `<i>${source}</i>`
    }
    div.innerHTML = content;
    return div;
}

document.addEventListener('DOMContentLoaded', handleFileUpload);

function handleFileUpload() {
    const fileInput = document.getElementById('fileInput');
    const uploadButton = document.getElementById('uploadButton');

    uploadButton.addEventListener('click', function() {
        if (fileInput.files.length === 0) {
            alert('Please select a file first.');
            return;
        }
        const file = fileInput.files[0];
        const formData = new FormData();
        formData.append('file', file);
        fetch('/create-embedding', {
            method: 'POST',
            body: formData,
        })
        .then(response => response.text())
        .then(data => {
            // console.log(data);
        })
        .catch(error => {
            // console.error(error);
        });
    });
}
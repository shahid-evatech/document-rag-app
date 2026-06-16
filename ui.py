def get_frontend_html() -> str:
    """Returns the raw HTML/JS string for the client-side user interface."""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Document QA App</title>
        <style>
            body { font-family: sans-serif; max-width: 650px; margin: 40px auto; padding: 20px; line-height: 1.6; }
            .box { border: 1px solid #ddd; padding: 20px; margin-bottom: 20px; border-radius: 6px; background: #f9f9f9; }
            button { background: #1a73e8; color: white; border: none; padding: 10px 15px; border-radius: 4px; cursor: pointer; }
            textarea { width: 100%; height: 60px; margin-bottom: 10px; }
            .source { background: #f1f3f4; border-left: 3px solid #1a73e8; padding: 10px; margin-top: 5px; font-size: 0.85em; }
        </style>
    </head>
    <body>
        <h2>📄 Simple Document Q&A (RAG)</h2>
        <div class="box">
            <h3>1. Upload Document</h3>
            <input type="file" id="fileInput" accept=".txt,.pdf">
            <button onclick="uploadFile()">Upload</button>
            <p id="uploadStatus"></p>
        </div>
        <div class="box">
            <h3>2. Ask a Question</h3>
            <textarea id="questionInput" placeholder="Ask something about the document..."></textarea>
            <button onclick="askQuestion()">Ask</button>
            <h4>Answer:</h4>
            <p id="answerOutput" style="font-weight: bold;"></p>
            <h4>Sources used:</h4>
            <div id="sourcesOutput"></div>
        </div>
        <script>
            async function uploadFile() {
                const fileInput = document.getElementById('fileInput');
                if (!fileInput.files[0]) return alert('Select a file.');
                const formData = new FormData();
                formData.append('file', fileInput.files[0]);
                document.getElementById('uploadStatus').innerText = "Processing...";
                const res = await fetch('/upload', { method: 'POST', body: formData });
                const data = await res.json();
                document.getElementById('uploadStatus').innerText = data.message || data.error;
            }
            async function askQuestion() {
                const question = document.getElementById('questionInput').value;
                document.getElementById('answerOutput').innerText = "Thinking...";
                document.getElementById('sourcesOutput').innerHTML = "";
                const res = await fetch('/ask', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ question: question })
                });
                const data = await res.json();
                document.getElementById('answerOutput').innerText = data.answer;
                if (data.sources && data.answer !== "I couldn't find that.") {
                    data.sources.forEach((src, idx) => {
                        const div = document.createElement('div');
                        div.className = 'source';
                        div.innerText = `[Source ${idx + 1}]: ${src}`;
                        document.getElementById('sourcesOutput').appendChild(div);
                    });
                }
            }
        </script>
    </body>
    </html>
    """
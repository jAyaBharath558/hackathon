const API_URL = "/query";

async function askQuestion() {

    const questionInput =
        document.getElementById("question");

    const question =
        questionInput.value.trim();

    if (!question) return;

    const chatBox =
        document.getElementById("chat-box");

    // User Message

    chatBox.innerHTML += `
        <div class="message user">
            ${question}
        </div>
    `;

    questionInput.value = "";

    try {

        const response =
            await fetch(API_URL, {

                method: "POST",

                headers: {
                    "Content-Type":
                    "application/json"
                },

                body: JSON.stringify({
                    question: question
                })
            });

        const data =
            await response.json();

        let sourceHTML = "";

        if (data.sources) {

            sourceHTML =
                data.sources.map(src =>

                    `<div>
                        📄 ${src.file_name}
                        (Page ${src.page_number})
                    </div>`

                ).join("");
        }

        chatBox.innerHTML += `
            <div class="message bot">

                <b>Answer:</b><br><br>

                ${data.answer}

                <div class="sources">

                    <b>Sources:</b>

                    ${sourceHTML}

                </div>

            </div>
        `;

        chatBox.scrollTop =
            chatBox.scrollHeight;

    } catch(error) {

        chatBox.innerHTML += `
            <div class="message bot">
                Error connecting to API
            </div>
        `;
    }
}
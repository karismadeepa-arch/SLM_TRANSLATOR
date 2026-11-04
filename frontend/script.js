async function translateText() {

    const englishText = document
        .getElementById("englishText")
        .value.trim();

    const tamilOutput = document.getElementById("tamilText");

    const status = document.getElementById("status");

    const button = document.getElementById("translateBtn");

    if (!englishText) {

        status.textContent = "Please enter English text.";

        return;
    }

    button.disabled = true;

    status.textContent = "Translating... Please wait.";

    tamilOutput.textContent = "";

    try {

        const response = await fetch("/translate", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                text: englishText
            })

        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Translation failed");
        }

        tamilOutput.textContent = data.tamil;

        status.textContent = "Translation completed!";

    }

    catch (error) {

        tamilOutput.textContent = "";

        status.textContent = error.message;

    }

    finally {

        button.disabled = false;

    }

}
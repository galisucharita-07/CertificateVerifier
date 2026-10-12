
const registerForm = document.getElementById("registerForm");
const verifyForm = document.getElementById("verifyForm");
const chainButton = document.getElementById("chainButton");

const registerResult = document.getElementById("registerResult");
const verifyResult = document.getElementById("verifyResult");
const chainResult = document.getElementById("chainResult");

// Convert a form into a JavaScript object
function getFormData(form) {
    const formData = new FormData(form);
    return Object.fromEntries(formData.entries());
}

// Display a result safely as text
function showMessage(element, message, type) {
    element.replaceChildren();

    const messageElement = document.createElement("p");
    messageElement.className = type;
    messageElement.textContent = message;

    element.appendChild(messageElement);
}

// Send data to Flask and read the response
async function sendRequest(url, data) {
    const response = await fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    });

    const result = await response.json();

    if (!response.ok) {
        throw new Error(result.message || "Request failed.");
    }

    return result;
}

// Register a certificate
registerForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    showMessage(registerResult, "Registering certificate...", "info");

    try {
        const data = getFormData(registerForm);
        const result = await sendRequest("/register", data);

        showMessage(
            registerResult,
            `${result.message} Block number: ${result.block_index}.`,
            "success"
        );

        registerForm.reset();
    } catch (error) {
        showMessage(registerResult, error.message, "error");
    }
});

// Verify a certificate
verifyForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    showMessage(verifyResult, "Verifying certificate...", "info");

    try {
        const data = getFormData(verifyForm);
        const result = await sendRequest("/verify", data);

        if (result.valid) {
            showMessage(
                verifyResult,
                `${result.message} Blockchain valid: ${result.blockchain_valid}.`,
                "success"
            );
        } else {
            showMessage(verifyResult, result.message, "error");
        }
    } catch (error) {
        showMessage(verifyResult, error.message, "error");
    }
});

// View blockchain blocks
chainButton.addEventListener("click", async function () {
    chainResult.replaceChildren();

    const loading = document.createElement("p");
    loading.textContent = "Loading blockchain...";
    chainResult.appendChild(loading);

    try {
        const response = await fetch("/chain");

        if (!response.ok) {
            throw new Error("Could not load the blockchain.");
        }

        const result = await response.json();
        chainResult.replaceChildren();

        const status = document.createElement("p");
        status.className = result.chain_valid ? "success" : "error";
        status.textContent = result.chain_valid
            ? "Blockchain integrity check passed."
            : "Blockchain integrity check failed.";

        chainResult.appendChild(status);

        result.chain.forEach(function (block) {
            const card = document.createElement("article");
            card.className = "block-card";

            const title = document.createElement("h3");
            title.textContent = `Block #${block.index}`;

            const timestamp = document.createElement("p");
            timestamp.textContent = `Timestamp: ${block.timestamp}`;

            const data = document.createElement("p");
            data.textContent = `Data: ${JSON.stringify(block.data)}`;

            const previousHash = document.createElement("p");
            previousHash.textContent = `Previous hash: ${block.previous_hash}`;

            const hash = document.createElement("p");
            hash.textContent = `Hash: ${block.hash}`;

            card.append(title, timestamp, data, previousHash, hash);
            chainResult.appendChild(card);
        });
    } catch (error) {
        showMessage(chainResult, error.message, "error");
    }
});

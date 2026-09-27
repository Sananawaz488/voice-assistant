const micButton = document.getElementById("micButton");
const statusText = document.getElementById("statusText");
const userText = document.getElementById("userText");
const novaText = document.getElementById("novaText");

const messageInput = document.getElementById("messageInput");
const sendButton = document.getElementById("sendButton");


// ==============================
// VOICE RECOGNITION
// ==============================

const SpeechRecognition =
    window.SpeechRecognition ||
    window.webkitSpeechRecognition;

let recognition = null;
let isListening = false;


if (SpeechRecognition) {

    recognition = new SpeechRecognition();

    recognition.continuous = false;
    recognition.interimResults = false;

    // English works well for English + Roman Urdu
    recognition.lang = "en-US";


    recognition.onstart = function () {

        isListening = true;

        micButton.classList.add("recording");

        statusText.textContent =
            "Listening... Speak now 🎤";
    };


    recognition.onresult = async function (event) {

        const transcript =
            event.results[0][0].transcript.trim();

        console.log("You said:", transcript);

        userText.textContent = transcript;

        statusText.textContent =
            "NOVA is thinking...";

        await sendMessage(transcript);
    };


    recognition.onerror = function (event) {

        console.error(
            "Speech recognition error:",
            event.error
        );

        isListening = false;

        micButton.classList.remove("recording");


        if (event.error === "not-allowed") {

            statusText.textContent =
                "Microphone permission is blocked.";

        } else if (event.error === "no-speech") {

            statusText.textContent =
                "I didn't hear you. Try again.";

        } else {

            statusText.textContent =
                "Voice error. Please try again.";
        }
    };


    recognition.onend = function () {

        isListening = false;

        micButton.classList.remove("recording");

    };

} else {

    console.error(
        "Speech Recognition is not supported."
    );

    statusText.textContent =
        "Please use Google Chrome for voice.";
}


// ==============================
// SPEAK NOVA'S RESPONSE
// ==============================

function speak(text) {

    if (!("speechSynthesis" in window)) {

        console.log(
            "Speech synthesis is not supported."
        );

        return;
    }


    window.speechSynthesis.cancel();


    const speech =
        new SpeechSynthesisUtterance(text);


    speech.lang = detectLanguage(text);

    speech.rate = 0.95;

    speech.pitch = 1.05;

    speech.volume = 1;


    const voices =
        window.speechSynthesis.getVoices();


    const preferredVoice =
        voices.find(function (voice) {

            return /female|zira|samantha|google.*female/i
                .test(voice.name);

        });


    if (preferredVoice) {

        speech.voice = preferredVoice;
    }


    window.speechSynthesis.speak(speech);
}


// ==============================
// LANGUAGE DETECTION
// ==============================

function detectLanguage(text) {

    const urduCharacters =
        /[\u0600-\u06FF]/;

    if (urduCharacters.test(text)) {

        return "ur-PK";
    }

    return "en-US";
}


// ==============================
// SEND MESSAGE TO BACKEND
// ==============================

async function sendMessage(message) {

    message = message.trim();


    if (!message) {

        return;
    }


    userText.textContent = message;

    novaText.textContent =
        "Thinking...";

    statusText.textContent =
        "NOVA is thinking...";


    try {

        const response =
            await fetch("/api/chat", {

                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify({
                    message: message
                })
            });


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.error ||
                "Something went wrong."
            );
        }


        novaText.textContent =
            data.reply;


        statusText.textContent =
            "Ready to listen";


        // NOVA speaks automatically
        speak(data.reply);


    } catch (error) {

        console.error(error);


        novaText.textContent =
            "Sorry, something went wrong.";


        statusText.textContent =
            "Something went wrong.";
    }
}


// ==============================
// MICROPHONE BUTTON
// ==============================

micButton.addEventListener(
    "click",
    function () {

        if (!recognition) {

            statusText.textContent =
                "Please use Google Chrome for voice.";

            return;
        }


        if (isListening) {

            recognition.stop();

            return;
        }


        try {

            recognition.start();

        } catch (error) {

            console.error(error);

        }

    }
);


// ==============================
// TEXT INPUT
// ==============================

sendButton.addEventListener(
    "click",
    function () {

        const message =
            messageInput.value.trim();


        if (!message) {

            return;
        }


        messageInput.value = "";

        sendMessage(message);
    }
);


messageInput.addEventListener(
    "keydown",
    function (event) {

        if (event.key === "Enter") {

            sendButton.click();
        }
    }
);


// ==============================
// LOAD AVAILABLE VOICES
// ==============================

window.speechSynthesis.onvoiceschanged =
    function () {

        window.speechSynthesis.getVoices();
    };
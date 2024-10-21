// app.js

window.onload = function () {
    let audio1 = document.getElementById("audio1");
    let audio2 = document.getElementById("audio2");
    let finalAudio = document.getElementById("finalAudio");
    let slider = document.getElementById("slider");
    let recordingSection = document.getElementById("recording-section");
    let images = slider.getElementsByTagName('img');
    let currentIndex = 0;

    // Function to change slider images
    function changeSliderImage() {
        images[currentIndex].style.display = "none";
        currentIndex = (currentIndex + 1) % images.length;
        images[currentIndex].style.display = "block";
    }

    // Play audio 1, then audio 2, then display recording section
    audio1.play();
    audio1.onended = function () {
        changeSliderImage();
        audio2.play();
    };

    audio2.onended = function () {
        changeSliderImage();
        recordingSection.style.display = "block";
    };

    // Recording logic (simplified)
    let recordButton = document.getElementById("recordButton");
    let stopButton = document.getElementById("stopButton");
    let recordStatus = document.getElementById("recordStatus");

    recordButton.onclick = function () {
        recordStatus.innerText = "Recording...";
        recordButton.disabled = true;
        stopButton.disabled = false;
    };

    stopButton.onclick = function () {
        recordStatus.innerText = "Recording stopped. Sending audio...";
        stopButton.disabled = true;

        // Simulate sending audio to backend
        fetch("/upload", {
            method: "POST",
            body: "recorded-audio.wav",  // In real-world app, this should be actual audio data.
        }).then(() => {
            recordStatus.innerText = "Audio sent!";
            finalAudio.style.display = "block";
            finalAudio.play();
        });
    };
};
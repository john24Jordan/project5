// Wait for the DOM to be loaded before initialising the media devices
document.addEventListener("DOMContentLoaded", () => {
    const captureButton = document.getElementById("captureButton");
    const capturedImageInput = document.getElementById("file-input");
    const captureForm = document.getElementById("captureForm");

// Access the user's camera with rear camera preference
navigator.mediaDevices.enumerateDevices()
.then(devices => {
    const rearCamera = devices.find(device => device.kind === 'videoinput' && device.label.toLowerCase().includes('back'));
    if (rearCamera) {
        return navigator.mediaDevices.getUserMedia({ video: { deviceId: rearCamera.deviceId } });
    } else {
        // If no rear camera found, fall back to any available camera
        return navigator.mediaDevices.getUserMedia({ video: true });
    }
})
.then((stream) => {
    // Create a video element to display the camera feed
    const video = document.getElementById("camera-feed");
    video.srcObject = stream;

    // Function to capture the image
    const captureImage = () => {
        const canvas = document.createElement("canvas");
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        const context = canvas.getContext("2d");
        context.drawImage(video, 0, 0, canvas.width, canvas.height);

        
        const imageDataUrl = canvas.toDataURL("image/jpg");

        // Set the base64 data in the hidden input field
        capturedImageInput.value = imageDataUrl;

        // Submit the form to save the image on the server
        captureForm.submit();
            };
            // `captureButton` click event
        captureButton.addEventListener("click", captureImage);
})
.catch((error) => {
    // Display an error message if access to media devices is denied
    console.error("Error accessing the camera:", error);
});
});
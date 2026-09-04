/**
 * Prediction Page JavaScript Logic
 * 
 * Manages:
 * - Dynamic tab toggle switching (Ear, Nose, Throat) without page reload
 * - Reusable drag-and-drop file uploader component
 * - Client-side validation (file existence, extensions, size limits)
 * - Fetch API POST execution with FormData
 * - Loading spinner states
 * - Rendering prediction result cards, horizontal probability bars, and safety recommendations
 * - Error handling and state resets
 */

document.addEventListener('DOMContentLoaded', () => {
    // Current Active Model State (Default: 'ear')
    let currentModel = 'ear';
    let selectedFile = null;

    // Model Configurations
    const modelConfigs = {
        ear: {
            title: "Upload Ear Image",
            description: "Upload a high-resolution otoscopic image for ear disease analysis.",
            endpoint: "/api/predict/ear",
            placeholderHint: "Drag & drop your ear image here, or click to browse"
        },
        nose: {
            title: "Upload Nose Image",
            description: "Upload an appropriate endoscopic or external image for nose disease analysis.",
            endpoint: "/api/predict/nose",
            placeholderHint: "Drag & drop your nose image here, or click to browse"
        },
        third: {
            title: "Upload Throat Image",
            description: "Upload a clear throat or oral cavity image for throat disease analysis.",
            endpoint: "/api/predict/third",
            placeholderHint: "Drag & drop your throat image here, or click to browse"
        }
    };

    // UI Element References
    const tabEar = document.getElementById('tabEar');
    const tabNose = document.getElementById('tabNose');
    const tabThird = document.getElementById('tabThird');
    
    const uploaderTitle = document.getElementById('uploaderTitle');
    const uploaderDesc = document.getElementById('uploaderDesc');
    
    const dropzone = document.getElementById('dropzone');
    const fileInput = document.getElementById('fileInput');
    const dropzoneHint = document.getElementById('dropzoneHint');
    
    const previewContainer = document.getElementById('previewContainer');
    const previewImg = document.getElementById('previewImg');
    const fileNameDisplay = document.getElementById('fileNameDisplay');
    const fileSizeDisplay = document.getElementById('fileSizeDisplay');
    const btnRemoveFile = document.getElementById('btnRemoveFile');
    
    const btnPredict = document.getElementById('btnPredict');
    const loadingBox = document.getElementById('loadingBox');
    const errorAlert = document.getElementById('errorAlert');
    
    const resultCard = document.getElementById('resultCard');
    const resultPredictionName = document.getElementById('resultPredictionName');
    const resultConfidenceBadge = document.getElementById('resultConfidenceBadge');
    const probabilityBarsContainer = document.getElementById('probabilityBarsContainer');
    
    const recTitle = document.getElementById('recTitle');
    const recMessage = document.getElementById('recMessage');
    const recAdvice = document.getElementById('recAdvice');
    
    const btnAnalyzeAnother = document.getElementById('btnAnalyzeAnother');
    const btnResetTypes = document.getElementById('btnResetTypes');

    // =========================================================================
    // 1. MODEL TAB SWITCHING
    // =========================================================================
    function switchModelTab(modelKey) {
        if (!modelConfigs[modelKey]) return;
        currentModel = modelKey;

        // Update active tab styling
        [tabEar, tabNose, tabThird].forEach(btn => btn?.classList.remove('active'));
        if (modelKey === 'ear' && tabEar) tabEar.classList.add('active');
        if (modelKey === 'nose' && tabNose) tabNose.classList.add('active');
        if (modelKey === 'third' && tabThird) tabThird.classList.add('active');

        // Update uploader interface strings dynamically
        const config = modelConfigs[modelKey];
        if (uploaderTitle) uploaderTitle.textContent = config.title;
        if (uploaderDesc) uploaderDesc.textContent = config.description;
        if (dropzoneHint) dropzoneHint.textContent = config.placeholderHint;

        // Hide results and clear errors when switching models
        hideError();
        hideResultCard();
    }

    if (tabEar) tabEar.addEventListener('click', () => switchModelTab('ear'));
    if (tabNose) tabNose.addEventListener('click', () => switchModelTab('nose'));
    if (tabThird) tabThird.addEventListener('click', () => switchModelTab('third'));

    // =========================================================================
    // 2. DRAG AND DROP & FILE UPLOADER
    // =========================================================================
    if (dropzone && fileInput) {
        dropzone.addEventListener('click', () => fileInput.click());

        // Dragover events
        ['dragenter', 'dragover'].forEach(eventName => {
            dropzone.addEventListener(eventName, (e) => {
                e.preventDefault();
                e.stopPropagation();
                dropzone.classList.add('dragover');
            }, false);
        });

        ['dragleave', 'drop'].forEach(eventName => {
            dropzone.addEventListener(eventName, (e) => {
                e.preventDefault();
                e.stopPropagation();
                dropzone.classList.remove('dragover');
            }, false);
        });

        // Drop file event
        dropzone.addEventListener('drop', (e) => {
            const dt = e.dataTransfer;
            const files = dt.files;
            if (files && files.length > 0) {
                handleFileSelection(files[0]);
            }
        });

        // File picker change event
        fileInput.addEventListener('change', (e) => {
            if (e.target.files && e.target.files.length > 0) {
                handleFileSelection(e.target.files[0]);
            }
        });
    }

    // Handle and Validate File Selection
    function handleFileSelection(file) {
        hideError();
        hideResultCard();

        if (!file) {
            showError("Please select an image file first.");
            return;
        }

        // Validate File Extension (JPG, JPEG, PNG)
        const allowedExtensions = ['image/jpeg', 'image/jpg', 'image/png'];
        const fileNameLower = file.name.toLowerCase();
        const isValidExtension = fileNameLower.endsWith('.jpg') || 
                                 fileNameLower.endsWith('.jpeg') || 
                                 fileNameLower.endsWith('.png');

        if (!allowedExtensions.includes(file.type) && !isValidExtension) {
            showError("Only JPG, JPEG, and PNG images are supported.");
            resetFileSelection();
            return;
        }

        // Validate File Size (Max 10 MB)
        const maxSizeBytes = 10 * 1024 * 1024; // 10MB
        if (file.size > maxSizeBytes) {
            showError("File size is too large. Please select an image smaller than 10MB.");
            resetFileSelection();
            return;
        }

        selectedFile = file;

        // Render File Metadata
        if (fileNameDisplay) fileNameDisplay.textContent = file.name;
        if (fileSizeDisplay) fileSizeDisplay.textContent = formatBytes(file.size);

        // Render Image Preview using FileReader
        const reader = new FileReader();
        reader.onload = (e) => {
            if (previewImg) previewImg.src = e.target.result;
            if (previewContainer) previewContainer.style.display = 'block';
            if (btnPredict) btnPredict.disabled = false;
        };
        reader.readAsDataURL(file);
    }

    // Format Bytes into Human-Readable String
    function formatBytes(bytes, decimals = 2) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const dm = decimals < 0 ? 0 : decimals;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
    }

    // Reset File Selection
    function resetFileSelection() {
        selectedFile = null;
        if (fileInput) fileInput.value = '';
        if (previewContainer) previewContainer.style.display = 'none';
        if (previewImg) previewImg.src = '';
        if (btnPredict) btnPredict.disabled = true;
    }

    if (btnRemoveFile) {
        btnRemoveFile.addEventListener('click', (e) => {
            e.stopPropagation();
            resetFileSelection();
            hideError();
            hideResultCard();
        });
    }

    // =========================================================================
    // 3. PREDICTION API FETCH & PREDICT BUTTON
    // =========================================================================
    if (btnPredict) {
        btnPredict.addEventListener('click', async () => {
            hideError();

            if (!selectedFile) {
                showError("Please select an image first.");
                return;
            }

            // UI Loading State
            setLoadingState(true);

            // Build FormData Payload
            const formData = new FormData();
            formData.append('image', selectedFile);

            const endpoint = modelConfigs[currentModel].endpoint;

            try {
                const response = await fetch(endpoint, {
                    method: 'POST',
                    body: formData
                });

                const data = await response.json();

                if (!response.ok || !data.success) {
                    throw new Error(data.error || "An error occurred during prediction.");
                }

                // Render Results Card
                displayPredictionResult(data);

            } catch (err) {
                showError(err.message || "Failed to communicate with prediction server. Please try again.");
            } finally {
                setLoadingState(false);
            }
        });
    }

    // Set Loading State
    function setLoadingState(isLoading) {
        if (isLoading) {
            if (loadingBox) loadingBox.style.display = 'block';
            if (btnPredict) {
                btnPredict.disabled = true;
                btnPredict.textContent = 'Analyzing image...';
            }
        } else {
            if (loadingBox) loadingBox.style.display = 'none';
            if (btnPredict) {
                btnPredict.disabled = false;
                btnPredict.textContent = 'PREDICT';
            }
        }
    }

    // =========================================================================
    // 4. RESULT CARD & PROBABILITY BARS RENDERING
    // =========================================================================
    function displayPredictionResult(data) {
        if (!resultCard) return;

        // Render Top Prediction & Confidence Badge
        if (resultPredictionName) resultPredictionName.textContent = data.prediction;
        if (resultConfidenceBadge) resultConfidenceBadge.textContent = `${data.confidence_percentage}% Confidence`;

        // Render Probability Bars
        if (probabilityBarsContainer) {
            probabilityBarsContainer.innerHTML = '';
            
            const probs = data.probabilities || {};
            // Sort probabilities in descending order
            const sortedEntries = Object.entries(probs).sort((a, b) => b[1] - a[1]);

            sortedEntries.forEach(([className, probValue]) => {
                const percentage = (probValue * 100).toFixed(1);
                const isTop = className === data.prediction;

                const rowDiv = document.createElement('div');
                rowDiv.className = `prob-row ${isTop ? 'top-prediction' : ''}`;

                rowDiv.innerHTML = `
                    <div class="prob-meta">
                        <span>${className} ${isTop ? '★' : ''}</span>
                        <span>${percentage}%</span>
                    </div>
                    <div class="prob-bar-track">
                        <div class="prob-bar-fill" style="width: 0%;"></div>
                    </div>
                `;

                probabilityBarsContainer.appendChild(rowDiv);

                // Trigger width animation in next tick
                setTimeout(() => {
                    const fillBar = rowDiv.querySelector('.prob-bar-fill');
                    if (fillBar) fillBar.style.width = `${percentage}%`;
                }, 50);
            });
        }

        // Render Recommendation Box
        const rec = data.recommendation || {};
        if (recTitle) recTitle.textContent = rec.title || "General Recommendation";
        if (recMessage) recMessage.textContent = rec.message || "";
        if (recAdvice) recAdvice.textContent = rec.advice || "";

        // Display Card & Scroll Smoothly into View
        resultCard.style.display = 'block';
        resultCard.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    function hideResultCard() {
        if (resultCard) resultCard.style.display = 'none';
    }

    // Action Buttons
    if (btnAnalyzeAnother) {
        btnAnalyzeAnother.addEventListener('click', () => {
            resetFileSelection();
            hideResultCard();
            hideError();
            window.scrollTo({ top: dropzone.offsetTop - 100, behavior: 'smooth' });
        });
    }

    if (btnResetTypes) {
        btnResetTypes.addEventListener('click', () => {
            resetFileSelection();
            hideResultCard();
            hideError();
            switchModelTab('ear');
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }

    // =========================================================================
    // 5. ERROR DISPLAY HELPERS
    // =========================================================================
    function showError(msg) {
        if (errorAlert) {
            errorAlert.textContent = msg;
            errorAlert.style.display = 'block';
        }
    }

    function hideError() {
        if (errorAlert) {
            errorAlert.style.display = 'none';
            errorAlert.textContent = '';
        }
    }
});

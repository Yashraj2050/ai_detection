class DeepGuardApp {
    constructor() {
        this.initializeElements();
        this.setupEventListeners();
    }

    initializeElements() {
        this.uploadArea = document.getElementById('uploadArea');
        this.fileInput = document.getElementById('fileInput');
        this.analysisSection = document.getElementById('analysisSection');
        this.fileInfo = document.getElementById('fileInfo');
        this.artifactScore = document.getElementById('artifactScore');
        this.motionScore = document.getElementById('motionScore');
        this.fusionScore = document.getElementById('fusionScore');
        this.confidenceText = document.getElementById('confidenceText');
        this.resetBtn = document.getElementById('resetBtn');
        this.reportBtn = document.getElementById('reportBtn');
        this.elaViz = document.getElementById('elaViz');
        this.dctViz = document.getElementById('dctViz');
    }

    setupEventListeners() {
        // Upload area events
        this.uploadArea.addEventListener('click', () => this.fileInput.click());
        this.uploadArea.addEventListener('dragover', this.handleDragOver.bind(this));
        this.uploadArea.addEventListener('dragleave', this.handleDragLeave.bind(this));
        this.uploadArea.addEventListener('drop', this.handleDrop.bind(this));
        
        // File input change
        this.fileInput.addEventListener('change', this.handleFileSelect.bind(this));
        
        // Button events
        this.resetBtn.addEventListener('click', this.resetAnalysis.bind(this));
        this.reportBtn.addEventListener('click', this.generateReport.bind(this));
    }

    handleDragOver(e) {
        e.preventDefault();
        this.uploadArea.classList.add('dragover');
    }

    handleDragLeave(e) {
        e.preventDefault();
        this.uploadArea.classList.remove('dragover');
    }

    handleDrop(e) {
        e.preventDefault();
        this.uploadArea.classList.remove('dragover');
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            this.processFile(files[0]);
        }
    }

    handleFileSelect(e) {
        const file = e.target.files[0];
        if (file) {
            this.processFile(file);
        }
    }

    processFile(file) {
        // Validate file type
        const validTypes = ['image/jpeg', 'image/jpg', 'image/png', 'video/mp4', 'video/avi'];
        if (!validTypes.includes(file.type)) {
            alert('Please upload a valid image (JPG, PNG) or video (MP4, AVI) file.');
            return;
        }

        // Display file info
        this.displayFileInfo(file);
        
        // Show analysis section
        this.analysisSection.style.display = 'block';
        this.analysisSection.scrollIntoView({ behavior: 'smooth' });
        
        // Start analysis simulation
        this.startAnalysis(file);
    }

    displayFileInfo(file) {
        const fileSize = (file.size / (1024 * 1024)).toFixed(2);
        const fileHash = this.generateMockHash();
        
        this.fileInfo.innerHTML = `
            <strong>File:</strong> ${file.name}<br>
            <strong>Size:</strong> ${fileSize} MB<br>
            <strong>Type:</strong> ${file.type}<br>
            <strong>Hash:</strong> ${fileHash}
        `;
    }

    generateMockHash() {
        return Array.from({length: 64}, () => Math.floor(Math.random() * 16).toString(16)).join('');
    }

    async startAnalysis(file) {
        // Reset scores
        this.artifactScore.innerHTML = '<div class="loading"></div>';
        this.motionScore.innerHTML = '<div class="loading"></div>';
        this.fusionScore.innerHTML = '<div class="loading"></div>';
        this.confidenceText.textContent = 'Analyzing...';

        // Simulate artifact detection
        await this.simulateDelay(2000);
        const artifactResult = this.simulateArtifactDetection(file);
        this.artifactScore.textContent = artifactResult.score + '%';
        this.artifactScore.style.color = this.getScoreColor(artifactResult.score);

        // Simulate motion analysis (for videos)
        await this.simulateDelay(1500);
        const motionResult = this.simulateMotionAnalysis(file);
        this.motionScore.textContent = motionResult.score + '%';
        this.motionScore.style.color = this.getScoreColor(motionResult.score);

        // Simulate fusion analysis
        await this.simulateDelay(1000);
        const fusionResult = this.simulateFusionAnalysis(artifactResult.score, motionResult.score);
        this.fusionScore.textContent = fusionResult.confidence + '%';
        this.fusionScore.style.color = this.getScoreColor(fusionResult.confidence);
        this.confidenceText.textContent = fusionResult.verdict;

        // Generate visualizations
        this.generateVisualizations(file);
    }

    simulateArtifactDetection(file) {
        // Simulate realistic artifact detection scores
        const baseScore = Math.random() * 100;
        const isImage = file.type.startsWith('image/');
        
        // Images tend to have more detectable artifacts
        const score = Math.round(isImage ? baseScore * 0.8 + 20 : baseScore * 0.6 + 10);
        
        return { score: Math.min(score, 95) };
    }

    simulateMotionAnalysis(file) {
        const isVideo = file.type.startsWith('video/');
        
        if (!isVideo) {
            return { score: 0 };
        }
        
        // Simulate motion analysis for videos
        const score = Math.round(Math.random() * 80 + 10);
        return { score };
    }

    simulateFusionAnalysis(artifactScore, motionScore) {
        // Combine scores with weighted average
        const weight1 = 0.7; // Artifact detection weight
        const weight2 = 0.3; // Motion analysis weight
        
        const combinedScore = Math.round(artifactScore * weight1 + motionScore * weight2);
        
        let verdict;
        if (combinedScore < 30) {
            verdict = '✅ Likely Authentic';
        } else if (combinedScore < 70) {
            verdict = '⚠️ Suspicious Content';
        } else {
            verdict = '🚨 Likely Deepfake';
        }
        
        return { confidence: combinedScore, verdict };
    }

    getScoreColor(score) {
        if (score < 30) return '#28a745'; // Green
        if (score < 70) return '#ffc107'; // Yellow
        return '#dc3545'; // Red
    }

    generateVisualizations(file) {
        // Simulate ELA visualization
        this.elaViz.innerHTML = `
            <div style="background: linear-gradient(45deg, #ff6b6b, #4ecdc4); height: 100%; border-radius: 8px; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold;">
                ELA Map Generated<br>
                <small>Compression artifacts highlighted</small>
            </div>
        `;

        // Simulate DCT visualization
        this.dctViz.innerHTML = `
            <div style="background: linear-gradient(45deg, #667eea, #764ba2); height: 100%; border-radius: 8px; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold;">
                DCT Analysis Complete<br>
                <small>Frequency domain patterns analyzed</small>
            </div>
        `;
    }

    simulateDelay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    resetAnalysis() {
        this.analysisSection.style.display = 'none';
        this.fileInput.value = '';
        
        // Scroll back to upload area
        this.uploadArea.scrollIntoView({ behavior: 'smooth' });
    }

    generateReport() {
        // Simulate PDF report generation
        const reportData = {
            timestamp: new Date().toISOString(),
            filename: this.fileInput.files[0]?.name || 'unknown',
            artifactScore: this.artifactScore.textContent,
            motionScore: this.motionScore.textContent,
            fusionScore: this.fusionScore.textContent,
            verdict: this.confidenceText.textContent
        };

        // Create a simple text report (in a real app, this would generate a PDF)
        const reportContent = `
DEEPGUARD ANALYSIS REPORT
========================

Timestamp: ${reportData.timestamp}
File: ${reportData.filename}

ANALYSIS RESULTS:
- Artifact Detection: ${reportData.artifactScore}
- Motion Analysis: ${reportData.motionScore}
- AI Confidence: ${reportData.fusionScore}
- Verdict: ${reportData.verdict}

This report was generated by DeepGuard AI-Powered Deepfake Detection Tool.
        `.trim();

        // Download as text file
        const blob = new Blob([reportContent], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `deepguard-report-${Date.now()}.txt`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);

        alert('📄 Report downloaded successfully!');
    }
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new DeepGuardApp();
});
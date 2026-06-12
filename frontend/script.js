// Ngrok static tunnel URL — permanent for this ngrok account
// IMPORTANT: Backend must be running locally + ngrok must be active for this to work
const API_URL = "https://freely-hypnosis-amusement.ngrok-free.dev/predict";

// Theme Toggle
const themeToggle = document.getElementById('themeToggle');
const body = document.body;

const savedTheme = localStorage.getItem('carynth-theme') || (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
if (savedTheme === 'dark') {
    body.setAttribute('data-theme', 'dark');
    themeToggle.innerHTML = '<i class="fa-solid fa-sun"></i>';
}

themeToggle.addEventListener('click', () => {
    if (body.getAttribute('data-theme') === 'dark') {
        body.removeAttribute('data-theme');
        localStorage.setItem('carynth-theme', 'light');
        themeToggle.innerHTML = '<i class="fa-solid fa-moon"></i>';
    } else {
        body.setAttribute('data-theme', 'dark');
        localStorage.setItem('carynth-theme', 'dark');
        themeToggle.innerHTML = '<i class="fa-solid fa-sun"></i>';
    }
});

// Scroll Journey Logic
const getStartedBtn = document.getElementById('getStartedBtn');
const builderSection = document.getElementById('builderSection');
const resultsSection = document.getElementById('resultsSection');

// Smooth scroll to builder
getStartedBtn.addEventListener('click', () => {
    builderSection.scrollIntoView({ behavior: 'smooth' });
});

// Intersection Observer for scroll animations
const observerOptions = {
    root: null,
    rootMargin: '0px',
    threshold: 0.15
};

const observer = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('is-visible');
            // Un-observer after animating once to prevent re-triggering constantly
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);

document.querySelectorAll('.animate-on-scroll').forEach(el => {
    observer.observe(el);
});

// Form Submission & API logic
document.getElementById('analysisForm').addEventListener('submit', async function (e) {
    e.preventDefault();

    const loadingState = document.getElementById('loadingState');
    const resultsContent = document.getElementById('resultsContent');
    const analyzeBtn = document.getElementById('analyzeBtn');

    // Reveal and scroll to results section
    resultsSection.classList.remove('hidden-section');
    resultsSection.style.display = 'flex'; // override hidden logic elegantly
    
    // Slight timeout to ensure layout shifts before scrolling
    setTimeout(() => {
        resultsSection.style.opacity = '1';
        resultsSection.scrollIntoView({ behavior: 'smooth' });
    }, 50);

    // Show loading, hide previous results
    resultsContent.classList.add('hidden');
    loadingState.classList.remove('hidden');

    const originalBtnText = analyzeBtn.innerHTML;
    analyzeBtn.disabled = true;
    analyzeBtn.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i> Processing...`;

    const formData = {
        cgpa: parseFloat(document.getElementById('cgpa').value),
        interest: document.getElementById('interest').value,
        skills: document.getElementById('skills').value,
        courses_completed: parseInt(document.getElementById('courses').value),
        projects_count: parseInt(document.getElementById('projects').value)
    };

    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'ngrok-skip-browser-warning': 'true'
            },
            body: JSON.stringify(formData)
        });

        if (!response.ok) throw new Error('API Error');

        const data = await response.json();

        // Simulated artificial delay for presentation UX
        setTimeout(() => {
            loadingState.classList.add('hidden');
            displayResults(data);
        }, 1200);

    } catch (error) {
        console.error(error);
        loadingState.classList.add('hidden');
        alert("Connection failed. Ensure backend is running.");
        builderSection.scrollIntoView({ behavior: 'smooth' }); // Scroll back up on error
    } finally {
        analyzeBtn.disabled = false;
        analyzeBtn.innerHTML = originalBtnText;
    }
});

// Add dynamic change listener to form inputs to hint that results will update
// If user has already seen results, scrolling back up and changing an input could just re-submit smoothly.
const inputs = document.querySelectorAll('#analysisForm input, #analysisForm select');
inputs.forEach(input => {
    input.addEventListener('change', () => {
        // If results section is visible and not loading, we can add a visual hint
        if (resultsSection.style.opacity === '1') {
            const analyzeBtn = document.getElementById('analyzeBtn');
            analyzeBtn.style.animation = 'pulse 2s infinite';
            // Custom CSS animation just for hinting
            if(!document.getElementById('dynamicStyle')) {
                const style = document.createElement('style');
                style.id = 'dynamicStyle';
                style.innerHTML = `@keyframes pulse { 0% { box-shadow: 0 0 0 0 rgba(16,185,129,0.7); } 70% { box-shadow: 0 0 0 10px rgba(16,185,129,0); } 100% { box-shadow: 0 0 0 0 rgba(16,185,129,0); } }`;
                document.head.appendChild(style);
            }
        }
    });
});

// Remove pulse when clicking analyze
document.getElementById('analyzeBtn').addEventListener('click', function() {
    this.style.animation = 'none';
});

function displayResults(data) {
    const resultsContent = document.getElementById('resultsContent');
    resultsContent.classList.remove('hidden');
    
    // Force reflow for animations
    void resultsContent.offsetWidth;

    // Reset animations by cloning and replacing elements to retrigger CSS animations
    const cards = resultsContent.querySelectorAll('.result-fade-in');
    cards.forEach(card => {
        card.style.animation = 'none';
        void card.offsetWidth;
        card.style.animation = null;
    });

    document.getElementById('roleResult').textContent = data.predicted_role;
    document.getElementById('clusterResult').textContent = `Cluster: Group ${data.cluster_id}`;

    const score = Math.round(data.career_score);
    document.getElementById('scoreValue').textContent = score;

    const gauge = document.getElementById('scoreGauge');
    const circumference = 283; // Approx 2 * pi * 45
    const offset = circumference - (score / 100) * circumference;

    gauge.style.strokeDashoffset = circumference;
    setTimeout(() => {
        gauge.style.strokeDashoffset = offset;
        if (score > 80) gauge.style.stroke = 'var(--success)';
        else if (score > 50) gauge.style.stroke = 'var(--warning)';
        else gauge.style.stroke = 'var(--danger)';
    }, 150);

    const gapList = document.getElementById('gapList');
    gapList.innerHTML = '';

    if (data.skill_gap.length === 0) {
        gapList.innerHTML = `<span class="tag safe"><i class="fa-solid fa-check"></i> Profile Optimized</span>`;
    } else {
        data.skill_gap.forEach(gap => {
            const tag = document.createElement('span');
            tag.className = 'tag';
            tag.innerHTML = `<i class="fa-solid fa-bolt"></i> ${gap}`;
            gapList.appendChild(tag);
        });
    }

    const roadmapList = document.getElementById('roadmapList');
    roadmapList.innerHTML = '';

    data.learning_path.forEach((step, index) => {
        const item = document.createElement('div');
        item.className = 'timeline-item';
        // Staggered fade in applied dynamically
        item.style.animation = `fadeInUp 0.5s cubic-bezier(0.16, 1, 0.3, 1) ${index * 0.15 + 0.3}s both`;
        item.innerHTML = `
            <div class="timeline-dot"></div>
            <div class="timeline-content">${step}</div>
        `;
        roadmapList.appendChild(item);
    });
}

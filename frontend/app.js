document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("preference-form");
    const resultsList = document.getElementById("results-list");
    const summarySection = document.getElementById("summary-section");
    const summaryText = document.getElementById("summary-text");
    const loadingState = document.getElementById("loading-state");
    const errorState = document.getElementById("error-state");
    const errorText = document.getElementById("error-text");
    const btnText = document.querySelector(".btn-text");
    const spinner = document.querySelector(".spinner");
    const healthDot = document.getElementById("health-dot");
    const healthStatus = document.getElementById("health-status");

    // Check system health on load
    async function checkHealth() {
        try {
            const response = await fetch("/health");
            const data = await response.json();
            if (data.status === "healthy") {
                healthDot.className = "health-dot healthy";
                healthStatus.textContent = "System Healthy";
            } else {
                healthDot.className = "health-dot unhealthy";
                healthStatus.textContent = "System Degraded";
            }
        } catch (error) {
            healthDot.className = "health-dot unhealthy";
            healthStatus.textContent = "System Offline";
        }
    }

    checkHealth();
    // Poll every 30 seconds
    setInterval(checkHealth, 30000);

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        // UI Reset
        resultsList.innerHTML = "";
        summarySection.classList.add("hidden");
        errorState.classList.add("hidden");
        loadingState.classList.remove("hidden");
        btnText.classList.add("hidden");
        spinner.classList.remove("hidden");

        const formData = new FormData(form);
        const prefs = {
            location: formData.get("location") || null,
            cuisine: formData.get("cuisine") || null,
            budget: formData.get("budget") || null,
            min_rating: (formData.get("min_rating") && !isNaN(parseFloat(formData.get("min_rating")))) ? parseFloat(formData.get("min_rating")) : null,
            notes: formData.get("notes") || null
        };

        try {
            const response = await fetch("/api/recommend", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(prefs)
            });

            if (!response.ok) {
                throw new Error(`API Error: ${response.statusText}`);
            }

            const data = await response.json();
            renderResults(data);

        } catch (error) {
            errorText.textContent = error.message;
            errorState.classList.remove("hidden");
        } finally {
            loadingState.classList.add("hidden");
            btnText.classList.remove("hidden");
            spinner.classList.add("hidden");
        }
    });

    function renderResults(data) {
        if (!data.results || data.results.length === 0) {
            // Still show the summary blurb if it contains an error message from the AI
            if (data.summary_blurb && data.summary_blurb.includes("expert")) {
                summaryText.textContent = data.summary_blurb;
                summarySection.classList.remove("hidden");
                resultsList.innerHTML = "";
            } else {
                resultsList.innerHTML = `
                    <div class="empty-state">
                        <h2>No matches found</h2>
                        <p>Try broadening your preferences or searching a different area.</p>
                    </div>
                `;
            }
            return;
        }

        // Render Summary Blurb
        if (data.summary_blurb) {
            summaryText.textContent = data.summary_blurb;
            summarySection.classList.remove("hidden");
        }

        // Render Cards
        data.results.forEach((res, index) => {
            const card = document.createElement("div");
            card.className = "result-card";
            card.style.animationDelay = `${index * 0.1}s`;

            const ratingHtml = res.rating ? `<div class="rating-badge">${res.rating}</div>` : '';
            const costHtml = res.cost ? `<span class="tag cost">${res.cost.toUpperCase()}</span>` : '';
            const cuisinesHtml = res.cuisines ? `<span class="tag cuisine">${res.cuisines}</span>` : '';

            card.innerHTML = `
                <div class="result-header">
                    <div>
                        <div class="result-title">${res.name}</div>
                        <div class="result-tags">
                            ${cuisinesHtml}
                            ${costHtml}
                        </div>
                    </div>
                    ${ratingHtml}
                </div>
                <div class="explanation">
                    ${res.explanation}
                </div>
            `;
            resultsList.appendChild(card);
        });
    }
});

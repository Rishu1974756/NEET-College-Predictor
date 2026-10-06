const API_URL = "/api";

const predictionForm = document.getElementById("predictionForm");

const rankInput = document.getElementById("rank");
const quotaSelect = document.getElementById("quota");
const stateSelect = document.getElementById("state");
const courseSelect = document.getElementById("course");
const candidateCategorySelect = document.getElementById("candidateCategory");
const allottedCategorySelect = document.getElementById("allottedCategory");

const predictBtn = document.getElementById("predictBtn");
const btnText = document.getElementById("btnText");

const formError = document.getElementById("formError");

const loadingSection = document.getElementById("loading");
const resultsSection = document.getElementById("resultsSection");
const resultsDiv = document.getElementById("results");
const resultSubtitle = document.getElementById("resultSubtitle");

const mobileMenuBtn = document.getElementById("mobileMenuBtn");
const mobileMenu = document.getElementById("mobileMenu");

document.addEventListener("DOMContentLoaded", () => {
    loadDropdowns();
});

async function loadDropdowns() {
    try {
        const response = await fetch(`${API_URL}/options`);

        if (!response.ok) {
            throw new Error("Could not load options");
        }

        const data = await response.json();

        populateSelect(quotaSelect, data.quota, "All Quotas");
        populateSelect(stateSelect, data.state, "All States");
        populateSelect(courseSelect, data.course, "Select Course");

        populateSelect(
            candidateCategorySelect,
            data.candidateCategory,
            "Select Category"
        );

        populateSelect(
            allottedCategorySelect,
            data.allottedCategory,
            "All Categories"
        );

        clearError();

    } catch (error) {
        console.error("Options error:", error);

        showError(
            "Could not load college options. Please start the backend."
        );
    }
}

function populateSelect(select, values, placeholder) {
    select.innerHTML = "";

    const firstOption = document.createElement("option");

    firstOption.value = "";
    firstOption.textContent = placeholder;

    select.appendChild(firstOption);

    values.forEach(value => {
        const option = document.createElement("option");

        option.value = value;
        option.textContent = value;

        select.appendChild(option);
    });
}

mobileMenuBtn.addEventListener("click", () => {
    mobileMenu.classList.toggle("show");
});

document.querySelectorAll(".mobile-menu a").forEach(link => {
    link.addEventListener("click", () => {
        mobileMenu.classList.remove("show");
    });
});

predictionForm.addEventListener("submit", async event => {
    event.preventDefault();

    clearError();

    const userData = {
        rank: Number(rankInput.value),
        quota: quotaSelect.value || null,
        state: stateSelect.value || null,
        course: courseSelect.value || null,
        candidateCategory: candidateCategorySelect.value,
        allottedCategory: allottedCategorySelect.value || null,
        phase: 1
    };

    if (!validateForm(userData)) {
        return;
    }

    await getPredictions(userData);
});

function validateForm(data) {
    if (!data.rank || data.rank < 1) {
        showError("Please enter a valid NEET rank.");
        rankInput.focus();
        return false;
    }

    if (!Number.isInteger(data.rank)) {
        showError("NEET rank must be a whole number.");
        rankInput.focus();
        return false;
    }

    if (!data.course) {
        showError("Please select a course.");
        courseSelect.focus();
        return false;
    }

    if (!data.candidateCategory) {
        showError("Please select your candidate category.");
        candidateCategorySelect.focus();
        return false;
    }

    return true;
}

async function getPredictions(userData) {
    setLoading(true);

    try {
        const response = await fetch(`${API_URL}/predict`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(userData)
        });

        const data = await response.json();

        if (!response.ok || !data.success) {
            throw new Error(
                data.error || "Prediction failed"
            );
        }

        displayResults(data.results, userData);

    } catch (error) {
        console.error("Prediction error:", error);

        showError(
            error.message || "Prediction failed. Please try again."
        );

    } finally {
        setLoading(false);
    }
}

function displayResults(colleges, userData) {
    resultsDiv.innerHTML = "";

    resultSubtitle.textContent =
        `Rank ${formatNumber(userData.rank)} · ${userData.course} · 2026 Round 1`;

    if (!colleges.length) {
        showNoResults();
        return;
    }

    colleges.forEach((college, index) => {
        resultsDiv.appendChild(
            createCollegeCard(
                college,
                index,
                userData.rank
            )
        );
    });

    resultsSection.style.display = "block";

    resultsSection.scrollIntoView({
        behavior: "smooth",
        block: "start"
    });
}

function createCollegeCard(college, index, studentRank) {
    const card = document.createElement("article");

    card.className = "result-card";

    const rankBadge = document.createElement("div");

    rankBadge.className = "result-rank";
    rankBadge.textContent = `#${index + 1}`;

    const info = document.createElement("div");

    info.className = "result-info";

    const title = document.createElement("h3");

    title.textContent = college.institute;

    const meta = document.createElement("div");

    meta.className = "result-meta";

    meta.innerHTML = `
        <span>📍 ${escapeHTML(college.state)}</span>
        <span>📖 ${escapeHTML(college.course)}</span>
        <span>◉ ${escapeHTML(college.quota)}</span>
    `;

    info.appendChild(title);
    info.appendChild(meta);

    const right = document.createElement("div");

    right.className = "result-right";

    const closingRank = Number(
        college.predictedClosingRank
    );

    const chance = calculateChance(
        closingRank,
        studentRank
    );

    right.innerHTML = `
        <div class="chance-row">
            <span class="chance-label">Chance of Admission</span>
            <span class="chance-value">${chance}%</span>
        </div>

        <div class="progress">
            <div
                class="progress-bar"
                style="width: ${chance}%"
            ></div>
        </div>

        <div class="result-details">
            <div class="detail-box">
                <small>Predicted Closing Rank</small>
                <strong>${formatNumber(closingRank)}</strong>
            </div>

            <div class="detail-box">
                <small>Round</small>
                <strong>Round ${college.phase}</strong>
            </div>
        </div>
    `;

    card.appendChild(rankBadge);
    card.appendChild(info);
    card.appendChild(right);

    return card;
}

function calculateChance(closingRank, studentRank) {
    if (!closingRank || !studentRank) {
        return 0;
    }

    if (studentRank <= closingRank) {
        const difference = closingRank - studentRank;

        if (difference >= closingRank * 0.3) {
            return 95;
        }

        if (difference >= closingRank * 0.15) {
            return 85;
        }

        if (difference >= closingRank * 0.05) {
            return 70;
        }

        return 60;
    }

    return 20;
}

function showNoResults() {
    resultsDiv.innerHTML = `
        <div class="result-card">
            <div style="
                grid-column: 1 / -1;
                text-align: center;
                padding: 30px;
            ">
                <h3>No matching colleges found</h3>

                <p style="
                    color: #71839e;
                    margin-top: 8px;
                ">
                    Try changing your rank or preferences.
                </p>
            </div>
        </div>
    `;

    resultsSection.style.display = "block";

    resultsSection.scrollIntoView({
        behavior: "smooth",
        block: "start"
    });
}

function setLoading(isLoading) {
    if (isLoading) {
        loadingSection.style.display = "block";
        resultsSection.style.display = "none";

        predictBtn.disabled = true;
        btnText.textContent = "Predicting...";
    } else {
        loadingSection.style.display = "none";

        predictBtn.disabled = false;
        btnText.textContent = "Predict My Colleges";
    }
}

function showError(message) {
    formError.textContent = message;
    formError.classList.add("show");
}

function clearError() {
    formError.textContent = "";
    formError.classList.remove("show");
}

function formatNumber(value) {
    if (
        value === null ||
        value === undefined ||
        value === ""
    ) {
        return "N/A";
    }

    const number = Number(value);

    if (Number.isNaN(number)) {
        return String(value);
    }

    return Math.round(number).toLocaleString("en-IN");
}

function escapeHTML(value) {
    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}
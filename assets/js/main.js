// assets/js/main.js

// NAV ACTIVE LINK
document.querySelectorAll(".nav a").forEach(link => {
  if (link.href === window.location.href) link.style.color = "#3b82f6";
});

// CALCULATOR FUNCTION
function calculateRevenue(data) {
  const conversion = data.conversion / 100;
  const closeRate = data.closeRate / 100;
  const improvement = data.improvement / 100;

  const leads = data.visitors * conversion;
  const closed = leads * closeRate;
  const currentRevenue = closed * data.jobValue;

  const improvedConversion = conversion * (1 + improvement);
  const improvedLeads = data.visitors * improvedConversion;
  const improvedClosed = improvedLeads * closeRate;
  const optimizedRevenue = improvedClosed * data.jobValue;

  return {
    current: currentRevenue,
    optimized: optimizedRevenue,
    lift: optimizedRevenue - currentRevenue,
    annual: (optimizedRevenue - currentRevenue) * 12
  };
}

document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("calculatorForm");
  if (!form) return;

  const categorySelect = document.getElementById("category");
  const industrySelect = document.getElementById("industry");

  let industryData = [];

  // FETCH JSON DATA
  fetch('data/industry-stats.json')
    .then(res => res.json())
    .then(json => {
      const categories = json.categories;
      categories.forEach(cat => {
        const opt = document.createElement('option');
        opt.value = cat.name;
        opt.textContent = cat.name;
        categorySelect.appendChild(opt);
      });

      industryData = categories;
    });

  // UPDATE INDUSTRY DROPDOWN BASED ON CATEGORY
  categorySelect.addEventListener('change', () => {
    const selectedCategory = categorySelect.value;
    industrySelect.innerHTML = '<option value="">--Choose Industry--</option>';

    const cat = industryData.find(c => c.name === selectedCategory);
    if (!cat) return;

    cat.industries.forEach(ind => {
      const opt = document.createElement('option');
      opt.value = JSON.stringify(ind); // Store industry data in value
      opt.textContent = ind.name;
      industrySelect.appendChild(opt);
    });
  });

  // AUTO-FILL FIELDS WHEN INDUSTRY SELECTED
  industrySelect.addEventListener('change', () => {
    const selectedIndustry = industrySelect.value;
    if (!selectedIndustry) return;

    const ind = JSON.parse(selectedIndustry);
    document.getElementById("visitors").value = ind.averageMonthlyVisitors;
    document.getElementById("conversion").value = ind.averageConversionRate;
    document.getElementById("jobValue").value = ind.averageJobValue;
    document.getElementById("closeRate").value = ind.averageCloseRate;
  });

  // FORM SUBMIT
  form.addEventListener("submit", e => {
    e.preventDefault();

    const data = {
      visitors: parseFloat(document.getElementById("visitors").value),
      conversion: parseFloat(document.getElementById("conversion").value),
      jobValue: parseFloat(document.getElementById("jobValue").value),
      closeRate: parseFloat(document.getElementById("closeRate").value),
      improvement: parseFloat(document.getElementById("improvement").value)
    };

    if (Object.values(data).some(v => isNaN(v) || v <= 0)) {
      alert("Please enter valid numbers greater than zero.");
      return;
    }

    const result = calculateRevenue(data);

    document.getElementById("results").classList.remove("hidden");
    document.getElementById("currentRevenue").innerText =
      result.current.toLocaleString("en-US", { style: "currency", currency: "USD" });
    document.getElementById("optimizedRevenue").innerText =
      result.optimized.toLocaleString("en-US", { style: "currency", currency: "USD" });
    document.getElementById("monthlyLift").innerText =
      result.lift.toLocaleString("en-US", { style: "currency", currency: "USD" });
    document.getElementById("annualLift").innerText =
      result.annual.toLocaleString("en-US", { style: "currency", currency: "USD" });
  });
});

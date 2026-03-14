document.addEventListener('DOMContentLoaded', () => {
  const categorySelect = document.getElementById('category');
  const industrySelect = document.getElementById('industry');
  const visitorsInput = document.getElementById('visitors');
  const conversionInput = document.getElementById('conversion');
  const closeRateInput = document.getElementById('closeRate');
  const jobValueInput = document.getElementById('jobValue');
  const calculatorForm = document.getElementById('calculatorForm');
  const resultsDiv = document.getElementById('results');

  // Pre-filled industry data for the "Wow" factor auto-fill
  const industryData = {
    "Legal": {
      "Personal Injury": { conv: 2.5, close: 15, value: 7500 },
      "Family Law": { conv: 3.0, close: 20, value: 3500 },
      "Criminal Defense": { conv: 3.5, close: 25, value: 2500 }
    },
    "Home Services": {
      "HVAC": { conv: 4.0, close: 35, value: 6500 },
      "Plumbing": { conv: 5.0, close: 40, value: 850 },
      "Roofing": { conv: 2.0, close: 20, value: 12000 }
    },
    "Medical & Dental": {
      "General Dentistry": { conv: 3.5, close: 45, value: 1200 },
      "Cosmetic Surgery": { conv: 1.5, close: 15, value: 8000 },
      "Chiropractic": { conv: 3.0, close: 40, value: 1500 }
    },
    "Specialty Contractors": {
      "Damage Restoration": { conv: 6.0, close: 50, value: 4500 },
      "Custom Remodeling": { conv: 1.5, close: 10, value: 25000 }
    }
  };

  // 1. Populate the Category Dropdown
  for (const category in industryData) {
    let option = document.createElement('option');
    option.value = category;
    option.textContent = category;
    categorySelect.appendChild(option);
  }

  // 2. Handle Category Selection to unlock Industries
  categorySelect.addEventListener('change', function() {
    // Reset industry dropdown
    industrySelect.innerHTML = '<option value="">--Choose Industry--</option>';
    const selectedCategory = this.value;
    
    if (selectedCategory && industryData[selectedCategory]) {
      for (const industry in industryData[selectedCategory]) {
        let option = document.createElement('option');
        option.value = industry;
        option.textContent = industry;
        industrySelect.appendChild(option);
      }
    }
  });

  // 3. Handle Industry Selection (Auto-fills the form)
  industrySelect.addEventListener('change', function() {
    const cat = categorySelect.value;
    const ind = this.value;
    
    if (cat && ind && industryData[cat][ind]) {
      const data = industryData[cat][ind];
      conversionInput.value = data.conv;
      closeRateInput.value = data.close;
      jobValueInput.value = data.value;
      
      // Flash blue to show the user the fields auto-filled
      [conversionInput, closeRateInput, jobValueInput].forEach(el => {
        el.style.borderColor = 'var(--brand-blue)';
        setTimeout(() => el.style.borderColor = '', 800);
      });
    }
  });

  // Currency Formatter
  const formatMoney = (amount) => {
    return new Intl.NumberFormat('en-US', { 
      style: 'currency', 
      currency: 'USD', 
      maximumFractionDigits: 0 
    }).format(amount);
  };

  // 4. Handle the Math when the button is clicked
  calculatorForm.addEventListener('submit', function(e) {
    e.preventDefault(); // Stops the page from refreshing
    
    // Grab the numbers from the form
    const visitors = parseFloat(visitorsInput.value) || 0;
    const convRate = parseFloat(conversionInput.value) || 0;
    const closeRate = parseFloat(closeRateInput.value) || 0;
    const jobVal = parseFloat(jobValueInput.value) || 0;
    const improvement = parseFloat(document.getElementById('improvement').value) || 0;

    // Calculate Current Revenue
    const currentLeads = visitors * (convRate / 100);
    const currentJobs = currentLeads * (closeRate / 100);
    const currentRev = currentJobs * jobVal;

    // Calculate Optimized Revenue (e.g., a 20% boost to their current conversion rate)
    const newConvRate = convRate * (1 + (improvement / 100));
    const newLeads = visitors * (newConvRate / 100);
    const newJobs = newLeads * (closeRate / 100);
    const newRev = newJobs * jobVal;

    // Calculate The Lift (The ROI)
    const monthlyLift = newRev - currentRev;
    const annualLift = monthlyLift * 12;

    // Inject the math into the hidden results box
    document.getElementById('currentRevenue').textContent = formatMoney(currentRev);
    document.getElementById('optimizedRevenue').textContent = formatMoney(newRev);
    document.getElementById('monthlyLift').textContent = '+' + formatMoney(monthlyLift);
    document.getElementById('annualLift').textContent = '+' + formatMoney(annualLift);

    // Un-hide the results box with a smooth reveal
    resultsDiv.classList.remove('hidden');
    
    // Auto-scroll down slightly so they see the results immediately
    resultsDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  });
});

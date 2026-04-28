(() => {
const root = document.documentElement;
const stored = localStorage.getItem("sytfix-theme");
const preferred = window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
root.setAttribute("data-theme", stored || preferred);
const themeButton = document.querySelector("[data-theme-toggle]");
const setThemeIcon = () => {
if (!themeButton) return;
themeButton.querySelector("span").textContent = root.getAttribute("data-theme") === "dark" ? "☀" : "☾";
themeButton.setAttribute("aria-label", root.getAttribute("data-theme") === "dark" ? "Switch to light mode" : "Switch to dark mode");
};
setThemeIcon();
themeButton?.addEventListener("click", () => {
const next = root.getAttribute("data-theme") === "dark" ? "light" : "dark";
root.setAttribute("data-theme", next);
localStorage.setItem("sytfix-theme", next);
setThemeIcon();
});
const menuButton = document.querySelector("[data-menu-toggle]");
const nav = document.querySelector(".nav");
menuButton?.addEventListener("click", () => {
document.body.classList.toggle("nav-open");
const open = document.body.classList.contains("nav-open");
menuButton.setAttribute("aria-expanded", String(open));
nav?.setAttribute("aria-hidden", String(!open));
});
document.querySelectorAll(".nav a").forEach(link => link.addEventListener("click", () => {
document.body.classList.remove("nav-open");
menuButton?.setAttribute("aria-expanded", "false");
}));
const observer = new IntersectionObserver(entries => {
entries.forEach(entry => {
if (entry.isIntersecting) entry.target.classList.add("in-view");
});
},{threshold:.12});
document.querySelectorAll(".reveal").forEach(el => observer.observe(el));
const roiForm = document.querySelector("[data-roi-form]");
roiForm?.addEventListener("input", () => {
const visits = Number(roiForm.querySelector("[name='visits']").value || 0);
const conversion = Number(roiForm.querySelector("[name='conversion']").value || 0) / 100;
const value = Number(roiForm.querySelector("[name='value']").value || 0);
const uplift = Number(roiForm.querySelector("[name='uplift']").value || 0) / 100;
const current = visits * conversion * value;
const projected = visits * (conversion + uplift) * value;
const delta = Math.max(0, projected - current);
document.querySelector("[data-roi-current]").textContent = current.toLocaleString("en-US",{style:"currency",currency:"USD",maximumFractionDigits:0});
document.querySelector("[data-roi-projected]").textContent = projected.toLocaleString("en-US",{style:"currency",currency:"USD",maximumFractionDigits:0});
document.querySelector("[data-roi-delta]").textContent = delta.toLocaleString("en-US",{style:"currency",currency:"USD",maximumFractionDigits:0});
});
roiForm?.dispatchEvent(new Event("input"));
const auditForm = document.querySelector("[data-audit-form]");
auditForm?.addEventListener("input", () => {
const url = auditForm.querySelector("[name='url']").value.trim();
const industry = auditForm.querySelector("[name='industry']").value;
const speed = Number(auditForm.querySelector("[name='speed']").value || 0);
const local = Number(auditForm.querySelector("[name='local']").value || 0);
const content = Number(auditForm.querySelector("[name='content']").value || 0);
const ai = Number(auditForm.querySelector("[name='ai']").value || 0);
const score = Math.max(18, Math.min(98, Math.round(100 - speed - local - content - ai - (url ? 0 : 8))));
const label = score >= 84 ? "Strong foundation" : score >= 68 ? "Good, but leaking demand" : score >= 50 ? "Visible technical drag" : "High-friction site";
document.querySelector("[data-audit-score]").textContent = score;
document.querySelector("[data-audit-label]").textContent = label;
document.querySelector("[data-audit-industry]").textContent = industry || "service business";
});
auditForm?.dispatchEvent(new Event("input"));
const contactForm = document.querySelector("[data-contact-form]");
contactForm?.addEventListener("submit", event => {
event.preventDefault();
const data = new FormData(contactForm);
const name = data.get("name") || "";
const email = data.get("email") || "";
const phone = data.get("phone") || "";
const site = data.get("site") || "";
const message = data.get("message") || "";
const subject = encodeURIComponent("SytFix audit request");
const body = encodeURIComponent(`Name: ${name}\nEmail: ${email}\nPhone: ${phone}\nWebsite: ${site}\n\n${message}`);
window.location.href = `mailto:alex@sytfix.com?subject=${subject}&body=${body}`;
});
})();

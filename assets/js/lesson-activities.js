(function () {
  "use strict";
  const activity = document.getElementById("lesson-activities");
  if (!activity) return;
  const initialHash = window.location.hash;
  function jumpToSection(hash, addHistory) {
    const target = document.getElementById(hash.slice(1));
    if (!target) return;
    // Capture the previous entry's position before moving the viewport.
    if (addHistory) window.history.pushState(null, "", hash);
    else window.history.replaceState(null, "", hash);
    // The shared theme's TOC observer can interrupt a long smooth scroll
    // when intermediate textbook headings enter the viewport.
    target.scrollIntoView({ behavior: "instant", block: "start" });
    // Goldmark wraps the empty topic anchor in a paragraph; its heading
    // follows that paragraph rather than the anchor itself.
    const focusTarget = target.tagName === "A" ?
      (target.nextElementSibling || target.parentElement.nextElementSibling || target) :
      (target.querySelector("h1, h2, h3") || target);
    if (!focusTarget.hasAttribute("tabindex")) focusTarget.setAttribute("tabindex", "-1");
    focusTarget.focus({ preventScroll: true });
  }
  document.querySelectorAll('.lesson-resource-shortcuts a[href^="#"], #navbarIcons a[href^="#"], #lesson-read-topic').forEach(link => {
    link.addEventListener("click", event => {
      if (event.button !== 0 || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
      const hash = link.getAttribute("href");
      if (!document.getElementById(hash.slice(1))) return;
      event.preventDefault();
      jumpToSection(hash, true);
    });
  });
  if (["#lesson-activities", "#lesson-simulation"].includes(initialHash)) {
    // Restore the requested activity after source images and the theme's
    // own initialization have established the final page height.
    window.addEventListener("load", () => jumpToSection(initialHash, false), { once: true });
  }
  window.addEventListener("popstate", () => {
    if (["#lesson-activities", "#lesson-simulation"].includes(window.location.hash)) {
      jumpToSection(window.location.hash, false);
    }
  });
  const tamil = activity.dataset.language === "ta";
  if (tamil) {
    for (const [id, label] of [["web-tab", "இணையம்"], ["books-tab", "நூல்கள்"], ["referencepanelLabel", "மேற்கோள்கள்"], ["videopanelLabel", "காணொலிகள்"]]) {
      const element = document.getElementById(id);
      if (element) element.textContent = label;
    }
  }
  const select = document.getElementById("lesson-topic-select");
  const answer = document.getElementById("lesson-recall-answer");
  const compare = document.getElementById("lesson-read-topic");
  const mark = document.getElementById("lesson-mark-reviewed");
  const reset = document.getElementById("lesson-clear-reviews");
  const progress = document.getElementById("lesson-review-progress");
  const drafts = new Map(), reviewed = new Set();
  let current = select.value;
  function update() {
    compare.setAttribute("href", "#" + current);
    mark.disabled = reviewed.has(current);
    mark.textContent = reviewed.has(current) ? (tamil ? "முடிக்கப்பட்டது" : "Reviewed") : (tamil ? "பயிற்சி முடிந்தது எனக் குறிக்கவும்" : "Mark reviewed");
    reset.disabled = !reviewed.size && !drafts.size && !answer.value;
    progress.textContent = `${reviewed.size} / ${select.options.length} ` + (tamil ? "தலைப்புகள் முடிக்கப்பட்டன" : "topics reviewed");
  }
  select.addEventListener("change", function () {
    drafts.set(current, answer.value);
    current = select.value;
    answer.value = drafts.get(current) || "";
    update();
  });
  answer.addEventListener("input", () => { drafts.set(current, answer.value); update(); });
  mark.addEventListener("click", () => { reviewed.add(current); update(); });
  reset.addEventListener("click", () => { reviewed.clear(); drafts.clear(); answer.value = ""; update(); });
  update();

  activity.querySelectorAll("[data-simulation]").forEach(section => {
    const form = section.querySelector("form"), output = section.querySelector(".simulation-result");
    const kind = section.dataset.simulation;
    function calculate() {
      if (!form.checkValidity()) {
        output.textContent = tamil ? "சரியான எண் மதிப்புகளை உள்ளிடவும்." : "Enter valid numeric values.";
        return;
      }
      const value = name => form.elements.namedItem(name).value;
      const fmt = number => number.toLocaleString(tamil ? "ta-IN" : "en-IN", { maximumFractionDigits: 2 });
      try {
        if (kind === "climate") {
          const result = window.LessonCalculators.climate(value("temperature"), value("startAltitude"), value("targetAltitude"));
          output.textContent = (tamil ? "இலக்கு வெப்பநிலை: " : "Target temperature: ") + fmt(result) + " °C";
        } else if (kind === "gdp") {
          const result = window.LessonCalculators.gdp(value("consumption"), value("investment"), value("government"), value("exports"), value("imports"));
          const unit = tamil ? " கோடி" : " crore";
          output.textContent = "GDP = ₹" + fmt(result.total) + unit + "; " + (tamil ? "நிகர ஏற்றுமதி = ₹" : "Net exports = ₹") + fmt(result.netExports) + unit;
        } else {
          const result = window.LessonCalculators.gst(value("price"), value("rate"));
          output.textContent = (tamil ? "வரி = ₹" : "Tax = ₹") + fmt(result.tax) + "; " + (tamil ? "மொத்தம் = ₹" : "Total = ₹") + fmt(result.total);
        }
      } catch (_) {
        output.textContent = tamil ? "சரியான எண் மதிப்புகளை உள்ளிடவும்." : "Enter valid numeric values.";
      }
    }
    form.addEventListener("submit", event => { event.preventDefault(); calculate(); });
    form.addEventListener("input", calculate);
    form.addEventListener("change", calculate);
    calculate();
  });
})();

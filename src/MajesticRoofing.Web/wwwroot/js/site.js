(() => {
  const money = (n) =>
    n.toLocaleString(undefined, { style: "currency", currency: "USD", maximumFractionDigits: 0 });

  const calc = ({ homeSize, stories, material, shape, pitch, tearOff }) => {
    const e = Math.min(12000, Math.max(500, Number(homeSize) || 2000));
    const g = Number(stories) || 1;
    const t = g === 1 ? 1.06 : g === 2 ? 1.25 : 1.42;
    const r = { simple: 1.05, standard: 1.2, complex: 1.4 }[shape] || 1.2;
    const i = { low: 1.04, standard: 1.13, steep: 1.34 }[pitch] || 1.13;
    const a = {
      architectural: [515, 650],
      premium: [650, 840],
      metal: [860, 1210],
    }[material] || [515, 650];
    const squares = Math.max(8, (e / g / 100) * t * r * i);
    const storyFee = Math.max(0, g - 1) * 725;
    const tear = tearOff ? [75, 105] : [0, 0];
    return {
      squares,
      area: squares * 100,
      low: squares * (a[0] + tear[0]) + storyFee,
      high: squares * (a[1] + tear[1]) + storyFee * 1.45,
    };
  };

  const bindPlanner = (root) => {
    const homeSize = root.querySelector("[data-home-size]");
    const stories = root.querySelector("[data-stories]");
    const material = root.querySelector("[data-material]");
    const shape = root.querySelector("[data-shape]");
    const tearOff = root.querySelector("[data-tearoff]");
    const rangeEl = root.querySelector("[data-range]");
    const areaEl = root.querySelector("[data-area]");
    const pitchButtons = [...root.querySelectorAll("[data-pitch]")];
    let pitch = "standard";

    const sync = () => {
      const result = calc({
        homeSize: homeSize?.value,
        stories: stories?.value,
        material: material?.value,
        shape: shape?.value,
        pitch,
        tearOff: !!tearOff?.checked,
      });
      if (rangeEl) {
        rangeEl.innerHTML = `${money(result.low)} <i>—</i> ${money(result.high)}`;
      }
      if (areaEl) {
        const es = document.documentElement.lang === "es";
        const label = es ? "Área estimada del techo" : "Estimated roof area";
        const units = es
          ? `${Math.round(result.area).toLocaleString()} pie² · ${result.squares.toFixed(1)} cuadrados`
          : `${Math.round(result.area).toLocaleString()} sq ft · ${result.squares.toFixed(1)} squares`;
        areaEl.textContent = `${label}: ${units}`;
      }
      document.querySelectorAll("[data-planner-range]").forEach((input) => {
        input.value = `${Math.round(result.low)}-${Math.round(result.high)}`;
      });
    };

    pitchButtons.forEach((btn) => {
      btn.addEventListener("click", () => {
        pitch = btn.getAttribute("data-pitch") || "standard";
        pitchButtons.forEach((b) => {
          const on = b === btn;
          b.classList.toggle("active", on);
          b.setAttribute("aria-pressed", on ? "true" : "false");
        });
        sync();
      });
    });

    [homeSize, stories, material, shape, tearOff].forEach((el) => {
      if (!el) return;
      el.addEventListener("input", sync);
      el.addEventListener("change", sync);
    });

    sync();
  };

  document.querySelectorAll("[data-roof-planner]").forEach(bindPlanner);

  // Minimal sandbox banner styling if CSS lacks it
  const style = document.createElement("style");
  style.textContent = `
    .sandbox-banner{background:#1a1a1a;color:#f5f5f0;font-size:.85rem}
    .sandbox-banner a{color:#d4a84b;text-decoration:underline}
    .language-toggle{display:inline-flex;align-items:center;justify-content:center;min-width:2.5rem;height:2.5rem;border:1px solid rgba(255,255,255,.25);border-radius:999px;font-weight:700;letter-spacing:.04em}
    .site-header .language-toggle{border-color:rgba(0,0,0,.2)}
  `;
  document.head.appendChild(style);
})();

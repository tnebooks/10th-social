(function (root) {
  "use strict";
  function finite(value, nonnegative = false) {
    if (value === null || value === undefined || value === "" ||
        (typeof value === "string" && !value.trim())) throw new RangeError("Enter a number");
    const number = Number(value);
    if (!Number.isFinite(number) || (nonnegative && number < 0)) throw new RangeError("Invalid value");
    return number;
  }
  const calculators = {
    climate(temperature, startAltitude, targetAltitude) {
      const differenceKm = finite(targetAltitude) / 1000 - finite(startAltitude) / 1000;
      return finite(finite(temperature) - 6.5 * differenceKm);
    },
    gdp(consumption, investment, government, exports, imports) {
      const netExports = finite(exports, true) - finite(imports, true);
      return { total: finite(finite(consumption, true) + finite(investment, true) + finite(government, true) + netExports), netExports: finite(netExports) };
    },
    gst(price, rate) {
      const amount = finite(price, true), percent = finite(rate, true);
      if (![0, 5, 12, 18, 28].includes(percent)) throw new RangeError("Use a textbook rate");
      const tax = finite(amount * (percent / 100));
      return { tax, total: finite(amount + tax) };
    }
  };
  if (typeof module !== "undefined" && module.exports) module.exports = calculators;
  else root.LessonCalculators = calculators;
})(typeof window !== "undefined" ? window : this);

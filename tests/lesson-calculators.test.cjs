const { test } = require('node:test');
const assert = require('node:assert/strict');
const { climate, gdp, gst } = require('../assets/js/lesson-calculators.js');

test('lapse rate uses the altitude difference, including Chennai above sea level', () => {
  assert.equal(climate(35, 0, 1000), 28.5);
  assert.ok(Math.abs(climate(35, 6.7, 2240) - 20.48355) < 1e-10);
  assert.equal(climate(20, 1000, 0), 26.5);
});
test('expenditure GDP subtracts imports rather than adding them', () => {
  assert.deepEqual(gdp(100, 40, 30, 20, 10), { total: 180, netExports: 10 });
  assert.deepEqual(gdp(100, 40, 30, 20, 50), { total: 140, netExports: -30 });
});
test('textbook GST rates apply to pre-tax price with transparent totals', () => {
  assert.deepEqual(gst(1000, 18), { tax: 180, total: 1180 });
  assert.deepEqual(gst(1000, 5), { tax: 50, total: 1050 });
  assert.deepEqual(gst(1000, 0), { tax: 0, total: 1000 });
});
test('empty, nonfinite or negative monetary inputs do not become plausible zeroes', () => {
  for (const value of ['', null, undefined, NaN, Infinity, -1]) {
    assert.throws(() => gst(value, 18), RangeError);
    assert.throws(() => gdp(value, 1, 1, 1, 1), RangeError);
  }
  assert.throws(() => gst(1000, 17), RangeError);
  assert.throws(() => climate('', 0, 1000), RangeError);
});
test('arithmetic overflow cannot be displayed as a valid learning result', () => {
  assert.throws(() => gdp(1e308, 1e308, 30, 20, 10), RangeError);
  assert.throws(() => gst(1.7e308, 28), RangeError);
  assert.throws(() => climate(Number.MAX_VALUE, 1e308, -1e308), RangeError);
  assert.ok(Number.isFinite(gst(1e308, 18).total));
});

#!/usr/bin/env node
"use strict";

// Independent exact-integer audit of the rank-four radius-thirteen obstruction.
// No imports, solver, randomness, network access, or file writes are used.
// Run: node audit_radius_thirteen.js > endpoint_audit_report.json
// This corroborates a general argument; it does not solve the fixed-parent code.

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

function parity(x) {
  let p = 0;
  while (x) { p ^= x & 1; x >>>= 1; }
  return p;
}

function transform(values) {
  const a = values.slice();
  for (let width = 1; width < a.length; width *= 2) {
    for (let start = 0; start < a.length; start += 2 * width) {
      for (let j = start; j < start + width; j++) {
        const left = a[j], right = a[j + width];
        a[j] = left + right;
        a[j + width] = left - right;
      }
    }
  }
  return a;
}

function canonical(x) {
  return ((x & 1) * ((x >> 1) & 1)) ^
         (((x >> 2) & 1) * ((x >> 3) & 1));
}

const singleHistogram = {}, doubleHistogram = {};
let cases = 0, affineSupportCases = 0;
for (let linear = 0; linear < 64; linear++) {
  for (let constant = 0; constant < 2; constant++) {
    const signs = Array.from({length: 64}, (_, x) =>
      1 - 2 * (canonical(x) ^ parity(linear & x) ^ constant));
    const wh = transform(signs);
    const support = wh.map((v, i) => v ? i : -1).filter(i => i >= 0);
    assert(support.length === 16, "Wrong rank-four support size");
    assert(support.every(i => Math.abs(wh[i]) === 16), "Wrong amplitude");
    const epsilon = wh.map(v => v / 16);
    assert(transform(epsilon).every((v, x) => v === 4 * signs[x]),
      "Wrong inverse normalization");

    const defects = support.map(a => [[a, 8]]);
    for (let j = 0; j < 16; j++) {
      for (let k = j + 1; k < 16; k++) {
        defects.push([[support[j], 4], [support[k], 4]]);
      }
    }
    assert(defects.length === 136, "Wrong endpoint case count");
    for (const defect of defects) {
      const candidate = epsilon.map(e => 10 * e);
      for (const [a, amount] of defect) candidate[a] -= amount * epsilon[a];
      assert(candidate.reduce((sum, v, i) => sum + v * epsilon[i], 0) === 152,
        "Wrong endpoint functional");
      const numerators = transform(candidate);
      // The restricted inverse is numerator/64. A signed four-point mean
      // must be half-integral, so every numerator must be divisible by 32.
      const bad = numerators.filter(v => v % 32 !== 0).length;
      assert(bad > 0, "An endpoint spectrum passed fiber integrality");
      assert(defect.length !== 1 || bad === 24, "Single-defect count mismatch");
      assert(defect.length !== 2 || bad >= 32, "Double-defect count mismatch");
      const histogram = defect.length === 1 ? singleHistogram : doubleHistogram;
      histogram[bad] = (histogram[bad] || 0) + 1;
      cases++;
      if (!support.includes(0)) affineSupportCases++;
    }
  }
}
assert(cases === 17408 && affineSupportCases === 13056,
  "Affine coverage totals mismatch");

// Positive control: radius fifteen is possible for the single-spectrum
// constraint. The delta at x=48 removes one point from x4*x5's support.
const h = Array.from({length: 64}, (_, x) => canonical(x));
const u = h.map((v, x) => v ^ (((x >> 4) & 1) * ((x >> 5) & 1)) ^
  (x === 48 ? 1 : 0));
const wu = transform(u.map(v => 1 - 2 * v));
const wh = transform(h.map(v => 1 - 2 * v));
const alignedHistogram = {};
wh.forEach((v, a) => {
  if (v) {
    const aligned = wu[a] * v / 16;
    alignedHistogram[aligned] = (alignedHistogram[aligned] || 0) + 1;
  }
});
const control = {
  formula: "h=x0*x1+x2*x3; u=h+x4*x5+delta_48",
  bit_convention: "x0 is the least significant bit; delta_48 is one only at x=48",
  truth_table_hex: "0x" + u.reduce((w, v, x) => w | (BigInt(v) << BigInt(x)), 0n).toString(16),
  weight: u.reduce((sum, v) => sum + v, 0),
  distance_to_h: u.reduce((sum, v, x) => sum + (v !== h[x] ? 1 : 0), 0),
  maximum_absolute_walsh: Math.max(...wu.map(Math.abs)),
  restricted_aligned_histogram: alignedHistogram,
  scope: "Single-spectrum sharpness only. This is not a fixed-E extension witness."
};
assert(control.weight === 27 && control.distance_to_h === 15 &&
  control.maximum_absolute_walsh === 10, "Sharpness control failed");
assert(alignedHistogram[6] === 6 && alignedHistogram[10] === 10,
  "Sharpness restricted spectrum mismatch");

console.log(JSON.stringify({
  date: "2026-10-21",
  status: "PASS",
  method: "Independent exact-integer JavaScript Walsh transform",
  rank_four_affine_variants: 128,
  endpoint_profiles_per_variant: 136,
  endpoint_profiles_checked: cases,
  endpoint_profiles_with_genuinely_affine_support: affineSupportCases,
  endpoint_profiles_passing_fiber_integrality: 0,
  single_defect_invalid_position_histogram: singleHistogram,
  double_defect_invalid_position_histogram: doubleHistogram,
  positive_control_at_radius_fifteen: control,
  scope: "Audits the radius-thirteen endpoint and all affine perturbations of one canonical rank-four form. Does not rerun the 32768-form fixed-parent enumeration, search f-space, establish global code nonexistence, or claim novelty."
}, null, 2));

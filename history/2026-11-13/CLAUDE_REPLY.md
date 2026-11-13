# Visible final reply, 2026-11-13

Transcribed from the visible final answer. Markdown headings/list formatting are normalized; mathematical wording is preserved. This is not a transcript of hidden reasoning. See DIALOGUE.md for corrections and scope.

**Identity (valid for any A, any message set; no hA = 0 assumed).** Let w(u) = wt(uA) with N = 27 columns c, zero columns allowed. Take a subspace U′ ≤ W of dimension d, any message x, and the flat F = x + U′. Let M(U′) be the number of columns vanishing on U′. A column that is nonzero on U′ is 1 on exactly half of F. A column vanishing on U′ is constant on F, equal to x·c. Hence Σ_{u∈F} w(u) = 2^{d−1}(N − E(x)), with E(x) = Σ_{c vanishing on U′} (−1)^{x·c} = M − 2Z₁, where Z₁ counts the columns vanishing on U′ with x·c = 1. Taking x = 0 gives Σ_{s∈U′} w(s) = 2^{d−1}(N − M).

**Coset-sum test.** The signed count E(x) ≡ M(U′) (mod 2) for every x. Therefore, for every flat, Σ_{x+U′} w ≡ Σ_{U′} w (mod 2^d), and 2^{d−1}(N−M) ≤ Σ_{x+U′} w ≤ 2^{d−1}(N+M). The right-hand side of the congruence depends only on labels inside W, not on the unknown bits of x. Repeated and zero columns are covered.

**Necessary vs sufficient.** These are necessary conditions for the labeled function w to come from a 27-column matrix. They are consequences of the full labeled Fourier model, so they are not sufficient alone. They restate parts of that model as cheap, x-independent cuts.

**What it can strengthen.**

- d = 2 is redundant. It reads Σ_flat ≡ Σ_{U′} (mod 4). Since w ≡ −wt(uB) (mod 4) and wt(uB)/2 mod 2 is a quadratic form q_B, both sides equal the polar value B(s₁,s₂), so it follows from q_A = q_B.
- d ≥ 3 is not. It involves w mod 8, beyond the mod-4 information from B. For windows {12,16}, 12 ≡ 4 and 16 ≡ 0 (mod 8), so it constrains the parity of the number of weight-12 labels on each flat or subspace. The unlabeled split histograms and first two moments cannot see this.

**Tiny affine-column control (V = F₂³, N = 5):**

- Columns are 100, 010, 111, 001, 011, giving w(000..111) = 0, 2, 3, 3, 3, 3, 2, 4.
- U′ = ⟨100, 010⟩ has Σ = 8, so N − M = 4 and M = 1 (the column 001).
- Flat x = 001 has Σ = 3+3+2+4 = 12 = 2(4 + 2·1). Here Z₁ = 1, and 12 ≡ 8 (mod 4).
- Negative control: set w(011) = 4. The parities are unchanged, but Σ = 14 ≢ 0 (mod 4), so the labeling is rejected.

**Certificate target (≤ 60 s).** From the actual B rows, take the 160 weight-14 messages T, where the label is forced to be 14.

1. Enumerate all affine 3-flats inside T. Each has Σ = 112 ≡ 0 (mod 8).
2. For each direction subspace U′, test Σ_{U′} w ≡ 0 (mod 8), using the forced labels together with the window sets.
3. A contradiction certificate is a direction subspace whose nonzero labels are all forced and whose sum is ≢ 0 (mod 8).
4. Stop if only conditions redundant with the d = 2 case or with the quadratic structure appear.

No exclusion is claimed.

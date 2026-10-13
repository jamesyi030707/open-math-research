# Note: Answer(C), local judges, LPO, and a black-box query bound (draft)

Status key: **[P]** full paper proof given here · **[W]** needs library wiring / compilation (nothing below was compiled) · **[?]** only proposed.
No novelty is claimed. Source facts about the repository are as reported by the reviewer (QuestioningDelay.agda L284–309), not re-read by me.

## 0. Conventions
- h-level: `isOfHLevel 0` contractible, `1` prop, `2` set, `3` groupoid.
- `P_C(n) := isOfHLevel (n+2) C`, for `C : Type ℓ`; `P_C(n) : Type ℓ`.
- `Answer(C) := (Σ n:ℕ, P_C n) ⊎ (∀n, ¬ P_C n) : Type ℓ` (Σ **not** truncated).
- `Judge_C := ∀n, Dec (P_C n)`.
- `K_n := EM ℤ (n+1) = K(ℤ,n+1) : Type₀`.
- Search `question C judge` starts at stage 1; stage k asks `isOfHLevel (suc k) C = P_C(k−1)`. So stage k ↔ n = k−1, k ≥ 1, and
  `question ≡ never ⇔ ∀n ¬P_C n` (the skipped `isProp` stage is harmless: prop ⇒ set = P_C(0)). **[P]** (given the repo's soundness/completeness C-77, **[W]**)

## 1. Elementary lemmas
- **F1** `P_C(n)` is a proposition. **[W]** (isPropIsOfHLevel)
- **F2** `P_C(n) → P_C(n+1)`. **[W]**
- **F3** `(Σ m, isOfHLevel m C) ↔ (Σ n, P_C n)` and `(∀m ¬isOfHLevel m C) ↔ (∀n ¬P_C n)`; hence `Answer(C) ↔ Dec(Σ m, isOfHLevel m C)`. **[P]**
- **Lemma M (least witness)** If `P : ℕ → Type` has each `P n` a proposition and each `Dec (P n)`, then `∥Σ n, P n∥ → Σ n, P n`. **[P]**
  Proof: `Q n := P n × ∀j<n, ¬P j`. `Σ n, Q n` is a proposition (two least witnesses coincide; each component is a prop). Bounded search over `j ≤ n` (decidable) turns `Σ P` into `Σ Q`. Apply truncation recursion into the prop `Σ Q`, then forget.
- **Lemma B (prefix-or)** `β n := α 0 ∨ … ∨ α n` (Bool, `β(n+1) = β n ∨ α(n+1)`). Then `β m ≡ true → Σ i≤m, α i ≡ true`; `β` is monotone; `α m ≡ true → β m ≡ true`. **[P]** (induction on m)

## 2. Three goals (all level-polymorphic)
- (a) `Q_C : (∀n, Dec (P_C n)) → Delay (Σ n, P_C n)`; sound, partial-complete, `Q ≡ never ⇔ ∀n ¬P_C n`. Semi-decision only.
- (b) `R_C : Dec (Σ n, P_C n) → Answer(C)` (no `later`). **[P]** from F3 (the repo's `whetherSettled` returns `Bool`; to match `Answer` it must return the certificate).
- (c₁) `Φ_ℓ : (C : Type ℓ) → Judge_C → Answer(C)`; (c₂) `Ψ_ℓ : (C : Type ℓ) → Answer(C)`.

Levels: `Φ_ℓ : Type (ℓ-suc ℓ)`. The universe `Type ℓ-zero : Type₁`, so it is an input of `Φ_1`, not `Φ_0`. `judgeU` lives at level 1. `Φ_ℓ ⇒ Φ_0` via `Lift` (h-level invariant under `Lift`, **[W]**).

## 3. LPO / LEM statements (certificate form)
- `LPO_Σ := ∀α:ℕ→Bool, (Σ n, α n ≡ true) ⊎ (∀n, α n ≡ false)`.
- `LPO_∥` with `∥Σ∥`. `LPO_∥ ⇔ LPO_Σ` by Lemma M (α decidable). **[P]**
- `LEM_ℓ := (X : Type ℓ) → isProp X → X ⊎ ¬X` (a function, not just a statement).

**Thm C1** `LPO_Σ ⇒ Φ_ℓ` for every ℓ. **[P]** Given judge `j`, let `α n := true` iff `j n = yes _`. `LPO_Σ` gives `n` with `j n = yes p` (so `P n`) or `∀n, j n = no _` (so `∀n ¬P n`). No monotonicity needed.

**Thm L (LEM ⇒ c₂, no choice principle)** `LEM_ℓ ⇒ Ψ_ℓ`. **[P]** `n ↦ LEM(P_C n)` is a judge (F1), uniformly in `n`, because LEM is itself a function. Apply LEM to `∥Σ n, P_C n∥ : Type ℓ`: yes ⇒ Lemma M gives `Σ`; no ⇒ `∀n ¬P_C n`. (Check in Agda: universe levels of `∥Σ∥`; prop-ness of `Σ Q`.)

## 4. Encoding lemma E (needed for the converse)
For `α : ℕ→Bool` define `Y n := (if β n then ⊤ else K_n) : Type₀` and `C_α := (n:ℕ) → Y n : Type₀`.

**Facts about K_n** (standard; the repo's C-81/C-82 state the same shape, **[W]**): `isOfHLevel (n+3) K_n`, `¬isOfHLevel (n+2) K_n`.
Boundary check: n=0, `K_0 = S¹`: groupoid (h-level 3), not a set. n=1: `K(ℤ,2)`: h-level 4, not 3. n=2: `K(ℤ,3)`: h-level 5, not 4.

**Lemma E** `P_{C_α}(m) ↔ (β m ≡ true)`. **[P] modulo the K_n facts and library lemmas isOfHLevelΠ, isOfHLevelRetract.**
- (⇐) β m = true. For each n: if β n = true then `Y n = ⊤` (any h-level). If β n = false then n < m (β monotone and β m = true), so `isOfHLevel (n+3) K_n` and `n+3 ≤ m+2`; by upward closure `isOfHLevel (m+2) (Y n)`. `isOfHLevelΠ` gives `isOfHLevel (m+2) C_α`. **No equivalence "tail ↦ ⊤" is needed.**
- (⇒) Suppose β m = false; then `Y m = K_m`. `K_m` is a **retract** of `C_α`: section `s x := (n ↦ x if n = m [after transporting along β m = false]; basepoint of Y n otherwise)`, retraction = projection at `m`. Basepoints: `embase` for `K_n`, `tt` for `⊤`; the case split on `n = m` uses `discreteℕ`. If `isOfHLevel (m+2) C_α` then `isOfHLevel (m+2) K_m` (retract), contradicting the K-fact. So `P(m) → β m = true` (Bool case analysis).
- Sanity (not used in the proof): first true at 0: `C_α ≃ ⊤`; at 1: `C_α ≃ S¹`; at 2: `C_α ≃ S¹ × K(ℤ,2)`.

**Thm C2′ (conditional on E)** `Φ_0 ⇒ LPO_Σ`, hence `Φ_ℓ ⇔ LPO_Σ` for all ℓ. **[P] given E.**
Given α, `judge n :=` decide `β n` and use E. Apply `Φ_0 C_α judge`. `inl (m,p)`: E gives β m = true; Lemma B gives `Σ i≤m, α i = true`. `inr h`: E gives `β m ≠ true`, so `β m = false`, so `α m = false` for all m.

## 5. What the equivalence does and does not mean
- Not computable: a computational reading of a `Φ` would decide Σ⁰₁ sequences (halting). External reading, **not** a theorem of the type theory. **[?]** (needs a stated realizability/extraction semantics)
- Fails in some model: needs a model where LPO fails. **[?]** not carried out.
- Logically independent: needs **both** a model with `Φ` (classical: Thm L) and a model without. **[?]** Only the first half is sketched; both would also need models of cubical type theory with the HITs used.

## 6. Black-box bound BB′ (single trajectory)
Model: deterministic oracle algorithm `A`; run on `α` halts after finitely many point queries (repeats and adaptivity allowed); **locality**: if `β` agrees with `α` on all positions queried in the halting run on `α`, the run on `β` is identical (same trace, same output). Outputs: `inl n` (claim α n = true) or `inr` (claim all false).

**Thm BB′** No such `A` is correct (Good) on both `α⁰ ≡ false` and a suitable monotone tail sequence. **[P]**
Proof: run `A` on `α⁰`; let S be the queried set (possibly empty). If the output is `inl n`, it is wrong on `α⁰` (no n with α⁰ n true; `n ∉ S` is irrelevant). Otherwise the output is `inr`. Let N := max S (N := −1 if S is empty) and `α¹ i := (i > N)`. `α¹` agrees with `α⁰` on S, so by locality the run on `α¹` has the same trace and output `inr`, but `α¹(N+1) = true`. ∎
- Uses halting only on `α⁰` and (by locality) on `α¹`; **no uniform time bound or well-founded tree** is assumed.
- Covers: Turing/RAM machines with oracle-query instructions, decision trees, Delay-coalgebra oracle programs, anything with locality.
- Does **not** cover: randomized algorithms (a separate probabilistic argument is needed), white-box access to the judge's code or proof (this is exactly goal (b)), extra oracles (e.g. a jump), non-halting runs (goal (a) is allowed to diverge on `α⁰`), quantum or infinite-time models.
- Finite check: `bb_adversary_demo.py` (44105 depth-2 trees; 20000 random adaptive algorithms; a deliberate white-box cheat is flagged as violating locality). A finite check is not a proof for all algorithms.
- BB′ is a statement about oracle algorithms. It is **not** a theorem about closed terms of cubical type theory, and not about the existence of the HoTT universe's level.

## 7. Status table
| item | status |
|---|---|
| F3, Lemma M, Lemma B, Thm C1, Thm L, BB′ | [P] |
| Lemma E (E⇐, E⇒), Thm C2′ | [P] modulo K_n facts, isOfHLevelΠ, isOfHLevelRetract, Lift, discreteℕ, universe levels; [W] |
| index/offset statement (§0) | [P] given C-77 as reported; [W] |
| formal Agda for any of the above | not written, nothing compiled |
| independence of Φ from the theory | [?] |
| computable-impossibility reading | [?] |
| randomized version of BB′ | [?] |

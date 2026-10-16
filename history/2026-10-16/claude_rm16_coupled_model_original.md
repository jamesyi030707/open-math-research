# Coupled Walsh model for ONE odd function f (handoff, not solved)
Identify coordinates with GF(64) by the map in rm16_membership.py. E = RM(1,6) + {q_gamma(y)=Tr8(gamma*y^36)}, gamma in span(1,theta,theta^2).
Goal: d(r,E)>=27 with r odd.  Let s_y=(-1)^{f(y)}, y in GF(64).
**Model M (exact):** s_y in {+1,-1}; #{y: s_y=-1} odd; for each of the 8 translates q (incl. 0) and each u in GF(64):
  | sum_y s_y (-1)^{q(y)+Tr(uy)} | <= 10        (512 integer inequalities; Walsh values are then in {+-2,+-6,+-10}).
Reason: wt(f+q+affine) = (64 -+ W_{f+q}(u))/2 >= 27 <=> |W_{f+q}(u)|<=10.
**Coupling:** each nonzero q is bent, W_q(v)=8(-1)^{q~(v)}; convolution gives W_{f+q}(u) = (1/8) sum_v W_f(v)(-1)^{q~(v+u)}. So the 8 spectra are determined by ONE W_f and are pointwise linked; per-block count models (n_{+-2},n_{+-6},n_{+-10} separately) discard this link, and also the requirement that W_f inverse-transforms to +-1 values.
**Moments:** Parseval (sum W^2=4096) holds for every translate. Fourth moment sum_u W^4 = 64 sum_d C_f(d)^2 (C_f autocorrelation, C_f(0)=64) is NOT fixed: it lies in [262144, 409600] under |W|<=10 and depends on f's autocorrelation.
Distribution feasibility (25 integer points) is necessary only; no coset/function is implied.

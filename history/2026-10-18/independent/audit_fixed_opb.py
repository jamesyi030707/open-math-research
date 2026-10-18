#!/usr/bin/env python3
"""Independently parse and audit the fixed E OPB encoding, without solving it.

This file deliberately neither imports the generator nor reads its manifest.
Its codeword construction uses GF(2) polynomial coefficient convolution,
rather than shifted integers or the generator's codeword helper.
"""

import argparse
import hashlib
import itertools
import json
import re
from collections import Counter
from pathlib import Path


class AuditError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise AuditError(message)


def independent_code():
    # The exponents are a separately transcribed specification.  Their integer
    # conversion is checked against the prescribed hexadecimal polynomial.
    exponents = [0, 2, 3, 5, 6, 12, 14, 16, 18, 19, 20, 22, 24, 26,
                 27, 29, 33, 34, 37, 40, 43, 44, 46, 48, 49, 50, 53]
    require(sum(2 ** j for j in exponents) == int("2759262d5d506d", 16),
            "Audit polynomial transcription mismatch")
    words = []
    for message in range(1024):
        coefficients = [0] * 64
        for j in range(10):
            if (message // (2 ** j)) % 2:
                for exponent in exponents:
                    coefficients[exponent + j] = (coefficients[exponent + j] + 1) % 2
        coefficients[63] = sum(coefficients[:63]) % 2
        words.append(tuple(coefficients))
    return words


def parse_opb(text, allow_equality=False):
    """Strict parser for the canonical OPB subset emitted by this deliverable.

    Allows whitespace and ordinary full-line comments; rejects objectives,
    duplicate variable terms, complements, missing terminators, and unconsumed
    text. In external mode, equality rows are expanded to two inequalities.
    It is intentionally not a general OPB parser.
    """
    lines = text.splitlines()
    require(bool(lines), "Empty OPB input")
    header = re.fullmatch(r"\*\s+#variable=\s*(\d+)\s+#constraint=\s*(\d+)\s*", lines[0])
    require(header is not None, "Missing or malformed OPB header")
    nvars, declared_rows = map(int, header.groups())
    rows = []
    source_rows = 0
    equality_rows = 0
    term_re = re.compile(r"([+-]?\d+)\s+x([1-9]\d*)")
    for number, line in enumerate(lines[1:], start=2):
        if not line.strip() or line.lstrip().startswith("*"):
            continue
        match = re.fullmatch(r"\s*(.*?)\s*(>=|=)\s*([+-]?\d+)\s*;\s*", line)
        require(match is not None, f"Malformed constraint on line {number}")
        lhs, relation, rhs = match.groups()
        require(relation != "=" or allow_equality, f"Equality requires external mode, line {number}")
        terms = {}
        position = 0
        for term in term_re.finditer(lhs):
            require(not lhs[position:term.start()].strip(), f"Unparsed term on line {number}")
            coefficient, variable = map(int, term.groups())
            require(coefficient != 0, f"Zero coefficient on line {number}")
            require(1 <= variable <= nvars, f"Out-of-range variable on line {number}")
            require(variable not in terms, f"Repeated variable on line {number}")
            terms[variable] = coefficient
            position = term.end()
        require(terms and not lhs[position:].strip(), f"Unparsed left side on line {number}")
        rows.append((terms, int(rhs)))
        source_rows += 1
        if relation == "=":
            equality_rows += 1
            rows.append(({variable: -coefficient for variable, coefficient in terms.items()}, -int(rhs)))
    require(source_rows == declared_rows, "Declared and parsed row counts disagree")
    return nvars, rows, source_rows, equality_rows


def audit_text(text, external=False, compact=False):
    nvars, rows, source_rows, equality_rows = parse_opb(text, allow_equality=external)
    expected_nvars = 57 if compact else 59
    parity_offset = 27 if compact else 1
    require(nvars == expected_nvars, f"Expected exactly {expected_nvars} Boolean variables")
    require(len(rows) == 1026, "Expected exactly 1026 inequalities")
    words = independent_code()
    require(len(set(words)) == 1024, "Expected 1024 distinct codewords")
    projections = {w[:10] for w in words}
    require(len(projections) == 1024, "Coordinates 0..9 fail information-set test")
    weights = Counter(sum(word) for word in words)
    require(weights == {0: 1, 28: 448, 32: 126, 36: 448, 64: 1},
            "Unexpected code weight enumerator")
    require(all(sum(word) % 2 == 0 for word in words), "Code is not even")
    expected_parity = {i: 1 for i in range(1, 55)}
    expected_parity.update({i: -(2 ** (i - 54)) for i in range(55, nvars + 1)})
    if external:
        canonical = [({i - 9: 1 if word[i] == 0 else -1 for i in range(10, 64)},
                      27 - sum(word)) for word in words]
        canonical += [(expected_parity, parity_offset),
                      ({i: -c for i, c in expected_parity.items()}, -parity_offset)]
        signature = lambda row: (tuple(sorted(row[0].items())), row[1])
        require(Counter(map(signature, rows)) == Counter(map(signature, canonical)),
                "External constraints do not equal the expected multiset after equality expansion")
        # Use the independently reconstructed order for semantic controls.
        rows = canonical
    for message, word in enumerate(words):
        terms, rhs = rows[message]
        require(set(terms) == set(range(1, 55)), f"Distance row {message}: wrong variables")
        require(rhs == 27 - sum(word), f"Distance row {message}: wrong threshold")
        # Coordinate i maps to variable i-9, i = 10,...,63.
        for i in range(10, 64):
            require(terms[i - 9] == (1 if word[i] == 0 else -1),
                    f"Distance row {message}: wrong coefficient at coordinate {i}")
    require(rows[1024] == (expected_parity, parity_offset), "Wrong forward parity inequality")
    require(rows[1025] == ({i: -c for i, c in expected_parity.items()}, -parity_offset),
            "Wrong reverse parity inequality")
    return words, rows, {
        "variables": nvars,
        "inequalities": len(rows),
        "source_constraint_rows": source_rows,
        "source_equality_rows": equality_rows,
        "parity_offset": parity_offset,
        "codewords": len(words),
        "information_set_projections": len(projections),
        "weight_enumerator": dict(sorted(weights.items())),
        "exact_distance_rows_checked": 1024,
        "exact_distance_coefficients_checked": 1024 * 54,
        "exact_parity_coefficients_checked": 2 * nvars,
    }


def value(terms, assignment):
    return sum(coefficient * assignment[variable - 1] for variable, coefficient in terms.items())


def semantic_controls(words, rows):
    # Both sides of the distance identity are affine on the free bits, so
    # agreement at the origin and all 54 unit vectors identifies the entire
    # affine function.  Two additional vectors guard dense evaluation paths.
    vectors = [(0,) * 54]
    vectors += [tuple(int(i == j) for i in range(54)) for j in range(54)]
    vectors += [(1,) * 54, tuple(i % 2 for i in range(54))]
    checks = 0
    for word, (terms, rhs) in zip(words, rows[:1024]):
        for free in vectors:
            f = (0,) * 10 + free
            distance = sum(a != b for a, b in zip(f, word))
            lhs = value(terms, free)
            require(lhs - rhs == distance - 27, "Distance identity failed")
            require((lhs >= rhs) == (distance >= 27), "Distance truth value failed")
            checks += 1
    parity_checks = 0
    parity_witnesses = {}
    auxiliary_bits = len(rows[-2][0]) - 54
    parity_offset = rows[-2][1]
    require(parity_offset in (1, 27), "Unexpected parity offset")
    zero_index = words.index((0,) * 64)
    all_ones_index = words.index((1,) * 64)
    effective_witnesses = {}
    for weight in range(55):
        free = (1,) * weight + (0,) * (54 - weight)
        accepted = []
        effective = []
        for t in range(2 ** auxiliary_bits):
            bits = tuple((t // (2 ** j)) % 2 for j in range(auxiliary_bits))
            assignment = free + bits
            actual = all(value(terms, assignment) >= rhs for terms, rhs in rows[-2:])
            require(actual == (weight == 2 * t + parity_offset), "Parity equivalence failed")
            if actual:
                accepted.append(t)
            bounded = actual and all(value(rows[i][0], assignment) >= rows[i][1]
                                     for i in (zero_index, all_ones_index))
            expected_bounded = 27 <= weight <= 37 and weight == 2 * t + parity_offset
            require(bounded == expected_bounded, "Parity plus extreme-row bounds failed")
            if bounded:
                effective.append(t)
            parity_checks += 1
        difference = weight - parity_offset
        expected = [difference // 2] if difference % 2 == 0 and 0 <= difference // 2 < 2 ** auxiliary_bits else []
        require(accepted == expected, "Wrong parity-witness count")
        require(len(effective) == int(weight % 2 == 1 and 27 <= weight <= 37),
                "Bounded parity has incorrect witness count")
        parity_witnesses[weight] = accepted
        effective_witnesses[weight] = effective
    # Information-set bijection gives a unique gauge translation.  Check
    # parity and exact distance multisets on all ambient standard basis words
    # plus a few dense cases; the general statement follows algebraically.
    representatives = [(0,) * 64]
    representatives += [tuple(int(i == j) for i in range(64)) for j in range(64)]
    representatives += [(1,) * 64, tuple(i % 2 for i in range(64))]
    projection_inverse = {word[:10]: word for word in words}
    for f in representatives:
        e0 = projection_inverse[f[:10]]
        normalized = tuple(a ^ b for a, b in zip(f, e0))
        require(normalized[:10] == (0,) * 10, "Gauge did not normalize prefix")
        require(sum(normalized) % 2 == sum(f) % 2, "Gauge changed parity")
        before = sorted(sum(a != b for a, b in zip(f, e)) for e in words)
        after = sorted(sum(a != b for a, b in zip(normalized, e)) for e in words)
        require(before == after, "Gauge changed distance multiset")
    return {
        "distance_identity_and_truth_checks": checks,
        "parity_assignments_exhaustively_checked": parity_checks,
        "admissible_odd_weights_have_unique_auxiliary": True,
        "parity_offset": parity_offset,
        "auxiliary_bits": auxiliary_bits,
        "parity_only_accepted_weights": [weight for weight, witnesses in parity_witnesses.items() if witnesses],
        "extreme_rows_plus_parity_accepted_weights": [weight for weight, witnesses in effective_witnesses.items() if witnesses],
        "gauge_multiset_sample_vectors": len(representatives),
        "auxiliary_range_after_extreme_rows": [13, 18] if parity_offset == 1 else [0, 5],
    }


def toy_controls():
    """Exhaustive 8-bit controls only; not a search on the 64-bit instance.

    Extended [8,4,4] Hamming code generated by polynomial 1+x+x^3.
    Its low four coordinates form an information set.  Threshold 1 is
    feasible for odd words; threshold 3 is infeasible.  Check every ambient
    f, all normalized representatives, and every two-bit t assignment.
    """
    basis = [[int(i in (j, j + 1, j + 3)) for i in range(7)] for j in range(4)]
    for row in basis:
        row.append(sum(row) % 2)
    words = [tuple(sum(bits[j] * basis[j][i] for j in range(4)) % 2 for i in range(8))
             for bits in itertools.product((0, 1), repeat=4)]
    require(Counter(map(sum, words)) == {0: 1, 4: 14, 8: 1}, "Bad toy code")
    inverse = {w[:4]: w for w in words}
    require(len(inverse) == 16, "Bad toy information set")
    reports = {}
    for target in (1, 3):
        ambient_good = 0
        normalized_good = set()
        for f in itertools.product((0, 1), repeat=8):
            mathematical = sum(f) % 2 == 1 and min(sum(a != b for a, b in zip(f, e)) for e in words) >= target
            e0 = inverse[f[:4]]
            reduced = tuple(a ^ b for a, b in zip(f, e0))
            free = reduced[4:]
            encoded = any(
                sum(free) - 2 * t >= 1 and -sum(free) + 2 * t >= -1
                and all(sum((1 - 2 * e[i]) * reduced[i] for i in range(4, 8)) >= target - sum(e) for e in words)
                for t in range(4)
            )
            require(mathematical == encoded, "Toy exhaustive equivalence failed")
            if mathematical:
                ambient_good += 1
                normalized_good.add(reduced)
        expected = (128, 8) if target == 1 else (0, 0)
        require((ambient_good, len(normalized_good)) == expected, "Unexpected toy outcome")
        reports[str(target)] = {"ambient_odd_solutions": ambient_good,
                                "gauge_odd_solutions": len(normalized_good),
                                "ambient_words_exhausted": 256}
    return reports


def negative_controls(text, compact=False):
    lines = text.splitlines()
    constraint_indices = [i for i, line in enumerate(lines) if line and not line.startswith("*")]
    first, second, last = constraint_indices[0], constraint_indices[1], constraint_indices[-1]
    mutants = {}
    nvars = 57 if compact else 59
    last_aux_coefficient = -8 if compact else -32
    parity_offset = 27 if compact else 1

    def replace_line(name, index, content):
        changed = lines.copy()
        changed[index] = content
        mutants[name] = "\n".join(changed) + "\n"

    replace_line("distance_rhs_plus_one", first, lines[first].replace(">= 27;", ">= 28;"))
    replace_line("distance_coefficient_sign_flip", first, lines[first].replace("+1 x1 ", "-1 x1 ", 1))
    replace_line("distance_variable_t_leak", first, lines[first].replace("x54 ", "x55 ", 1))
    replace_line("duplicate_distance_row", second, lines[first])
    replace_line("wrong_auxiliary_weight", last - 1, lines[last - 1].replace(
        f"{last_aux_coefficient} x{nvars}", f"{last_aux_coefficient // 2} x{nvars}"))
    replace_line("wrong_reverse_parity_sign", last, lines[last].replace(f">= {-parity_offset};", f">= {parity_offset};"))
    replace_line("wrong_declared_variables", 0, lines[0].replace(str(nvars), str(nvars + 1), 1))
    replace_line("missing_terminator", first, lines[first][:-1])
    replace_line("duplicate_term", first, lines[first].replace(" >=", " +1 x1 >=", 1))
    mutants["dropped_distance_row"] = "\n".join(lines[:second] + lines[second + 1:]) + "\n"
    mutants["dropped_reverse_parity"] = "\n".join(lines[:last] + lines[last + 1:]) + "\n"
    # Even updating the declared row count must not permit a missing row.
    mutants["missing_row_with_revised_header"] = mutants["dropped_distance_row"].replace("1026", "1025", 1)
    outcomes = {}
    for label, mutant in mutants.items():
        require(mutant != text, f"No-op mutant {label}")
        try:
            audit_text(mutant, compact=compact)
        except AuditError as error:
            outcomes[label] = str(error)
        else:
            raise AuditError(f"Negative control accepted: {label}")
    return outcomes


def external_format_controls(text, compact=False):
    # Accept both requested parity syntaxes, and arbitrary row order, while
    # still checking every coefficient and the exact constraint multiset.
    lines = text.splitlines()
    constraints = [line for line in lines if line and not line.startswith("*")]
    comments = [line for line in lines[1:] if line.startswith("*")]
    variants = {
        "reordered_inequalities": "\n".join([lines[0]] + comments + list(reversed(constraints))) + "\n",
        "parity_equality": "\n".join(
            [lines[0].replace("1026", "1025")] + comments + constraints[:-2]
            + [constraints[-2].replace(" >= ", " = ")]) + "\n",
        "negative_parity_equality": "\n".join(
            [lines[0].replace("1026", "1025")] + comments + constraints[:-2]
            + [constraints[-1].replace(" >= ", " = ")]) + "\n",
    }
    report = {}
    for label, variant in variants.items():
        _, _, result = audit_text(variant, external=True, compact=compact)
        report[label] = {"status": "PASS", "source_constraint_rows": result["source_constraint_rows"]}
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("opb", type=Path)
    parser.add_argument("--report", type=Path)
    parser.add_argument("--external", action="store_true", help="Allow arbitrary row order and one parity equality instead of two inequalities")
    parser.add_argument("--compact", action="store_true", help="Expect 57 variables and sum(f)-2u=27 with a three-bit u")
    args = parser.parse_args()
    raw = args.opb.read_bytes()
    text = raw.decode("ascii")
    words, rows, exact = audit_text(text, external=args.external, compact=args.compact)
    # The negative-control suite uses a canonical serialization built from
    # audited rows so that external syntax does not affect mutation targets.
    control_text = f"* #variable= {exact['variables']} #constraint= 1026\n" + "\n".join(
        " ".join(f"{coefficient:+d} x{variable}" for variable, coefficient in sorted(terms.items()))
        + f" >= {rhs};" for terms, rhs in rows) + "\n"
    report = {
        "status": "PASS",
        "input": str(args.opb),
        "opb_sha256": hashlib.sha256(raw).hexdigest(),
        "opb_bytes": len(raw),
        "independence": "No generator import or manifest read; polynomial coefficient convolution",
        "external_input_mode": args.external,
        "exact_audit": exact,
        "semantic_controls": semantic_controls(words, rows),
        "exhaustive_toy_controls": toy_controls(),
        "negative_controls_rejected": negative_controls(control_text, compact=args.compact),
        "external_format_positive_controls": external_format_controls(control_text, compact=args.compact),
        "solver_invoked": False,
        "fixed_64_bit_feasibility": "NOT DETERMINED",
        "scope": "Exact fixed-code encoding and bounded controls only; no global nonexistence or novelty claim.",
    }
    rendered = json.dumps(report, indent=2) + "\n"
    if args.report:
        args.report.write_text(rendered, encoding="ascii")
    print(rendered, end="")


if __name__ == "__main__":
    main()

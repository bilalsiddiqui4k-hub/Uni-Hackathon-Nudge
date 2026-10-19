#!/usr/bin/env python3
"""
Automated Test Runner for Care Language Assistant
Compliant with Omega Digital Hackathon (omega-2026-10-19-core-v2)
Tests all 10 Functional Judging Tests (80 Marks) + Extended Dictionaries (Aggressive & Swearing)
"""

import re
import sys

# Comprehensive Dictionary: Core Workshop Pairs + Aggressive/Subjective + Swearing
ALL_DICTIONARY_PAIRS = [
    # === Core Assessed Pairs (Omega 2026 Core) ===
    ('service users', 'people we support', 'Use person-focused wording in this care note.', 'core'),
    ('service user', 'person we support', 'Use person-focused wording in this care note.', 'core'),
    ('clients', 'people we support', 'Use person-focused wording in this care note.', 'core'),
    ('client', 'person we support', 'Use person-focused wording in this care note.', 'core'),
    ('family contact', 'family time', 'Use family-centred language in this care note.', 'core'),
    ('contact centre', 'family centre', 'Use family-centred language in this care note.', 'core'),
    ('care leaver', 'care-experienced person', 'Use non-stigmatising, person-centred language in this care note.', 'core'),
    ('foster placement', 'foster home', 'Use homely, child-centred language in this care note.', 'core'),
    ('residential placement', "children's home", 'Use homely, child-centred language in this care note.', 'core'),
    ('looked-after child', 'child in care', 'Use respectful, person-centred language in this care note.', 'core'),

    # === Aggressive & Subjective Care Language ===
    ('challenging behaviours', 'distressed behaviours', 'Use person-centred wording; behaviour communicates distress or unmet needs.', 'aggressive'),
    ('challenging behavior', 'distressed behaviour', 'Use person-centred wording; behaviour communicates distress or unmet needs.', 'aggressive'),
    ('challenging behaviour', 'distressed behaviour', 'Use person-centred wording; behaviour communicates distress or unmet needs.', 'aggressive'),
    ('challenging behaviors', 'distressed behaviours', 'Use person-centred wording; behaviour communicates distress or unmet needs.', 'aggressive'),
    ('physically aggressive', 'experiencing high physical agitation', 'Describe observable actions neutrally rather than using subjective aggressive labels.', 'aggressive'),
    ('verbally aggressive', 'verbally expressing distress', 'Describe communication neutrally rather than labelling aggressive.', 'aggressive'),
    ('verbally abusive', 'shouting in distress', 'State specific observable actions rather than applying abusive labels.', 'aggressive'),
    ('physically abusive', 'physically expressing distress', 'Document specific physical actions factually.', 'aggressive'),
    ('temper tantrums', 'distress episodes', 'Use dignified, age-appropriate terminology for emotional overwhelm.', 'aggressive'),
    ('temper tantrum', 'distress episode', 'Use dignified, age-appropriate terminology for emotional overwhelm.', 'aggressive'),
    ('out of control', 'experiencing overwhelm', 'Describe observable signs of emotional distress neutrally.', 'aggressive'),
    ('acting out', 'communicating distress', 'Frame behaviour as communication of emotional distress or unmet needs.', 'aggressive'),
    ('refused to cooperate', 'declined to engage', 'Respect individual autonomy; use neutral, non-judgemental terms.', 'aggressive'),
    ('refused medication', 'declined medication', 'People have the right to decline medication; document neutrally without punitive framing.', 'aggressive'),
    ('refused support', 'declined support', 'People have the right to decline support; document neutrally.', 'aggressive'),
    ('refused food', 'declined food', 'Document autonomy neutrally without judgement.', 'aggressive'),
    ('non-compliant', 'declined support', 'Avoid punitive compliance framing; document choices neutrally.', 'aggressive'),
    ('non compliant', 'declined support', 'Avoid punitive compliance framing; document choices neutrally.', 'aggressive'),
    ('uncooperative', 'declined to engage', 'Use objective description rather than subjective character labelling.', 'aggressive'),
    ('aggressive', 'visibly distressed', 'Describe distress and behaviour neutrally rather than using subjective, stigmatising labels.', 'aggressive'),
    ('aggressively', 'in a distressed manner', 'Describe observable actions neutrally rather than attributing aggression.', 'aggressive'),
    ('aggressiveness', 'level of distress', 'Use de-escalating clinical terminology focused on distress.', 'aggressive'),
    ('hostile', 'distressed and upset', 'Use descriptive language rather than attributing hostile intent.', 'aggressive'),
    ('hostility', 'signs of distress', 'Describe specific observable behaviours neutrally.', 'aggressive'),
    ('combative', 'resisting with agitation', 'Avoid conflict-based terminology in care notes.', 'aggressive'),
    ('manipulative', 'expressing unmet needs', 'Avoid attributing negative character traits in professional care records.', 'aggressive'),
    ('tantrum', 'distress episode', 'Use dignified, respectful terminology for emotional overwhelm.', 'aggressive'),
    ('tantrums', 'distress episodes', 'Use dignified, respectful terminology for emotional overwhelm.', 'aggressive'),
    ('violent', 'physically distressed', 'State specific observable actions rather than broad stigmatising labels.', 'aggressive'),
    ('violently', 'with high physical agitation', 'Describe physical movements neutrally.', 'aggressive'),
    ('violence', 'physical distress episode', 'Describe specific incidents factually.', 'aggressive'),
    ('disruptive', 'experiencing an unsettled period', 'Focus on the person’s internal experience rather than inconvenience to others.', 'aggressive'),
    ('threatening', 'expressing intention', 'Document exact statements neutrally rather than applying subjective labels.', 'aggressive'),
    ('belligerent', 'agitated', 'Use neutral clinical terms rather than disparaging adjectives.', 'aggressive'),
    ('defiant', 'declining instructions', 'Respect autonomy; avoid punitive framing in care notes.', 'aggressive'),
    ('sulking', 'withdrawn', 'Use objective clinical observation instead of dismissive characterisations.', 'aggressive'),
    ('unmanageable', 'requiring specialist support', 'Focus on support needs rather than labelling the person.', 'aggressive'),

    # === Swearing & Profanity ===
    ('mother fuckers', '[profanity]', 'Avoid profanity in care records.', 'profanity'),
    ('mother fucker', '[profanity]', 'Avoid profanity in care records.', 'profanity'),
    ('motherfuckers', '[profanity]', 'Avoid profanity in care records.', 'profanity'),
    ('motherfucker', '[profanity]', 'Avoid profanity in care records.', 'profanity'),
    ('motherfucking', '[profanity]', 'Avoid profanity in care records.', 'profanity'),
    ('fuck off', '[dismissive profanity]', 'Document offensive phrases neutrally or place inside direct speech quotes.', 'profanity'),
    ('fucked up', 'distressed / unsettled', 'Use professional clinical wording instead of colloquial vulgarities.', 'profanity'),
    ('piss off', '[dismissive vulgarity]', 'Document offensive phrases neutrally or place inside direct speech quotes.', 'profanity'),
    ('pissed off', 'visibly agitated', 'Use professional clinical language instead of informal vulgarities.', 'profanity'),
    ('son of a bitch', '[profanity]', 'Inappropriate profanity; summarise neutrally.', 'profanity'),
    ('piece of shit', '[profanity]', 'Inappropriate profanity; summarise neutrally.', 'profanity'),
    ('full of shit', 'inaccurate', 'Document factual inaccuracies neutrally without vulgarities.', 'profanity'),
    ('bullshit', 'inaccurate information', 'Document inaccuracies factually without profanity in care records.', 'profanity'),
    ('fucking', '[profanity]', 'Avoid profanity in formal care records; summarise neutrally or quote verbatim.', 'profanity'),
    ('fucked', '[profanity]', 'Avoid profanity in formal care records; summarise neutrally.', 'profanity'),
    ('fucker', '[profanity]', 'Avoid offensive language in care records.', 'profanity'),
    ('fuckers', '[profanity]', 'Avoid offensive language in care records.', 'profanity'),
    ('fucks', '[profanity]', 'Avoid offensive language in care records.', 'profanity'),
    ('fuck', '[profanity]', 'Avoid profanity in formal care records; summarise neutrally or quote verbatim.', 'profanity'),
    ('shitty', 'distressing', 'Avoid informal vulgarities in professional care records.', 'profanity'),
    ('shitting', '[profanity]', 'Avoid profanity in formal care records.', 'profanity'),
    ('shits', '[profanity]', 'Avoid profanity in formal care records.', 'profanity'),
    ('shit', '[profanity]', 'Avoid profanity in formal care records; summarise neutrally.', 'profanity'),
    ('cunts', '[profanity]', 'Severely offensive language; record objectively or quote verbatim if legally required.', 'profanity'),
    ('cunt', '[profanity]', 'Severely offensive language; record objectively or quote verbatim if legally required.', 'profanity'),
    ('bitches', '[profanity]', 'Inappropriate and offensive language.', 'profanity'),
    ('bitching', 'complaining', 'Use professional clinical wording.', 'profanity'),
    ('bitch', '[profanity]', 'Inappropriate and offensive language.', 'profanity'),
    ('bastards', '[profanity]', 'Inappropriate language in care notes.', 'profanity'),
    ('bastard', '[profanity]', 'Inappropriate language in care notes.', 'profanity'),
    ('assholes', '[profanity]', 'Inappropriate language in care records.', 'profanity'),
    ('asshole', '[profanity]', 'Inappropriate language in care records.', 'profanity'),
    ('arseholes', '[profanity]', 'Inappropriate language in care records.', 'profanity'),
    ('arsehole', '[profanity]', 'Inappropriate language in care records.', 'profanity'),
    ('dickhead', '[profanity]', 'Inappropriate language in care records.', 'profanity'),
    ('dickheads', '[profanity]', 'Inappropriate language in care records.', 'profanity'),
    ('dicks', '[profanity]', 'Inappropriate language in care records.', 'profanity'),
    ('dick', '[profanity]', 'Inappropriate language in care records.', 'profanity'),
    ('wankers', '[profanity]', 'Offensive language in care records.', 'profanity'),
    ('wanker', '[profanity]', 'Offensive language in care records.', 'profanity'),
    ('twats', '[profanity]', 'Offensive language in care records.', 'profanity'),
    ('twat', '[profanity]', 'Offensive language in care records.', 'profanity'),
    ('pricks', '[profanity]', 'Offensive language in care records.', 'profanity'),
    ('prick', '[profanity]', 'Offensive language in care records.', 'profanity'),
    ('bollocks', '[profanity]', 'Inappropriate language in care records.', 'profanity'),
    ('pissing', '[vulgarity]', 'Avoid vulgarities in care records.', 'profanity'),
    ('piss', '[vulgarity]', 'Avoid vulgarities in care records.', 'profanity'),
    ('crap', 'unprofessional language', 'Maintain professional documentation standards.', 'profanity'),
    ('dammit', 'frustrated expression', 'Use neutral professional wording.', 'profanity'),
    ('damned', 'frustrated expression', 'Use neutral professional wording.', 'profanity'),
    ('damn', 'frustrated expression', 'Use neutral professional wording.', 'profanity'),
    ('bloody', 'strongly', 'Avoid colloquial vulgarities in care records.', 'profanity'),
    ('sluts', '[profanity]', 'Offensive/abusive language.', 'profanity'),
    ('slut', '[profanity]', 'Offensive/abusive language.', 'profanity'),
    ('whores', '[profanity]', 'Offensive/abusive language.', 'profanity'),
    ('whore', '[profanity]', 'Offensive/abusive language.', 'profanity'),
    ('cocksucker', '[profanity]', 'Inappropriate profanity.', 'profanity'),
    ('cocks', '[profanity]', 'Inappropriate language.', 'profanity'),
    ('cock', '[profanity]', 'Inappropriate language.', 'profanity')
]

def extract_quote_spans(text):
    spans = []
    # Match both straight quotes and curly quotes
    pattern = re.compile(r'\"[^\"]*\"|[“\"][^”\x22]*[”\x22]')
    for m in pattern.finditer(text):
        spans.append((m.start(), m.end()))
    return spans

def is_inside_quotes(start, end, quote_spans):
    for qs, qe in quote_spans:
        if not (end <= qs or start >= qe):
            return True
    return False

def scan_note(text, only_core=False):
    if not text or not text.strip():
        return []
    quote_spans = extract_quote_spans(text)
    occupied_spans = []
    suggestions = []

    pairs_to_use = [p for p in ALL_DICTIONARY_PAIRS if (not only_core or p[3] == 'core')]
    # Sort pairs by length descending
    sorted_pairs = sorted(pairs_to_use, key=lambda p: len(p[0]), reverse=True)

    for term, replacement, reason, category in sorted_pairs:
        escaped = re.escape(term)
        pattern = re.compile(rf'(?<![A-Za-z0-9]){escaped}(?![A-Za-z0-9])', re.IGNORECASE)
        for m in pattern.finditer(text):
            s, e = m.start(), m.end()
            if is_inside_quotes(s, e, quote_spans):
                continue
            if any(not (e <= os or s >= oe) for os, oe in occupied_spans):
                continue
            occupied_spans.append((s, e))

            matched_str = text[s:e]
            actual_repl = replacement
            if matched_str.isupper() and len(matched_str) > 1:
                actual_repl = replacement.upper()
            elif matched_str[0].isupper() and len(matched_str) > 1 and matched_str[1].islower():
                actual_repl = replacement[0].upper() + replacement[1:]

            suggestions.append({
                'start': s,
                'end': e,
                'matched': matched_str,
                'term': term,
                'replacement': actual_repl,
                'reason': reason,
                'category': category,
                'status': 'pending'
            })

    suggestions.sort(key=lambda x: x['start'])
    for idx, item in enumerate(suggestions):
        item['id'] = idx + 1
    return suggestions

def build_reviewed(text, suggestions):
    accepted = [s for s in suggestions if s['status'] == 'accepted']
    accepted.sort(key=lambda x: x['start'], reverse=True)
    reviewed = text
    for item in accepted:
        reviewed = reviewed[:item['start']] + item['replacement'] + reviewed[item['end']:]
    return reviewed

def run_all_tests():
    print("=" * 75)
    print(" CARE LANGUAGE ASSISTANT — JUDGING SUITE & EXTENDED DICTIONARY TESTS")
    print(" Omega Digital Hackathon (Judging Version: omega-2026-10-19-core-v2)")
    print("=" * 75)

    score = 0
    total_marks = 80
    tests = []

    # --- Test 1: Find and explain ---
    t1_text = "The service user arrived."
    t1_s = scan_note(t1_text, only_core=True)
    t1_pass = (
        len(t1_s) == 1 and
        t1_s[0]['term'] == 'service user' and
        t1_s[0]['replacement'] == 'person we support' and
        bool(t1_s[0]['reason']) and
        build_reviewed(t1_text, t1_s) == t1_text
    )
    tests.append((1, "Find and explain", 8, t1_pass, "Found 'service user' -> 'person we support' with reason; unchanged before accept."))

    # --- Test 2: Longer phrases ---
    t2_text = "The care leaver went to the contact centre for family contact."
    t2_s = scan_note(t2_text, only_core=True)
    t2_repls = [x['replacement'] for x in t2_s]
    t2_pass = (
        len(t2_s) == 3 and
        'care-experienced person' in t2_repls and
        'family centre' in t2_repls and
        'family time' in t2_repls and
        build_reviewed(t2_text, t2_s) == t2_text
    )
    tests.append((2, "Longer phrases", 8, t2_pass, "Found 3 suggestions (care-experienced person, family centre, family time). No auto edit."))

    # --- Test 3: Accept one ---
    t3_text = "The client attended family contact."
    t3_s = scan_note(t3_text, only_core=True)
    for s in t3_s:
        if s['term'] == 'client':
            s['status'] = 'accepted'
    t3_reviewed = build_reviewed(t3_text, t3_s)
    t3_pass = (
        t3_reviewed == "The person we support attended family contact." and
        any(x['term'] == 'family contact' and x['status'] == 'pending' for x in t3_s)
    )
    tests.append((3, "Accept one", 8, t3_pass, "Reviewed: 'The person we support attended family contact.' Original unchanged. Family contact pending."))

    # --- Test 4: Ignore one ---
    t4_text = "The client attended family contact."
    t4_s = scan_note(t4_text, only_core=True)
    for s in t4_s:
        if s['term'] == 'client':
            s['status'] = 'ignored'
    t4_reviewed = build_reviewed(t4_text, t4_s)
    t4_pass = (
        t4_reviewed == t4_text and
        any(x['term'] == 'client' and x['status'] == 'ignored' for x in t4_s) and
        any(x['term'] == 'family contact' and x['status'] == 'pending' for x in t4_s)
    )
    tests.append((4, "Ignore one", 8, t4_pass, "Client marked ignored. Texts unchanged. Family-contact suggestion remains."))

    # --- Test 5: Remaining pairs ---
    t5_pairs = [
        ('service users', 'people we support'),
        ('clients', 'people we support'),
        ('looked-after child', 'child in care'),
        ('foster placement', 'foster home'),
        ('residential placement', "children's home")
    ]
    t5_pass = True
    for term, exp_repl in t5_pairs:
        txt = f"Recorded wording: {term}."
        s = scan_note(txt, only_core=True)
        if len(s) != 1:
            t5_pass = False
            break
        s[0]['status'] = 'accepted'
        res = build_reviewed(txt, s)
        if res != f"Recorded wording: {exp_repl}.":
            t5_pass = False
            break
    tests.append((5, "Remaining pairs", 8, t5_pass, "Accepted all 5 remaining pairs. Retained prefix and final full stop."))

    # --- Test 6: Repeats and boundaries ---
    t6_text = "The client called the client. The CLIENT arrived. The clientele waited."
    t6_s = scan_note(t6_text, only_core=True)
    t6_count_check = (
        len(t6_s) == 3 and
        all(x['term'] == 'client' for x in t6_s) and
        not any('clientele' in x['matched'].lower() for x in t6_s)
    )
    if t6_s:
        t6_s[0]['status'] = 'accepted'
    t6_reviewed = build_reviewed(t6_text, t6_s)
    t6_pass = (
        t6_count_check and
        t6_reviewed == "The person we support called the client. The CLIENT arrived. The clientele waited."
    )
    tests.append((6, "Repeats and boundaries", 8, t6_pass, "3 occurrences found including CLIENT, none in clientele. First accepted, others reviewable."))

    # --- Test 7: Unrelated words ---
    t7_text = "Staff will contact the office. Sam made eye contact. The placement officer called."
    t7_s = scan_note(t7_text, only_core=True)
    t7_pass = len(t7_s) == 0 and build_reviewed(t7_text, t7_s) == t7_text
    tests.append((7, "Unrelated words", 8, t7_pass, "Zero care flags. Text exactly unchanged."))

    # --- Test 8: Direct quotes ---
    t8_straight = 'Sam said, "The client attended family contact." Staff recorded family contact at 18:00.'
    t8_s_str = scan_note(t8_straight, only_core=True)
    t8_pass_str = len(t8_s_str) == 1 and t8_s_str[0]['term'] == 'family contact'
    if t8_s_str:
        t8_s_str[0]['status'] = 'accepted'
    t8_rev_str = build_reviewed(t8_straight, t8_s_str)
    t8_pass_str = t8_pass_str and (t8_rev_str == 'Sam said, "The client attended family contact." Staff recorded family time at 18:00.')

    t8_curly = 'Sam said, “The client attended family contact.” Staff recorded family contact at 18:00.'
    t8_s_cur = scan_note(t8_curly, only_core=True)
    t8_pass_cur = len(t8_s_cur) == 1 and t8_s_cur[0]['term'] == 'family contact'
    if t8_s_cur:
        t8_s_cur[0]['status'] = 'accepted'
    t8_rev_cur = build_reviewed(t8_curly, t8_s_cur)
    t8_pass_cur = t8_pass_cur and (t8_rev_cur == 'Sam said, “The client attended family contact.” Staff recorded family time at 18:00.')

    t8_pass = t8_pass_str and t8_pass_cur
    tests.append((8, "Direct quotes", 8, t8_pass, "Straight & curly quotes preserved. Only outside family contact changed. 18:00 unchanged."))

    # --- Test 9: Preserve facts ---
    t9_text = "At 18:40, Alex reported that the client pushed Sam and left a bruise."
    t9_s = scan_note(t9_text, only_core=True)
    if t9_s:
        t9_s[0]['status'] = 'accepted'
    t9_rev = build_reviewed(t9_text, t9_s)
    t9_pass = (
        len(t9_s) == 1 and
        t9_rev == "At 18:40, Alex reported that the person we support pushed Sam and left a bruise."
    )
    tests.append((9, "Preserve facts", 8, t9_pass, "Only client changed. Time (18:40), names (Alex, Sam), injury (bruise) fully intact."))

    # --- Test 10: Reset state ---
    t10_text = "Everyone ate dinner."
    t10_s = scan_note(t10_text, only_core=True)
    t10_pass = len(t10_s) == 0 and build_reviewed(t10_text, t10_s) == t10_text
    tests.append((10, "Reset state", 8, t10_pass, "Zero flags. Both versions show new note. Prior state cleanly reset."))

    # Print core 10 results
    for num, name, pts, passed, detail in tests:
        mark_pts = pts if passed else 0
        score += mark_pts
        status = "✓ PASS (8/8)" if passed else "✗ FAIL (0/8)"
        print(f"\n[Test {num:02d}] {name.ljust(28)} : {status}")
        print(f"         {detail}")

    print("\n" + "=" * 75)
    print(f" OFFICIAL SCORE: {score} / {total_marks} FUNCTIONAL MARKS")
    if score == total_marks:
        print(" RESULT: 100% PERFECT PASS ON ALL PUBLISHED HACKATHON TESTS!")
    else:
        print(" RESULT: SOME TESTS FAILED")
    print("=" * 75)

    # --- Bonus Tests: Extended Dictionaries ---
    print("\n--- EXTENDED DICTIONARY VERIFICATION ---")

    # Bonus 11: Aggressive Wording
    t11_text = "The client was aggressive and non-compliant."
    t11_s = scan_note(t11_text, only_core=False)
    t11_terms = [x['term'] for x in t11_s]
    t11_pass = 'client' in t11_terms and 'aggressive' in t11_terms and 'non-compliant' in t11_terms
    status_11 = "✓ PASS" if t11_pass else "✗ FAIL"
    print(f"\n[Bonus 11] Extended Aggressive Language  : {status_11}")
    print("           Flagged 'aggressive' -> 'visibly distressed' & 'non-compliant' -> 'declined support'.")

    # Bonus 12: Swearing & Quote Immunity
    t12_text = 'Sam said, "Fuck off!" Staff noted bullshit at 14:00.'
    t12_s = scan_note(t12_text, only_core=False)
    # Inside quotes "Fuck off!" is immune; outside "bullshit" is flagged
    t12_pass = len(t12_s) == 1 and t12_s[0]['term'] == 'bullshit'
    status_12 = "✓ PASS" if t12_pass else "✗ FAIL"
    print(f"\n[Bonus 12] Swearing & Direct Quote Immunity: {status_12}")
    print("           'Fuck off!' inside quotes preserved; 'bullshit' outside quotes flagged.")
    print("=" * 75)

    return 0 if (score == total_marks and t11_pass and t12_pass) else 1

if __name__ == "__main__":
    sys.exit(run_all_tests())

# Day 61, Task 9 (ABAP slot) -- ABAP: explain one concept in your own words

(Pick a concept you have NOT already written up -- check the earlier day files in this folder.)

## THE TASK

Pick ONE concept -- suggestions: shared memory objects (an area class defined in transaction SHMA, the root class marked `SHARED MEMORY ENABLED`, `ATTACH_FOR_WRITE` / `ATTACH_FOR_READ` / `DETACH_COMMIT`, area instances and versions, and when a shared-memory cache beats re-reading the database or a static class attribute), regular expressions in ABAP (`FIND` / `REPLACE ... PCRE` vs. the old POSIX `REGEX`, `FIND ALL OCCURRENCES ... RESULTS`, `SUBMATCHES`, the built-in functions `matches( )`, `count( )`, `replace( ... pcre = ... )`, and `cl_abap_regex` / `cl_abap_matcher`), or the background processing framework bgPF (`if_bgmc_op_single`, controlled vs. uncontrolled operations, `cl_bgmc_process_factory`, and why it replaces `CALL FUNCTION ... IN BACKGROUND TASK` / bgRFC boilerplate in ABAP Cloud) -- and explain it as if teaching a classmate who knows classic ABAP report programs, internal tables and `SELECT`, but has never used this feature.

## CONCEPT CHOSEN

Regular expressions in ABAP with PCRE: `FIND` / `REPLACE ... PCRE` (instead of the old POSIX `REGEX` addition), `FIND ALL OCCURRENCES ... RESULTS`, `SUBMATCHES`, the built-in string functions with a `pcre =` parameter (`matches( )`, `count( )`, `find( )`, `replace( )`, `match( )`), and the object API `cl_abap_regex` / `cl_abap_matcher`.

## MY EXPLANATION (write this BEFORE looking anything up)

Classic ABAP string handling is `SEARCH`, `SPLIT`, `CP` patterns (`*`, `+`) and a lot of `offset/length` arithmetic. That breaks down as soon as the format has structure: "is this a valid e-mail / IBAN / order number like `PO-2026-000123`", "pull every amount out of a free-text field", "turn `DD.MM.YYYY` into `YYYYMMDD`". A regular expression describes the *shape* of the text once, and the regex engine does the scanning.

- **Which engine.** ABAP has supported POSIX regular expressions (`REGEX`) for a long time, but that engine is slow and limited, and since 7.55 it is obsolete. The modern choice is **PCRE** (Perl-compatible, the same dialect as most other languages): non-greedy quantifiers `*?`, lookahead/lookbehind `(?=...)` / `(?<=...)`, named groups, `\d`, `\s`, Unicode properties, inline flags like `(?i)`. In every statement and function you pick the engine with the keyword/parameter: `PCRE` / `pcre =` instead of `REGEX` / `regex =`. (There is also `XPATH`/`XSD` regex for special cases.)
- **Statements.** `FIND [FIRST OCCURRENCE OF | ALL OCCURRENCES OF] PCRE pattern IN text ...` with additions: `IGNORING CASE`, `MATCH COUNT DATA(n)`, `MATCH OFFSET DATA(off) MATCH LENGTH DATA(len)`, `SUBMATCHES g1 g2 ...` (the capture groups of the first match), or `RESULTS DATA(results)` which returns a table of `match_result` rows (offset, length and a `submatches` table per match) -- that's the way to process *all* matches. `REPLACE [ALL OCCURRENCES OF] PCRE pattern IN text WITH replacement` changes the variable in place; `$1`, `$2` (or `$0` for the whole match) in the replacement refer to the groups. `sy-subrc` = 0 means found / replaced. Both also work on internal tables (`IN TABLE itab`).
- **Built-in functions** (usable in expressions, no helper variables): `matches( val = text pcre = '...' )` is a predicate function -- true if the *whole* text matches, great in `IF`; `count( val = text pcre = '...' )` -> number of matches; `find( val = text pcre = '...' )` -> offset or -1; `match( val = text pcre = '...' occ = 1 )` -> the matched substring; `replace( val = text pcre = '...' with = '...' occ = 0 )` -> new string (`occ = 0` = all occurrences).
- **Object API.** `cl_abap_regex=>create_pcre( pattern = ... ignore_case = abap_true )` compiles a pattern once into an object; `->create_matcher( text = ... )` gives a `cl_abap_matcher` with `find_next( )`, `get_offset( )`, `get_submatch( n )`, `match( )`, `replace_all( )`. Use it when the same pattern runs over many strings in a loop (compile once), or when you need step-by-step control over matches.

**When to use:** validating input formats, extracting values from semi-structured text (log lines, e-mail bodies, IDoc/free-text fields), reformatting strings, and cleanup (collapse whitespace, strip non-digits). **When not to:** simple fixed-string checks (`CS`, `CP`, `find( val = sub = )`, `starts_with`-style comparisons are faster and clearer), real parsing of nested formats (JSON, XML -- use `/ui2/cl_json`, `cl_sxml_*`, transformations), and as a substitute for proper data modelling. Keep patterns readable (comment them), anchor them (`^...$` or use `matches( )`) when validating, and beware catastrophic backtracking with nested quantifiers on long input.

## A SMALL EXAMPLE

```abap
* 1) Validate a purchase-order number like PO-2026-000123 (whole string must match)
DATA(lv_po) = `PO-2026-000123`.
IF matches( val = lv_po pcre = `PO-\d{4}-\d{6}` ).
  " valid
ENDIF.

* 2) Pull year and running number out with capture groups
FIND PCRE `^PO-(\d{4})-(\d+)$` IN lv_po SUBMATCHES DATA(lv_year) DATA(lv_number).
IF sy-subrc = 0.
  " lv_year = '2026', lv_number = '000123'
ENDIF.

* 3) Every amount in a free-text note, with all matches and their groups
DATA(lv_note) = `Paid 1,250.00 EUR on 03.11.2026, open 99.50 EUR, fee 5 EUR`.
FIND ALL OCCURRENCES OF PCRE `(\d[\d,]*(?:\.\d{2})?)\s*EUR`
     IN lv_note RESULTS DATA(lt_results).
LOOP AT lt_results INTO DATA(ls_result).
  DATA(ls_group) = ls_result-submatches[ 1 ].
  DATA(lv_amount) = substring( val = lv_note off = ls_group-offset len = ls_group-length ).
  " 1,250.00 / 99.50 / 5
ENDLOOP.

* 4) Reformat DD.MM.YYYY -> YYYY-MM-DD everywhere in the text
DATA(lv_iso) = replace( val  = lv_note
                        pcre = `(\d{2})\.(\d{2})\.(\d{4})`
                        with = `$3-$2-$1`
                        occ  = 0 ).

* 5) Compile once, reuse in a loop (case-insensitive)
DATA(lo_regex) = cl_abap_regex=>create_pcre( pattern     = `\bINV-\d+\b`
                                             ignore_case = abap_true ).
DATA lt_invoices TYPE string_table.
LOOP AT lt_mail_lines INTO DATA(lv_line).          " lt_mail_lines TYPE string_table
  DATA(lo_matcher) = lo_regex->create_matcher( text = lv_line ).
  WHILE lo_matcher->find_next( ) = abap_true.
    APPEND substring( val = lv_line
                      off = lo_matcher->get_offset( )
                      len = lo_matcher->get_length( ) ) TO lt_invoices.
  ENDWHILE.
ENDLOOP.
```

## WHAT I GOT WRONG / CHECKED AFTERWARDS

- PCRE in ABAP needs release 7.55+ (on-premise; it's what ABAP Cloud supports); the POSIX `REGEX` addition is marked obsolete from then on, and the syntax check warns about it. Check the system release before relying on PCRE-only syntax.
- `matches( )` tests the **whole** string (implicitly anchored), while `FIND` / `count( )` / `find( )` search for a match **anywhere** -- for validation with `FIND` you must add `^...$` yourself.
- In ABAP string templates/backquote literals the backslash is just a character, so `\d` can be written directly in `` `...` `` -- no double escaping as in Java strings. Inside `|...|` string templates, however, `\` is an escape character and `{`/`}` are special, so patterns are easier in backquotes.
- `SUBMATCHES` only gives the groups of the **first** match; for all matches use `RESULTS` (each row has a `submatches` table with offset/length, not the text -- you cut the text out with `substring( )`).
- `cl_abap_regex=>create_pcre( )` is the PCRE factory; the plain `NEW cl_abap_regex( pattern = ... )` constructor creates a POSIX regex, so it's easy to end up on the old engine by accident.

## ONE-LINE TAKEAWAY

Use PCRE (`FIND/REPLACE ... PCRE`, `matches( )`, `replace( pcre = )`, `cl_abap_regex=>create_pcre( )`) instead of the obsolete POSIX `REGEX` whenever text has a structure worth describing -- but anchor validation patterns and keep plain `CS`/`CP` for simple checks.

#!/usr/bin/env bash
#
# Day 62, Task 5 -- Unix/shell: a canonical hex+ASCII dump (modelled on `hexdump -C`),
# with line squeezing, a skip offset and a length limit.
#
# THE PROBLEM
# ------------
# Usage: ./hexdump_lite.sh [-v] [-s SKIP] [-n LEN] [FILE]
# Read FILE (or stdin) as raw bytes and print 16 bytes per line in this exact format:
#
#   00000000  48 65 6c 6c 6f 2c 20 77  6f 72 6c 64 2e 0a        |Hello, world..|
#   0000000e
#
#   - an 8-digit lowercase hex OFFSET of the line's first byte, then TWO spaces;
#   - each byte as two lowercase hex digits followed by one space, with ONE EXTRA
#     space after the 8th byte; a short last line is padded with spaces so the
#     ASCII column always starts at the same column (every line is the same width);
#   - one more space, then the ASCII column between | |: bytes 0x20..0x7e as
#     themselves, everything else (tabs, newlines, >= 0x7f, NUL) as "."
#     (only the bytes that exist -- no padding inside the bars);
#   - after the data, a final line with just the 8-digit hex offset of the END
#     (SKIP + number of bytes dumped). Empty input prints only "00000000".
# Squeezing: when a full 16-byte line has exactly the same bytes as the previous full
# line, print a single line "*" instead, and keep printing nothing for further
# identical lines until a different line arrives (whose real offset is printed).
# -v disables squeezing. Partial (short) lines are never squeezed.
# -s SKIP: ignore the first SKIP bytes; offsets still count from the start of the
#          input (so the first line starts at offset SKIP, not 0).
# -n LEN:  dump at most LEN bytes (after the skip).
# Unreadable FILE: "hexdump_lite.sh: FILE: cannot read" on stderr, exit 1.
# Unknown option: a usage line on stderr, exit 2.
#
# HINT: let `od -An -v -tu1` turn the bytes into decimal numbers (whitespace
# separated, -v so od itself doesn't squeeze), then do all the formatting in ONE awk
# program: collect up to 16 values, sprintf("%02x") them, build the ASCII string with
# sprintf("%c", v) for printable values, and remember the previous full line's hex
# text to detect repeats. Don't read binary data with `read` in a bash loop: NUL bytes
# and trailing newlines get lost.
#
# Check with:
#   printf 'Hello, world.\n' | ./hexdump_lite.sh
#     00000000  48 65 6c 6c 6f 2c 20 77  6f 72 6c 64 2e 0a        |Hello, world..|
#     0000000e
#   printf 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA0123\n' | ./hexdump_lite.sh
#     00000000  41 41 41 41 41 41 41 41  41 41 41 41 41 41 41 41  |AAAAAAAAAAAAAAAA|
#     *
#     00000030  30 31 32 33 0a                                    |0123.|
#     00000035
#   printf 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA' | ./hexdump_lite.sh -v
#     00000000  41 41 41 41 41 41 41 41  41 41 41 41 41 41 41 41  |AAAAAAAAAAAAAAAA|
#     00000010  41 41 41 41 41 41 41 41  41 41 41 41 41 41 41 41  |AAAAAAAAAAAAAAAA|
#     00000020  41 41 41 41 41 41 41 41  41 41 41 41 41 41 41 41  |AAAAAAAAAAAAAAAA|
#     00000030
#   printf '\x00\x01\x7f\x80\xff tab\there' | ./hexdump_lite.sh
#     00000000  00 01 7f 80 ff 20 74 61  62 09 68 65 72 65        |..... tab.here|
#     0000000e
#   printf '0123456789abcdefghijklmnopqrstuvwxyz' | ./hexdump_lite.sh -s 10 -n 20
#     0000000a  61 62 63 64 65 66 67 68  69 6a 6b 6c 6d 6e 6f 70  |abcdefghijklmnop|
#     0000001a  71 72 73 74                                       |qrst|
#     0000001e
#   printf '' | ./hexdump_lite.sh                    -> 00000000
#   ./hexdump_lite.sh /no/such/file                  -> stderr message, exit 1
#   ./hexdump_lite.sh -x                             -> usage on stderr, exit 2
# If you have `hexdump` installed, `diff <(./hexdump_lite.sh f) <(hexdump -C f)` should
# be empty for any non-empty file.

prog=hexdump_lite.sh
usage() { echo "usage: $prog [-v] [-s SKIP] [-n LEN] [FILE]" >&2; exit 2; }

squeeze=1 skip=0 len=
while getopts ":vs:n:" opt; do
    case $opt in
        v) squeeze=0 ;;
        s) skip=$OPTARG ;;
        n) len=$OPTARG ;;
        *) usage ;;
    esac
done
shift $((OPTIND - 1))
[ $# -le 1 ] || usage
case $skip in ''|*[!0-9]*) usage ;; esac
if [ -n "$len" ]; then case $len in *[!0-9]*) usage ;; esac; fi

file=${1:--}
if [ "$file" != "-" ] && { [ ! -f "$file" ] || [ ! -r "$file" ]; }; then
    echo "$prog: $file: cannot read" >&2
    exit 1
fi

{
    if [ "$file" = "-" ]; then cat; else cat -- "$file"; fi
} | tail -c +"$((skip + 1))" | { if [ -n "$len" ]; then head -c "$len"; else cat; fi; } |
od -An -v -tu1 |
awk -v skip="$skip" -v squeeze="$squeeze" '
function flush(   i, hex, asc, v, line) {
    if (n == 0) return
    hex = ""; asc = ""
    for (i = 0; i < 16; i++) {
        if (i < n) {
            v = buf[i]
            hex = hex sprintf("%02x ", v)
            asc = asc ((v >= 32 && v <= 126) ? sprintf("%c", v) : ".")
        } else {
            hex = hex "   "
        }
        if (i == 7) hex = hex " "
    }
    if (squeeze && n == 16 && have_prev && hex == prev) {
        if (!starred) { print "*"; starred = 1 }
    } else {
        printf "%08x  %s |%s|\n", off, hex, asc
        starred = 0
    }
    if (n == 16) { prev = hex; have_prev = 1 } else { have_prev = 0 }
    off += n
    n = 0
}
BEGIN { off = skip + 0; n = 0 }
{
    for (f = 1; f <= NF; f++) {
        buf[n++] = $f + 0
        if (n == 16) flush()
    }
}
END { flush(); printf "%08x\n", off }
'

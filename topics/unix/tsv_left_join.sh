#!/usr/bin/env bash
#
# Day 61, Task 6 -- Unix/shell: LEFT OUTER JOIN two TSV files on a key column (unsorted input, 1:N).
#
# THE PROBLEM
# ------------
# Usage: ./tsv_left_join.sh [-k L:R] LEFT.tsv RIGHT.tsv
# Both files are tab-separated with a HEADER line. -k L:R names the 1-based key column
# in LEFT (L) and in RIGHT (R); default 1:1.
# Output (stdout, tab-separated):
#   - header: the LEFT header, followed by the RIGHT header WITHOUT its key column;
#   - every LEFT row, in LEFT file order, followed by the non-key columns of EVERY
#     matching RIGHT row (one output line per match, in RIGHT file order -- 1:N fan-out);
#   - a LEFT row with no match gets one "NULL" per right non-key column.
# Neither file is sorted, so `join` (which needs sorted input and drops the left order)
# is not the tool here -- don't use join(1) or sort(1).
# After the join, print "unmatched right rows: N" to STDERR, where N counts the RIGHT data
# rows whose key never matched any LEFT row (orders for unknown users, etc.).
# Keys are compared as exact strings ("02" != "2"). Fields may contain spaces.
# Exit 2 with a usage line on stderr for: a malformed -k (must be two positive integers),
# a wrong number of files, an unreadable file, or a key column larger than that file's
# number of header columns.
#
# HINT: awk -F'\t' -v OFS='\t' with the RIGHT file first (NR == FNR): store the rows per
# key as cnt[key]++ ; row[key, cnt[key]] = "<tab>col<tab>col...". Then, while reading
# LEFT, print $0 followed by each stored row (or the NULL filler), and mark used[key].
# In END, sum cnt[k] for the keys that were never used.
#
# Check with:
#   printf 'user_id\tname\tcity\n1\tAni\tYerevan\n2\tDavit\tGyumri\n3\tLilit\tYerevan\n4\tTigran\tVanadzor\n5\tNarek\tYerevan\n' > /tmp/users.tsv
#   printf 'order_id\tuser_id\tamount\n100\t2\t15.50\n101\t3\t7.00\n102\t2\t42.00\n103\t9\t3.25\n104\t3\t1.00\n105\t8\t9.99\n' > /tmp/orders.tsv
#   ./tsv_left_join.sh -k 1:2 /tmp/users.tsv /tmp/orders.tsv
# Expected stdout (<TAB> = a tab):
#   user_id<TAB>name<TAB>city<TAB>order_id<TAB>amount
#   1<TAB>Ani<TAB>Yerevan<TAB>NULL<TAB>NULL
#   2<TAB>Davit<TAB>Gyumri<TAB>100<TAB>15.50
#   2<TAB>Davit<TAB>Gyumri<TAB>102<TAB>42.00
#   3<TAB>Lilit<TAB>Yerevan<TAB>101<TAB>7.00
#   3<TAB>Lilit<TAB>Yerevan<TAB>104<TAB>1.00
#   4<TAB>Tigran<TAB>Vanadzor<TAB>NULL<TAB>NULL
#   5<TAB>Narek<TAB>Yerevan<TAB>NULL<TAB>NULL
# Expected stderr:
#   unmatched right rows: 2
#
#   ./tsv_left_join.sh -k 2:1 /tmp/orders.tsv /tmp/users.tsv
# Expected stdout:
#   order_id<TAB>user_id<TAB>amount<TAB>name<TAB>city
#   100<TAB>2<TAB>15.50<TAB>Davit<TAB>Gyumri
#   101<TAB>3<TAB>7.00<TAB>Lilit<TAB>Yerevan
#   102<TAB>2<TAB>42.00<TAB>Davit<TAB>Gyumri
#   103<TAB>9<TAB>3.25<TAB>NULL<TAB>NULL
#   104<TAB>3<TAB>1.00<TAB>Lilit<TAB>Yerevan
#   105<TAB>8<TAB>9.99<TAB>NULL<TAB>NULL
# Expected stderr:
#   unmatched right rows: 3
#
#   ./tsv_left_join.sh -k 1:7 /tmp/users.tsv /tmp/orders.tsv   -> usage on stderr, exit 2
#   ./tsv_left_join.sh -k x:1 /tmp/users.tsv /tmp/orders.tsv   -> usage on stderr, exit 2
#   ./tsv_left_join.sh /tmp/users.tsv                          -> usage on stderr, exit 2

usage() {
    echo "usage: $(basename "$0") [-k L:R] LEFT.tsv RIGHT.tsv   (L, R = 1-based key columns)" >&2
    exit 2
}

lk=1
rk=1
while getopts ":k:" opt; do
    case "$opt" in
        k) case "$OPTARG" in
               *:*) lk="${OPTARG%%:*}"; rk="${OPTARG#*:}" ;;
               *)   usage ;;
           esac
           case "$lk" in ''|*[!0-9]*) usage ;; esac
           case "$rk" in ''|*[!0-9]*) usage ;; esac
           lk=$((10#$lk)); rk=$((10#$rk))
           { [ "$lk" -ge 1 ] && [ "$rk" -ge 1 ]; } || usage ;;
        *) usage ;;
    esac
done
shift $((OPTIND - 1))
[ $# -eq 2 ] || usage
left="$1"
right="$2"
for f in "$left" "$right"; do
    { [ -f "$f" ] && [ -r "$f" ]; } || usage
done
ncols() { head -n 1 "$1" | awk -F'\t' '{ print NF }'; }
[ "$lk" -le "$(ncols "$left")" ] || usage
[ "$rk" -le "$(ncols "$right")" ] || usage

awk -F'\t' -v OFS='\t' -v lk="$lk" -v rk="$rk" '
function strip_cr() { sub(/\r$/, ""); }
# RIGHT file first: remember the non-key columns of every row, grouped by key
NR == FNR {
    strip_cr()
    rest = ""
    for (i = 1; i <= NF; i++) if (i != rk) rest = rest OFS $i
    if (FNR == 1) {
        rhead = rest
        filler = ""
        for (i = 1; i < NF; i++) filler = filler OFS "NULL"
        next
    }
    key = $rk
    if (!(key in cnt)) order[++nkeys] = key
    row[key, ++cnt[key]] = rest
    next
}
# LEFT file: emit in file order, fanning out over all matches
{
    strip_cr()
    if (FNR == 1) { print $0 rhead; next }
    key = $lk
    if (key in cnt) {
        used[key] = 1
        for (j = 1; j <= cnt[key]; j++) print $0 row[key, j]
    } else {
        print $0 filler
    }
}
END {
    unmatched = 0
    for (k = 1; k <= nkeys; k++) if (!(order[k] in used)) unmatched += cnt[order[k]]
    printf "unmatched right rows: %d\n", unmatched > "/dev/stderr"
}' "$right" "$left"

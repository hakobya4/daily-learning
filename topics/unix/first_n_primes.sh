#!/usr/bin/env bash
#
# Day 51, Task 5 -- Unix/shell: first N primes.
#
# THE PROBLEM
# ------------
# Usage: ./first_n_primes.sh N
# Print the first N prime numbers, one per line. Exit 1 (with a usage message on stderr)
# if N is not a positive integer.
#
# HINT: awk loop with trial division by the primes found so far (stop at sqrt), or
# factor(1) from coreutils. Do not hard-code a list.
#
# Check with:
#   ./first_n_primes.sh 5
# Expected:
#   2
#   3
#   5
#   7
#   11

if [ "$#" -ne 1 ] || ! [[ "$1" =~ ^[0-9]+$ ]] || [ "$((10#$1))" -lt 1 ]; then
    echo "usage: $0 N   (N must be a positive integer)" >&2
    exit 1
fi

awk -v n="$((10#$1))" 'BEGIN {
    found = 0
    for (c = 2; found < n; c++) {
        is_prime = 1
        for (i = 1; i <= found && primes[i] * primes[i] <= c; i++)
            if (c % primes[i] == 0) { is_prime = 0; break }
        if (is_prime) { primes[++found] = c; print c }
    }
}'

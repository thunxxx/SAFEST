#!/bin/bash
awk '/<div class="premium-content">/{flag=1;next}/</div>/{flag=0}flag' "$1" > report.txt

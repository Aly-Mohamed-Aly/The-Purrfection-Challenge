haystack ="sadbutsad"
needle = "sad"
r = len(needle)
x = len(haystack)
if x < r:
    print(-1)
for i in range(x - r):
    print(haystack[i:i + r ])
    if haystack[i:i + r] == needle:
        print(i)
if needle == haystack:
    print(0)
print(-1)
''' writing_prompt_stats
Spits out some useful stats about your writing prompts. Can be used
to determine how much data your model will have for each character.
'''

with open("writing_prompts.txt", "r") as f:
    lines=f.readlines()

all_chars={}
for line in lines:
    for char in line[:-1]:
        if char in all_chars:
            all_chars[char] += 1
        else:
            all_chars[char] = 1

all_used_chars = []
keys=[]
for key in all_chars:
    keys.append(key)

for key in sorted(keys):
    val=all_chars[key]
    print(key, ":", val)
    all_used_chars.append(key)

print()
all_used_chars.sort()
#print(all_used_chars)
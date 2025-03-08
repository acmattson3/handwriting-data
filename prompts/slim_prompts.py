''' slim_prompts
Simple script to make a file containing a subset of
another file's prompts.
'''

if __name__=="__main__":
    orig_prompts = []
    with open("writing_prompts_orig.txt", "r") as f:
        orig_prompts = f.readlines()
    with open("slimmed_prompts.txt", "w") as new:
        for i, line in enumerate(orig_prompts):
            if i % 6 == 0:
                new.write(line)

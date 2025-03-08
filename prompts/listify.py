with open("writing_prompts_orig.txt", "r") as f:
    prompts = []
    for prompt in f.readlines():
        prompts.append(prompt[:-1])
    with open("listified.txt", "w") as nf:
        nf.write(str(prompts))

print("# prompts:", len(prompts))

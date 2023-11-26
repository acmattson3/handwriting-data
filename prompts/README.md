# Preparing Data

With the default configurations, preparing your handwriting data for synthesis is as easy as running prepare_data.py. Currently, this program disregards the writer's ID, and as such, all data will be lumped into one training set as if one writer is responsible. Assuming you fit this assumption (i.e., you wrote all of your data), you're good to go.

## Working with the data
Once you run the file, a new directory called "processed" will appear in this directory. This new directory will contain the data you need to place in the data directory in the [handwriting synthesis AI repository](https://github.com/sjvasquez/handwriting-synthesis) that you should have cloned somewhere. The Dockerfile in this directory provides an easy way to run the handwriting synthesis AI. Run the docker image this dockerfile generates and open the container interactively and you will have a fully working handwriting-synthesis repository. As stated, the "processed" directory needs to be copied into the data directory of the handwriting synthesis AI. Do so by running the following command from within the directory this README is placed in:

```
docker cp processed/. your_container_id:/root/handwriting-synthesis/data/processed
```

If more detailed instructions are requested, this README file will be updated later to include them.

## Modifying Handwriting Synthesis
I am currently (as of 11/14/23) struggling to get the handwriting synthesis training to work on GPU with my data, but I did successfully get it working on CPU. Two changes must be made to the source code files:

First, in data_frame.py, add this line:
```python
...
def batch_generator(self, batch_size, shuffle=True, num_epochs=10000, allow_smaller_final_batch=False):
    allow_smaller_final_batch=True # ADD ME
    epoch_num = 0
    while epoch_num < num_epochs:
        if shuffle:
            self.shuffle()
...
```
Next, in tf_base_model.py in the fit function, change the following:
```python
...
def fit(self):
...
                # validation evaluation
                val_start = time.time()
                val_batch_df = next(val_generator)
                val_feed_dict = {
                    getattr(self, placeholder_name, None): data
                    for placeholder_name, data in val_batch_df.items() if hasattr(self, placeholder_name)
                }

                val_feed_dict.update({self.learning_rate_var: self.learning_rate, self.beta1_decay_var: self.beta1_decay})
                if hasattr(self, 'keep_prob'):
                    val_feed_dict.update({self.keep_prob: 1.0})
                if hasattr(self, 'is_training'):
                    val_feed_dict.update({self.is_training: False})

                vals=[] # ADD ME
                for val in self.metrics.values(): # ADD ME
                    vals.append(val) # ADD ME
                results = self.session.run(
                    fetches=[self.loss] + vals, # CHANGE ME
                    feed_dict=val_feed_dict
                )
                val_loss = results[0]
```

After these changes have been made, make sure to delete the contents of the checkpoints directory, and then you can successfully train the AI on your handwriting data! 

This solution is a little crude, but it works, and is how I trained the AI on my handwriting data. Below is an example of what happens when you give the AI too little data. This is supposed to say:

```
Now this is a story all about how
My life got flipped turned upside down
And I'd like to take a minute, just sit right there
I'll tell you how I became the prince of a town called Bel-Air
```

Here is what the AI came up with:

![usage_demo](https://github.com/acmattson3/handwriting-data/assets/112522139/a2a75355-0784-46aa-858c-703b41025f7f)

The AI nails the general shape of my sentences, and even copies my tendency to write sentences on wavy lines. With the little data I gave it, though, it fails to reproduce the actual words. It even fails to reproduce the general length or shape of the words, let alone the letters. All this means for me is that I have more writing to do!

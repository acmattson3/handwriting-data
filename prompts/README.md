# Preparing Data

With the default configurations, preparing your handwriting data for synthesis is as easy as running prepare_data.py. Currently, this program disregards the writer's ID, and as such, all data will be lumped into one training set as if one writer is responsible. Assuming you fit this assumption (i.e., you wrote all of your data), you're good to go.

## Working with the data
Once you run the file, a new directory called "processed" will appear in this directory. This new directory will contain the data you need to place in the data directory in the [handwriting synthesis AI repository](https://github.com/sjvasquez/handwriting-synthesis) that you should have cloned somewhere. The Dockerfile in this directory provides an easy way to run the handwriting synthesis AI. Run the docker image this dockerfile generates and open the container interactively and you will have a fully working handwriting-synthesis repository. As stated, the "processed" directory needs to be copied into the data directory of the handwriting synthesis AI. Do so by running the following command from within the directory this README is placed in:

```
docker cp processed/. your_container_id:/root/handwriting-synthesis/data/processed
```

If more detailed instructions are requested, this README file will be updated later to include them.

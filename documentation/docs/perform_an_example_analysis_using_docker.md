# DOCKER IMAGE

Another way to distribute packages is using Docker. Docker is a service that deliver software
in so called containers. All containers have their own libraries and packages.

A Docker container has inside all dependencies and applications. This increase
the reproducibility of a specific analysis.
In this example all the tools required for the analysis are inside the image that will be generated.

In order to start the analysis you can build the image from the Dockerfile or you can
pull it.

1) Build the image using the Dockerfile.

The Dockerfile can be downloaded from ZENODO and then in the same directory
type:

``` bash 
docker build -t grad-seq-analysis:dev .
```

This command builds an image called grad-seq-analysis.

2) You can pull the Docker image by running

```
bash docker pull silviadigiorgio/grad-seq-analysis:latest
```

This command build an image called silviadigiorgio/grad-seq-analysis

In order to avoid root permission when running Docker, 
Singularity can be used.
For this reason, the example analysis provided, is done using singularity.

You can download singularity in [here](https://sylabs.io/guides/3.0/user-guide/installation.html#)

Once you have singularity in your computer you can run this command:

```
singularity build grad-seq-analysis.sif docker://silviadigiorgio/grad-seq-analysis:1.0
```

This will create an image that can be used to perform the analyis.
Before starting the analysis we also recommend to create folders input and output in the main directory.

At the end you will have inside the analysis folder the created image and the two folders

```bash
.
├── grad-seq-analysis.sif
├── input
└── output

```

Now you can start the analysis downloading from ncbi the fastq files from the ncbi server.

``` bash 
for i in            \
    SRR12067299     \
    SRR12067300     \
    SRR12067301     \
    SRR12067302     \
    SRR12067303     \
    SRR12067304     \
    SRR12067305     \
    SRR12067306     \
    SRR12067307     \
    SRR12067308     \
    SRR12067309     \
    SRR12067310     \
    SRR12067311     \
    SRR12067312     \
    SRR12067313     \
    SRR12067314     \
    SRR12067315     \
    SRR12067316     \
    SRR12067317     \
    SRR12067318     \
    SRR12067319     \
    SRR12067320     \
; do 
    fastq-dump --bzip2 $i; 
  done
```

You can download the reference genome and the annotation file from ZENODO.





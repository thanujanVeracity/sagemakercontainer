# sagemakercontainer


For more information, see the Amazon SageMaker Developer Guide sections on [using Docker containers for training](https://docs.aws.amazon.com/sagemaker/latest/dg/your-algorithms.html).

## :hammer_and_wrench: Installation

To install this library in your Docker image, add the following line to your [Dockerfile](https://docs.docker.com/engine/reference/builder/):

``` dockerfile
RUN pip3 install sagemaker-training
```

## :computer: Usage

The following are brief how-to guides.
For complete, working examples of custom training containers built with the SageMaker Training Toolkit, please see [the example notebooks](https://github.com/awslabs/amazon-sagemaker-examples/tree/master/advanced_functionality/custom-training-containers).

### Create a Docker image and train a model

1. Write a training script (eg. `train.py`).

2. [Define a container with a Dockerfile](https://docs.docker.com/get-started/part2/#define-a-container-with-dockerfile) that includes the training script and any dependencies.

    The training script must be located in the `/opt/ml/code` directory.
    The environment variable `SAGEMAKER_PROGRAM` defines which file inside the `/opt/ml/code` directory to use as the training entry point.
    When training starts, the interpreter executes the entry point defined by `SAGEMAKER_PROGRAM`.
    Python and shell scripts are both supported.
    
    ``` docker
    FROM yourbaseimage:tag
  
    # install the SageMaker Training Toolkit 
    RUN pip3 install sagemaker-training

    # copy the training script inside the container
    COPY train.py /opt/ml/code/train.py

    # define train.py as the script entry point
    ENV SAGEMAKER_PROGRAM train.py
    ```

3. Build and tag the Docker image.

    ``` shell
    docker build -t custom-training-container .
    ```

4. Use the Docker image to start a training job using the [SageMaker Python SDK](https://github.com/aws/sagemaker-python-sdk).

    ``` python
    from sagemaker.estimator import Estimator

    estimator = Estimator(image_name="custom-training-container",
                          role="SageMakerRole",
                          train_instance_count=1,
                          train_instance_type="local")

    estimator.fit()
    ```
    
    To train a model using the image on SageMaker, [push the image to ECR](https://docs.aws.amazon.com/AmazonECR/latest/userguide/docker-push-ecr-image.html) and start a SageMaker training job with the image URI.
    

### Pass arguments to the entry point using hyperparameters

Any hyperparameters provided by the training job are passed to the entry point as script arguments.
The SageMaker Python SDK uses this feature to pass special hyperparameters to the training job, including `sagemaker_program` and `sagemaker_submit_directory`.
The complete list of SageMaker hyperparameters is available [here](https://github.com/aws/sagemaker-training-toolkit/blob/master/src/sagemaker_training/params.py).

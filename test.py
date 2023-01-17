from sagemaker.estimator import Estimator

estimator = Estimator(image_uri="custom-training-container",
                      role="SageMakerRole",
                      instance_count=1,
                      instance_type="local")

estimator.fit()



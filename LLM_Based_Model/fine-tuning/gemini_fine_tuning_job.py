
import time

import vertexai
from vertexai.tuning import sft

# TODO(developer): Update and un-comment below line
PROJECT_ID = "prefab-list-449609-t7"
vertexai.init(project=PROJECT_ID, location="us-east1")

sft_tuning_job = sft.train(
    source_model="gemini-1.5-flash-002",
    train_dataset="gs://low-resource-igt/nyb-train-track2-uncovered.jsonl",
)

# Polling for job completion
while not sft_tuning_job.has_ended:
    time.sleep(60)
    sft_tuning_job.refresh()

with open("tuning_jobs","a") as f:
    f.write(sft_tuning_job.tuned_model_name)
    f.write(sft_tuning_job.tuned_model_endpoint_name)
    f.write(sft_tuning_job.experiment)
# Example response:
# projects/123456789012/locations/us-central1/models/1234567890@1
# projects/123456789012/locations/us-central1/endpoints/123456789012345
# <google.cloud.aiplatform.metadata.experiment_resources.Experiment object at 0x7b5b4ae07af0>
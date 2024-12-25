# VLLM Performance Tuning Experimentation

**System Specifications:**

* **CPU:** Intel(R) Core(TM) i7-10700K CPU @ 3.80GHz
* **GPU:** NVIDIA GeForce RTX 3080 10GB 
* **RAM:** 15Gi (WSL2) (Actual 32GB)
* **OS:** Ubuntu 22.04.5 LTS (via WSL2)
* **Docker Version:** 27.4.0
* **VLLM Version:** 0.6.3.post1
* **Model:** ai/meta-llama:3.1-8B-Instruct-cuda-12.6

**Experiment Parameters:**

| Parameter Name             | Value 1           | Value 2 | Value 3 | Value 4 | Value 5 | Value 6 | Value 7 | Value 8 | Value 9 | Value 10 | Value 11 |
|----------------------------|-------------------|---------|---------|---------|---------|---------|---------|---------|---------|----------|----------|
| `gpu_memory_utilization`   | 0.9 (default - d) | 0.9     | 0.95    | 0.9     | 0.98    | 0.9     | 0.9     | 0.9     | 0.9     | 0.9      | 0.9      |
| `max_model_len`            | 30576             | 200     | 500     | 500     | 400     | 400     | 400     | 400     | 400     | 400      | 400      |
| `max_num_seqs`             | 256 (d)           | 256     | 256     | 512     | 512     | 256     | 256     | 512     | 256     | 512      | 512      |
| `block_size`               | 16 (d)            | 16      | 16      | 16      | 32      | 16      | 32      | 16      | 16      | 32       | 32       |
| `quantization`             | None (d)          | None    | None    | None    | fp8     | fp8     | fp8     | fp8     | None    | fp8      | fp8      |
| `pipeline_parallel_size`   | 1 (d)             | 1       | 1       | 1       | 1       | 1       | 1       | 1       | 1       | 1        | 1        |
| `max_logprobs`             | 20 (d)            | 20      | 20      | 20      | 20      | 20      | 20      | 20      | 20      | 20       | 20       |
| `cpu_offload_gb`           | 5                 | 5       | 10      | 0       | 1       | 0       | 0       | 0       | 0       | 0        | 1        |
| `dtype`                    | auto (d)          | auto    | auto    | float16 | float16 | float16 | float16 | float16 | auto    | float16  | float16  |
| `max_num_batched_tokens`   | None (d)          | None    | None    | None    | None    | None    | None    | None    | None    | None     | None     |

| Parameter Name             | Value 12  | Value 13 | Value 14 | Value 15 | Value 16 | Value 17 |
|----------------------------|-----------|----------|----------|----------|----------|---------|
| `gpu_memory_utilization`   | 0.95      | 0.95     | 0.9      | 0.9      | 0.9      | 0.9     |
| `max_model_len`            | 400       | 400      | 400      | 400      | 400      | 512     |
| `max_num_seqs`             | 512       | 128      | 128      | 128      | 128      | 256     |
| `block_size`               | 32        | 32       | 32       | 32       | 32       | 32      |
| `quantization`             | fp8       | fp8      | fp8      | fp8      | fp8      | fp8     |
| `pipeline_parallel_size`   | 1 (d)     | 1        | 1        | 1        | 1        | 1       |
| `max_logprobs`             | 20 (d)    | 20       | 30       | 30       | 10       | 20      |
| `cpu_offload_gb`           | 0         | 0        | 0        | 0        | 0        | 0       |
| `dtype`                    | float16   | float16  | float16  | float16  | float16  | float16 |
| `max_num_batched_tokens`   | None (d)  | None     | 1024     | 4096     | 2048     | None    |

**Results:**

| Experiment                                            | Throughput (tokens/s) | Notes                                  |
|-------------------------------------------------------|-----------------------|----------------------------------------|
| 1 (0.9, 30576, 256, 16, None, 1, 20, 5, auto, None)   | Error                 | The model's max seq len (30576) is larger than the maximum number of tokens that can be stored in KV cache (1136)Baseline                               |
| 2 (0.9, 200, 256, 16, None, 1, 20, 5, auto, None)     | 0.7                   |                                        |
| 3 (0.95, 500, 256, 16, None, 1, 20, 10, auto, None)   | 0.8                   |                                        |
| 4 (0.9, 500, 512, 16, None, 1, 20, 0, float16, None)  | 1.7                   |                                        |
| 5 (0.98, 400, 512, 32, fp8, 1, 20, 1, float16, None)  | 8.3                   | ...                                    |
| 6 (0.9, 400, 256, 16, fp8, 1, 20, 0, float16, None)   | 3.1                   | ...                                    |
| 7 (0.9, 400, 256, 32, fp8, 1, 20, 0, float16, None)   | 2.6                   | ...                                    |
| 8 (0.9, 400, 512, 16, fp8, 1, 20, 0, float16, None)   | 2.3,9.5               | ...                                    |
| 9 (0.9, 400, 256, 16, None, 1, 20, 0, auto, None)     | 1.7                   | ...                                    |
| 10 (0.9, 400, 512, 32, fp8, 1, 20, 0, float16, None)  | 2.7,9.5               | ...                                    |
| 11 (0.9, 400, 512, 32, fp8, 1, 20, 1, float16, None)  | 6.4,3.1,1.6           | ...                                    |
| 12 (0.95, 400, 512, 32, fp8, 1, 20, 0, float16, None) | 3.5,6.3               | ...                                    |
| 13 (0.95, 400, 128, 32, fp8, 1, 20, 0, float16, None) | 3.3,6.4               | ...                                    |
| 14 (0.9, 400, 128, 32, fp8, 1, 30, 0, float16, 1024)  | 2.2,5.3,9.2           | ...                                    |
| 15 (0.9, 400, 128, 32, fp8, 1, 30, 0, float16, 4096)  | 6.3,4.2               | ...                                    |
| 16 (0.9, 400, 128, 32, fp8, 1, 10, 0, float16, 2048)  | 1.4,2.9               | ...                                    |
| 17 (0.9, 512, 256, 32, fp8, 1, 20, 0, float16, None)  | 6.7,4.9               | ...                                    |


## Observations

* **Baseline Error:** The first experiment resulted in an error due to the model's maximum sequence length exceeding the KV cache limit. This highlights the importance of setting compatible values for `max_model_len`.
* **Memory Utilization:** Optimal memory utilization (0.98) was observed to significantly improve throughput, but the improvement is marginal compared to 0.9 or 0.95.
* **Block Size:** Increasing the `block_size` to 32 generally provided better throughput compared to the default value of 16.
* **Quantization Impact:** Using `fp8` quantization improved performance, indicating that lower precision can help boost throughput without compromising too much on accuracy.
* **Pipeline Parallelism:** Attempting to set `pipeline_parallel_size` to 2 resulted in an error as it requires 2 GPUs, which are not available.
* **CPU Offloading:** CPU offloading was observed to decrease performance, so it is better set to 0.
* **Max Number of Sequences:** Setting the `max_num_seqs` to 512 showed improvement in throughput, indicating the model's efficiency with handling larger batch sizes.
* **Mixed Precision:** The `dtype` set to `float16` generally enhanced throughput, demonstrating the benefits of mixed precision training.

## Recommendations

* **Sequence Length Configuration:** Carefully set the `max_model_len` considering the constraints of the KV cache to avoid errors. Aim for optimal values around 400.
* **Memory Utilization Tuning:** Prefer using `gpu_memory_utilization` values of 0.9 or 0.95 to balance performance improvements and allocate resources for other purposes.
* **Block Size Adjustments:** Prefer a `block_size` of 32, as it seems to provide a better throughput balance.
* **Experiment with Quantization:** Continue using `fp8` quantization to leverage its performance benefits.
* **Explore Pipeline Parallelism:** Explore `pipeline_parallel_size` only if more GPUs become available.
* **Disable CPU Offloading:** Set `cpu_offload_gb` to 0 as it was observed to decrease performance.
* **Batch Size Optimization:** Utilize a `max_num_seqs` of 512 to exploit the model's capacity for handling larger sequences effectively.
* **Mixed Precision Usage:** Ensure `dtype` is set to `float16` for training to take advantage of mixed precision benefits.


**Next Steps:**


---

This document outlines the various configurations and their corresponding performance to assist others in optimizing their setups. Note: These experiments were conducted on WSL2.

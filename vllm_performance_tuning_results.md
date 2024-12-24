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

| Parameter Name             | Value 1           | Value 2 | Value 3 | Value 4 | Value 5 | Value 6 | Value 7 | Value 8 | Value 9 | Best Value |
|----------------------------|-------------------|---------|---------|---------|---------|---------|---------|---------|---------|------------|
| `gpu_memory_utilization`   | 0.9 (default - d) | 0.9     | 0.95    | 0.9     | 0.98    | 0.9     | 0.9     | 0.9     | 0.9     |            |
| `max_model_len`            | 30576             | 200     | 500     | 500     | 400     | 400     | 400     | 400     | 400     |            |
| `max_num_seqs`             | 256 (d)           | 256     | 256     | 512     | 512     | 256     | 256     | 512     | 256     |            |
| `block_size`               | 16 (d)            | 16      | 16      | 16      | 32      | 16      | 32      | 16      | 16      |            |
| `quantization`             | None (d)          | None    | None    | None    | fp8     | fp8     | fp8     | fp8     | None    |            |
| `pipeline_parallel_size`   | 1 (d)             | 1       | 1       | 1       | 1       | 1       | 1       | 1       | 1       |            |
| `max_logprobs`             | 20 (d)            | 20      | 20      | 20      | 20      | 20      | 20      | 20      | 20      |            |
| `cpu_offload_gb`           | 5                 | 5       | 10      | 0       | 1       | 0       | 0       | 0       | 0       |            |
| `dtype`                    | auto (d)          | auto    | auto    | float16 | float16 | float16 | float16 | float16 | auto    |            |
| `max_num_batched_tokens`   | None (d)          | None    | None    | None    | None    | None    | None    | None    | None    |            |



**Results:**

| Experiment                                           | Throughput (tokens/s) | Notes                                  |
|------------------------------------------------------|-----------------------|----------------------------------------|
| 1 (0.9, 30576, 256, 16, None, 1, 20, 5, auto, None)  | Error                 | The model's max seq len (30576) is larger than the maximum number of tokens that can be stored in KV cache (1136)Baseline                               |
| 2 (0.9, 200, 256, 16, None, 1, 20, 5, auto, None)    | 0.7                   | |
| 3 (0.95, 500, 256, 16, None, 1, 20, 10, auto, None)  | 0.8                   |  |
| 4 (0.9, 500, 512, 16, None, 1, 20, 0, float16, None) | 1.7                   |  |
| 5 (0.98, 400, 512, 32, fp8, 1, 20, 1, float16, None) | 8.3                   | ...             |
| 6 (0.9, 400, 256, 16, fp8, 1, 20, 0, float16, None)  | 3.1                   | ...             |
| 7 (0.9, 400, 256, 32, fp8, 1, 20, 0, float16, None)  | 2.6                   | ...             |
| 8 (0.9, 400, 512, 16, fp8, 1, 20, 0, float16, None)  | 2.3,9.5               | ...             |
| 9 (0.9, 400, 256, 16, None, 1, 20, 0, auto, None)    | 1.7                   | ...             |

**Observations:**



**Recommendations:**



**Next Steps:**


---

This document outlines the various configurations and their corresponding performance to assist others in optimizing their setups. Note: These experiments were conducted on WSL2.

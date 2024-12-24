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

| Parameter Name        | Value 1 | Value 2 | Value 3 | ... | Best Value |
|-----------------------|--------|--------|--------|-----|------------|
| `gpu_memory_utilization` | 0.95   | 0.98   | 0.99   | ... | 0.98       |
| `max_model_len`        | 500    | 400    | 350    | ... | 400        |
| `max_num_seqs`         | 256    | 512    | 1024   | ... | 512        |
| `block_size`           | 16     | 32     | 64     | ... | 32         |
| `quantization`         | fp8    | bfloat16 | fp16   | ... | fp8        |
| `pipeline_parallel_size` | 1    | 2      | 4      | ... | 2          | 
| ...                   | ...    | ...    | ...    | ... | ...        |

**Results:**

| Experiment                              | Throughput (tokens/s) | Notes                                  |
|-----------------------------------------|-----------------------|----------------------------------------|
| 1 (0.95, 500, 256, 16, fp8, 1)          | 1.7                   | Baseline                               |
| 2 (0.98, 400, 512, 32, fp8, 1)          | 3.8                   | Improved with higher memory utilization|
| 3 (0.98, 400, 512, 32, fp8, 2)          | 4.1                   | Further optimized with pipeline parallelism |
| 4 (0.98, 400, 512, 32, fp8, 2)          | **4.5**               | Best performance with current parameters |
| ...                                     | ...                   | ...                                    |

**Observations:**

* [Add your observations here. For example: "Increasing `gpu_memory_utilization` initially improved performance, but further increases led to instability. Pipeline parallelism provided a significant boost in throughput."]

**Recommendations:**

* [Summarize your findings and recommendations. For example: "Based on these results, we recommend using the following parameter combination: `gpu_memory_utilization=0.98`, `max_model_len=400`, `pipeline_parallel_size=2`, ..."]

**Next Steps:**

* [List any further experiments or optimizations you plan to investigate.]

---

This document outlines the various configurations and their corresponding performance to assist others in optimizing their setups. Note: These experiments were conducted on WSL2.


# AdaServe: Multi-SLO LLM Serving with Speculative Decoding

## 1. Project Overview

This project implements a prototype inspired by AdaServe,
which explores speculative decoding for Large Language Model serving.

A smaller draft model proposes tokens, and a larger target model
verifies those tokens.

## 2. Models Used

- Draft model: Qwen2.5-0.5B-Instruct
- Target model: Qwen2.5-1.5B-Instruct

## 3. Implementation

- Model loading and inference
- Speculative decoding
- SLO configuration
- SLO-based token allocation prototype
- Throughput allocation prototype
- Performance evaluation
- Speculation depth comparison

## 4. Experimental Environment

- Google Colab
- NVIDIA Tesla T4 GPU
- PyTorch
- Hugging Face Transformers

## 5. Experimental Results

Baseline average latency: 2.574 seconds

| Depth | Speculative Latency |
|-------|---------------------|
| 2     | 4.482 seconds       |
| 4     | 3.780 seconds       |
| 6     | 3.742 seconds       |
| 8     | 3.752 seconds       |

Best tested speculative depth: 6

All tested speculative outputs matched the baseline outputs.

## 6. Limitations

- This is a prototype, not a complete reproduction of AdaServe.
- Smaller Qwen models were used due to GPU limitations.
- The original A100 and FlexFlow Serve environment was not reproduced.
- Speculative decoding was slower than baseline in these experiments.
- The SLO and throughput allocation components are simplified prototypes.

## 7. Conclusion

The prototype demonstrates speculative token generation,
target-model verification, and speculation-depth evaluation.

Depth 6 achieved the lowest average latency among the tested
speculative configurations. However, normal cached generation
remained faster in this experimental setup.

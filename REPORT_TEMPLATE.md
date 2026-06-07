# CSC4005 Lab 7 Report – Compression: KD + Quantization Trade-offs

## 1. Thông tin

- Họ tên: [Nguyễn Trung Thành]
- Mã sinh viên: [1771040022]
- Lớp: [KHMT_17_01]
- Link GitHub repo: [Nhập link repo]
- Kỹ thuật chọn: **Quantization**
- Link W&B nếu dùng KD: [Không áp dụng]
- Link model nếu không commit trực tiếp: models/vit_smartcampus_dynamic_int8.onnx

## 2. Mô tả baseline model

| Nội dung | Giá trị |
|---|---|
| Bài toán | Smart Campus Scene Classification |
| Dataset | MIT Indoor Scenes 67 subset |
| Số lớp | 5 |
| Baseline model | ViT B/16 (Vision Transformer) |
| Baseline format | PyTorch / ONNX |
| Baseline checkpoint/ONNX | checkpoints/best_model.pt / models/vit_smartcampus.onnx |
| Baseline model size | 327.39 MB |

## 3. Kỹ thuật nén đã chọn

### Nếu chọn Quantization

| Thông tin | Giá trị |
|---|---|
| Loại quantization | Dynamic |
| Input model | models/vit_smartcampus.onnx |
| Output model | models/vit_smartcampus_dynamic_int8.onnx |
| Dạng dữ liệu sau nén | INT8 (QInt8) |
| Công cụ | onnxruntime.quantization |

Mô tả ngắn:

```text
Dynamic quantization là kỹ thuật chuyển đổi trọng số (weights) của mô hình từ
FP32 sang INT8 (QInt8) mà không cần calibration data hay inference lại. Chỉ các
layer tích chập (MatMul, Gemm) được quantize, phép tính quantized được thực hiện
động tại runtime. Kỹ thuật này nhanh, đơn giản, và phù hợp để deploy trên CPU
hoặc server mà không cần GPU.

Lợi ích:
- Giảm 74.73% kích thước model (327 MB -> 83 MB)
- Tăng 70.57% throughput (9.50 -> 16.21 img/s)
- Giảm 41.37% latency (105.24 ms -> 61.70 ms)
- Chỉ mất 0.38% accuracy và 0.53% macro-F1
```

### Nếu chọn Knowledge Distillation

| Thông tin | Giá trị |
|---|---|
| Teacher model | ... |
| Student model | ... |
| alpha | ... |
| temperature | ... |
| epochs | ... |
| batch size | ... |
| optimizer | ... |

Công thức loss sử dụng:

```text
loss = alpha * CE(student_logits, labels) + (1 - alpha) * KD_loss(student_logits, teacher_logits, T)
```

## 4. Kết quả đánh giá

| Model | Accuracy | Macro-F1 | Model size (MB) |
|---|---:|---:|---:|
| Baseline | 98.35% | 97.78% | 327.39 |
| Compressed | 97.97% | 97.25% | 82.72 |

Nhận xét:

- **Accuracy giảm:** 0.38% (từ 98.35% xuống 97.97%)
- **Macro-F1 giảm:** 0.53% (từ 97.78% xuống 97.25%)
- **Mức giảm này có chấp nhận được không?** Có, vì:
  - Mức mất mát rất nhỏ (< 1%), accuracy vẫn đạt 97.97% - rất cao cho bài toán phân loại 5 lớp
  - Trong bối cảnh triển khai thực tế, chênh lệch 0.38% là không đáng kể
  - Đặc biệt khi so với lợi ích: model nhẹ hơn 4 lần và nhanh hơn 41%

## 5. Kết quả benchmark

| Model | Batch size | Mean latency (ms) | P95 latency (ms) | Throughput (img/s) | Size (MB) |
|---|---:|---:|---:|---:|---:|
| Baseline | 1 | 105.24 | 107.82 | 9.50 | 327.39 |
| Compressed | 1 | 61.70 | 72.72 | 16.21 | 82.72 |
| Baseline | 4 | - | - | - | - |
| Compressed | 4 | - | - | - | - |
| Baseline | 8 | - | - | - | - |
| Compressed | 8 | - | - | - | - |

Ghi chú: Model ONNX được export với batch_size cố định = 1 nên chỉ benchmark được với bs=1. Các batch size 4 và 8 không khả dụng.

## 6. Bảng trade-off

| Model | Accuracy | Macro-F1 | Mean latency @bs=1 | Throughput @bs=1 | Size | Nhận xét |
|---|---:|---:|---:|---:|---:|---|
| Baseline | 98.35% | 97.78% | 105.24 ms | 9.50 img/s | 327.39 MB | Mô hình đầy đủ, độ chính xác cao nhất |
| Compressed | 97.97% | 97.25% | 61.70 ms | 16.21 img/s | 82.72 MB | Nhẹ hơn 4 lần, nhanh hơn 41%, mất 0.38% accuracy |

## 7. Phân tích

Trả lời:

1. **Mô hình sau nén nhỏ hơn bao nhiêu phần trăm?**
   - Nhỏ hơn **74.73%** (từ 327.39 MB xuống 82.72 MB), tương đương giảm **4 lần** về kích thước.

2. **Latency giảm hay tăng?**
   - Latency **giảm** rõ rệt: từ 105.24 ms xuống 61.70 ms, giảm **41.37%**.

3. **Throughput thay đổi thế nào?**
   - Throughput **tăng** từ 9.50 img/s lên 16.21 img/s, tăng **70.57%**, nghĩa là xử lý được nhiều ảnh hơn trong cùng thời gian.

4. **Accuracy/F1 giảm nhiều không?**
   - Không nhiều: accuracy chỉ giảm **0.38%** (98.35% -> 97.97%), macro-F1 giảm **0.53%** (97.78% -> 97.25%). Mức mất mát rất nhỏ, hoàn toàn có thể chấp nhận được.

5. **Nếu triển khai trên CPU hoặc edge device, bạn có chọn compressed model không?**
   - **Có**, vì:
     - Model nhẹ hơn 4 lần, dễ triển khai trên các hệ thống có bộ nhớ hạn chế
     - Latency nhanh hơn 41%, phù hợp với yêu cầu real-time inference
     - Accuracy vẫn đạt 97.97% - rất cao cho bài toán Smart Campus
     - Không cần GPU, chỉ cần CPU là chạy được

6. **Nếu không chọn, lý do là gì?**
   - Không có lý do để không chọn compressed model trong trường hợp này. Trade-off rất có lợi: lợi ích về kích thước và tốc độ lớn hơn nhiều so với mức mất mát accuracy rất nhỏ.

## 8. Khi nào chọn KD, khi nào chọn Quantization?

Viết nhận xét ngắn:

- **Khi nào quantization phù hợp?**
  - Khi đã có model train tốt và không muốn train lại
  - Khi cần giảm kích thước model nhanh chóng
  - Khi triển khai trên CPU hoặc server (không cần GPU mạnh)
  - Khi chấp nhận được mức mất mát accuracy nhỏ (< 2-3%)
  - Khi không có thời gian hoặc tài nguyên để train lại model

- **Khi nào KD phù hợp?**
  - Khi cần model nhỏ hơn rất nhiều lần (VD: từ 300MB xuống 5-10MB)
  - Khi muốn thay đổi kiến trúc model hoàn toàn (VD: từ ViT sang MobileNet)
  - Khi có GPU để train student model
  - Khi cần kiểm soát sự mất mát accuracy một cách chủ động thông qua alpha và temperature
  - Khi ứng dụng cần model chạy trên thiết bị edge rất hạn chế tài nguyên

- **Nếu được làm lại, bạn sẽ chọn kỹ thuật nào cho hệ thống Smart Campus?**
  - Vẫn chọn **Quantization** cho hệ thống Smart Campus trong trường hợp này vì:
    - Đã có ViT model train tốt, không cần train lại
    - Quantization cho kết quả tốt với trade-off rất có lợi (4x nhẹ, 1.7x nhanh, < 0.5% mất accuracy)
    - Không cần GPU, dễ triển khai trên server trường học
    - Nếu cần model nhỏ hơn nữa cho edge device (< 20MB), có thể cân nhắc thêm KD

## 9. Kết luận

Tóm tắt:

- **Kỹ thuật nén đã dùng:** Dynamic Quantization (FP32 → INT8/QInt8) sử dụng `onnxruntime.quantization.quantize_dynamic`. Kỹ thuật này quantize hóa trọng số của mô hình mà không cần calibration data, phù hợp để deploy nhanh trên CPU.

- **Kết quả chính:**
  - Model size: 327.39 MB → 82.72 MB (giảm **74.73%**)
  - Latency: 105.24 ms → 61.70 ms (giảm **41.37%**)
  - Throughput: 9.50 → 16.21 img/s (tăng **70.57%**)
  - Accuracy: 98.35% → 97.97% (mất **0.38%**)
  - Macro-F1: 97.78% → 97.25% (mất **0.53%**)

- **Trade-off quan trọng nhất:** Compression ratio rất cao (4 lần) kết hợp với latency giảm 41% nhưng chỉ mất 0.38% accuracy - đây là một trade-off rất có lợi cho triển khai thực tế. Dynamic quantization đặc biệt hiệu quả với model ONNX ViT vì phần lớn kích thước nằm ở các layer MatMul và Gemm - các layer được quantize hiệu quả nhất.

- **Bài học rút ra:**
  1. Không phải lúc nào model nhỏ hơn cũng tốt hơn - cần cân bằng giữa accuracy, latency và kích thước
  2. Quantization là cách nén nhanh và hiệu quả khi đã có model tốt sẵn
  3. Luôn đánh giá lại accuracy sau quantization vì kết quả phụ thuộc vào phần cứng và phần mềm
  4. Với Smart Campus, quantization là lựa chọn tối ưu để deploy ViT trên CPU với hiệu suất cao

# TỔNG HỢP TOÀN BỘ NỘI DUNG CHI TIẾT TỪ HAI BÀI BÁO KHOA HỌC

Tài liệu này ghi chép lại **toàn bộ nội dung, công thức toán học, kiến trúc mô hình, thuật toán, bộ câu lệnh (prompts), bảng số liệu thực nghiệm, biểu đồ, nghiên cứu cắt bỏ (ablation study), nghiên cứu tình huống (case study), hạn chế và phụ lục** được đọc và trích xuất chi tiết từ hai bài báo trong thư mục `docs/`:

1. **Bài báo 1 (`docs/2025.acl-long.85.pdf`):** *Open-World Attribute Mining for E-Commerce Products with Multimodal Self-Correction Instruction Tuning (MSIT)* — Hội nghị ACL 2025 (Volume 1: Long Papers, trang 1702–1714).
2. **Bài báo 2 (`docs/3746027.3754591.pdf`):** *Entity Graph Alignment and Visual Reasoning for Multimodal Fake News Detection (CMA-VRP)* — Hội nghị ACM Multimedia 2025 (MM '25, trang 2486–2495).

---

# PHẦN I: NỘI DUNG TOÀN DIỆN BÀI BÁO 1 — MSIT (ACL 2025)

## 1. Thông tin chung (Metadata)

- **Tiêu đề gốc:** *Open-World Attribute Mining for E-Commerce Products with Multimodal Self-Correction Instruction Tuning*
- **Tên viết tắt khung phương pháp:** **MSIT** (*Multimodal Self-Correction Instruction Tuning*)
- **Hội nghị công bố:** *Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)*, trang 1702–1714, diễn ra từ ngày 27/07 đến 01/08/2025. Bản quyền ©2025 Association for Computational Linguistics.
- **Nhóm tác giả và đơn vị công tác:**
  - **Jiaqi Li**$^{1,3*}$ (`jqli@seu.edu.cn`) — Đồng tác giả đầu (*Co-first author*)
  - **Yanming Li**$^{1,3*}$ (`liyanming@seu.edu.cn`) — Đồng tác giả đầu (*Co-first author*)
  - **Xiaoli Shen**$^{3,4}$ (`220232260@seu.edu.cn`)
  - **Chuanyi Zhang**$^{2}$ (`20231104@hhu.edu.cn`)
  - **Guilin Qi**$^{3,4\dagger}$ (`gqi@seu.edu.cn`) — Tác giả liên hệ (*Corresponding author*)
  - **Sheng Bi**$^{5}$ (`shengbi@seu.edu.cn`)
- **Đơn vị trực thuộc:**
  1. School of Cyber Science and Engineering, Southeast University, Nanjing, China (Trường Khoa học và Kỹ thuật Không gian mạng, Đại học Đông Nam, Nam Kinh, Trung Quốc).
  2. College of Artificial Intelligence and Automation, Hohai University, Nanjing, China (Trường Trí tuệ Nhân tạo và Tự động hóa, Đại học Hà Hải, Nam Kinh, Trung Quốc).
  3. Key Laboratory of New Generation Artificial Intelligence Technology and Its Interdisciplinary Applications (Southeast University), Ministry of Education, China (Phòng thí nghiệm Trọng điểm về Công nghệ AI Thế hệ mới và Ứng dụng Liên ngành, Bộ Giáo dục Trung Quốc).
  4. School of Computer Science and Engineering, Southeast University, Nanjing, China (Trường Khoa học và Kỹ thuật Máy tính, Đại học Đông Nam).
  5. Law and Innovation Lab, School of Law, Southeast University (Phòng thí nghiệm Luật và Đổi mới sáng tạo, Trường Luật, Đại học Đông Nam).

---

## 2. Tóm tắt (Abstract) và Đặt vấn đề (Introduction)

### 2.1. Nội dung phần Tóm tắt (Abstract)

- **Bối cảnh:** Trong thương mại điện tử (e-commerce), việc Khai thác Thuộc tính Sản phẩm (*Product Attribute Mining - AM*) hiệu quả đóng vai trò thiết yếu nhằm làm giàu đặc trưng sản phẩm và hỗ trợ người tiêu dùng đưa ra quyết định mua sắm.
- **Vấn đề hiện tại:** Các phương pháp AM hiện hành thường chỉ tập trung trích xuất thuộc tính từ văn bản đơn phương thức (*unimodal text*), chưa tận dụng hết dữ liệu đa phương thức (*multimodal data*).
- **Giải pháp đề xuất:** Bài báo đề xuất khung phương pháp mới mang tên **Multimodal Self-Correction Instruction Tuning (MSIT)** để khai thác các thuộc tính tiềm năng mới từ cả hình ảnh và văn bản bằng cách sử dụng các Mô hình Ngôn ngữ Lớn Đa phương thức (*Multimodal Large Language Models - MLLMs*).
- **Quy trình tinh chỉnh (Tuning process) gồm 2 bộ dữ liệu:**
  1. **Attribute Generation Tuning Data (AGTD):** Được xây dựng bằng kỹ thuật học trong ngữ cảnh (*In-Context Learning - ICL*) với một tập nhỏ thuộc tính hạt giống (*seed attributes*), giúp MLLM trích xuất chính xác các cặp thuộc tính - giá trị (*attribute-value pairs*) từ thông tin đa phương thức.
  2. **Chain-of-Thought Tuning Data (CTTD):** Nhằm đưa suy luận tường minh (*explicit reasoning*) vào mô hình và nâng cao độ chính xác trích xuất, CTTD kết hợp một quy trình suy luận 5 bước có cấu trúc (*structured 5-step reasoning process*) để tự sửa lỗi (*self-correction*).
- **Quy trình suy luận (Inference process) gồm 3 giai đoạn (3-stage inference):** Lọc bỏ các thuộc tính dư thừa/trùng lặp (*redundant attributes*) và xác thực tuần tự (*sequentially validate*) từng thuộc tính được sinh ra.
- **Kết quả:** Các thực nghiệm toàn diện trên 2 bộ dữ liệu (WOAM và OAMine mở rộng đa phương thức) chứng minh MSIT vượt trội hơn hẳn các phương pháp tiên tiến nhất (*state-of-the-art - SOTA*).

### 2.2. Nội dung phần Giới thiệu (Section 1 — Introduction)

- **Vai trò của thuộc tính sản phẩm:** Thuộc tính sản phẩm làm phong phú các điểm bán hàng (*selling points*), giúp người tiêu dùng ra quyết định sáng suốt (Xu et al., 2019; Yan et al., 2021; Shinzato et al., 2023). Tuy nhiên, do sự xuất hiện liên tục của các sản phẩm mới, các sàn thương mại điện tử thường xuyên đối mặt với tình trạng dữ liệu thuộc tính bị thiếu hụt hoặc không đầy đủ.
- **Bài toán Khai thác Thuộc tính Sản phẩm Thế giới Mở (*Open-World Product Attribute Mining - AM*):** (Zhang et al., 2022; Xu et al., 2023) Giải quyết nhu cầu trên bằng cách trích xuất các thuộc tính tiềm năng mới từ hồ sơ sản phẩm (*product profiles*) mà không bị bó buộc trong một lược đồ cố định trước.
- **Hai hạn chế lớn của các công trình hiện có (Minh họa tại Hình 1 trang 1702):**
  1. **Chưa tận dụng đầy đủ thông tin đa phương thức (*Underutilization of multimodal information*):**
     - Các phương pháp gần đây (Zhang et al., 2022; Xu et al., 2023) chỉ dựa vào dữ liệu văn bản (mô tả hoặc tiêu đề sản phẩm).
     - Tuy nhiên, hình ảnh sản phẩm cung cấp nhiều thuộc tính giá trị. Như minh họa ở **Hình 1(a)** và **Hình 1(c)** với sản phẩm bột trà xanh *"Organic Matcha Green Tea; Japanese Everyday Drink | 100% Pure Culinary Grade | Sugar Free, Eco-friendly Bag..."*: các mô hình ngôn ngữ tiền huấn luyện (PLM) chỉ dùng văn bản sẽ trích xuất được `{"Tea_Type": "Green", "Sugar": "Sugar-free"}` nhưng bỏ lỡ các thuộc tính quan trọng hiển thị rõ trên bao bì trong ảnh như hình dạng sản phẩm (`"Product_shape": "Powder"`) và trọng lượng (`"Weight": "1lb"`).
  2. **Thiếu vắng quá trình suy luận tường minh (*Absence of explicit reasoning*):**
     - Các công trình đời đầu (Ghani et al., 2006; Zheng et al., 2018a; Mehta et al., 2021; Fu et al., 2022) coi AM là bài toán phân loại (*classification task*).
     - Các nghiên cứu gần đây hơn (Zou et al., 2024; Shinzato et al., 2023; Zhang et al., 2023b; Li et al., 2023b; Chen, 2024; Khandelwal et al., 2023) dùng mô hình ngôn ngữ sinh (*generative language models*), nhưng thường sinh trực tiếp kết quả mà không có bước suy luận tường minh.
     - Như minh họa ở **Hình 1(b)**, khi đưa ảnh và văn bản vào MLLM thông thường mà không có suy luận tường minh, mô hình có thể trích xuất các thuộc tính sai lệch/không hợp lệ (*Invalid Attributes*) như `"Harvest": "Premium First Harvest"` hoặc `"Marketing Claims": "Calm and clarity"` mà không kiểm chứng tính liên quan hay tính đúng đắn dựa trên ngữ cảnh và tri thức thông thường (*common sense*).
- **Ba đóng góp chính của bài báo:**
  1. Tiên phong trong việc khám phá khai thác thuộc tính tiềm năng bằng MLLM, mở rộng bài toán Attribute Mining sang thiết lập đa phương thức (*multimodal settings*).
  2. Đề xuất một khung phương pháp toàn diện có khả năng khám phá thuộc tính từ cả thông tin văn bản lẫn thị giác, theo sau bởi quy trình suy luận chuỗi tư duy (*Chain-of-Thought - CoT*) 5 bước để tự sửa lỗi các thuộc tính được sinh ra.
  3. Mở rộng 2 bộ dữ liệu đơn phương thức (WOAM và OAMine) thành bộ dữ liệu đa phương thức, và chứng minh tính ưu việt của MSIT qua thực nghiệm trên cả hai bộ dữ liệu.

---

## 3. Các nghiên cứu liên quan (Section 2 — Related Work)

### 3.1. Mô hình Ngôn ngữ Lớn Đa phương thức (Multi-modal Large Language Models)

- **BLIP-2** (Li et al., 2023a): Đạt hiệu năng SOTA trong các tác vụ thị giác - ngôn ngữ bằng cách tận dụng bộ mã hóa ảnh tiền huấn luyện đóng băng (*frozen pre-trained image encoders*), mô hình ngôn ngữ lớn đóng băng và bộ biến đổi truy vấn nhẹ (*lightweight query transformers / Q-Former*).
- **InstructBLIP** (Dai et al., 2023): Cải tiến BLIP-2 bằng cách thực hiện tinh chỉnh theo chỉ dẫn thị giác - ngôn ngữ (*vision-language instruction tuning*), vượt qua mô hình **Flamingo** (Alayrac et al., 2022) trong các tác vụ zero-shot.
- **LLaVA** (Liu et al., 2023): Sử dụng **GPT-4** (OpenAI, 2023) để sinh dữ liệu tuân thủ chỉ dẫn đa phương thức và huấn luyện mô hình quy mô lớn cho việc hiểu ngôn ngữ và thị giác tổng quát.

### 3.2. Khai thác Thuộc tính (Attribute Mining)

- Các nghiên cứu về khai thác thuộc tính sản phẩm trong thương mại điện tử nhận được nhiều sự quan tâm (Shinzato et al., 2022; Karamanolakis et al., 2020; Zheng et al., 2018b):
  - **OpenTag** (Zheng et al., 2018a): Dùng mạng nơ-ron (BiLSTM-CRF + Attention) và học chủ động (*active learning*) để xác định các thuộc tính bị thiếu, nhưng không mở rộng được khung lược đồ thuộc tính (*does not expand attribute frameworks*).
  - **LATEX-Numeric** (Mehta et al., 2021): Trích xuất các thuộc tính số (*numerical attributes*) thông qua giám sát từ xa (*distant supervision*) và học đa tác vụ (*multitask learning*), loại bỏ việc gán nhãn thủ công.
  - **CMA-CLIP** (Fu et al., 2022): Mô hình hóa việc hoàn thiện thuộc tính như bài toán phân loại sử dụng Cross-Modality Attention CLIP, nhưng giả định kịch bản thế giới đóng (*closed-world scenario*).
  - **Các phương pháp sinh (Generative approaches)** (Roy et al., 2021; Xu et al., 2023): Coi hoàn thiện thuộc tính là bài toán mô hình hóa sinh, dùng LLM để sinh giá trị thuộc tính nhưng bị giới hạn ở các danh mục sản phẩm cụ thể và chưa xét đến việc sinh thuộc tính cá nhân hóa/mở rộng đa phương thức.

---

## 4. Phương pháp Đề xuất (Section 3 — Proposed Method)

### 4.1. Phát biểu Bài toán Toán học

- Trong tác vụ Khai thác Thuộc tính Thế giới Mở Đa phương thức (*Multimodal Open-World Attribute Mining*), sản phẩm thứ $i$ được ký hiệu là $\mathcal{P}_i$, bao gồm:
  - Một văn bản (tiêu đề *title* và điểm nổi bật *bullet point*) $\mathcal{T}_i$ gồm $w_i$ token:
    $$\mathcal{T}_i = \left\{s_1^i, s_2^i, \dots, s_{w_i}^i\right\}$$
  - Một hình ảnh sản phẩm $\mathcal{I}_i$.
- **Mục tiêu:** Trích xuất một tập hợp gồm $k$ thuộc tính liên quan và áp dụng được:
  $$\mathcal{A}_i = \{a_1, a_2, \dots, a_k\}$$
  từ đầu vào $(\mathcal{T}_i, \mathcal{I}_i)$, từ các đặc trưng cơ bản (màu sắc, kích thước) đến các thuộc tính phức tạp (chất liệu, kiểu dáng).
- Mỗi thuộc tính $a_m$ tương ứng với một giá trị cụ thể trong tập giá trị:
  $$\mathcal{V}_i = \{v_1, v_2, \dots, v_k\}$$
- **Yêu cầu của thiết lập Thế giới Mở (Open-World setting):** Toàn bộ các thuộc tính cần được trích xuất mà không bị giới hạn trong một lược đồ định sẵn (*not limited to a pre-defined schema*).
- **Định dạng đầu ra thống nhất của MLLM sinh:** Mô hình sinh ra một chuỗi văn bản biểu diễn các cặp thuộc tính và giá trị tương ứng dưới định dạng JSON:
  $$\{a_1 : v_1, a_2 : v_2, \dots, a_k : v_k\}$$

### 4.2. Tổng quan Kiến trúc MSIT (Hình 2 trang 1704)

Khung MSIT được chia thành 3 thành phần chính:

1. **Xây dựng Dữ liệu Tinh chỉnh Sinh Thuộc tính (*Attribute Generation Tuning Data Construction - AGTD*):** Trích xuất riêng biệt thuộc tính từ ảnh và văn bản bằng học trong ngữ cảnh (ICL) với GPT-4, sau đó hợp nhất chúng.
2. **Xây dựng Dữ liệu Tinh chỉnh Chuỗi Tư duy (*Chain-of-Thought Tuning Data Construction - CTTD*):** Hướng dẫn mô hình thực hiện quy trình suy luận 5 bước có cấu trúc trên cả mẫu dương và mẫu âm tương phản.
3. **Suy luận Thuộc tính Sản phẩm (*Product Attribute Inference*):** Sử dụng quy trình 3 giai đoạn (Sinh theo lô $\rightarrow$ Lọc thuộc tính lặp $\rightarrow$ Suy luận tuần tự với CoT 5 bước) trên mô hình MLLM đã được tinh chỉnh bằng LoRA.

---

### 4.3. Mục 3.1: Xây dựng Dữ liệu Tinh chỉnh Sinh Thuộc tính (AGTD)

1. **Bộ dữ liệu thô (Raw Dataset):**
   - Mở rộng 2 bộ dữ liệu đơn phương thức gốc là **WOAM** (Xu et al., 2023) và **OAMine** (Zhang et al., 2022) sang đa phương thức.
   - Bao gồm các ngành hàng thương mại điện tử phổ biến như Trà (*Tea*), Vitamin, Ghế sofa (*Sofa*), và Ốp lưng điện thoại (*Phone Case*).
   - Hình ảnh sản phẩm tương ứng được thu thập trực tiếp từ trang **Amazon.com**.
2. **Bộ dữ liệu hạt giống (Seed Dataset):**
   - Với mỗi loại sản phẩm, tập hạt giống chứa một số loại thuộc tính áp dụng được.
   - Nhóm tác giả xây dựng và gán nhãn thủ công (*manually construct and annotate*) tập dữ liệu hạt giống để đảm bảo tính nhất quán với đặc điểm sản phẩm, đồng thời làm mịn các loại thuộc tính mơ hồ hoặc quá thô (*coarse-grained*) thành các loại thuộc tính chi tiết mới (*fine-grained types*).
3. **Sinh dữ liệu bằng Học trong Ngữ cảnh (In-Context Learning Generation):**
   - Sử dụng **In-Context Learning** (Zhang et al., 2023a) với **GPT-4** (OpenAI, 2023) dựa trên một tập nhỏ thuộc tính và giá trị hạt giống (Prompt chi tiết tại Phụ lục A.1).
   - **Phát hiện quan trọng về Thiên lệch Chú ý Phương thức (*Modality Attention Bias*):** Trong các thử nghiệm ban đầu, nhóm tác giả quan sát thấy nếu đưa cả hình ảnh và văn bản vào GPT-4 cùng một lúc (*simultaneously*), GPT-4 sẽ hầu như chỉ sinh ra các thuộc tính từ thông tin văn bản và bỏ qua hình ảnh.
   - **Giải pháp tách biệt phương thức (*Modality-Separated Generation*):** Để giảm thiểu thiên lệch chú ý phương thức, hình ảnh và mô tả văn bản được đưa vào GPT-4 **riêng biệt** (*separately*) để sinh các thuộc tính tiềm năng (`Attribute From Image` và `Attribute From Text`).
   - **Rà soát thủ công & Hợp nhất (Manual Review & Merging):** Các thuộc tính sinh ra được kiểm duyệt thủ công để lọc bỏ thuộc tính sai, đảm bảo chất lượng cao. Cuối cùng, GPT-4 được sử dụng để hợp nhất (*merge*) các thuộc tính đã lọc từ ảnh và văn bản thành một tập thống nhất (Prompt chi tiết tại Phụ lục A.2).

---

### 4.4. Mục 3.2: Xây dựng Dữ liệu Tinh chỉnh Chuỗi Tư duy (CTTD)

- **Lý do không dùng Vanilla CoT:** Các nghiên cứu gần đây (Zhang et al., 2023c) chỉ ra rằng dạng CoT thông thường (*vanilla CoT*) — cho phép LLM tự do xuất ra quá trình suy luận một cách không phân biệt — sẽ làm giảm hiệu năng do hiện tượng **sinh các lý giải ảo giác (*hallucinated rationales*)**.
- **Giải pháp Quy trình Suy luận 5 bước có cấu trúc (*5-Step Structured Reasoning Process*):** Chia quá trình suy luận thành 5 bước rõ ràng và chỉ định mục tiêu đầu ra cụ thể cho từng bước (Prompt tại Phụ lục A.3):
  - **Bước 1 — Thu hẹp phạm vi loại sản phẩm (*Product Type Range Narrowing*):**
    MLLM xác định loại sản phẩm hiện tại dựa trên hình ảnh và văn bản tương ứng (ví dụ: ốp lưng điện thoại, trà, vitamin,...) nhằm thu hẹp phạm vi các thuộc tính có thể có của sản phẩm, tạo ngữ cảnh cho các bước suy luận tiếp theo.
  - **Bước 2 — Suy luận với Tri thức Thông thường Nội tại (*Reasoning with Internal Common-sense Knowledge*):**
    Sử dụng tri thức thông thường nội tại kết hợp sàng lọc sơ bộ để xác định xem thuộc tính đang xét có áp dụng được cho loại sản phẩm đó không.
    *Ví dụ:* Khi đánh giá thuật ngữ chuyên biệt như `'screen_size'` (kích thước màn hình) có phù hợp với sản phẩm `vitamins` hay không, xét theo ngữ cảnh thông thường là không phù hợp. Ngoài ra, nếu ý nghĩa của thuộc tính không rõ ràng (*unclear*), nó sẽ sơ bộ bị coi là không phù hợp; nếu ý nghĩa rõ ràng, tri thức thông thường sẽ hướng dẫn phán đoán sơ bộ xem thuộc tính có khớp với loại sản phẩm không và giải thích lý do.
  - **Bước 3 — Xác thực Thuộc tính dựa trên Hình ảnh (*Image-Based Attribute Validation*):**
    Đánh giá xem thuộc tính có bắt nguồn từ hình ảnh hay không. Nếu thuộc tính được coi là hợp lệ sau bước sàng lọc ban đầu (Bước 2), mô hình suy luận giá trị thuộc tính ước lượng (*rough attribute value*) từ hình ảnh để xác nhận sự hiện diện của nó (vì ảnh không phải lúc nào cũng cung cấp giá trị chữ viết tường minh nên chỉ cần xác định giá trị ước lượng).
  - **Bước 4 — Xác minh Thuộc tính dựa trên Văn bản (*Text-Based Attribute Verification*):**
    Đánh giá xem thuộc tính có bắt nguồn từ văn bản hay không. Nếu Bước 2 sơ bộ xác định sản phẩm có thể có thuộc tính này, mô hình sẽ kiểm tra văn bản; nếu suy luận được từ văn bản thì phải trích xuất **giá trị thuộc tính chính xác (*exact attribute value*)**.
  - **Bước 5 — Đánh giá Cuối cùng và Ra Quyết định (*Final Evaluation and Decision-Making*):**
    Tổng hợp toàn bộ lập luận từ 4 bước trước và đưa ra quyết định cuối cùng xem sản phẩm có thuộc tính đó từ dữ liệu đã cho hay không, kết thúc bằng một câu trả lời dứt khoát là **`yes`** hoặc **`no`** ở đoạn văn cuối cùng.
- **Dữ liệu Tinh chỉnh Chuỗi Tư duy Tương phản (*Contrastive Chain-of-Thought Tuning Data*):**
  - Vì các thuộc tính lấy từ AGTD đã qua kiểm duyệt thủ công nên nếu chỉ dùng chúng để tạo CTTD thì quyết định cuối cùng ở Bước 5 luôn là `'yes'`.
  - Để **ngăn ngừa hiện tượng quá khớp (*overfitting*)** trong quá trình tinh chỉnh, nhóm tác giả giới thiệu **Contrastive CoT Tuning Data**:
    - **Mẫu dương (*Positive samples*):** Các thuộc tính hợp lệ của chính sản phẩm đó (nhãn `'yes'`).
    - **Mẫu âm (*Negative samples*):** Các thuộc tính được lấy từ các loại sản phẩm khác (*different product types*), trải qua quá trình chọn lọc thủ công nghiêm ngặt.
    - **Cân bằng dữ liệu:** Số lượng mẫu dương và mẫu âm được đảm bảo **cân bằng (balanced 1:1)**.

---

### 4.5. Mục 3.3: Huấn luyện Mô hình (Model Training)

- **Các mô hình nền tảng được tinh chỉnh:** Ba MLLM mạnh và phổ biến:
  1. **LLaVA-7B** (Liu et al., 2023)
  2. **Qwen-VL** (Bai et al., 2023)
  3. **InternLM (InternLM-XComposer2-7B)** (Dong et al., 2024)
- **Phương pháp tinh chỉnh:** Sử dụng **Low-Rank Adaptation (LoRA)** — đóng băng mô hình ngôn ngữ gốc (*freeze the language model*) và chỉ huấn luyện mô-đun phân rã hạng thấp (*rank-decomposition module*) của tầng Transformer.
- **Hàm mục tiêu huấn luyện (Công thức 1 trang 1705):**
  Cho tập dữ liệu tinh chỉnh theo chỉ dẫn $\mathcal{D} = \text{AGTD} \cup \text{CTTD}$, mục tiêu huấn luyện là tìm bộ tham số LoRA $\hat{\theta}$ tối ưu cho mô hình $\mathcal{M}_{\hat{\theta}}$:
  $$\arg\min_{\hat{\theta}} \mathbb{E}_{(\mathcal{I}_i, \mathcal{T}_i) \in \mathcal{D}} \left[ \sum_{s=1}^{s_j} \log P_{\mathcal{M}_{\hat{\theta}}} \left( s_w^i \mid \mathcal{I}_i, s_1^i, \dots, s_{w-1}^i \right) \right] \quad (1)$$
  trong đó $\mathcal{T}_i = s_1^i, s_2^i, \dots, s_w^i$ và $\hat{\theta}$ biểu thị các tham số của LoRA trong MLLM.

---

### 4.6. Mục 3.4: Suy luận Thuộc tính 3 Giai đoạn (3-Stage Attribute Inference)

1. **Giai đoạn 1 — Sinh Thuộc tính theo Lô (*Batch Attribute Generation*):**
   - MLLM đã tinh chỉnh nhận đầu vào là ảnh và văn bản của mẫu thử nghiệm, sinh ra một lô các thuộc tính và giá trị liên quan.
   - Một tập hợp các thuộc tính và giá trị chuẩn hóa (dạng JSON) được trích xuất từ văn bản đầu ra.
2. **Giai đoạn 2 — Lọc các Thuộc tính Lặp lại (*Filtering Repeated Attributes*):**
   - Nhằm giảm chi phí tính toán cho Giai đoạn 3 và nâng cao độ chính xác, hệ thống dựa trên luật (*rule-based system*) kết hợp mô hình nhúng từ `word2vec-google-news-300` được áp dụng để loại bỏ các thuộc tính trùng lặp ngữ nghĩa từ Giai đoạn 1 (ví dụ: `'type'` và `'product type'` được nhận diện là bản sao của nhau). Chi tiết 3 quy tắc xóa được trình bày tại Phụ lục B.2.
3. **Giai đoạn 3 — Suy luận Thuộc tính Tuần tự với CoT 5 bước (*Sequential Attribute Inference with 5-step CoT*):**
   - Lần lượt đưa từng thuộc tính (sau khi đã lọc ở Giai đoạn 2) vào MLLM để suy luận kiểm chứng bằng quy trình CoT 5 bước.
   - Một thuộc tính có được giữ lại (*reserved*) hay bị loại bỏ được quyết định bởi kết quả đầu ra `yes` hoặc `no` ở bước cuối cùng (Bước 5) của CoT.

---

## 5. Thiết lập Thực nghiệm và Toàn bộ Kết quả (Section 4 — Experiments)

### 5.1. Thiết lập Thực nghiệm (Section 4.1 — Experiment Setup)

- **Bộ dữ liệu (Datasets):**
  1. **WOAM** (Xu et al., 2023): Gồm **4 danh mục sản phẩm**: *Tea* (Trà), *Vitamin*, *Sofa* (Ghế sofa), và *Phone Case* (Ốp lưng điện thoại), với **hơn 9.000 mô tả tiếng Anh cho mỗi danh mục**. Tập thuộc tính hạt giống (*seed attribute set*) chứa trung bình **16,5 loại thuộc tính** và **22 giá trị trên mỗi loại**.
  2. **OAMine** (Zhang et al., 2022): Gồm **100 loại sản phẩm**, với **1.943 sản phẩm kiểm thử được gán nhãn thủ công** thuộc **10 loại sản phẩm**, trung bình **11,5 thuộc tính trên mỗi loại** và **48,1 giá trị duy nhất trên mỗi thuộc tính**.
  - **Mở rộng đa phương thức & Chia tập dữ liệu:** Cả hai bộ dữ liệu được mở rộng sang đa phương thức bằng ảnh thu thập từ Amazon.com. Sử dụng **1.000 mẫu AGTD** và **300 mẫu CTTD** để huấn luyện (*training*), và **1.000 mẫu** để kiểm thử (*testing*).
- **Độ đo Đánh giá (Evaluation Metrics):**
  - Sử dụng 2 độ đo:
    1. **Precision (Độ chính xác):** Tỷ lệ dự đoán dương tính thật (*true positives*) trên tổng số dự đoán dương tính.
    2. **Recall (Độ phủ):** Tỷ lệ dự đoán dương tính thật trên tổng số dương tính thực tế (*actual positives*).
  - Đánh giá dưới 2 chế độ khớp như các nghiên cứu trước (Roy et al., 2021; Zheng et al., 2018a):
    - **Exact Match (Khớp chính xác):** Đòi hỏi sự nhất quán tuyệt đối với nhãn chuẩn vàng (*gold standard*).
    - **Similar Match (Khớp tương đồng):** Cho phép từ đồng nghĩa (*synonyms*), coi dự đoán thuộc tính là đúng nếu khớp với bất kỳ từ đồng nghĩa nào của nhãn chuẩn.
- **Chi tiết Cài đặt (Implementation Details):**
  - Framework: **PyTorch**, chạy trên **01 GPU NVIDIA Tesla A100**.
  - Bộ tối ưu hóa (*Optimizer*): **Adam**, tốc độ học (*learning rate*) = **$3 \times 10^{-4}$ (`3e-4`)**.
  - Phương pháp tinh chỉnh: **LoRA** cho cả 3 MLLM, huấn luyện trong **10 epochs**.
  - Giải mã khi suy luận (*Inference decoding*): **top_p sampling** với **`temperature = 0.2`** và **`top_p = 0.7`**.
  - Báo cáo **giá trị trung bình và độ lệch chuẩn ($\text{mean} \pm \text{std}$)** qua **5 lần chạy độc lập (5 independent trials)** với các `random seed` khác nhau.
- **Các Mô hình Đối sánh (Baselines — 10 mô hình):**
  - *Nhóm MLLM mã nguồn mở & thương mại (8 mô hình):*
    1. **VisualGLM-6B** (Ding et al., 2021): Mô hình hội thoại đa phương thức hỗ trợ ảnh và song ngữ Trung - Anh.
    2. **InstructBLIP (Instructblip-vicuna-7B)** (Dai et al., 2023): Dùng kiến trúc BLIP-2 cho tinh chỉnh chỉ dẫn thị giác.
    3. **Qwen-VL-chat-7B** (Bai et al., 2023): Mô hình suy luận liên quan đến ảnh trong các tác vụ định hướng văn bản.
    4. **DeepSeek-VL-7B** (Lu et al., 2024): Mô hình mã nguồn mở cho việc hiểu thị giác - ngôn ngữ thế giới thực.
    5. **InternLM-XComposer2-7B** (Dong et al., 2024): Mô hình chuyên biệt về đọc hiểu văn bản - hình ảnh.
    6. **LLaVA-7B** và **LLaVA-13B** (Liu et al., 2023): Mô hình MLLM mã nguồn mở ở 2 quy mô tham số.
    7. **GPT-4** (OpenAI, 2023): Mô hình đa phương thức thương mại của OpenAI.
  - *Nhóm Baseline chuyên biệt cho Khai thác Thuộc tính — AM (2 mô hình):*
    8. **OA-Mine** (Zhang et al., 2022): Sử dụng các bộ phân loại siêu dữ liệu (*meta-classifiers*) và phân cụm (*clustering*) cho các giá trị thuộc tính.
    9. **Amacer** (Xu et al., 2023): Cải thiện khả năng tổng quát hóa bằng điều chuẩn tự giám sát (*self-supervised regularization*).

---

### 5.2. Kết quả Thực nghiệm Chính (Section 4.2 — Table 1 trang 1706)

Dưới đây là toàn bộ số liệu nguyên bản từ **Bảng 1 (Table 1: WOAM and OAMine performance of visual language models)** trong bài báo (đơn vị: %, kèm độ lệch chuẩn qua 5 lần chạy):

| Mô hình (Model) | WOAM — Similar Match Precision | WOAM — Similar Match Recall | WOAM — Exact Match Precision | WOAM — Exact Match Recall | OAMine — Similar Match Precision | OAMine — Similar Match Recall | OAMine — Exact Match Precision | OAMine — Exact Match Recall |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **VisualGLM-6B** | $40.32 \pm 1.24$ | $5.25 \pm 0.11$ | $17.80 \pm 0.65$ | $2.83 \pm 0.34$ | $44.12 \pm 0.28$ | $18.98 \pm 0.27$ | $17.46 \pm 0.89$ | $9.38 \pm 0.00$ |
| **Instructblip-vicuna-7B** | $39.79 \pm 0.58$ | $6.62 \pm 0.00$ | $13.87 \pm 3.18$ | $2.75 \pm 0.23$ | $40.16 \pm 0.23$ | $19.78 \pm 0.30$ | $19.78 \pm 0.30$ | $5.76 \pm 0.05$ |
| **Qwen-VL-chat-7B** | $36.86 \pm 0.29$ | $35.38 \pm 1.82$ | $10.29 \pm 0.19$ | $17.61 \pm 1.42$ | $43.06 \pm 0.11$ | $58.09 \pm 0.08$ | $18.63 \pm 0.08$ | $36.15 \pm 0.36$ |
| **DeepSeek-VL-7B** | $42.93 \pm 0.25$ | $36.51 \pm 0.45$ | $12.15 \pm 1.33$ | $19.95 \pm 1.49$ | $53.00 \pm 0.02$ | $56.05 \pm 0.47$ | $25.03 \pm 0.47$ | $36.10 \pm 0.56$ |
| **InternLM-XComposer2-7B** | $52.19 \pm 0.28$ | $31.99 \pm 0.69$ | $23.16 \pm 0.82$ | $19.14 \pm 0.80$ | $69.31 \pm 0.00$ | $45.12 \pm 0.37$ | $36.23 \pm 0.37$ | $27.18 \pm 0.27$ |
| **LLAVA-7B** | $40.49 \pm 1.50$ | $56.21 \pm 1.60$ | $10.61 \pm 1.31$ | $26.22 \pm 4.46$ | $47.07 \pm 0.08$ | $54.99 \pm 0.08$ | $16.71 \pm 0.02$ | $26.82 \pm 0.03$ |
| **LLAVA-13B** | $41.22 \pm 3.29$ | $64.62 \pm 1.59$ | $10.52 \pm 1.35$ | $37.72 \pm 4.91$ | $51.87 \pm 0.21$ | $58.59 \pm 3.27$ | $21.46 \pm 0.99$ | $37.75 \pm 1.19$ |
| **GPT-4** | $52.03 \pm 1.33$ | $65.35 \pm 4.23$ | $15.51 \pm 2.01$ | $41.60 \pm 5.14$ | $64.92 \pm 0.14$ | $55.75 \pm 2.36$ | $29.25 \pm 2.36$ | $33.72 \pm 0.03$ |
| **OA-Mine** | $42.27 \pm 1.29$ | $53.62 \pm 1.59$ | $17.52 \pm 1.35$ | $26.72 \pm 1.91$ | $53.85 \pm 0.15$ | $47.71 \pm 0.01$ | $18.15 \pm 0.01$ | $35.69 \pm 0.67$ |
| **Amacer** | $51.27 \pm 0.82$ | $58.30 \pm 0.17$ | $21.91 \pm 0.53$ | $29.23 \pm 0.90$ | $58.41 \pm 0.26$ | $51.65 \pm 0.12$ | $22.98 \pm 1.04$ | $38.84 \pm 0.05$ |
| **MSIT (QWen)** | $59.95 \pm 0.40$ | $41.60 \pm 0.57$ | $20.00 \pm 0.11$ | $23.75 \pm 0.34$ | $65.01 \pm 0.19$ | $52.44 \pm 0.13$ | $24.61 \pm 0.01$ | $38.13 \pm 0.08$ |
| **MSIT (InternLM)** | $63.40 \pm 0.34$ | $46.80 \pm 0.34$ | $25.00 \pm 0.26$ | $25.53 \pm 0.23$ | $70.79 \pm 0.28$ | $46.99 \pm 0.13$ | $37.52 \pm 0.09$ | $27.37 \pm 0.05$ |
| **MSIT (LLAVA-7B)** | **$66.90 \pm 0.53$** | **$66.99 \pm 2.13$** | **$35.34 \pm 2.71$** | **$52.50 \pm 3.93$** | **$74.50 \pm 0.17$** | **$63.06 \pm 0.45$** | **$54.33 \pm 0.45$** | **$51.54 \pm 0.05$** |

**Nhận xét chính của tác giả từ Bảng 1:**

- Trên **WOAM**, `MSIT (LLaVA-7B)` đạt Similar Match Precision cao nhất là **66,90%** (so với mô hình tốt thứ nhì là InternLM-XComposer2-7B 52,19% và GPT-4 52,03%) và Recall đạt **66,99%** (vượt qua GPT-4 ở mức 65,35%). Về Exact Match, MSIT đạt Precision **35,34%** và Recall **52,50%**, tăng vọt so với GPT-4 (Precision 15,51%, Recall 41,60%).
- Trên **OAMine**, `MSIT (LLaVA-7B)` đạt Similar Match Precision **74,50%** và Recall **63,06%** (vượt xa mô hình đứng thứ hai về Precision là InternLM-XComposer2-7B với 69,31% P / 45,12% R). Về Exact Match, MSIT đạt Precision **54,33%** và Recall **51,54%**, cao hơn nhiều so với Amacer (22,98% P và 38,84% R).
- So sánh trực tiếp với backbone gốc `LLaVA-7B` chưa tinh chỉnh, MSIT nâng Exact Match Precision trên WOAM từ **10,61% lên 35,34%** (tăng hơn 3,3 lần), và trên OAMine từ **16,71% lên 54,33%**. Điều này chứng minh hiệu quả mạnh mẽ của phương pháp tinh chỉnh chỉ dẫn tự sửa lỗi đa phương thức trên cả 3 kiến trúc Qwen, InternLM và LLaVA-7B.

---

### 5.3. Nghiên cứu Cắt bỏ (Section 4.3 — Ablation Study, Table 2 trang 1707)

Bảng 2 đánh giá đóng góp của từng thành phần huấn luyện (`AGTD`, `CTTD`) và từng giai đoạn suy luận (`S1`: Batch Attribute Generation, `S2`: Filtering Repeated Attributes, `S3`: Sequential Attribute Inference with 5-step CoT) trên nền tảng LLaVA-7B:

| AGTD | CTTD | S1 | S2 | S3 | WOAM Similar P | WOAM Similar R | WOAM Exact P | WOAM Exact R | OAMine Similar P | OAMine Similar R | OAMine Exact P | OAMine Exact R |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| | | | | | $40.49 \pm 1.50$ | $56.21 \pm 1.60$ | $10.61 \pm 1.31$ | $26.22 \pm 4.46$ | $47.07 \pm 0.08$ | $54.99 \pm 0.08$ | $16.71 \pm 0.02$ | $26.82 \pm 0.03$ |
| ✔ | ✔ | ✔ | ✔ | | $63.72 \pm 0.83$ | **$67.91 \pm 1.79$** | $29.47 \pm 2.14$ | **$53.69 \pm 4.27$** | $71.48 \pm 0.13$ | **$63.82 \pm 0.00$** | $46.93 \pm 0.14$ | **$52.82 \pm 0.00$** |
| ✔ | | ✔ | ✔ | | $62.15 \pm 1.46$ | $62.52 \pm 3.19$ | $28.27 \pm 3.86$ | $46.85 \pm 5.48$ | $72.07 \pm 0.15$ | $61.80 \pm 0.15$ | $51.35 \pm 0.01$ | $49.58 \pm 0.00$ |
| ✔ | | ✔ | | ✔ | $60.37 \pm 1.93$ | $64.46 \pm 2.89$ | $23.30 \pm 2.30$ | $49.03 \pm 6.45$ | $68.14 \pm 0.10$ | $62.79 \pm 0.00$ | $41.56 \pm 0.06$ | $51.32 \pm 0.00$ |
| | ✔ | ✔ | ✔ | ✔ | $50.15 \pm 2.23$ | $45.88 \pm 0.50$ | $22.01 \pm 3.30$ | $29.97 \pm 4.58$ | $47.98 \pm 0.38$ | $36.48 \pm 0.02$ | $21.81 \pm 0.07$ | $19.52 \pm 0.05$ |
| ✔ | ✔ | ✔ | | ✔ | $63.89 \pm 1.50$ | $67.42 \pm 2.06$ | $32.61 \pm 1.06$ | $52.86 \pm 4.06$ | $70.79 \pm 0.17$ | $63.18 \pm 0.27$ | $49.87 \pm 0.00$ | $51.81 \pm 0.02$ |
| **✔** | **✔** | **✔** | **✔** | **✔** | **$66.90 \pm 0.53$** | $66.99 \pm 2.13$ | **$35.34 \pm 2.71$** | $52.50 \pm 3.93$ | **$74.50 \pm 0.17$** | $63.06 \pm 0.45$ | **$54.33 \pm 0.45$** | $51.54 \pm 0.00$ |

**Phân tích chi tiết từ Bảng 2:**

- **Thành phần huấn luyện (Training Components):**
  - Chỉ dùng `AGTD` (`AGTD + S1 + S2`) đã mang lại cải thiện đáng kể (Similar Match P = 62,15%, R = 62,52% trên WOAM).
  - Chỉ dùng `CTTD` mà không có `AGTD` (`CTTD + S1 + S2 + S3`) cải thiện ít hơn nhiều (Similar Match P = 50,15%, R = 45,88% trên WOAM) vì mô hình thiếu kỹ năng sinh cặp thuộc tính - giá trị chuẩn hóa ở bước đầu.
  - Khi kết hợp cả `AGTD + CTTD`, mô hình đạt hiệu quả cao trên cả Precision và Recall.
- **Thành phần suy luận (Inference Components):**
  - Nếu bỏ `S2` (tức chỉ chạy `AGTD + CTTD + S1 + S3`), Recall cao hơn một chút (67,42% so với 66,99% trên WOAM) nhưng Precision thấp hơn đáng kể (63,89% so với 66,90% ở Similar Match; 32,61% so với 35,34% ở Exact Match) do các thuộc tính trùng lặp không được lọc bỏ.
  - Nếu bỏ `S3` (tức chỉ chạy `AGTD + CTTD + S1 + S2`), Recall đạt mức cao nhất (67,91% Similar Match, 53,69% Exact Match trên WOAM), nhưng Precision giảm mạnh (từ 66,90% xuống 63,72% ở Similar Match, và từ 35,34% xuống 29,47% ở Exact Match). Việc bổ sung `S3` (suy luận CoT 5 bước) giúp lọc bỏ các thuộc tính dương tính giả (*false positives*), đẩy Precision đạt đỉnh trên cả 2 bộ dữ liệu.

---

### 5.4. Thảo luận về Định dạng Đầu ra của AGTD (Section 4.4 — Table 3 trang 1707)

Bảng 3 so sánh hiệu năng trên WOAM khi định dạng đầu ra của AGTD chỉ gồm tên thuộc tính (`Attri-only`) so với khi gồm cả cặp thuộc tính và giá trị (`Attri-Value`):

| Định dạng (Format) | Similar Match Precision | Similar Match Recall | Exact Match Precision | Exact Match Recall |
| :--- | :---: | :---: | :---: | :---: |
| **Attri-only** | $58.19 \pm 4.23$ | $50.81 \pm 1.26$ | $28.68 \pm 0.45$ | $38.37 \pm 0.34$ |
| **Attri-Value** | **$66.90 \pm 0.53$** | **$66.99 \pm 2.13$** | **$35.34 \pm 2.71$** | **$52.50 \pm 3.93$** |

- **Kết luận Mục 4.4:** Khi đổi định dạng đầu ra sang chỉ xuất tên thuộc tính (`Attri-only`), Exact Match Precision và Recall giảm xuống chỉ còn **28,68%** và **38,37%** (thấp hơn `Attri-Value` lần lượt 6,66 điểm % và 14,13 điểm %; ở Similar Match giảm từ 66,90% xuống 58,19% P và từ 66,99% xuống 50,81% R). Việc bắt buộc mô hình sinh cặp `attribute: value` tạo sự gắn kết ngữ nghĩa chặt chẽ giữa tên thuộc tính và bằng chứng cụ thể trong ảnh/văn bản.

---

### 5.5. Phân tích Kích thước Dữ liệu Huấn luyện (Section 4.5 — Figure 3 trang 1706–1708)

- **Hình 3(a) — Thay đổi kích thước dữ liệu AGTD (từ 200 đến 900 mẫu trên WOAM):**
  - Similar Match Precision tăng từ **54,76% lên 56,70%**.
  - Exact Match Precision tăng đều đặn từ **26,13% lên 30,85%**, trong khi Exact Match Recall tăng từ **40,31% lên 43,46%** với dải sai số hẹp, chứng tỏ tính ổn định khi mở rộng quy mô AGTD.
- **Hình 3(b) — Thay đổi kích thước dữ liệu CTTD (100, 200, 300 mẫu trên WOAM):**
  - Similar Match Precision tăng từ **63,36% lên 66,90%**, và Similar Match Recall tăng mạnh từ **53,88% lên 66,99%** khi kích thước CTTD tăng.
  - Exact Match Precision tăng nhẹ từ **35,21% lên 35,34%**, còn Exact Match Recall tăng vọt từ **42,89% lên 52,50%**. Điều này khẳng định suy luận tường minh qua dữ liệu CoT hỗ trợ đắc lực cho việc nhận diện chính xác thuộc tính.

---

### 5.6. Phân tích Khai thác Thuộc tính từ các Nguồn Đầu vào Khác nhau (Section 4.6 — Figure 4 trang 1706–1708)

- **Hình 4** so sánh biểu đồ cột giữa GPT-4 và MSIT trên 3 loại đầu vào riêng biệt: `image` (hình ảnh), `bullet` (điểm nổi bật), và `title` (tiêu đề):
  - Với đầu vào **Image (`MSIT-image` vs `GPT-4-image`)**: MSIT đạt Similar Match Precision **69,21%** (so với **63,81%** của GPT-4) và Exact Match Precision **40,96%** (so với **23,81%** của GPT-4).
  - Với đầu vào **Bullet points (`MSIT-bullet` vs `GPT-4-bullet`)**: MSIT vượt trội rõ rệt về Similar Match Recall với **58,37%** so với **47,19%** của GPT-4.
  - Ngoài ra, phân bố Recall cho thấy hình ảnh luôn mang lại một số lượng lớn thuộc tính trích xuất được, khẳng định tính đúng đắn của hướng tiếp cận đa phương thức.

---

### 5.7. Phân tích Khả năng Thích nghi Miền (Section 4.7 — Domain Adaptation, Figure 5 trang 1706–1708)

- **Thiết kế thực nghiệm:** Thực hiện kiểm chứng chéo (*cross-validation* dạng Leave-One-Category-Out) trên 4 danh mục của bộ dữ liệu WOAM: **Sofa, Phone, Tea, và Vitamin**. Trong mỗi thí nghiệm, mô hình được huấn luyện trên dữ liệu của 3 danh mục và đánh giá trực tiếp trên danh mục thứ 4 chưa từng thấy (*unseen product category*).
- **Kết quả trên biểu đồ radar Hình 5(a)–(d):**
  - MSIT bao phủ diện tích lớn nhất trên cả 4 trục (`similar_pre`, `similar_rec`, `exact_pre`, `exact_rec`), vượt qua tất cả các mô hình đối sánh (`InternLM-XComposer2-7B`, `Amacer`, `OA-Mine`, và `GPT-4`) trên mọi danh mục.
  - Đặc biệt, MSIT đạt Similar Match Precision và Exact Match Precision nổi bật trên danh mục **Sofa** (**69,21%** và **40,96%**) và **Tea** (**69,21%** và **40,96%**), chứng minh khả năng tổng quát hóa mạnh mẽ sang các ngành hàng mới trong thực tế.

---

### 5.8. Hiệu quả của Cơ chế Tự sửa lỗi (Section 4.8 — Effectiveness of Self-Correction, Figure 6 trang 1707–1708)

- **Hình 6** trực quan hóa phân bố phán đoán thuộc tính sau giai đoạn suy luận thứ 3 trên tổng số **1.028 thuộc tính**:
  - **93,3%** thuộc tính được phán đoán là dương tính (*Positive Judgments* — giữ lại).
  - **6,7%** thuộc tính được gán nhãn phán đoán âm tính (*Negative Judgments* — loại bỏ).
  - Trong số 6,7% phán đoán âm tính này, có tới **98,6%** là các thuộc tính sai được tự sửa lỗi chính xác (*Self-corrected Negatives*), và chỉ có **1,4%** bị phán đoán nhầm (*Misjudged Negatives*).
  - Kết quả này chứng minh MSIT tự sửa lỗi gần như toàn bộ các dự đoán sai với sự đánh đổi tối thiểu về Recall để đổi lấy mức tăng lớn về Precision.

---

### 5.9. Nghiên cứu Tình huống (Section 4.9 — Case Study, Figure 7 & Figure 8 trang 1708)

1. **Hình 7 — Hai ví dụ suy luận CoT 5 bước của MSIT:**
   - **Hình 7(a) — Kịch bản trích xuất từ Hình ảnh (`"Packaging Type"`):**
     - *Sản phẩm:* `"English Tea Store Honey Sticks, Mango, 1.3 Pound"`.
     - *Product Text:* `"Add a tropical treat to your tea, Wonderful snacks for the kids, Honey sticks are 6 inches long, Gluten Free"`.
     - *Chuỗi suy luận 5 bước của MSIT:*
       - `(Product Type Judgement)`: Nhận diện sản phẩm là `"Honey Sticks, Mango"`.
       - `(Judge With External Knowledge)`: Thuộc tính `'Packaging Type'` chỉ cách thức sản phẩm được đóng gói hoặc trình bày.
       - `(Judge from Image)`: Hình ảnh hiển thị rõ ràng sản phẩm được đóng gói trong túi (`packaged in a pouch`).
       - `(Judge from Text)`: Văn bản được cung cấp không đề cập tường minh đến loại bao bì.
       - `Conclusion`: **`Yes`**. (Chứng minh khả năng khai thác thuộc tính từ tín hiệu thị giác khi văn bản bị khuyết).
   - **Hình 7(b) — Kịch bản trích xuất từ Văn bản (`"Return Policy"`):**
     - *Sản phẩm:* `"SckoonCup Beginner Choice - Made in The USA"`.
     - *Product Text:* `"...90 DAY MONEY BACK GUARANTEE: Only Sckoon can guarantee the quality. Return for a refund in 90 days., BUY WITH CONFIDENCE: from Sckoon Organics an innovative..."`.
     - *Chuỗi suy luận 5 bước của MSIT:*
       - `(Product Type Judgement)`: Nhận diện loại sản phẩm.
       - `(Judge With External Knowledge)`: Thuộc tính `'return_policy'` chỉ các điều kiện hoàn trả và hoàn tiền sản phẩm.
       - `(Judge from Image)`: Từ hình ảnh không có chỉ dấu tường minh nào về chính sách hoàn trả.
       - `(Judge from Text)`: Văn bản có đề cập `"90 DAY MONEY BACK GUARANTEE"` và `"BUY WITH CONFIDENCE"`, chỉ ra rằng sản phẩm có chính sách hoàn trả.
       - `Conclusion`: **`Yes`**. (Chứng minh khả năng dùng bằng chứng văn bản khi hình ảnh không đủ thông tin).
2. **Hình 8 — So sánh kết quả trích xuất giữa Qwen, GPT-4 và MSIT:**
   - *Sản phẩm:* `"Chiquita Banana Bread Mix 13.7 oz (1 Box makes 12 Delicious Slices) by Chiquita"`.
   - **Qwen (`Qwen-VL`):** Thất bại trong việc trích xuất thuộc tính hữu ích, trả về hàng loạt giá trị `"Unknown"` (`{"servings": "Unknown", "special_features": "Unknown", "mfg_date": "Unknown", "best_by_date": "Unknown"...}`).
   - **GPT-4:** Nhận diện được các thuộc tính bề mặt như `{"Package Type": "Stand-up pouch with a resealable zipper", "Colors": "Predominantly yellow", "Brand History": "Chiquita is a well-known for bananas."}` nhưng bỏ sót các thông tin cốt lõi về thành phần và định lượng sản phẩm, đồng thời sinh ra thuộc tính lan man (`Brand History`).
   - **MSIT (Ours):** Qua 3 giai đoạn (`Batch Generation` $\rightarrow$ `Repeated Attribute Filter` $\rightarrow$ `Sequential Attribute Inference`), trích xuất chính xác và đầy đủ bộ thuộc tính:

     ```json
     {
       "Attributes": {
         "brand": "Chiquita",
         "product_name": "Banana Bread Mix",
         "type": "Banana Bread Mix",
         "net_weight": "13.7 oz (380g)",
         "quantity": "13.7 oz ",
         "ingredients": ["Bananas", "Flour", "...", "Salt"],
         "flavor": "Hearty"
       }
     }
     ```

---

### 5.10. Kết luận và Hạn chế của Bài báo 1 (Section 4.10 & Limitations trang 1708–1709)

- **Kết luận:** MSIT giải quyết thành công hai hạn chế lớn của bài toán Khai thác Thuộc tính Sản phẩm Thương mại Điện tử Thế giới Mở bằng cách kết hợp dữ liệu đa phương thức (văn bản + hình ảnh) và tự sửa lỗi dương tính giả thông qua quy trình suy luận CoT 5 bước.
- **Hạn chế (Limitations):** Hạn chế chính của công trình nằm ở phạm vi quy mô tham số của các MLLM được tinh chỉnh. Do giới hạn về tài nguyên tính toán, nhóm tác giả chỉ thực hiện tinh chỉnh trên ba mô hình MLLM 7 tỷ tham số (**7B-parameter MLLMs**: LLaVA-7B, Qwen-VL-7B, InternLM-7B) mà chưa mở rộng sang các MLLM quy mô lớn hơn như **13B tham số trở lên**.

---

## 6. Toàn bộ Nội dung Phụ lục A và Phụ lục B của Bài báo 1 (Trang 1712–1714)

### 6.1. Phụ lục A.1: Prompt sinh thuộc tính văn bản và thuộc tính hình ảnh

Prompt gồm 3 phần: *Task Description*, *In-context Learning* (4 ví dụ mẫu thuộc 4 ngành hàng Sofa, Trà, Vitamin, Ốp lưng), và *Text/Image information of the product*. Khi sinh thuộc tính ảnh, chỉ cần đổi chữ `text` thành `image` ở phần Task Description và truyền thông tin ảnh ở phần thứ 3.

**Nguyên văn Prompt tại Phụ lục A.1:**

- **Task Description:**
  > You are a world-class algorithm for extracting information in structured formats.
  > There are some product descriptions, and your task is to extract the attribute values from the text information of the product in a JSON format.
  > Please provide me with the corresponding attribute value of the attribute. If there is no corresponding attribute value in the information I provide you, please do not provide me with this attribute.
- **In-context learning (4 JSON mẫu):**

  ```json
  {
    "type": "Sofa",
    "material_frame": "Gold legs",
    "style": "Modern, minimalist",
    "size": "Three-Seater Sofa",
    "color": "White",
    "Padding": "High-Density Foam",
    "Accessories": "Throw Pillows",
    "Special Features": "Electric Reclining",
    "Maintenance Requirements": "Dry Clean Only"
  }
  {
    "brand": "Traditional Medicinals",
    "type": "herbal tea",
    "flavor": "eucalyptus and mint",
    "caffeine_content": "caffeine-free",
    "quantity": "16 tea bags",
    "Packaging Type": "Tea bags",
    "Storage conditions": "Dry and Well-Ventilated Area",
    "Processing Level": "Fermented",
    "Aroma": "Rich",
    "Tea Benefits": ["Refreshment", "Digestive Aid"]
  }
  {
    "brand": "Rugby",
    "product_name": "Tab-A-Vite Multivitamin Tablets",
    "serving_size": "2 tablets",
    "number_of_servings": 30,
    "Dosage Form": "Tablet",
    "Target Audience": "Adults",
    "Indications": "Vitamin Supplementation",
    "key_nutrients": [
      "Thiamin (as Thiamine HCI)",
      "Vitamin B6 (Pyridoxine HCI)",
      "Calcium (as Dicalcium Phosphate)",
      "Magnesium (as Magnesium Oxide)"
    ]
  }
  {
    "Type": "Phone case",
    "Material": "Silicone",
    "Design": "Transparent",
    "Function": "Shockproof",
    "Compatibility": "Compatible Models",
    "Color": "Black",
    "Thickness": "Ultra-thin",
    "Weight": "Lightweight",
    "Texture": "Smooth"
  }
  ```

- **Text information of the product:**
  > Below is the text information of the product whose attributes I want you to extract
  > Title: ...
  > Bullet point: ...

### 6.2. Phụ lục A.2: Prompt hợp nhất thuộc tính văn bản và hình ảnh

- **Task Description:**
  > The following is the information of the attribute value pairs extracted from the image and text of the same product respectively. Please help me merge them into one. The same attributes will be regarded as one after being merged. If I only provide text or image information, then there is no need to merge and directly output the text or image information I provide. If you encounter a attribute like Features, which is a bit general, try to give more detailed attribute. Please let the output follow the json format strictly and do not send me any other text.
- **Image and text attributes:**
  > Image attributes: `{Attribute1:value1, Attribute2:value2, ...}`
  > Text attributes: `{Attribute1:value1, Attribute2:value2, ...}`

### 6.3. Phụ lục A.3: Prompt sinh Dữ liệu Tinh chỉnh Chuỗi Tư duy (CTTD)

- **Task Description:**
  > I will provide you with product images as well as text information and attributes. Please judge whether the product has this attribute. Please follow the steps below to reason step by step and give your reasoning process.
- **Five-step Chain of thought:**
  > - **Step 1:** In this step, you need to determine the type of product based on pictures and text information, such as whether the product is a mobile phone case, tea, or other types of products.
  > - **Step 2:** This step requires analyzing the meaning of the attributes. If the attribute's meaning is unclear, we will make a preliminary determination that it cannot be considered a product attribute. If the intent of the attribute is clear, use common sense to initially judge whether the attribute matches the product type, and initially explain the meaning of the attribute and why it may match the product.
  > - **Step 3:** If you preliminarily judge in the second step that this type of product may have this attribute, then please use the picture I provided to guess its attribute value to confirm that the product indeed has this attribute. Since images do not provide explicit attribute value information, there is no need to derive exact attribute values. You only need to determine a rough attribute value to confirm.
  > - **Step 4:** If you preliminarily judge that this type of product may have this attribute in the second step, then in this step, please use the text I provided to guess its attribute value to confirm that the product indeed has this attribute. If you inferred an attribute value from the text, give the exact attribute value.
  > - **Step 5:** please combine the reasoning from the above steps to draw a conclusion whether the product has this attribute.
  > Please mark the last paragraph with yes or no. No other text is needed in this paragraph.
- **The product's text and image information and the attributes that need to be judged:**
  > Image: ...
  > Title: ...
  > Bullet Point: ...
  > The attribute i want to judge is $\text{Attribute}_i$

### 6.4. Phụ lục B.1 & Bảng 4: Danh sách 10 câu lệnh chỉ dẫn cho Sinh Thuộc tính theo Lô (Stage 1)

1. *"Extract the information from the title, bullet points, and product picture into JSON format."*
2. *"Convert the attribute values of the product from the provided information into JSON format."*
3. *"Generate the product attribute values in JSON format based on the provided title, bullet points, and picture."*
4. *"Compile the product's characteristic attributes into JSON format according to the provided information."*
5. *"Extract the product attribute information into JSON format from the provided title, bullet points, and picture."*
6. *"Parse the product's features and attributes into JSON format from the given information."*
7. *"Extract the product's characteristics into JSON format using the provided title, bullet points, and picture."*
8. *"Retrieve and organize the product's attribute values into JSON format from the provided information."*
9. *"Compile the product's attribute information into JSON format based on the title, bullet points, and picture content."*
10. *"Generate JSON-formatted product attribute data based on the provided information."*

### 6.5. Phụ lục B.2: Quy tắc xóa các thuộc tính có ý nghĩa tương đồng (Stage 2)

- **Điều kiện đồng nghĩa giữa 2 cụm từ (*phrases*):** Hai cụm từ được xác định là đồng nghĩa nếu các từ con (*subwords*) của cụm từ này tương ứng **một-đối-một (*one-to-one*)** với các từ con của cụm từ kia.
- **Cách tính độ tương đồng giữa 2 từ con:** Sử dụng mô hình **`word2vec-google-news-300`**, tính độ tương đồng cosine (*cosine similarity*) giữa hai vector từ con và đặt ngưỡng (*threshold*). Nếu một trong hai cụm từ chỉ có **1 từ con**, một **ngưỡng cao hơn (*higher threshold*)** sẽ được áp dụng vì cụm 1 từ con dễ bị khớp ngẫu nhiên với một từ con trong cụm khác hơn.
- **Ba quy tắc quyết định xóa một trong hai cụm từ đồng nghĩa:**
  - **Rule 1:** Nếu chỉ có một thuộc tính có số lượng từ con bằng 1 (giả sử thuộc tính đó là $A$, và cụm từ còn lại là thuộc tính $B$), thì thuộc tính bị xóa phụ thuộc vào số lượng từ con của $B$:
    - Nếu số từ con của $B$ **bằng 3** ($|B| = 3$): **Xóa thuộc tính $A$**.
    - Nếu số từ con của $B$ **lớn hơn 3** ($|B| > 3$): **Xóa thuộc tính $B$**.
  - **Rule 2:** Nếu một thuộc tính có **2 từ con** (thuộc tính $A$), và thuộc tính kia có **từ 3 từ con trở lên** ($|B| \ge 3$, thuộc tính $B$): **Chọn xóa thuộc tính $B$**.
  - **Rule 3:** Nếu hai thuộc tính có **cùng số lượng từ con** ($|A| = |B|$): **Chọn ngẫu nhiên một thuộc tính để xóa**.

### 6.6. Phụ lục B.3 & Bảng 5: Danh sách 5 câu lệnh chỉ dẫn cho Lọc Thuộc tính Sai (Stage 3)

1. *"I provide you with text and image information of a product along with one attribute of this product. Please determine if this product possesses this attribute through the text and image. Let's think step by step, and please provide your reasoning process."*
2. *"Here's textual and visual data about a product, along with a specific attribute. Your job is to discern if this attribute applies to the product, using both the text and the visuals. Let's methodically analyze the information, detailing your reasoning process step by step."*
3. *"I present you with textual and visual data about a product, along with a single attribute associated with it. Your task is to determine whether this product exhibits this attribute, utilizing both the text and the image. Let's think step by step, and please provide your reasoning process."*
4. *"I provide you with the text and picture information of a product and an attribute of this product, please help me judge whether this product has this attribute through the text and picture, we will think step by step, please give your reasoning process."*
5. *"I will give you the text and image information of a product, as well as one of its attributes. Please use the text and image to help me determine whether the product has this attribute. Let's think step by step, and please explain your reasoning process."*

---

# PHẦN II: NỘI DUNG TOÀN DIỆN BÀI BÁO 2 — CMA-VRP (ACM MM 2025)

## 1. Thông tin chung (Metadata)

- **Tiêu đề gốc:** *Entity Graph Alignment and Visual Reasoning for Multimodal Fake News Detection*
- **Tên viết tắt khung phương pháp:** **CMA-VRP** (*Cross-Modal Alignment with Visual Reasoning Prompting*)
- **Hội nghị công bố:** *Proceedings of the 33rd ACM International Conference on Multimedia (MM '25)*, ngày 27–31/10/2025, tại Dublin, Ireland. Nhà xuất bản ACM, New York, NY, USA, 10 trang (trang 2486–2495).
- **DOI:** `https://doi.org/10.1145/3746027.3754591` | **ISBN:** `979-8-4007-2035-2/2025/10`
- **CCS Concepts:**
  - *Security and privacy* $\rightarrow$ *Social aspects of security and privacy*
  - *Information systems* $\rightarrow$ *Multimedia information systems*
- **Keywords:** Multimodal Fake News Detection, Chain-of-thought Prompting, Graph Neural Networks, Contrastive Learning.
- **Nhóm tác giả và đơn vị công tác:**
  1. **Guoyi Li** (`liguoyi@iie.ac.cn`) — Institute of Information Engineering, Chinese Academy of Sciences (Viện Kỹ thuật Thông tin, Viện Hàn lâm Khoa học Trung Quốc), Bắc Kinh, Trung Quốc.
  2. **Die Hu** (`hudie@iie.ac.cn`) — Institute of Information Engineering, Chinese Academy of Sciences, Bắc Kinh, Trung Quốc.
  3. **Xiaomeng Fu** (`fuxiaomeng@iie.ac.cn`) — Institute of Information Engineering, Chinese Academy of Sciences, Bắc Kinh, Trung Quốc.
  4. **Qirui Tang** (`tangqirui@iie.ac.cn`) — Institute of Information Engineering, Chinese Academy of Sciences, Bắc Kinh, Trung Quốc.
  5. **Yulei Wu** (`y.l.wu@bristol.ac.uk`) — Department of Electrical and Electronic Engineering, University of Bristol (Đại học Bristol), Bristol, Vương quốc Anh.
  6. **Xiaodan Zhang**$^*$ (`zhangxiaodan@iie.ac.cn`) — Tác giả liên hệ (*Corresponding author*), Institute of Information Engineering, Chinese Academy of Sciences, Bắc Kinh, Trung Quốc.
  7. **Honglei Lyu** (`lvhonglei@iie.ac.cn`) — Institute of Information Engineering, Chinese Academy of Sciences, Bắc Kinh, Trung Quốc.

---

## 2. Tóm tắt (Abstract) và Đặt vấn đề (Introduction)

### 2.1. Nội dung phần Tóm tắt (Abstract)

- **Bối cảnh:** Sự gia tăng của tin giả đa phương thức (*multimodal fake news*) đe dọa việc phổ biến thông tin đáng tin cậy bằng cách khai thác nhiều phương thức (văn bản, hình ảnh) để tạo nội dung lừa đảo, thu hút sự chú ý, gây ảnh hưởng nghiêm trọng đến an toàn xã hội.
- **Thách thức của các phương pháp hiện tại:**
  1. Gặp khó khăn trong căn chỉnh liên phương thức (*cross-modal alignment*) như sự bất đồng ngữ nghĩa tinh vi (*semantic inconsistencies*) và các mối quan hệ thị giác - ngữ nghĩa phức tạp (*complex visual-semantic relations*).
  2. Dễ bị tổn thương trước các mẫu dữ liệu chất lượng thấp hoặc chứa nhiễu (*low-quality or noisy samples*).
- **Giải pháp đề xuất — CMA-VRP (*Cross-Modal Alignment with Visual Reasoning Prompting*):**
  1. **Mô hình hóa đồ thị thực thể & Học tương phản đồ thị:** Biểu diễn các thực thể văn bản và hình ảnh bằng đồ thị (*graphs*) để nắm bắt các tương tác ngữ nghĩa chi tiết (*fine-grained semantic interactions*) và tăng cường tính nhất quán liên phương thức thông qua học tương phản đồ thị (*graph contrastive learning*).
  2. **Trích xuất thuộc tính suy luận thị giác sâu bằng LLM và LVLM:** Khác với các phương pháp chỉ dựa vào đặc trưng ảnh nông (*shallow image features* như cạnh, kết cấu bề mặt từ VGG/ResNet), CMA-VRP tận dụng LLM và LVLM để nắm bắt các thuộc tính thị giác - ngữ nghĩa sâu liên quan đến suy luận (như hành động, bối cảnh, biểu cảm).
  3. **Dung hợp ngữ nghĩa liên phương thức dựa trên đồ thị (*Graph-based cross-modal semantic fusion*):** Thống nhất biểu diễn văn bản và thị giác.
  4. **Căn chỉnh chu trình liên phương thức (*Cross-modal cycle alignment*):** Căn chỉnh phân phối của các phương thức bằng cách giảm sự sai lệch ngữ nghĩa, lọc nhiễu đặc thù theo từng phương thức (*modality-specific noise*) và trích xuất các biểu diễn bất biến qua các miền (*invariant representations across domains*).

### 2.2. Nội dung phần Giới thiệu (Section 1 — Introduction)

- **Phân tích các hạn chế hiện hữu (Minh họa qua Hình 1 trang 2487):**
  - **Hạn chế 1 — Thiếu khả năng mô hình hóa ngữ nghĩa thị giác sâu (*Insufficient deep visual semantic modeling capabilities*):**
    - Các mô hình thị giác truyền thống thường dựa vào các đặc trưng thị giác nông (*shallow visual features* như cạnh và kết cấu) trích xuất từ **VGG** [42] hoặc **ResNet50** [57], bỏ qua vai trò quan trọng của các đặc trưng thị giác sâu (như quan hệ không gian và tương tác ngữ nghĩa).
    - *Ví dụ Hình 1(a):* Bài đăng có văn bản *"Protesters from unite against fascism held a peaceful protest around the institution in Bolton."* (Người biểu tình tổ chức cuộc biểu tình ôn hòa tại Bolton). Bề ngoài bối cảnh ảnh và văn bản có vẻ khớp nhau, nhưng biểu cảm căng thẳng và hành động xô xát bị cảnh sát khống chế trong ảnh ngầm chỉ xu hướng bạo lực, mâu thuẫn với ngữ nghĩa *"peaceful"* (ôn hòa) của văn bản.
    - Các mô hình LVLM gần đây (dòng BLIP [23, 24], LLaVA [26, 27]) có khả năng nhận diện thực thể và tri thức thế giới tốt, nhưng lại **kém nhạy cảm với các sự bất đồng liên phương thức tinh vi** [31, 40] như sự sai khác trong hành động hoặc nội dung khẩu hiệu (*slogan content*).
    - *Ví dụ Hình 1(b):* Bài đăng *"The politician's controversial policy gained graduates of @RutgersU support."* (Chính sách gây tranh cãi của chính trị gia nhận được sự ủng hộ của sinh viên tốt nghiệp @RutgersU). Nếu bỏ qua chi tiết thị giác là tấm biển ghi dòng chữ **"not in my name"** do một khán giả giơ lên trong ảnh, mô hình sẽ lầm tưởng văn bản và hình ảnh nhất quán với nhau.
  - **Hạn chế 2 — Sự hiện diện của nhiễu cố hữu trong tin tức chất lượng thấp trên mạng xã hội (*Inherent noise in low-quality social media news*):**
    - Ảnh tin tức do bị nén (*compression*) hoặc độ phân giải thấp (*low resolution*) có thể không cung cấp đầy đủ thông tin ngữ nghĩa, chỉ nhận diện được một phần thực thể.
    - *Ví dụ Hình 1(c):* Bài đăng *"@RT_com: Police say explosion also took place in a bar near #Paris stadium."* đi kèm bức ảnh ban đêm rất mờ, nơi chỉ có thực thể thị giác như *"police car"* (xe cảnh sát) là dễ phân biệt.
    - Ngoài ra, các nền tảng mạng xã hội dùng nhiều ký hiệu như `#` để gắn thẻ chủ đề/nhắc tên người dùng, hoặc người đăng chèn các dòng chữ đóng dấu (*title watermarks*) nổi bật mang định kiến chủ quan mạnh.
    - *Ví dụ Hình 1(d):* Bài đăng *"Financial and entertainment industries unite for charity on September 18."* nhưng bức ảnh lại bị đè bởi dòng chữ watermark lớn màu vàng *"Public Focus! Transparency Concerns Arise Over Charity Fund!"* làm che khuất nội dung gốc và gây nhiễu quá trình nhận thức của mô hình.

- **Ba động lực nghiên cứu cốt lõi của nhóm tác giả (Minh họa tại Hình 2 trang 2487):**
  1. **Mô hình hóa đồ thị phát hiện sự bất đồng ở cấp độ thực thể (*Entity-level inconsistencies*):** Như **Hình 2(a)** (văn bản *"David Bowie and Catherine Deneuve intimately relaxing at the Neptune diner in Astoria 1982."* được biểu diễn thành đồ thị cú pháp gồm các nút `David Bowie`, `Catherine Deneuve`, `relaxing`, `intimately`, `Neptune diner`, `Astoria`, `1982` và đồ thị thị giác gồm `Woman`, `Man`, `Table`, `Bottle`, `Bread`, `Sunglasses` với các cạnh `sitting`, `holding`, `on`, `in`, `near`), phân tích chi tiết cấp thực thể giúp nắm bắt tương tác liên phương thức.
  2. **Tận dụng LLM và LVLM để trích xuất Đặc trưng Suy luận Thị giác (*Visual Reasoning Features - VRF*):** Như **Hình 2(b)**, định nghĩa VRF là các ngữ nghĩa thị giác then chốt hỗ trợ kiểm chứng tuyên bố (*claim verification*), giúp làm lộ diện các xung đột ngữ nghĩa ẩn (ví dụ: đối chiếu yêu cầu *"appear calm and non-confrontational"* từ thực thể văn bản với thực tế *"tightly by police officers"* từ thực thể thị giác).
  3. **Học biến đổi miền phương thức (*Modality-domain transformation learning*):** Thay vì chỉ dựa vào dữ liệu cặp ảnh - văn bản đã căn chỉnh tường minh (*explicitly paired text-image data*), chiếu các thực thể và mô tả vào một không gian ngữ nghĩa chung (*shared semantic space*) để trích xuất các liên kết liên phương thức ổn định ngay cả từ dữ liệu không bắt cặp hoặc chứa nhiễu.

- **Bốn đóng góp chính của Bài báo 2:**
  1. Đề xuất phương pháp căn chỉnh liên phương thức kết hợp mô hình hóa đồ thị thực thể đa phương thức và dung hợp suy luận thị giác.
  2. Thiết kế cơ chế học tương phản đồ thị (liên đồ thị và nội đồ thị) cùng dung hợp đồ thị để thống nhất căn chỉnh ngữ nghĩa đa phương thức và đặc trưng sâu.
  3. Thiết kế cơ chế biến đổi miền phương thức dựa trên CycleGAN tích hợp đặc trưng suy luận thị giác cùng khung bộ phân biệt kép để giảm nhiễu và trích xuất đặc trưng bất biến phương thức (*modality-invariant features*).
  4. Đánh giá thực nghiệm sâu rộng trên 3 bộ dữ liệu thế giới thực (Twitter, Pheme, Weibo) chứng minh hiệu quả và độ bền vững vượt trội trước nhiễu.

---

## 3. Các nghiên cứu liên quan (Section 2 — Related Work)

### 3.1. Phát hiện Tin giả Đa phương thức (Section 2.1)

- Các phương pháp tiêu biểu tập trung vào căn chỉnh liên phương thức để phát hiện sự bất đồng:
  - **CAFE** [4] (Chen et al., WWW 2022): Tích hợp căn chỉnh liên phương thức và học độ mơ hồ (*ambiguity learning*) để dung hợp thích ứng các đặc trưng đơn phương thức.
  - **COOLANT** [51] (Wang et al., ACM MM 2023): Sử dụng học tương phản liên phương thức (*cross-modal contrastive learning*) để căn chỉnh đặc trưng ảnh và văn bản vào một không gian thống nhất.

### 3.2. Phát hiện Tin giả Tăng cường Thực thể (Section 2.2 — Entity-Enhanced Fake News Detection)

- Khai thác liên kết ngữ nghĩa, tri thức nền và tương tác của các thực thể [11, 25, 33, 39, 59, 60]:
  - **InfoSurgeon** [11] (Fung et al., ACL 2021): Dùng liên kết thực thể (*entity linking*) và suy luận đồ thị tri thức (*knowledge graph reasoning*) để xác định sự bất đồng ngữ nghĩa giữa văn bản và hình ảnh.
  - **EM-FEND** [39] (Qi et al., ACM MM 2021): Kết hợp nhận diện thực thể thị giác để tăng cường căn chỉnh thực thể giữa văn bản và ảnh.
  - **Điểm yếu:** Thường bỏ qua việc mô hình hóa sự bất đồng chi tiết (*fine-grained inconsistency modeling*) và suy giảm mạnh khi gặp dữ liệu chất lượng thấp hoặc nhiễu lan truyền [4, 33].

### 3.3. Phát hiện Tin giả Tăng cường bởi LLM/LVLM (Section 2.3 — LLM-Enhanced Fake News Detection)

- Các nghiên cứu gần đây [6, 7, 46, 52, 53, 58] khai thác khả năng suy luận của LLM và mở rộng sang LVLM như **LLaVA** [28], **MiniGPT-4** [62], **FKA-Owl** [30], **SNIFFER** [40].
- **NLIN** [60] (Zhang et al., IJCAI 2024): Thống nhất nội dung đa phương thức vào không gian ngôn ngữ tự nhiên và tinh chỉnh LLM với tri thức ngoài.
- **Điểm yếu của LVLM trực tiếp hoặc LVLM tinh chỉnh:**
  1. Thường bỏ sót các chi tiết hình ảnh nhỏ và các mối quan hệ không gian (*spatial relationships*).
  2. Các LVLM được tinh chỉnh (*fine-tuned LVLMs*) rất dễ gặp hiện tượng **ảo giác (*hallucinations*)** — nhận diện nhầm các đối tượng chưa từng thấy thành các đối tượng quen thuộc trong tập huấn luyện [8, 17], làm suy giảm độ ổn định của việc căn chỉnh liên phương thức.

---

## 4. Phương pháp Đề xuất Chi tiết (Section 3 — Methodology & Hình 3 trang 2489)

Kiến trúc **CMA-VRP** (minh họa tại **Hình 3**) gồm **3 phân hệ nối tiếp và bổ trợ nhau**:

1. **Khởi tạo Đồ thị Hướng Thực thể và Suy luận Thị giác (*Entity-Driven Graph and Visual Reasoning Initialization* — Mục 3.1).**
2. **Căn chỉnh và Dung hợp Đồ thị Liên phương thức (*Cross-Modal Graph Alignment and Fusion* — Mục 3.2).**
3. **Học Bất biến Chu trình Đối kháng (*Adversarial Cycle-Consistent Invariant Learning* — Mục 3.3).**

---

### 4.1. Phân hệ 1: Khởi tạo Đồ thị Hướng Thực thể và Suy luận Thị giác (Section 3.1)

#### 4.1.1. Xây dựng Đồ thị Đơn phương thức (Section 3.1.1 — Unimodal Graph Construction)

Cho một cặp bản tin đa phương thức $(I, T)$:

1. **Đồ thị Văn bản ($\mathcal{G}_t = (\mathcal{V}_T, \mathcal{E}_T)$):**
   - Được tạo thông qua các bộ phân tích cú pháp phụ thuộc (*dependency parsers*) gồm **Stanford NLP** [34], **TexSmart NLP tools** [29] (và `spaCy en_core_web_trf` trong phần cài đặt).
   - Tập nút $\mathcal{V}_t$ biểu diễn các đơn vị cú pháp/thực thể văn bản; tập cạnh $\mathcal{E}_t$ biểu diễn các kết nối phụ thuộc cú pháp giữa chúng.
   - Ma trận kề $A_t$ nhận giá trị `0` hoặc `1` thể hiện sự vắng mặt hay hiện diện của cạnh giữa các nút.
   - Biểu diễn nhúng nút văn bản $X_t$ được trích xuất bằng **BERT** (`BERT-base-Uncased`) [9].
   - Ma trận biến đổi cạnh khả học (*trainable edge transformation matrix*) $Z_t$ được dùng để tinh chỉnh các phụ thuộc ngữ nghĩa.
2. **Đồ thị Thị giác ($\mathcal{G}_v = (\mathcal{V}_I, \mathcal{E}_I)$):**
   - Dựa trên mô hình sinh đồ thị cảnh (*scene graph generation model*) [44] với **Mask-RCNN** [14] làm mạng xương sống (*backbone*), xác định các đối tượng chính và quan hệ giữa chúng (ví dụ: `holding`, `wearing`, `sitting`).
   - Top-$k$ đối tượng có điểm phân loại cao nhất tạo thành tập thực thể thị giác hợp lệ $\mathcal{V}_v$, trong khi các quan hệ không gian/ngữ nghĩa tạo thành tập cạnh $\mathcal{E}_v$, được mã hóa trong ma trận mặt nạ kề $A_v$.
   - Các nút ($\mathcal{V}_v$) và cạnh ($\mathcal{E}_v$) được biểu diễn bởi các vector đặc trưng $X_v$ và $Z_v$ trích xuất từ đầu ra của Mask-RCNN.
   - **Nút toàn cục (*Global node* $v_g$):** Mã hóa toàn bộ bức ảnh thành một nút toàn cục $v_g$ và liên kết nó với tất cả các thực thể trong ảnh để cung cấp ngữ nghĩa thị giác toàn cục.
   - **Nút văn bản OCR ($v_{ocr}$):** Sử dụng hệ thống **Rosetta OCR** [2] để trích xuất các phần tử văn bản nằm trong ảnh (như khẩu hiệu *slogans*, biển biểu tình, watermark), phân tích cú pháp tương tự như trên và mã hóa thành các nút bổ sung $v_{ocr}$ trong đồ thị thị giác, liên kết với các thực thể thị giác $\mathcal{V}_v$ thông qua các cạnh không gian/ngữ nghĩa.

#### 4.1.2. Suy luận Thị giác dựa trên CoT Hướng Chân lý (Section 3.1.2 — Truth-Driven CoT-based Visual Reasoning)

- **Mục đích:** Cung cấp thông tin suy luận liên quan đến quan hệ không gian, động lực hành vi (*behavioral dynamics*) và ngữ cảnh tri thức cho từng đối tượng.
- **Cơ chế Prompting 2 tầng (*Dual-layer Visual Reasoning Prompting - VRP*) không cần tinh chỉnh (*without any fine-tuning*):**
  - Để ngăn ngừa nhiễu giao thoa liên phương thức (*cross-modal interference*) khi trích xuất đặc trưng suy luận ban đầu, nhóm tác giả tách riêng việc xử lý thực thể văn bản và thực thể thị giác:
    - Dùng **Mistral-7B** [18] (LLM) để xử lý các thực thể văn bản.
    - Dùng **LLaVA-1.6-13B** [27] (LVLM) để xử lý các thực thể thị giác.
  - **Tầng Prompt 1 — Sinh lập luận kiểm chứng cho từng thực thể:**
    - *Prompt 1:*
      > *"For each object, consider the rationale for how its visual features justify whether the claim contains misinformation."*
    - *Output 1 mẫu:*
      > *(Textual Entity) Protester: It is necessary to determine whether the scene depicts a protest and whether the individuals' actions align with the description of a "peaceful" protest. Bolton: ...*
      > *(Visual Entity) Man_0: The man appears to be a protester. If the protester's demeanor and actions contradict the description, it points to a discrepancy...*
  - **Tầng Prompt 2 — Tóm tắt các đặc trưng thị giác tương ứng với từng lập luận:**
    - *Prompt 2:*
      > *"Summarize the corresponding visual features of each object for each rationale."*
    - *Output 2 mẫu:*
      > *(Textual Entity) { The protesters should appear calm and non-confrontational, with no signs of aggression or violence. }, {...}*
      > *(Visual Entity) { Intense facial expression, tightly restrained by police...}, {...}, {...}*
  - **Mã hóa thành vector đặc trưng:** Các văn bản suy luận thị giác thu được cho $N_t$ thực thể văn bản và $N_v$ thực thể thị giác được đưa qua bộ mã hóa **BERT** [9] để thu được hai tập vector Đặc trưng Suy luận Thị giác: **$VRF_t$** và **$VRF_v$**.

---

### 4.2. Phân hệ 2: Căn chỉnh và Dung hợp Đồ thị Liên phương thức (Section 3.2)

#### 4.2.1. Học Tương phản Đồ thị (Section 3.2.1 — Graph Contrastive Learning)

Kết hợp hai cấp độ học tương phản: **Liên đồ thị (*Inter-Graph*)** và **Nội đồ thị (*Intra-Graph*)**.

1. **Học Tương phản Liên đồ thị (*Inter-Graph Contrastive Learning*):**
   - Xét một lô huấn luyện gồm $N$ cặp ảnh - văn bản $\{x_i\}_{i=1}^N$, trong đó mỗi cặp đóng vai trò là mẫu neo (*anchor sample*) $x_i = \{s_t^i, s_v^i\}$ với đồ thị văn bản và thị giác tương ứng $\{(\mathcal{G}_t^i, \mathcal{G}_v^i)\}_{i=1}^N$. Một lô $N$ cặp chứa $N$ cặp dương $\mathcal{X}^+$ và $N^2 - N$ cặp âm $\mathcal{X}^-$.
   - Đầu tiên, tổng hợp biểu diễn nút của từng đồ thị bằng hàm $\text{READOUT}(\cdot)$ [55] (**Công thức 1 trang 2489**):
     $$X_v^m = \text{READOUT}_v\left(\{h_i : v_i \in \mathcal{V}_I\}\right), \quad X_t^m = \text{READOUT}_t\left(\{h_i : v_i \in \mathcal{V}_T\}\right) \quad (1)$$
     trong đó $h_i$ là nhúng nút, $\mathcal{V}_I$ và $\mathcal{V}_T$ là tập nút thị giác và văn bản, còn $X_t^m = f(s_t)$ và $X_v^m = f(s_v)$ là đặc trưng văn bản và thị giác đã tổng hợp.
   - **Ma trận căn chỉnh mềm có tham số làm mượt khả học $\theta$:** Để giảm thiểu sự mơ hồ ngữ nghĩa tiềm ẩn trong căn chỉnh liên phương thức (vì hai mẫu khác nhau trong cùng lô vẫn có thể chia sẻ một phần ngữ nghĩa tương đồng), mục tiêu căn chỉnh được định nghĩa lại bằng cách kết hợp nhãn one-hot tiêu chuẩn $Y_{ij}$ với ma trận căn chỉnh mềm hướng dẫn bởi độ tương đồng $S_{ij}$ (**Công thức 2 trang 2489**):
     $$S_{ij} = \frac{\exp\left(\text{sim}\left(X_t^m[i], X_v^m[j]\right) / \tau\right)}{\sum_{j'} \exp\left(\text{sim}\left(X_t^m[i], X_v^m[j']\right) / \tau\right)}, \quad \tilde{Y}_{ij} = \theta \cdot Y_{ij} + (1 - \theta) \cdot S_{ij} \quad (2)$$
     trong đó $\theta \in [0, 1]$ là tham số làm mượt khả học (*learnable smoothing parameter*) được **khởi tạo bằng $0.5$**, $\text{sim}(\cdot)$ là độ tương đồng cosine, và $\tau$ là tham số nhiệt độ (*temperature parameter*).
   - **Hàm mất mát tương phản liên đồ thị (**Công thức 3 trang 2490**):**
     $$\mathcal{L}_{inter} = \mathbb{E} \left[ - \sum_{i,j} \tilde{Y}_{ij} \log \frac{\exp\left(\text{sim}\left(f(s_t[i]), f(s_v[j])\right) / \tau\right)}{\sum_{j'} \exp\left(\text{sim}\left(f(s_t[i]), f(s_v[j'])\right) / \tau\right)} \right] \quad (3)$$

2. **Học Tương phản Nội đồ thị (*Intra-Graph Contrastive Learning*):**
   Nhằm căn chỉnh biểu diễn của cùng một thực thể xuyên qua các phương thức khác nhau và chống lại sự thống trị của một phương thức đơn lẻ, quy trình gồm 3 bước:
   - **(i) Ghép thực thể (*Entity Matching*):** Theo [13, 60], tận dụng khả năng nhận diện thực thể thị giác mạnh mẽ của LVLM để xác định các thực thể thị giác $\mathcal{V}_v$ và kiểm tra xem các thực thể văn bản tương ứng có tồn tại trong đồ thị văn bản $\mathcal{G}_t$ hay không, từ đó nối $\mathcal{G}_t$ và $\mathcal{G}_v$ để tạo thành **đồ thị đa phương thức $\mathcal{G}_m = \{\mathcal{V}_m, \mathcal{E}_m\}$**.
   - **(ii) Che thực thể để tạo mẫu dương (*Entity Masking*):** Áp dụng kỹ thuật che thực thể lên $\mathcal{G}_m$ với xác suất **$p_m = 0.2$**, thay thế đặc trưng của các nút bị che bằng vector nhúng ngẫu nhiên (*random embeddings*) nhằm mô phỏng việc mất mát thông tin, buộc mô hình tập trung vào các thực thể và quan hệ còn lại. Đồ thị tăng cường dương là:
     $$\mathcal{V}_+(\mathcal{G}) = (M \otimes \mathcal{V}_m, \mathcal{E}_m)$$
     trong đó $M$ là vector mặt nạ cho các nút thực thể $\mathcal{V}_m$, còn $\mathcal{E}_m$ giữ nguyên để bảo toàn thông tin quan hệ.
   - **(iii) Khai thác mẫu âm bằng nhiễu trộn (*Negative Mining*):** Trộn ngẫu nhiên các mẫu của cùng phương thức nhưng có nhãn đối lập và nối ngẫu nhiên các thực thể liên phương thức. Với mẫu gốc neo $x_i^a = \{s_t^i, s_v^i\}$, mẫu dương là $x_i^+$ (từ bước Entity Masking), còn mẫu âm nhiễu loạn $x_i^-$ được sinh bằng hàm trích xuất ngẫu nhiên $d(\cdot)$ để trộn phương thức:
     $$x_i^- = \left\{s_t^i, s_v^{d(i)}\right\} \quad \text{hoặc} \quad x_i^- = \left\{s_t^{d(i)}, s_v^i\right\}$$
     với đồ thị đa phương thức tương ứng ký hiệu là $\mathcal{V}_-(\mathcal{G})$.
   - **Hàm mất mát tương phản nội đồ thị theo InfoNCE [36] / SimCLR [3] (**Công thức 4 trang 2490**):**
     $$\mathcal{L}_{intra} = -\mathbb{E}_{x \sim \mathcal{X}} \left[ \log \frac{\exp\left(\text{sim}\left(g(x^a), g(x^+)\right) / \tau\right)}{\sum_{x^- \in \mathcal{X}^-} \exp\left(\text{sim}\left(g(x^a), g(x^-)\right) / \tau\right)} \right] \quad (4)$$
     trong đó $g(\cdot)$ biểu thị biểu diễn thu được sau bước dung hợp đồ thị liên phương thức (Mục 3.2.2).
   - **Tổng hàm mất mát học tương phản đồ thị:**
     $$\mathcal{L}_{cl} = \mathcal{L}_{intra} + \mathcal{L}_{inter}$$

#### 4.2.2. Dung hợp Đồ thị Liên phương thức (Section 3.2.2 — Cross-modal Graph Fusion)

- **Bốn nút loại tổng quát (*Four generic type nodes*):** Vì một số từ trong văn bản không có đối tượng thị giác trực tiếp tương ứng, nhóm tác giả định nghĩa 4 nút loại tổng quát: **`misc`** (hỗn hợp), **`person`** (con người), **`location`** (địa điểm), và **`organization`** (tổ chức), liên kết từng từ văn bản với các nút thị giác được phát hiện thông qua các từ tổng quát này bằng các cạnh liên phương thức (*inter-modal edges*).
- **Kiến trúc $L$ tầng dung hợp ($L = 2$):** Kết hợp Mạng tích chập đồ thị (GCN) [56], Chú ý đơn phương thức (*Unimodal Attention - Uni-Att*) trong khung Transformer, và Cơ chế cổng liên phương thức (*Cross-modal Gating*) tích hợp đặc trưng suy luận thị giác $VRF_t$:
  - **Dung hợp nội phương thức (*Intra-modal fusion* — Công thức 5 trang 2490):**
    $$C_t^{(l)} = \text{Softmax}\left( A_t \cdot \frac{Q_t^{(l-1)} \left(K_t^{(l-1)}\right)^\top}{\sqrt{d}} \right) \cdot V_t^{(l-1)} \quad (5)$$
    trong đó truy vấn, khóa và giá trị $Q_t^{(l)}, K_t^{(l)}, V_t^{(l)} \in \mathbb{R}^{n \times d}$ được định nghĩa có tích hợp thông tin cạnh $\phi(Z_t)$:
    $$Q_t^{(l-1)} = W_Q^{(l-1)} \cdot H_t^{(l-1)}, \quad K_t^{(l-1)} = W_K^{(l-1)} \cdot H_t^{(l-1)} + \phi(Z_t), \quad V_t^{(l-1)} = W_V^{(l-1)} \cdot H_t^{(l-1)} + \phi(Z_t)$$
    với $\phi$ là hàm khả học (như tầng tuyến tính), $W_Q, W_K, W_V$ là các ma trận tham số, và giá trị khởi tạo $H_t^{(0)} = X_t$.
  - **Dung hợp liên phương thức qua cơ chế cổng tích hợp $VRF_t$ (*Inter-modal fusion* — Công thức 6 & 7 trang 2490):**
    $$R_{tu}^{(l)} = C_{tu}^{(l)} + \sum_{j \in \mathcal{N}_v(u)} \alpha_{i,j} \cdot C_{vj}^{(l)} + W_{vt}^{(l)} \cdot VRF_t(u) \quad (6)$$
    $$\alpha_{i,j} = W_1^{(l)} C_{tu}^{(l)} + W_2^{(l)} C_{vj}^{(l)} \quad (7)$$
    trong đó $\mathcal{N}_v(u)$ là tập các nút thị giác láng giềng của nút văn bản $u$, và $W_{vt}^{(l)}$ là trọng số khả học để tích hợp đặc trưng suy luận thị giác $VRF_t(u)$.
  - **Cập nhật qua mạng truyền thẳng theo vị trí (FFN) và tổng hợp cuối cùng:**
    $$H_t^{(l)} = \text{FFN}\left(R_t^{(l)}\right)$$
    Trạng thái nút thị giác $H_v^{(L)}$ cũng được tính song song tương tự. Sau $L$ tầng dung hợp, biểu diễn cuối cùng của văn bản $H_t^{(L)}$ và thị giác $H_v^{(L)}$ được tổng hợp qua hàm $\text{READOUT}$ để tạo ra $m_{\mathcal{G}_m}$, chính là **biểu diễn nhất quán ngữ nghĩa (*semantic consistency representation*)**:
    $$o = m_{\mathcal{G}_m}$$

---

### 4.3. Phân hệ 3: Học Bất biến Chu trình Đối kháng (Section 3.3 — Adversarial Cycle-Consistent Invariant Learning - ACCIL)

Phân hệ này (góc dưới bên phải Hình 3) gồm 2 mô-đun con: **Căn chỉnh chu trình thị giác - ngữ nghĩa (VSCA)** và **Trích xuất đặc trưng bất biến phương thức (Modality-Invariant Feature Extraction)** nhằm xử lý các thực thể không bắt cặp (*unmatched entities*) và triệt tiêu nhiễu đặc thù phương thức.

#### 4.3.1. Căn chỉnh Chu trình Thị giác - Ngữ nghĩa (Section 3.3.1 — Visual-Semantic Cycle Alignment - VSCA)

- Áp dụng mạng đối kháng nhất quán chu trình (*CycleGAN*) [63] kết hợp **khoảng cách Wasserstein (*Wasserstein distance*)** [38] để căn chỉnh nhúng thực thể từ đồ thị văn bản $\mathcal{G}_t$ và đồ thị thị giác $\mathcal{G}_v$ thông qua biến đổi miền phương thức.
- **Đưa đặc trưng suy luận thị giác (VRF) vào khoảng cách Wasserstein (**Công thức 8 trang 2491**):**
  $$W(\mathcal{G}_t, \mathcal{G}_v) = \inf_{\gamma \sim \Pi(\mathcal{G}_t, \mathcal{G}_v)} \mathbb{E}_{(u, w) \sim \gamma} \left[ wd(u, w) \cdot |w - u| \right] \quad (8)$$
  trong đó trọng số ngữ nghĩa đặc thù tác vụ giữa thực thể văn bản $u$ và thực thể thị giác $w$ được tính bằng độ tương đồng giữa hai vector VRF của chúng:
  $$wd(u, w) = \text{sim}\left(VRF_t(u), VRF_v(w)\right)$$
- **Hàm mất mát của bộ phân biệt $D_s$ (**Công thức 9 trang 2491**):**
  Bộ phân biệt $D_s$ phân biệt nhúng nút từ các phương thức khác nhau trong khi bộ trích xuất đặc trưng cực tiểu hóa khoảng cách Wasserstein:
  $$\mathcal{L}_{cycle} = -\mathbb{E}_{u \sim \mathcal{G}_t} \left[ D_s\left(u, VRF_t(u)\right) \right] + \mathbb{E}_{w \sim \mathcal{G}_v} \left[ D_s\left(w, VRF_v(w)\right) \right] \quad (9)$$
  với $\mathcal{L}_G^* = -\mathcal{L}_{D_s}^*$. Sau khi căn chỉnh, các biểu diễn thực thể được tổng hợp qua hàm $\text{READOUT}$ để thu được các biểu diễn phương thức thống nhất $e_v$ và $e_t$.

#### 4.3.2. Trích xuất Đặc trưng Bất biến Phương thức (Section 3.3.2 — Modality-Invariant Feature Extraction)

- Thiết kế **khung bộ phân biệt kép (*dual-discriminator framework* — gồm $D_0$ và $D_1$)**:
  - **Bộ phân biệt thứ nhất $D_0$:** Là một bộ phân loại nhị phân hoạt động trong không gian con tiềm ẩn chung, hướng dẫn tầng chiếu bất biến $I$:
    $$D_0(x) = \text{softmax}\left(D_0(I(x))\right)$$
    với $x = c = I(e)$, trong đó $e \in \{e_t, e_v\}$ là nhúng phương thức đã căn chỉnh, $I$ là tầng chiếu bất biến (*invariant projection layer*), và $c$ là đặc trưng bất biến phương thức sau khi chiếu.
  - Khi $D_0$ hoạt động tối ưu, $D_0^i(x)$ cho biết xác suất mẫu thuộc về phương thức $i$. Từ đó xác định **trọng số bất biến phương thức (*modality-invariant weighting*)**:
    $$w_i(x) = 1 - D_0^i(x)$$
    (Nếu $D_0$ càng dễ nhận ra mẫu thuộc phương thức $i$, tức $D_0^i(x)$ lớn, thì đặc trưng đó càng mang tính đặc thù phương thức nên nhận trọng số bất biến $w_i(x)$ nhỏ; ngược lại nếu $D_0$ bị đánh lừa, trọng số bất biến $w_i(x)$ sẽ lớn).
  - **Bộ phân biệt thứ hai $D_1$ và trò chơi đối kháng Minimax có trọng số (**Công thức 10 trang 2491**):**
    Theo [49], cực tiểu hóa phân kỳ Jensen-Shannon (JSD) thông qua trò chơi minimax với bộ phân biệt thứ hai $D_1$ (trong đó $w(x)$ độc lập với $D_1$, còn $p_{e_t}$ và $p_{e_v}$ là phân phối của hai phương thức):
    $$\min_I \max_{D_1} \mathcal{L}_{D_1} = \mathbb{E}_{e \sim p_{e_t}} \left[ w_t(x) \log\left(D_1(I(e))\right) \right] + \mathbb{E}_{e \sim p_{e_v}} \left[ w_v(x) \log\left(1 - D_1(I(e))\right) \right] \quad (10)$$
  - **Nghiệm tối ưu của $D_1$ với $I$ và $D_0$ cố định (**Công thức 11 trang 2491**):**
    $$D_1^{i*}(x) = \frac{w_i(x) p_{e_i}(x)}{w_t(x) p_{e_t}(x) + w_v(x) p_{e_v}(x)} \quad (11)$$
  - **Thay điều kiện $D_1^*$ vào trò chơi minimax (**Công thức 12 trang 2491**):**
    $$\mathcal{L}_{D_1} = -\log(10) + 2 \cdot \text{JSD}\left( w_t(x) \cdot p_{e_t}(x) \parallel w_v(x) \cdot p_{e_v}(x) \right) \quad (12)$$
    Phân kỳ Jensen-Shannon (JSD) đạt cực tiểu toàn cục khi hai phân phối có trọng số bằng nhau: $w_t(x) p_{e_t}(x) = w_v(x) p_{e_v}(x)$.
  - **Tổng hợp đặc trưng bất biến phương thức $c_m$:**
    Với $w_i(x) = w_i(I(e_i))$ và $p_{e_i} = I(e_i) = c_i$, thu được biểu diễn bất biến phương thức $c_m$ bằng phép gộp cực đại (*max-pooling*) trên các đặc trưng đã nhân trọng số:
    $$c_m = \max\{w_t c_t, w_v c_v\}$$
  - **Hàm mất mát của toàn bộ phân hệ đối kháng ACCIL:**
    $$\mathcal{L}_{adv} = \mathcal{L}_{D_0} + \mathcal{L}_{D_1} + \mathcal{L}_{cycle}$$

#### 4.3.3. Phân loại Tin giả Cuối cùng và Hàm Mất mát Tổng thể (Công thức 13 trang 2491)

- Biểu diễn bản tin cuối cùng $\hat{x}$ là phép ghép nối (*concatenation* $\oplus$) giữa đặc trưng đồ thị đa phương thức nhất quán ngữ nghĩa ($o$) và đặc trưng bất biến phương thức ($c_m$):
  $$\hat{x} = o \oplus c_m$$
- Đưa $\hat{x}$ qua tầng kết nối đầy đủ (*fully connected layer*) để dự đoán phân phối nhãn $\hat{y}$ và tối ưu hóa hàm mất mát Cross-Entropy $\mathcal{L}_y$ (**Công thức 13 trang 2491**):
  $$\hat{y} = \text{softmax}(w \hat{x} + b), \quad \mathcal{L}_y = -y \log(\hat{y}) - (1 - y) \log(1 - \hat{y}) \quad (13)$$
- **Hàm mất mát tổng thể của toàn mô hình CMA-VRP:**
  $$\mathcal{L}_{total} = \mathcal{L}_y + \lambda \mathcal{L}_{cl} + \beta \mathcal{L}_{adv}$$
  trong đó $\lambda$ và $\beta$ là hai siêu tham số cân bằng (trong thực nghiệm đặt **$\lambda = 0.5$** và **$\beta = 0.1$**).

---

## 5. Thiết lập Thực nghiệm và Toàn bộ Kết quả Bài báo 2 (Section 4 & Section 5)

### 5.1. Bộ dữ liệu, Baselines và Chi tiết Huấn luyện (Section 4 trang 2491–2492)

- **Ba bộ dữ liệu thực tế (Datasets):**
  1. **Twitter** (MediaEval Verifying Multimedia Use task [1]):
     - Tập huấn luyện (*Training*): **7.898 tin thật (*real*)** và **6.026 tin giả (*fake*)**.
     - Tập kiểm thử (*Testing*): **1.972 tin thật** và **3.830 tin giả**.
  2. **Pheme** [41]: Bộ dữ liệu xác minh tin tức mạng xã hội từ 5 sự kiện thời sự nóng (*five breaking stories*), gồm **1.972 mẫu tin thật** và **3.830 mẫu tin giả**, với **3.670 hình ảnh**.
  3. **Weibo** [19]: Bộ dữ liệu phát hiện tin giả tiếng Trung trên mạng xã hội Weibo:
     - Tập huấn luyện (*Training*): **6.840 tin thật** và **5.007 tin giả**.
     - Tập kiểm thử (*Testing*): **996 tin thật** và **1.000 tin giả**.
- **Mười mô hình đối sánh (Baselines — chia làm 4 nhóm):**
  - *Nhóm 1 — Mô hình đơn phương thức (Unimodal models):*
    1. **BERT** [9]: Mô hình Transformer cho văn bản.
    2. **ResNet34** [42]: Mạng tích chập cho phân loại hình ảnh.
  - *Nhóm 2 — Phương pháp căn chỉnh và dung hợp đa phương thức sâu (Cross-modal alignment & fusion):*
    3. **MVAE** [20]: Multimodal Variational Autoencoder học biểu diễn chung ảnh - văn bản.
    4. **CFFN** [22]: Mạng căn chỉnh ngữ nghĩa thị giác và văn bản qua tính nhất quán cặp từ - vùng ảnh (*word-region pair consistency*).
    5. **Event-Radar** [33] (ACL 2024): Phát hiện tin giả qua sự bất đồng cấp sự kiện (*event-level inconsistencies*) và tích hợp đặc trưng đa góc nhìn (*multi-view feature integration*).
    6. **InfoSurgeon** [11] (ACL 2021): Kiểm tra tính nhất quán thông tin chi tiết liên phương tiện trên đồ thị tri thức.
    7. **COOLANT** [51] (ACM MM 2023): Sử dụng học tương phản liên phương thức và cơ chế chú ý.
  - *Nhóm 3 & 4 — Các mô hình dựa trên LVLM và LVLM tinh chỉnh (LLM/LVLM-based methods):*
    8. **LLaVA** [27]: LVLM mạnh dựa trên tinh chỉnh chỉ dẫn thị giác.
    9. **LLaVA + SPT** [21]: Tích hợp kỹ thuật tinh chỉnh gợi ý mềm (*Soft Prompt Tuning - SPT*).
    10. **NLIN** [60] (IJCAI 2024): Thống nhất tin tức đa phương thức vào không gian ngôn ngữ tự nhiên bằng kiến trúc mã hóa - giải mã kèm prompt.
- **Chi tiết Cài đặt và Siêu tham số (Implementation Details — trang 2492):**
  - Phân tích cú pháp câu: **spaCy (`en_core_web_trf`)** (kết hợp Stanford NLP / TexSmart).
  - Khởi tạo đặc trưng văn bản: **BERT-base-Uncased** [48].
  - Đặc trưng thị giác: Mô hình sinh đồ thị cảnh (*scene graph generation*) [44] với Mask-RCNN.
  - Suy luận thị giác (VRP): **Mistral-7B** [18] (cho thực thể văn bản) và **LLaVA-1.6-13B** [27] (cho thực thể thị giác).
  - Huấn luyện: Tốc độ học ban đầu **`learning_rate = 0.001`** (hệ số suy giảm `decay = 0.5`), dừng sớm (*early stopping*) sau **5/50 epochs**.
  - Xác suất che thực thể trong học tương phản nội đồ thị: **$p_m = 0.2$**.
  - Số tầng dung hợp đồ thị: **$L = 2$**.
  - Trọng số hàm mất mát: **$\lambda = 0.5$**, **$\beta = 0.1$**.

---

### 5.2. Kết quả Thực nghiệm Tổng thể trên 3 Bộ dữ liệu (Section 4.1 — Table 1 trang 2492)

Dưới đây là **toàn bộ bảng số liệu nguyên bản từ Bảng 1 (Table 1: Experimental results on Twitter, Pheme, and Weibo datasets)** của Bài báo 2 (ký hiệu `*` biểu thị kiểm định ý nghĩa thống kê vượt qua Event-Radar và COOLANT với $p < 0.05$):

#### Bảng 1A: Kết quả trên bộ dữ liệu **Twitter**

| Phương pháp (Method) | Accuracy | Fake News Precision | Fake News Recall | Fake News F1-score | Real News Precision | Real News Recall | Real News F1-score |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **BERT** | 0.629 | 0.801 | 0.489 | 0.608 | 0.575 | 0.750 | 0.651 |
| **ResNet34** | 0.550 | 0.535 | 0.534 | 0.534 | 0.513 | 0.513 | 0.513 |
| **MVAE** | 0.757 | 0.831 | 0.661 | 0.772 | 0.738 | 0.713 | 0.772 |
| **CFFN** | 0.886 | 0.898 | 0.884 | 0.882 | 0.887 | 0.882 | 0.889 |
| **Event-Radar** | 0.902 | 0.892 | 0.903 | 0.901 | 0.932 | 0.883 | 0.910 |
| **InfoSurgeon** | 0.855 | 0.851 | 0.849 | 0.850 | 0.859 | 0.858 | 0.859 |
| **COOLANT** | 0.908 | 0.904 | 0.902 | 0.903 | 0.912 | 0.911 | 0.912 |
| **LLaVA** | 0.641 | 0.687 | 0.584 | 0.680 | 0.613 | 0.632 | 0.624 |
| **LLaVA+SPT** | 0.783 | 0.813 | 0.693 | 0.790 | 0.743 | 0.785 | 0.774 |
| **NLIN** | 0.883 | 0.916 | 0.796 | 0.893 | 0.875 | 0.888 | 0.867 |
| **CMA-VRP (Ours)** | **$0.930^*$** | **$0.938$** | **$0.923^*$** | **$0.926^*$** | **$0.934^*$** | **$0.945$** | **$0.932^*$** |

#### Bảng 1B: Kết quả trên bộ dữ liệu **Pheme**

| Phương pháp (Method) | Accuracy | Fake News Precision | Fake News Recall | Fake News F1-score | Real News Precision | Real News Recall | Real News F1-score |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **BERT** | 0.713 | 0.875 | 0.563 | 0.682 | 0.649 | 0.824 | 0.725 |
| **ResNet34** | 0.649 | 0.751 | 0.439 | 0.568 | 0.535 | 0.710 | 0.611 |
| **MVAE** | 0.776 | 0.801 | 0.749 | 0.795 | 0.745 | 0.746 | 0.798 |
| **CFFN** | 0.869 | 0.872 | 0.877 | 0.854 | 0.872 | 0.869 | 0.874 |
| **Event-Radar** | 0.901 | **0.920** | 0.822 | 0.831 | 0.905 | 0.904 | 0.902 |
| **InfoSurgeon** | 0.859 | 0.799 | 0.780 | 0.829 | 0.833 | 0.823 | 0.847 |
| **COOLANT** | 0.883 | 0.860 | 0.903 | 0.881 | 0.904 | 0.864 | 0.882 |
| **LLaVA** | 0.664 | 0.734 | 0.623 | 0.698 | 0.638 | 0.617 | 0.627 |
| **LLaVA+SPT** | 0.792 | 0.796 | 0.793 | 0.810 | 0.793 | 0.787 | 0.785 |
| **NLIN** | 0.903 | 0.887 | 0.904 | 0.883 | 0.863 | 0.868 | 0.875 |
| **CMA-VRP (Ours)** | **$0.926^*$** | $0.913$ | **$0.916^*$** | **$0.927^*$** | **$0.922^*$** | **$0.927$** | **$0.926^*$** |

#### Bảng 1C: Kết quả trên bộ dữ liệu **Weibo**

| Phương pháp (Method) | Accuracy | Fake News Precision | Fake News Recall | Fake News F1-score | Real News Precision | Real News Recall | Real News F1-score |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **BERT** | 0.731 | 0.730 | 0.731 | 0.731 | 0.730 | 0.731 | 0.731 |
| **ResNet34** | 0.675 | 0.682 | 0.665 | 0.664 | 0.685 | 0.683 | 0.679 |
| **MVAE** | 0.820 | 0.855 | 0.780 | 0.816 | 0.791 | 0.861 | 0.825 |
| **CFFN** | 0.894 | 0.876 | 0.817 | 0.841 | 0.902 | 0.915 | 0.899 |
| **Event-Radar** | 0.910 | 0.881 | 0.862 | 0.891 | 0.915 | 0.914 | 0.910 |
| **InfoSurgeon** | 0.866 | 0.795 | 0.776 | 0.785 | 0.861 | 0.868 | 0.863 |
| **COOLANT** | 0.915 | 0.909 | 0.926 | 0.914 | 0.912 | **0.924** | 0.911 |
| **LLaVA** | 0.750 | 0.785 | 0.713 | 0.734 | 0.720 | 0.771 | 0.719 |
| **LLaVA+SPT** | 0.833 | 0.854 | 0.795 | 0.839 | 0.813 | 0.832 | 0.826 |
| **NLIN** | 0.911 | 0.913 | 0.914 | 0.904 | 0.907 | 0.917 | 0.913 |
| **CMA-VRP (Ours)** | **$0.938^*$** | **$0.933$** | **$0.942^*$** | **$0.941^*$** | **$0.929^*$** | $0.906$ | **$0.938^*$** |

**Phân tích chính từ Bảng 1:**

- CMA-VRP đạt Accuracy cao nhất trên cả 3 bộ dữ liệu: **93,0%** trên Twitter (vượt COOLANT 90,8% và Event-Radar 90,2%), **92,6%** trên Pheme (vượt NLIN 90,3% và Event-Radar 90,1%), và **93,8%** trên Weibo (vượt COOLANT 91,5% và NLIN 91,1%).
- BERT vượt ResNet34 trên cả 3 tập dữ liệu, cho thấy vai trò quan trọng của xử lý văn bản trong xác minh tin tức.
- Các mô hình LVLM dùng trực tiếp (`LLaVA` đạt 64,1% trên Twitter) hoặc tinh chỉnh (`LLaVA+SPT`, `NLIN`) dù có cải thiện nhưng vẫn kém hơn CMA-VRP do thiếu nhạy cảm với các biến thiên thực thể chi tiết và bị giới hạn khả năng tổng quát hóa khi fine-tune mô hình lớn.

---

### 5.3. Kiểm thử Độ Bền vững trước Nhiễu và Che khuất (Robustness Testing — Figure 4 trang 2492–2493)

Nhóm tác giả thực hiện 3 bài kiểm tra độ bền vững chuyên sâu (minh họa tại **Hình 4(a)–(f)**):

1. **Tiêm nhiễu Gaussian (*Gaussian Noise Injection* — Hình 4a trên Twitter, Hình 4b trên Weibo):**
   - Tiêm nhiễu Gaussian với cường độ (*Noise Intensity*) tăng dần theo thang logarit từ $0, 1, 10^1, 10^2, \dots, 10^8$ vào biểu diễn thực thể đa phương thức [32, 33] nhằm mô phỏng suy giảm chất lượng thông tin (văn bản nhiễu, ảnh mờ).
   - Kết quả: Khi cường độ nhiễu tăng lên $10^8$, mọi mô hình đối sánh đều suy giảm mạnh (dưới 0.50–0.70), nhưng đường biểu diễn của **CMA-VRP** giữ độ ổn định cao nhất và mức giảm Accuracy nhỏ nhất (vẫn duy trì quanh mức ~0.78–0.80 ở cường độ nhiễu cực đại).
2. **Che khuất Văn bản - Hình ảnh (*Text-Image Occlusion / Masking* — Hình 4c trên Twitter, Hình 4d trên Weibo):**
   - Trích xuất **500 mẫu** từ tập kiểm thử, che khuất (*occlude*) các vùng văn bản và hình ảnh với tỷ lệ che (*Mask Rate*) từ **0%, 10%, 20%, 30%, 40% đến 50%**, và lọc thủ công các mẫu giữ nguyên nhãn nhất quán trước và sau khi che khuất.
   - Kết quả: CMA-VRP vượt qua cả nhóm phương pháp học biểu diễn (COOLANT, Event-Radar, CFFN, InfoSurgeon, MVAE) lẫn nhóm phương pháp dựa trên LLM (NLIN, LLaVA+SPT, LLaVA) ở mọi mức tỷ lệ che khuất nhờ dung hợp đồ thị liên phương thức và suy luận thị giác VRF giúp suy diễn tính nhất quán logic từ phần thông tin còn lại.
3. **Phân tích Vai trò của ACCIL qua Khoảng cách Wasserstein (Hình 4e và Hình 4f):**
   - So sánh mô hình đầy đủ (`w ACCIL`) và biến thể bỏ ACCIL (`w/o ACCIL`) trên Twitter và Weibo khi tăng cường độ nhiễu từ $0$ đến $10^8$:
   - **Hình 4(e) — Tác động lên Accuracy:** Biến thể `w/o ACCIL` bị sụt giảm Accuracy rất dốc khi nhiễu vượt quá $10^3$, trong khi `w ACCIL` giữ đường Accuracy gần như phẳng hơn nhiều.
   - **Hình 4(f) — Mức tăng Khoảng cách Wasserstein (*WD Increase*):** Khoảng cách Wasserstein nhỏ hơn phản ánh độ chồng lấp phân phối cao hơn (căn chỉnh liên phương thức tốt hơn). Khi không có ACCIL (`w/o ACCIL`), WD tăng vọt và dao động mạnh (tăng thêm hơn $0.45$ ở mức nhiễu $10^8$), trong khi có ACCIL (`w ACCIL`) giữ mức tăng WD thấp hơn nhiều (chỉ quanh $\sim 0.30$), chứng minh ACCIL triệt tiêu hiện tượng trôi dạt ngữ nghĩa do nhiễu (*noise-induced semantic drift*).

---

### 5.4. Nghiên cứu Cắt bỏ (Ablation Analysis — Table 2 trang 2493)

Bảng 2 đánh giá đóng góp của từng thành phần kiến trúc trong CMA-VRP bằng cách loại bỏ từng thành phần riêng lẻ trên cả 3 bộ dữ liệu Twitter, Pheme và Weibo:

- `-w/o VRF`: Bỏ đặc trưng suy luận thị giác (*Visual Reasoning Features*).
- `-w/o GCL_inter`: Bỏ học tương phản liên đồ thị (*Inter-graph Contrastive Learning*).
- `-w/o GCL_intra`: Bỏ học tương phản nội đồ thị (*Intra-graph Contrastive Learning*).
- `-w/o CMGAF`: Bỏ toàn bộ mô-đun căn chỉnh và dung hợp đồ thị liên phương thức (*Cross-Modal Graph Alignment and Fusion*).
- `-w/o ACCIL`: Bỏ toàn bộ phân hệ học bất biến chu trình đối kháng (*Adversarial Cycle-Consistent Invariant Learning*).
- `-w/o VSCA`: Bỏ thành phần căn chỉnh chu trình thị giác - ngữ nghĩa (*Visual-Semantic Cycle Alignment*).

**Toàn bộ số liệu nguyên bản từ Bảng 2 (Table 2 trang 2493):**

| Mô hình / Biến thể (Model) | Twitter Accuracy | Twitter F1 score | Pheme Accuracy | Pheme F1 score | Weibo Accuracy | Weibo F1 score |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **CMA-VRP (Full)** | **0.930** | **0.929** | **0.926** | **0.926** | **0.938** | **0.940** |
| **-w/o VRF** | 0.905 | 0.902 | 0.902 | 0.900 | 0.912 | 0.911 |
| **-w/o $\text{GCL}_{inter}$** | 0.914 | 0.913 | 0.908 | 0.906 | 0.920 | 0.918 |
| **-w/o $\text{GCL}_{intra}$** | 0.920 | 0.921 | 0.910 | 0.911 | 0.916 | 0.919 |
| **-w/o CMGAF** | 0.895 | 0.895 | 0.887 | 0.894 | 0.896 | 0.893 |
| **-w/o ACCIL** | 0.908 | 0.901 | 0.896 | 0.898 | 0.914 | 0.909 |
| **-w/o VSCA** | 0.915 | 0.917 | 0.905 | 0.908 | 0.918 | 0.920 |

**Phân tích từ Bảng 2:**

- Việc loại bỏ **CMGAF (`-w/o CMGAF`)** gây sụt giảm hiệu năng lớn nhất trên cả 3 tập dữ liệu (Accuracy giảm xuống 0.895 trên Twitter, 0.887 trên Pheme, và 0.896 trên Weibo), chứng tỏ mô-đun căn chỉnh và dung hợp đồ thị liên phương thức đóng vai trò trụ cột.
- Loại bỏ **VRF (`-w/o VRF`)** làm Accuracy giảm từ 0.930 xuống 0.905 (Twitter), từ 0.926 xuống 0.902 (Pheme), và từ 0.938 xuống 0.912 (Weibo), khẳng định thông tin thị giác - ngữ nghĩa sâu từ LLM/LVLM thông qua VRP là tối quan trọng.
- Loại bỏ **ACCIL (`-w/o ACCIL`)** cũng làm giảm mạnh hiệu năng (giảm 2,2% trên Twitter, 3,0% trên Pheme, 2,4% trên Weibo), chứng minh vai trò thiết yếu của học bất biến chu trình đối kháng.

---

### 5.5. Phân tích Định tính bằng t-SNE (Section 4.2 — Qualitative Analysis, Figure 5 trang 2493)

- Sử dụng thuật toán **t-SNE** [47] để trực quan hóa các vector đặc trưng ngay trước tầng phân loại trên tập kiểm thử **Weibo** cho 6 cấu hình (**Hình 5(a)–(f)**):
  - **(a) `CMA-VRP`:** Hai cụm điểm màu cam (Fake/Real) và xanh dương tách biệt hoàn toàn với ranh giới phân lớp rất rõ ràng.
  - **(b) `w/o VRF`:** Ranh giới giữa hai cụm bắt đầu có vùng giao thoa ở giữa.
  - **(c) `w/o CMGAF`:** Ranh giới bị xóa nhòa nặng nề, hai cụm trộn lẫn vào nhau trên diện rộng.
  - **(d) `w/o ACCIL`:** Hai cụm bị kéo dãn và chồng lấn ở vùng biên.
  - **(e) `Noise` (CMA-VRP đầy đủ dưới nhiễu Gaussian cường độ $10^6$):** Vẫn bảo toàn được sự phân tách rõ rệt giữa hai lớp dù dưới tác động của nhiễu mạnh.
  - **(f) `Noise w/o ACCIL` (Không có ACCIL dưới nhiễu Gaussian $10^6$):** Các điểm dữ liệu của hai lớp bị phân tán hỗn loạn và chồng chéo hoàn toàn, minh chứng trực quan cho khả năng chống nhiễu của ACCIL.

---

### 5.6. Nghiên cứu Tình huống (Section 5 — Case Study, Figure 6 trang 2493)

- **Mẫu tin giả trong Hình 6:**
  - *Văn bản:* `"(Fake) David Bowie dressed as Tilda Swinton and Tilda dressed as David Bowie, a bizarre act that occurred after their relationship broke down due to creative differences."` (Tin giả tuyên bố mối quan hệ của họ đã tan vỡ do bất đồng sáng tạo).
  - *Các thực thể được trích xuất:*
    - Thực thể thị giác (màu cam): `Tilda Swinton`, `David Bowie`, `handbag`, `coat_1`, `coat_0`.
    - Thực thể văn bản (màu xanh lam): `Tilda Swinton`, `David Bowie`, `dressed`, `relationship`, `after`.
  - *Đặc trưng Suy luận Thị giác (Visual Reasoning Features):*
    - `coat_0`: *"Light-colored, loose-fitting, with a decorative collar as a focal point. Minimalist yet stylish..."*
    - `handbag`: *"As part of a woman's accessories, it reinforces the feminine image."*
    - `David Bowie` (thị giác): *"Neat hair, long coat, formal attire, and a calm expression, resembling David Bowie's public image."*
    - `David Bowie` (văn bản): *"A very famous musician, which makes the audience associate him with his iconic slicked-back hairstyle and high cheekbones..."*
  - *Quan hệ thực thể thị giác (Visual Entity Relation):*
    - `(Tilda Swinton, holding, David Bowie)`, `(Tilda Swinton, wearing, coat_0)`, `(Tilda Swinton, holding, handbag)`, `(David Bowie, wearing, coat_1)`.
  - *Quan hệ thực thể văn bản (Textual Entity Relation):*
    - `(Tilda Swinton, nsubj, dressed)`, `(relationship, pobj, after)`, `(Tilda Swinton, conj, David Bowie)`.
  - **Cơ chế phát hiện của CMA-VRP:** Đồ thị liên phương thức nắm bắt được mối quan hệ chi tiết giữa các thực thể thị giác như `(Tilda Swinton, holding hands / holding, David Bowie)` cùng biểu cảm thân thiết, điềm tĩnh — mâu thuẫn trực tiếp với tuyên bố trong văn bản rằng mối quan hệ của họ đã tan vỡ (*"their relationship broke down"*), giúp mô hình phân loại chính xác đây là **Tin giả (Fake)**.

---

# PHẦN III: TỔNG HỢP MỐI LIÊN HỆ KHOA HỌC GIỮA HAI BÀI BÁO

Mặc dù **Bài báo 1 (MSIT — ACL 2025)** giải quyết bài toán *Khai thác Thuộc tính Sản phẩm Thương mại Điện tử Thế giới Mở* và **Bài báo 2 (CMA-VRP — ACM MM 2025)** giải quyết bài toán *Phát hiện Tin giả Đa phương thức trên Mạng xã hội*, khi đặt cạnh nhau trong cùng một khung nghiên cứu về **Trí tuệ Nhân tạo Đa phương thức (Multimodal AI & Vision-Language Reasoning)**, hai công trình thể hiện sự giao thoa và bổ trợ sâu sắc trên **5 trục phương pháp luận**:

| Trục phân tích | Bài báo 1: MSIT (ACL 2025) | Bài báo 2: CMA-VRP (ACM MM 2025) | Điểm giao thoa & Bổ trợ học thuật |
| :--- | :--- | :--- | :--- |
| **1. Bản chất bài toán đa phương thức** | **Trích xuất & Sinh cấu trúc mở (*Open-World Generative Extraction*):** Từ $(I, T)$ sinh tập cặp `{attribute: value}` không giới hạn lược đồ. | **Căn chỉnh & Kiểm chứng tính xác thực (*Cross-Modal Verification & Classification*):** Từ $(I, T)$ phát hiện mâu thuẫn ngữ nghĩa tinh vi để phân loại `Real/Fake`. | Cả hai đều xuất phát từ thực tế rằng thông tin cốt lõi nằm rải rác hoặc ẩn sâu trong tương tác giữa **Hình ảnh** và **Văn bản**, nơi phương pháp đơn phương thức hoặc đặc trưng nông thất bại. |
| **2. Giải quyết thiên lệch phương thức (Modality Bias)** | Phát hiện GPT-4 bị thiên lệch chú ý vào văn bản khi đưa ảnh và text vào cùng lúc $\rightarrow$ **Tách riêng từng phương thức (*Modality-Separated ICL*)** khi sinh dữ liệu AGTD rồi mới hợp nhất. | Phát hiện nhiễu giao thoa liên phương thức (*cross-modal interference*) $\rightarrow$ **Tách riêng 2 tầng VRP**: dùng **Mistral-7B** cho thực thể văn bản và **LLaVA-1.6-13B** cho thực thể thị giác, kết hợp xây dựng 2 đồ thị $\mathcal{G}_t, \mathcal{G}_v$ độc lập trước khi dung hợp. | Cùng chia sẻ nguyên lý thiết kế: **Khởi tạo/Khai thác độc lập trên từng phương thức trước, hợp nhất/căn chỉnh liên phương thức sau** để tránh một phương thức lấn át phương thức kia. |
| **3. Suy luận Chuỗi Tư duy (Chain-of-Thought) chống Ảo giác** | Thay thế Vanilla CoT bằng **Quy trình CoT 5 bước có cấu trúc** (Loại SP $\rightarrow$ Tri thức thông thường $\rightarrow$ Kiểm chứng ảnh $\rightarrow$ Kiểm chứng văn bản $\rightarrow$ Kết luận Yes/No) để tự sửa lỗi dương tính giả. | Sử dụng **Truth-Driven CoT-based Visual Reasoning Prompting (VRP) 2 bước** (Sinh lập luận kiểm chứng $\rightarrow$ Tóm tắt đặc trưng thị giác kỳ vọng/thực tế) mà không cần fine-tune LVLM để tránh ảo giác. | Cả hai đều chứng minh việc dùng trực tiếp MLLM/LVLM hoặc Vanilla CoT sinh ra ảo giác (*hallucinations*), và giải quyết bằng **CoT phân rã theo bước có định hướng kiểm chứng**. |
| **4. Học Tương phản (Contrastive Learning)** | Xây dựng **Contrastive CoT Tuning Data** cân bằng 1:1 giữa mẫu dương (thuộc tính đúng của SP) và mẫu âm (thuộc tính lấy từ loại SP khác) để chống quá khớp. | Thiết kế **Graph Contrastive Learning kép**: Liên đồ thị ($\mathcal{L}_{inter}$ với tham số làm mượt $\theta$) và Nội đồ thị ($\mathcal{L}_{intra}$ với Entity Masking $p_m=0.2$ để tạo mẫu dương và trộn phương thức nhãn đối lập $d(\cdot)$ để tạo mẫu âm). | Đều sử dụng kỹ thuật **tạo mẫu âm bằng cách hoán đổi/lấy chéo thuộc tính hoặc thực thể từ mẫu khác** nhằm buộc mô hình học ranh giới ngữ nghĩa sắc bén. |
| **5. Cơ chế Lọc nhiễu và Tinh lọc Đa tầng** | **3-Stage Inference:** Giai đoạn 2 dùng Word2Vec + 3 quy tắc độ dài subword để lọc dư thừa; Giai đoạn 3 dùng CoT 5 bước để lọc thuộc tính sai (đạt tỷ lệ tự sửa lỗi 98,6%). | **ACCIL (CycleGAN Wasserstein + Dual-Discriminator JSD):** Biến đổi miền phương thức có trọng số VRF và bộ phân biệt kép $D_0, D_1$ để lọc nhiễu mạng xã hội (watermark, ảnh mờ, hashtag rác). | MSIT lọc nhiễu ở **không gian đầu ra rời rạc (symbolic/output space)** qua quy tắc từ vựng và CoT, trong khi CMA-VRP lọc nhiễu ở **không gian biểu diễn liên tục (latent representation space)** qua học đối kháng chu trình. |

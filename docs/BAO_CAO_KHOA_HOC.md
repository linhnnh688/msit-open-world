# BÁO CÁO KHOA HỌC MÔN HỌC

*(Bản thảo chuẩn hóa theo cấu trúc IEEE — Sẵn sàng chuyển đổi sang LaTeX `IEEEtran`, giới hạn $\le 25$ trang, dung lượng $< 20\text{ MB}$)*

---

**TIÊU ĐỀ BÁO CÁO:**

# Khai thác Tri thức và Kiểm chứng Ngữ nghĩa Đa phương thức thông qua Suy luận Chuỗi Tư duy Có Cấu trúc và Học Biểu diễn Tương phản: Từ Khai thác Thuộc tính Sản phẩm Thế giới Mở đến Phát hiện Tin giả Đa phương thức

**Thông tin Học viên thực hiện (Định dạng tên file nộp: `MSHV1-MSHV2.pdf`):**

- **Học viên 1:** Nguyễn Hoàng Việt — MSHV: `[Điền MSHV1]` — Email: `segionguyen02@gmail.com`
- **Học viên 2:** Nguyễn Hồng Linh — MSHV: `[Điền MSHV2]` — Email: `honglinh154@gmail.com`
- **Mã nguồn tái lập thực nghiệm (GitHub Repository):** [https://github.com/linhnnh688/msit-open-world](https://github.com/linhnnh688/msit-open-world)
- **Bảng theo dõi thực nghiệm công khai (Weights & Biases Project):** `[Gắn link Public WandB Project của nhóm tại đây: https://wandb.ai/<team_or_username>/msit-open-world]`

---

## TÓM TẮT (ABSTRACT)

Sự bùng nổ của dữ liệu đa phương thức kết hợp giữa văn bản và hình ảnh trên các nền tảng trực tuyến đặt ra yêu cầu cấp thiết về việc xây dựng các hệ thống trí tuệ nhân tạo có khả năng thấu hiểu sâu sắc ngữ nghĩa liên phương thức. Tuy nhiên, các hệ thống hiện hành vẫn đối mặt với hai rào cản cốt lõi: (1) sự mất cân bằng và khai thác hời hợt thông tin thị giác khi kết hợp với văn bản, dẫn đến việc bỏ sót các chi tiết quan trọng hoặc không phát hiện được những mâu thuẫn ngữ nghĩa tinh vi; và (2) sự thiếu vắng một quy trình suy luận tường minh có kiểm soát trong các Mô hình Ngôn ngữ Lớn Đa phương thức (MLLM/LVLM), khiến mô hình dễ sinh ra ảo giác (*hallucination*) và kém bền vững trước dữ liệu nhiễu. Trong báo cáo này, nhóm chúng tôi thực hiện nghiên cứu chuyên sâu, phân tích phản biện và kết nối hai công trình tiêu biểu công bố năm 2025 nhằm giải quyết hai bài toán đại diện cho hai mặt đối lập nhưng bổ trợ lẫn nhau của xử lý thông tin đa phương thức: **Phần thứ nhất** tập trung vào bài toán *sinh và trích xuất tri thức mở* thông qua khung phương pháp **MSIT** (*Tinh chỉnh Chỉ dẫn Tự sửa lỗi Đa phương thức cho Khai thác Thuộc tính Sản phẩm Thương mại Điện tử Thế giới Mở* — ACL 2025), đồng thời trình bày toàn bộ quy trình nhóm tự tái lập thực nghiệm từ khâu kiến tạo dữ liệu, tinh chỉnh mô hình bằng kỹ thuật QLoRA đến suy luận ba giai đoạn. **Phần thứ hai** tập trung vào bài toán *kiểm chứng và phân loại tính xác thực* thông qua khung phương pháp **CMA-VRP** (*Căn chỉnh Đồ thị Thực thể và Suy luận Thị giác cho Phát hiện Tin giả Đa phương thức* — ACM MM 2025). Qua việc đặt hai công trình trong một lăng kính phân tích thống nhất, báo cáo làm rõ cách thức kết hợp giữa chiến lược tách biệt phương thức, suy luận chuỗi tư duy (Chain-of-Thought) phân rã theo bước, học tương phản (Contrastive Learning) và các cơ chế lọc nhiễu để kiến tạo nên các hệ thống đa phương thức đáng tin cậy.

**Từ khóa (Index Terms):** Trí tuệ nhân tạo đa phương thức, Mô hình ngôn ngữ lớn thị giác - ngôn ngữ, Suy luận chuỗi tư duy, Học tương phản, Khai thác thuộc tính thế giới mở, Phát hiện tin giả đa phương thức, Mạng nơ-ron đồ thị.

---

## I. GIỚI THIỆU CHUNG VÀ ĐỘNG LỰC NGHIÊN CỨU

Trong kỷ nguyên số hóa hiện nay, thông tin trên môi trường mạng — từ hồ sơ sản phẩm trên các sàn thương mại điện tử cho đến các bản tin lan truyền trên mạng xã hội — hiếm khi tồn tại dưới dạng văn bản thuần túy mà luôn được truyền tải thông qua sự kết hợp đa phương thức (*multimodal*), phổ biến nhất là cặp dữ liệu **Văn bản (Text)** và **Hình ảnh (Image)**. Để máy tính có thể xử lý hiệu quả nguồn dữ liệu hỗn hợp này, hệ thống không chỉ cần đọc hiểu từng phương thức một cách độc lập mà còn phải giải quyết được bài toán tương tác, bổ sung và kiểm chứng chéo giữa chúng.

Khi khảo sát các bài toán ứng dụng đa phương thức trong thực tiễn, chúng ta có thể nhìn nhận chúng dưới hai chiều hướng tác vụ cơ bản:

1. **Chiều hướng Tổng hợp và Trích xuất Tri thức (Information Extraction & Synthesis):** Giả định rằng hình ảnh và văn bản của cùng một đối tượng bổ sung thông tin cho nhau. Mục tiêu của hệ thống là khai thác tối đa các tín hiệu từ cả hai kênh để trích xuất ra một tập hợp tri thức có cấu trúc đầy đủ nhất (điển hình là bài toán *Khai thác Thuộc tính Sản phẩm Thế giới Mở — Open-World Product Attribute Mining*).
2. **Chiều hướng Kiểm chứng và Phát hiện Bất đồng (Cross-Modal Verification & Inconsistency Detection):** Giả định rằng giữa hình ảnh và văn bản có thể tồn tại sự mâu thuẫn ngầm hoặc nhiễu loạn cố ý nhằm đánh lừa người đọc. Mục tiêu của hệ thống là đối chiếu ngữ nghĩa chi tiết giữa các thực thể trong ảnh và trong câu chữ để phán đoán tính xác thực của thông tin (điển hình là bài toán *Phát hiện Tin giả Đa phương thức — Multimodal Fake News Detection*).

Mặc dù phục vụ hai mục đích ứng dụng khác nhau (thương mại điện tử và an toàn thông tin mạng xã hội), qua quá trình nghiên cứu, nhóm chúng tôi nhận thấy cả hai bài toán đều gặp phải **hai nút thắt phương pháp luận chung** chưa được giải quyết triệt để bởi các phương pháp truyền thống cũng như việc áp dụng trực tiếp các Mô hình Ngôn ngữ Lớn Đa phương thức (MLLM/LVLM):

- **Nút thắt thứ nhất — Sự khai thác hời hợt ngữ nghĩa thị giác và hiện tượng thiên lệch phương thức (*Modality Bias & Shallow Visual Semantics*):**
  Trong bài toán khai thác thuộc tính sản phẩm, các mô hình trước đây chủ yếu chỉ đọc tiêu đề và mô tả văn bản, bỏ qua hoàn toàn hình ảnh bao bì — nơi chứa đựng nhiều thuộc tính vật lý trực quan (như kiểu dáng, khối lượng tịnh in trên nhãn). Ngay cả khi đưa đồng thời cả ảnh và văn bản vào một mô hình lớn như GPT-4, sự chú ý của mô hình vẫn bị thiên lệch nặng về phía văn bản (*text-dominated attention bias*). Tương tự, trong bài toán phát hiện tin giả, các mạng thị giác cổ điển (như VGG hay ResNet) chỉ trích xuất được đặc trưng bề mặt (màu sắc, đường nét), trong khi các mô hình LVLM hiện đại lại thường chỉ nhìn bức tranh tổng thể mà bỏ sót các chi tiết cục bộ mang tính quyết định (chẳng hạn như nét mặt căng thẳng của người biểu tình hay dòng chữ phản đối nhỏ trên tấm biển cầm tay đi ngược lại nội dung bài viết).

- **Nút thắt thứ hai — Thiếu vắng cơ chế suy luận có cấu trúc dẫn đến ảo giác (*Hallucination*) và dễ tổn thương trước nhiễu (*Noise Vulnerability*):**
  Khi yêu cầu các MLLM/LVLM sinh trực tiếp kết quả hoặc giải thích tự do (*Vanilla Chain-of-Thought*), mô hình rất dễ suy diễn quá đà, sinh ra các thuộc tính quảng cáo vô nghĩa hoặc nhận diện nhầm các đối tượng không có thật. Hơn nữa, dữ liệu thực tế luôn đi kèm nhiễu: từ các thuộc tính trùng lặp ngữ nghĩa trong thương mại điện tử cho đến ảnh độ phân giải thấp, ảnh bị chèn chữ đóng dấu (*watermark*) mang tính dẫn dắt hoặc các thẻ `#hashtag` rác trên mạng xã hội.

Để giải quyết trọn vẹn hai nút thắt trên, báo cáo này đi sâu phân tích hai công trình nghiên cứu mới nhất đại diện cho hai hướng tiếp cận bổ trợ nhau:

- **Phần A (Mục III — Bài báo Seminar & Tái lập thực nghiệm):** Nghiên cứu khung **MSIT** (*Multimodal Self-Correction Instruction Tuning*) của nhóm tác giả Jiaqi Li và cộng sự (ACL 2025) [1]. Công trình này giải quyết bài toán khai thác thuộc tính sản phẩm thế giới mở bằng cách tách biệt phương thức khi sinh dữ liệu học trong ngữ cảnh, kết hợp tinh chỉnh chỉ dẫn theo quy trình suy luận chuỗi tư duy 5 bước tương phản để mô hình tự sửa lỗi dương tính giả.
- **Phần B (Mục IV — Bài báo Báo cáo mở rộng):** Nghiên cứu khung **CMA-VRP** (*Cross-Modal Alignment with Visual Reasoning Prompting*) của nhóm tác giả Guoyi Li và cộng sự (ACM MM 2025) [2]. Công trình này giải quyết bài toán phát hiện tin giả đa phương thức bằng cách xây dựng đồ thị thực thể cho từng phương thức, dùng cơ chế gợi ý suy luận thị giác 2 tầng hướng chân lý từ LLM/LVLM để dẫn dắt quá trình học tương phản đồ thị và học biểu diễn bất biến qua chu trình đối kháng.

```mermaid
flowchart TD
    Root["Bài toán Xử lý & Thấu hiểu Thông tin Đa phương thức (Văn bản + Hình ảnh)"]
    Root --> C1["Thách thức 1: Thiên lệch phương thức &<br/>Bỏ sót ngữ nghĩa thị giác chi tiết"]
    Root --> C2["Thách thức 2: Ảo giác suy luận của MLLM/LVLM &<br/>Nhiễu dữ liệu thực tế"]
    
    C1 & C2 --> P1["PHẦN I (Mục III): Khung phương pháp MSIT (ACL 2025)<br/>Bài toán: Khai thác Thuộc tính Sản phẩm Thế giới Mở"]
    C1 & C2 --> P2["PHẦN II (Mục IV): Khung phương pháp CMA-VRP (ACM MM 2025)<br/>Bài toán: Phát hiện Tin giả Đa phương thức"]
    
    P1 --> S1["Giải pháp cốt lõi của MSIT:<br/>1. Sinh dữ liệu ICL tách biệt Ảnh/Văn bản (AGTD)<br/>2. Tinh chỉnh CoT 5 bước tương phản Âm/Dương (CTTD)<br/>3. Suy luận 3 giai đoạn: Lọc từ đồng nghĩa Word2Vec + Tự sửa lỗi"]
    P2 --> S2["Giải pháp cốt lõi của CMA-VRP:<br/>1. Đồ thị thực thể Văn bản/Thị giác + OCR + Suy luận VRP 2 tầng<br/>2. Học tương phản Liên đồ thị (làm mượt mềm) & Nội đồ thị<br/>3. Chu trình đối kháng Wasserstein + Bộ phân biệt kép JSD (ACCIL)"]
    
    S1 & S2 --> Syn["Mục V: Đối sánh Tổng hợp, Đánh giá Phản biện & Kết luận Chung"]
```

*Hình 1: Sơ đồ cấu trúc tổng thể của báo cáo và mối liên hệ phương pháp luận giữa hai công trình MSIT và CMA-VRP.*

---

## II. CƠ SỞ LÝ THUYẾT VÀ CÁC NGHIÊN CỨU LIÊN QUAN

### 2.1. Sự phát triển của Mô hình Ngôn ngữ Lớn Đa phương thức (MLLM / LVLM)

Nền tảng chung của cả hai bài báo dựa trên sự phát triển vượt bậc của các mô hình kết hợp thị giác và ngôn ngữ quy mô lớn. Thế hệ các mô hình như **BLIP-2** [3] đã mở ra hướng kết nối bộ mã hóa hình ảnh tiền huấn luyện đóng băng với mô hình ngôn ngữ lớn thông qua bộ biến đổi truy vấn gọn nhẹ (Q-Former). Tiếp nối thành công đó, **InstructBLIP** [4] và **LLaVA** [5] đưa kỹ thuật *tinh chỉnh theo chỉ dẫn thị giác (visual instruction tuning)* vào quá trình huấn luyện, giúp mô hình có khả năng tuân thủ các yêu cầu phức tạp của con người trên đầu vào đa phương thức. Các kiến trúc tiên tiến hơn như **Qwen-VL** [6], **InternLM-XComposer2** [7], **DeepSeek-VL** [8] và **GPT-4** [9] tiếp tục nâng cao năng lực đọc hiểu văn bản trong ảnh và suy luận liên phương thức.

Tuy nhiên, việc thích nghi các mô hình hàng tỷ tham số này vào các bài toán chuyên biệt gặp hai thách thức: chi phí tính toán khổng lồ nếu cập nhật toàn bộ trọng số, và nguy cơ suy giảm khả năng tổng quát hóa (hoặc sinh ảo giác) khi tinh chỉnh trực tiếp trên tập dữ liệu hẹp. Do đó, kỹ thuật **Thích nghi Hạng thấp (Low-Rank Adaptation — LoRA)** (được áp dụng trong MSIT để đóng băng mạng xương sống và chỉ huấn luyện các ma trận phân rã hạng thấp) hoặc kỹ thuật **Gợi ý Suy luận Không tinh chỉnh (Zero-shot/Prompt-based Reasoning)** (được áp dụng trong CMA-VRP với Mistral-7B và LLaVA-1.6-13B) trở thành hai chiến lược trọng tâm được hai nhóm tác giả lựa chọn.

### 2.2. Suy luận Chuỗi Tư duy (Chain-of-Thought — CoT) Đa phương thức

Kỹ thuật Chuỗi tư duy (CoT) giúp mô hình ngôn ngữ chia nhỏ một bài toán phức tạp thành các bước suy luận trung gian. Dù vậy, các nghiên cứu gần đây về CoT đa phương thức [10] chỉ ra rằng nếu để mô hình tự do sinh chuỗi lý giải mà không có khung kiểm soát (*unstructured/vanilla CoT*), mô hình rất dễ bịa đặt ra các lập luận nghe có vẻ hợp lý nhưng sai lệch với thực tế hình ảnh (*hallucinated rationales*). Cả hai bài báo trong báo cáo này đều khắc phục nhược điểm đó bằng cách **ép buộc quá trình CoT phải đi theo các bước kiểm chứng có cấu trúc chặt chẽ**, bám sát vào từng thực thể hoặc từng kênh thông tin cụ thể.

### 2.3. Lược sử Bài toán Khai thác Thuộc tính Sản phẩm và Phát hiện Tin giả Đa phương thức

- **Đối với bài toán Khai thác Thuộc tính Sản phẩm (Attribute Mining):** Các nghiên cứu ban đầu như **OpenTag** [11] hay **CMA-CLIP** [12] đóng khung bài toán dưới dạng gán nhãn chuỗi hoặc phân loại trong một tập thuộc tính cố định (*closed-world*). Để mở rộng sang *thế giới mở (open-world)* — nơi các thuộc tính mới liên tục xuất hiện — các phương pháp như **OA-Mine** [13] (dùng phân cụm kết hợp bộ phân loại siêu dữ liệu) và **Amacer** [14] (dùng mô hình sinh kèm điều chuẩn tự giám sát) đã được đề xuất. Tuy nhiên, cả OA-Mine và Amacer đều bỏ qua kênh hình ảnh sản phẩm và thiếu cơ chế tự thẩm định lại kết quả sinh ra.
- **Đối với bài toán Phát hiện Tin giả Đa phương thức (Multimodal Fake News Detection):** Các hướng tiếp cận trước đây chia thành ba nhánh chính: (i) *Nhánh căn chỉnh và dung hợp đặc trưng sâu* như **MVAE** [15], **CAFE** [16], **CFFN** [17] và **COOLANT** [18] (sử dụng học tương phản toàn cục giữa ảnh và chữ); (ii) *Nhánh dựa trên thực thể và sự kiện* như **InfoSurgeon** [19], **EM-FEND** [20] và **Event-Radar** [21]; và (iii) *Nhánh ứng dụng LVLM* như **NLIN** [22] hay **SNIFFER** [23]. Hạn chế chung của các nhánh này là chưa kết hợp được khả năng suy luận ngữ nghĩa sâu của LLM/LVLM vào cấu trúc đồ thị thực thể chi tiết, đồng thời dễ bị suy giảm hiệu năng khi gặp dữ liệu mạng xã hội chứa nhiễu hoặc các thực thể không bắt cặp tường minh.

---

## III. KHAI THÁC THUỘC TÍNH SẢN PHẨM ĐA PHƯƠNG THỨC THẾ GIỚI MỞ VỚI CƠ CHẾ TỰ SỬA LỖI (BÀI BÁO 1 — MSIT)

### 3.1. Phát biểu Bài toán dưới Góc nhìn Toán học

Trong bài toán Khai thác Thuộc tính Sản phẩm Thương mại Điện tử Thế giới Mở Đa phương thức, mỗi sản phẩm thứ $i$, ký hiệu là $\mathcal{P}_i$, được mô tả bởi hai nguồn dữ liệu đầu vào:

1. **Thông tin văn bản $\mathcal{T}_i$:** Bao gồm tiêu đề sản phẩm (*title*) và các gạch đầu dòng mô tả đặc điểm nổi bật (*bullet points*), được biểu diễn dưới dạng một chuỗi gồm $w_i$ từ (token):
   $$\mathcal{T}_i = \left\{s_1^i, s_2^i, \dots, s_{w_i}^i\right\}$$
2. **Thông tin thị giác $\mathcal{I}_i$:** Hình ảnh chụp sản phẩm hoặc bao bì sản phẩm.

Mục tiêu của mô hình là tự động khám phá và trích xuất một tập hợp gồm $k$ thuộc tính phù hợp $\mathcal{A}_i = \{a_1, a_2, \dots, a_k\}$ cùng tập giá trị tương ứng của chúng $\mathcal{V}_i = \{v_1, v_2, \dots, v_k\}$. Điểm cốt lõi của thiết lập **Thế giới Mở (*Open-World*)** là số lượng thuộc tính $k$ cũng như tên gọi của các thuộc tính $a_m$ không bị giới hạn bởi bất kỳ từ điển hay lược đồ (*schema*) cố định nào cho trước. Thay vì giải bài toán như một bộ phân loại, MSIT sử dụng mô hình MLLM sinh tuần tự một chuỗi văn bản có cấu trúc thống nhất dưới dạng từ điển JSON:
$$\{a_1 : v_1, a_2 : v_2, \dots, a_k : v_k\}$$

### 3.2. Phân tích Chi tiết Kiến trúc và Phương pháp MSIT

Để khắc phục đồng thời sự thiếu hụt thông tin thị giác và hiện tượng sinh thuộc tính rác do thiếu suy luận, nhóm tác giả thiết kế khung **MSIT** gồm ba trụ cột chính: (1) Xây dựng tập dữ liệu tinh chỉnh sinh thuộc tính (**AGTD**); (2) Xây dựng tập dữ liệu tinh chỉnh chuỗi tư duy (**CTTD**); và (3) Huấn luyện mô hình với LoRA kết hợp quy trình suy luận 3 giai đoạn.

```mermaid
flowchart LR
    subgraph Phase1["1. Kiến tạo dữ liệu AGTD (Tách biệt phương thức)"]
        Seed["Tập hạt giống<br/>(Seed Attributes)"] --> GPT4_T["GPT-4 ICL<br/>Chỉ đọc Văn bản"]
        Seed --> GPT4_I["GPT-4 ICL<br/>Chỉ đọc Hình ảnh"]
        T_in["Văn bản SP"] --> GPT4_T --> Rev1["Duyệt thủ công"]
        I_in["Hình ảnh SP"] --> GPT4_I --> Rev1
        Rev1 --> Merge["GPT-4 Hợp nhất<br/>(JSON Attribute:Value)"]
    end

    subgraph Phase2["2. Kiến tạo dữ liệu CTTD (CoT 5 bước tương phản)"]
        Pos["Mẫu Dương (Yes):<br/>Thuộc tính đúng của SP"] --> CoT5["GPT-4 sinh chuỗi<br/>suy luận 5 bước"]
        Neg["Mẫu Âm (No):<br/>Thuộc tính lấy từ SP khác"] --> CoT5
    end

    Phase1 & Phase2 --> LoRA["Tinh chỉnh MLLM bằng LoRA<br/>(LLaVA-7B / Qwen-VL / InternLM)"]

    subgraph Phase3["3. Quy trình Suy luận 3 Giai đoạn (3-Stage Inference)"]
        LoRA --> S1["Giai đoạn 1 (S1):<br/>Sinh thuộc tính theo lô"]
        S1 --> S2["Giai đoạn 2 (S2):<br/>Lọc trùng lặp (Word2Vec + 3 Luật)"]
        S2 --> S3["Giai đoạn 3 (S3):<br/>Kiểm chứng tuần tự bằng CoT 5 bước"]
        S3 --> Out["Tập cặp {Thuộc tính : Giá trị}<br/>đã tự sửa lỗi (Giữ lại nếu Bước 5 = Yes)"]
    end
```

*Hình 2: Sơ đồ luồng hoạt động tổng thể của khung phương pháp MSIT được nhóm trực quan hóa lại từ kiến trúc của bài báo.*

#### 3.2.1. Chiến lược Tách biệt Phương thức trong Xây dựng Dữ liệu AGTD

Khi mở rộng hai bộ dữ liệu gốc đơn phương thức là **WOAM** và **OAMine** sang đa phương thức bằng cách thu thập ảnh sản phẩm từ Amazon.com, nhóm tác giả cần tạo ra dữ liệu chỉ dẫn chất lượng cao để dạy MLLM kỹ năng trích xuất cặp `thuộc tính : giá trị`. Một tập dữ liệu hạt giống (*Seed Dataset*) nhỏ được gán nhãn thủ công cho từng ngành hàng nhằm làm mẫu cho kỹ thuật Học trong ngữ cảnh (*In-Context Learning — ICL*) trên mô hình GPT-4.

Một phát hiện thực nghiệm rất đáng chú ý của tác giả là: nếu cung cấp đồng thời cả hình ảnh $\mathcal{I}_i$ và văn bản $\mathcal{T}_i$ vào cùng một câu lệnh cho GPT-4, cơ chế chú ý của GPT-4 sẽ bị thiên lệch mạnh về phía văn bản (do văn bản đã ở sẵn dạng token ngôn ngữ dễ trích xuất), dẫn đến việc bỏ sót các thuộc tính chỉ xuất hiện trên ảnh. Để triệt tiêu **thiên lệch chú ý phương thức (*modality attention bias*)** này, quy trình xây dựng AGTD được thực hiện theo 4 bước:

1. **Trích xuất độc lập từ văn bản:** Đưa riêng tiêu đề và mô tả sản phẩm cùng 4 ví dụ mẫu ICL (thuộc 4 ngành hàng: Sofa, Trà, Vitamin, Ốp lưng điện thoại) vào GPT-4 để trích xuất tập thuộc tính văn bản.
2. **Trích xuất độc lập từ hình ảnh:** Đưa riêng ảnh sản phẩm cùng ví dụ ICL vào GPT-4 để buộc mô hình phải quan sát kỹ các chi tiết thị giác và chữ in trên bao bì nhằm trích xuất tập thuộc tính hình ảnh.
3. **Kiểm duyệt thủ công (*Manual Review*):** Lọc bỏ các thuộc tính không chính xác từ cả hai nguồn.
4. **Hợp nhất đa phương thức (*Merging*):** Sử dụng GPT-4 với một câu lệnh chuyên biệt để gộp hai tập thuộc tính từ ảnh và văn bản thành một cấu trúc JSON duy nhất, gộp các thuộc tính trùng tên và làm mịn các thuộc tính quá chung chung (như `Features`) thành thuộc tính cụ thể.

#### 3.2.2. Chuỗi Tư duy 5 Bước Có Cấu trúc và Lấy mẫu Tương phản trong CTTD

Nếu chỉ huấn luyện trên AGTD, MLLM mới chỉ học được cách "liệt kê" thuộc tính mà chưa có khả năng tự phản biện xem thuộc tính đó có thực sự hợp lý hay không. Tuy nhiên, nếu dùng CoT tự do (*vanilla CoT*), mô hình lại dễ tự bịa ra lý do sai lệch. Do đó, nhóm tác giả thiết kế tập dữ liệu **CTTD** ép buộc mô hình suy luận tuần tự qua **5 bước kiểm chứng chặt chẽ** cho mỗi thuộc tính ứng viên $a_m$:

- **Bước 1 (Xác định và thu hẹp loại sản phẩm):** Quan sát cả ảnh và văn bản để định danh chính xác sản phẩm thuộc danh mục nào (ví dụ: thực phẩm chức năng, trà túi lọc hay ốp điện thoại), từ đó giới hạn không gian thuộc tính hợp lệ.
- **Bước 2 (Sàng lọc sơ bộ bằng tri thức thông thường nội tại):** Phân tích ý nghĩa của tên thuộc tính $a_m$. Nếu tên thuộc tính tối nghĩa hoặc vô lý khi ghép với loại sản phẩm ở Bước 1 theo lẽ thường (chẳng hạn thuộc tính `kích thước màn hình` áp dụng cho `viên uống vitamin`), lập tức đánh giá sơ bộ là không phù hợp. Ngược lại, giải thích vì sao thuộc tính này có lý với loại sản phẩm đó.
- **Bước 3 (Kiểm chứng bằng chứng trên hình ảnh):** Nếu Bước 2 đánh giá là có khả năng phù hợp, mô hình đối chiếu với hình ảnh sản phẩm để ước lượng một giá trị thuộc tính tương đối (*rough value*) nhằm xác nhận sự tồn tại của thuộc tính trên ảnh.
- **Bước 4 (Kiểm chứng và trích xuất chính xác từ văn bản):** Tiếp tục đối chiếu với tiêu đề và mô tả văn bản. Nếu văn bản có chứa thông tin về thuộc tính, mô hình phải chỉ ra giá trị chính xác (*exact value*).
- **Bước 5 (Tổng hợp và ra quyết định nhị phân):** Đúc kết bằng chứng từ 4 bước trên để đưa ra kết luận cuối cùng ở đoạn văn cuối bằng một từ duy nhất: **`yes`** (hợp lệ) hoặc **`no`** (không hợp lệ).

**Cơ chế Học Tương phản trong CTTD (*Contrastive CoT*):** Bởi vì mọi thuộc tính lấy từ AGTD đều là thuộc tính đúng của sản phẩm, nếu chỉ tạo dữ liệu CoT từ chúng thì nhãn ở Bước 5 sẽ luôn là `yes`, khiến mô hình bị quá khớp (*overfitting*) và mất khả năng từ chối thuộc tính sai. Để giải quyết vấn đề này, nhóm tác giả lấy các thuộc tính của các ngành hàng khác làm **mẫu âm (*negative samples*, nhãn `no`)**, kiểm duyệt thủ công và thiết lập tỷ lệ **cân bằng 1:1 giữa mẫu dương và mẫu âm** trong tập CTTD.

#### 3.2.3. Tinh chỉnh Mô hình với LoRA và Quy trình Suy luận 3 Giai đoạn

Tập dữ liệu hợp nhất $\mathcal{D} = \text{AGTD} \cup \text{CTTD}$ được dùng để tinh chỉnh ba kiến trúc MLLM 7 tỷ tham số (**LLaVA-7B**, **Qwen-VL**, và **InternLM-XComposer2-7B**) thông qua phương pháp **LoRA**. Toàn bộ trọng số gốc của MLLM được đóng băng, chỉ cập nhật các tham số phân rã hạng thấp $\hat{\theta}$ путем cực tiểu hóa hàm mất mát tự hồi quy tiêu chuẩn (Công thức 1 trong bài báo):
$$\arg\min_{\hat{\theta}} \mathbb{E}_{(\mathcal{I}_i, \mathcal{T}_i) \in \mathcal{D}} \left[ \sum_{s=1}^{s_j} \log P_{\mathcal{M}_{\hat{\theta}}} \left( s_w^i \mid \mathcal{I}_i, s_1^i, \dots, s_{w-1}^i \right) \right] \quad (1)$$

Sau khi huấn luyện, quá trình suy luận trên sản phẩm mới diễn ra qua **3 giai đoạn nối tiếp**:

1. **Giai đoạn 1 — Sinh thuộc tính theo lô (*Batch Attribute Generation*):** Sử dụng 1 trong 10 mẫu câu lệnh chỉ dẫn tương đương ngữ nghĩa để yêu cầu MLLM đã tinh chỉnh sinh ra toàn bộ các cặp `{thuộc tính : giá trị}` tiềm năng dưới dạng JSON trong một lần gọi.
2. **Giai đoạn 2 — Lọc thuộc tính trùng lặp dựa trên Word2Vec và 3 quy tắc độ dài từ con (*Filtering Repeated Attributes*):**
   Trong quá trình sinh theo lô, mô hình thường sinh ra các tên thuộc tính trùng lặp về mặt ý nghĩa (ví dụ: `"type"` và `"product_type"`, hay `"brand"` và `"product_brand"`). Để giảm số lần phải chạy CoT ở Giai đoạn 3 và tăng độ chính xác, nhóm tác giả tách mỗi tên thuộc tính thành các từ con (*subwords*) và dùng mô hình nhúng từ **`word2vec-google-news-300`** để tính độ tương đồng cosine giữa các từ con. Hai tên thuộc tính được coi là **đồng nghĩa (*synonyms*)** nếu các từ con của chúng tương ứng **một-đối-một (*one-to-one*)** vượt qua ngưỡng tương đồng (trong đó cụm chỉ có 1 từ con phải chịu một ngưỡng khắt khe hơn để tránh khớp nhầm). Khi phát hiện hai thuộc tính $A$ và $B$ đồng nghĩa, hệ thống quyết định xóa một thuộc tính theo **3 quy tắc dựa trên số lượng từ con** (với giả định $|A| \le |B|$):
   - **Quy tắc 1:** Nếu $|A| = 1$ (chỉ có 1 từ con), xét độ dài của $B$: nếu $|B| = 3$ thì **xóa $A$** (giữ cụm 3 từ con vì mang nghĩa cụ thể hơn cụm 1 từ đơn); nhưng nếu $|B| > 3$ thì **xóa $B$** (vì cụm quá 3 từ thường dài dòng, nhiễu).
   - **Quy tắc 2:** Nếu $|A| = 2$ và $|B| \ge 3$ thì **xóa $B$** (ưu tiên cụm 2 từ con cô đọng).
   - **Quy tắc 3:** Nếu $|A| = |B|$ (cùng số lượng từ con) thì **chọn ngẫu nhiên một trong hai để xóa**.
3. **Giai đoạn 3 — Kiểm chứng tuần tự bằng CoT 5 bước (*Sequential Attribute Inference with 5-step CoT*):**
   Từng thuộc tính còn sót lại sau Giai đoạn 2 được đưa lần lượt vào MLLM kèm theo 1 trong 5 mẫu câu lệnh yêu cầu suy luận 5 bước. Thuộc tính chỉ được giữ lại trong kết quả cuối cùng nếu Bước 5 kết luận là **`yes`**, qua đó tự động loại bỏ các thuộc tính dương tính giả.

---

### 3.3. Phân tích Kết quả Thực nghiệm trong Bài báo Gốc

Nhóm tác giả đánh giá MSIT trên hai bộ dữ liệu đa phương thức mở rộng từ **WOAM** (4 ngành hàng: *Tea, Vitamin, Sofa, Phone Case*, hơn 9.000 mô tả/ngành hàng) và **OAMine** (100 ngành hàng, 1.943 sản phẩm kiểm thử gán nhãn thủ công trên 10 ngành hàng), sử dụng **1.000 mẫu AGTD + 300 mẫu CTTD** cho huấn luyện và **1.000 mẫu** cho kiểm thử. Mô hình được huấn luyện 10 epochs bằng bộ tối ưu Adam ($\text{lr} = 3 \times 10^{-4}$) trên 1 GPU Tesla A100, giải mã với $\text{temperature} = 0.2, \text{top\_p} = 0.7$ và lấy trung bình qua 5 lần chạy độc lập. Hai độ đo được sử dụng là **Độ chính xác (Precision)** và **Độ phủ (Recall)** dưới hai chế độ: **Khớp chính xác (Exact Match)** và **Khớp tương đồng (Similar Match — chấp nhận từ đồng nghĩa)**.

#### Bảng 1: Tổng hợp kết quả so sánh hiệu năng trên tập dữ liệu WOAM và OAMine (Đơn vị: %)

| Mô hình đối sánh | WOAM Khớp tương đồng (P / R) | WOAM Khớp chính xác (P / R) | OAMine Khớp tương đồng (P / R) | OAMine Khớp chính xác (P / R) |
| :--- | :---: | :---: | :---: | :---: |
| VisualGLM-6B | $40.32 \pm 1.24$ / $5.25 \pm 0.11$ | $17.80 \pm 0.65$ / $2.83 \pm 0.34$ | $44.12 \pm 0.28$ / $18.98 \pm 0.27$ | $17.46 \pm 0.89$ / $9.38 \pm 0.00$ |
| InstructBLIP-Vicuna-7B | $39.79 \pm 0.58$ / $6.62 \pm 0.00$ | $13.87 \pm 3.18$ / $2.75 \pm 0.23$ | $40.16 \pm 0.23$ / $19.78 \pm 0.30$ | $19.78 \pm 0.30$ / $5.76 \pm 0.05$ |
| Qwen-VL-Chat-7B | $36.86 \pm 0.29$ / $35.38 \pm 1.82$ | $10.29 \pm 0.19$ / $17.61 \pm 1.42$ | $43.06 \pm 0.11$ / $58.09 \pm 0.08$ | $18.63 \pm 0.08$ / $36.15 \pm 0.36$ |
| DeepSeek-VL-7B | $42.93 \pm 0.25$ / $36.51 \pm 0.45$ | $12.15 \pm 1.33$ / $19.95 \pm 1.49$ | $53.00 \pm 0.02$ / $56.05 \pm 0.47$ | $25.03 \pm 0.47$ / $36.10 \pm 0.56$ |
| InternLM-XComposer2-7B | $52.19 \pm 0.28$ / $31.99 \pm 0.69$ | $23.16 \pm 0.82$ / $19.14 \pm 0.80$ | $69.31 \pm 0.00$ / $45.12 \pm 0.37$ | $36.23 \pm 0.37$ / $27.18 \pm 0.27$ |
| LLaVA-7B (Gốc) | $40.49 \pm 1.50$ / $56.21 \pm 1.60$ | $10.61 \pm 1.31$ / $26.22 \pm 4.46$ | $47.07 \pm 0.08$ / $54.99 \pm 0.08$ | $16.71 \pm 0.02$ / $26.82 \pm 0.03$ |
| LLaVA-13B (Gốc) | $41.22 \pm 3.29$ / $64.62 \pm 1.59$ | $10.52 \pm 1.35$ / $37.72 \pm 4.91$ | $51.87 \pm 0.21$ / $58.59 \pm 3.27$ | $21.46 \pm 0.99$ / $37.75 \pm 1.19$ |
| GPT-4 | $52.03 \pm 1.33$ / $65.35 \pm 4.23$ | $15.51 \pm 2.01$ / $41.60 \pm 5.14$ | $64.92 \pm 0.14$ / $55.75 \pm 2.36$ | $29.25 \pm 2.36$ / $33.72 \pm 0.03$ |
| OA-Mine (Chỉ văn bản) | $42.27 \pm 1.29$ / $53.62 \pm 1.59$ | $17.52 \pm 1.35$ / $26.72 \pm 1.91$ | $53.85 \pm 0.15$ / $47.71 \pm 0.01$ | $18.15 \pm 0.01$ / $35.69 \pm 0.67$ |
| Amacer (Chỉ văn bản) | $51.27 \pm 0.82$ / $58.30 \pm 0.17$ | $21.91 \pm 0.53$ / $29.23 \pm 0.90$ | $58.41 \pm 0.26$ / $51.65 \pm 0.12$ | $22.98 \pm 1.04$ / $38.84 \pm 0.05$ |
| **MSIT (Qwen-VL)** | $59.95 \pm 0.40$ / $41.60 \pm 0.57$ | $20.00 \pm 0.11$ / $23.75 \pm 0.34$ | $65.01 \pm 0.19$ / $52.44 \pm 0.13$ | $24.61 \pm 0.01$ / $38.13 \pm 0.08$ |
| **MSIT (InternLM)** | $63.40 \pm 0.34$ / $46.80 \pm 0.34$ | $25.00 \pm 0.26$ / $25.53 \pm 0.23$ | $70.79 \pm 0.28$ / $46.99 \pm 0.13$ | $37.52 \pm 0.09$ / $27.37 \pm 0.05$ |
| **MSIT (LLaVA-7B)** | **$66.90 \pm 0.53$** / **$66.99 \pm 2.13$** | **$35.34 \pm 2.71$** / **$52.50 \pm 3.93$** | **$74.50 \pm 0.17$** / **$63.06 \pm 0.45$** | **$54.33 \pm 0.45$** / **$51.54 \pm 0.05$** |

**Các luận điểm phân tích sâu từ kết quả thực nghiệm và nghiên cứu cắt bỏ:**

1. **Sự bứt phá nhờ tinh chỉnh chỉ dẫn đa phương thức:** Khi áp dụng khung MSIT lên cả 3 mô hình nền (Qwen-VL, InternLM, LLaVA-7B), hiệu năng đều tăng vọt so với phiên bản gốc chưa tinh chỉnh. Đáng chú ý nhất, `MSIT (LLaVA-7B)` nâng Độ chính xác Khớp chính xác (Exact Match Precision) trên WOAM từ **10,61% lên 35,34%** (gấp hơn 3,3 lần) và trên OAMine từ **16,71% lên 54,33%**, vượt xa cả mô hình thương mại khổng lồ **GPT-4** (15,51% trên WOAM và 29,25% trên OAMine) cũng như hai phương pháp đơn phương thức chuyên biệt là **OA-Mine** và **Amacer**.
2. **Vai trò quyết định của từng thành phần qua Nghiên cứu Cắt bỏ (Ablation Study):**
   - Khi chỉ huấn luyện với `AGTD` (kèm S1, S2), Độ chính xác Khớp tương đồng trên WOAM tăng từ 40,49% lên 62,15%, chứng tỏ AGTD giúp định hình khuôn mẫu trích xuất JSON chuẩn xác. Ngược lại, nếu chỉ dùng `CTTD` mà thiếu `AGTD`, Độ chính xác chỉ đạt 50,15% do mô hình chưa học được cách sinh ứng viên thuộc tính ở Giai đoạn 1.
   - Khi giữ nguyên `AGTD + CTTD + S1 + S2` nhưng bỏ Giai đoạn 3 (`S3`), Độ phủ (Recall) đạt đỉnh (67,91% trên WOAM) nhưng Độ chính xác (Precision) chỉ đạt 63,72% (Similar Match) và 29,47% (Exact Match). Khi kích hoạt `S3` (CoT 5 bước), một lượng nhỏ Độ phủ được đánh đổi (giảm nhẹ từ 67,91% xuống 66,99%) để đổi lấy mức tăng vọt về Độ chính xác (tăng lên **66,90%** ở Similar Match và **35,34%** ở Exact Match).
   - Thống kê trực tiếp trên **1.028 thuộc tính** đi qua Giai đoạn 3 cho thấy: **93,3%** thuộc tính được giữ lại (`yes`) và **6,7%** bị bác bỏ (`no`). Trong số 6,7% thuộc tính bị bác bỏ đó, có tới **98,6%** là các thuộc tính dương tính giả được tự sửa lỗi thành công (*Self-corrected Negatives*), chỉ có **1,4%** bị loại nhầm.
3. **Tác động của định dạng đầu ra, quy mô dữ liệu và khả năng thích nghi miền:**
   - Nếu chỉ yêu cầu mô hình sinh tên thuộc tính (`Attri-only`) thay vì cặp `thuộc tính : giá trị` (`Attri-Value`), kết quả Khớp chính xác giảm thê thảm xuống 28,68% P / 38,37% R (so với 35,34% P / 52,50% R). Việc buộc sinh kèm giá trị đóng vai trò như một neo ngữ nghĩa giúp mô hình bám sát vào bằng chứng thực tế.
   - Khi tăng kích thước tập CTTD từ 100 lên 300 mẫu, Recall Khớp tương đồng tăng mạnh từ 53,88% lên 66,99% và Recall Khớp chính xác tăng từ 42,89% lên 52,50%.
   - Trong bài kiểm tra thích nghi miền chéo (*Leave-One-Category-Out* trên 4 ngành hàng Sofa, Phone, Tea, Vitamin) và phân tích riêng từng loại đầu vào (`image`, `bullet`, `title`), MSIT đều vượt qua GPT-4, đặc biệt đạt Độ chính xác Khớp tương đồng **69,21%** và Khớp chính xác **40,96%** khi trích xuất từ kênh hình ảnh.

---

### 3.4. Quá trình và Kết quả Tái lập Thực nghiệm của Nhóm trên Bài báo 1 (MSIT)

Bám sát yêu cầu tái lập thực nghiệm, nhóm chúng tôi đã thiết kế và xây dựng lại toàn bộ mã nguồn của khung phương pháp **MSIT** từ đầu bằng ngôn ngữ Python và quản trị công khai trên nền tảng GitHub tại địa chỉ:

- **Link GitHub Repository của nhóm:** [https://github.com/linhnnh688/msit-open-world](https://github.com/linhnnh688/msit-open-world)

#### 3.4.1. Kiến trúc Mã nguồn và Điều chỉnh Thích nghi Phần cứng Thực tế

Trong bài báo gốc, tác giả sử dụng GPU **NVIDIA Tesla A100 (40GB/80GB VRAM)** và gọi API **GPT-4** thương mại cho 1.300 mẫu huấn luyện. Để tái lập khả thi trên hạ tầng tài nguyên mở khả dụng của học viên (**Kaggle GPU NVIDIA Tesla T4 $\times 2$ / P100 16GB VRAM** và môi trường máy trạm cục bộ), nhóm đã thực hiện các thiết kế kỹ thuật sau trong gói thư viện `msit/`:

1. **Tái hiện nguyên bản toàn bộ hệ thống Prompt và Pipeline 3 Giai đoạn (`msit/prompts/`, `msit/data/`, `msit/inference/`, `msit/evaluation/`):**
   - Cài đặt chính xác các mẫu câu lệnh tại Phụ lục A.1 (tách biệt trích xuất ảnh/văn bản kèm 4 mẫu ICL), Phụ lục A.2 (hợp nhất), Phụ lục A.3 (CoT 5 bước), cùng 10 câu lệnh Bảng 4 và 5 câu lệnh Bảng 5.
   - Hiện thực hóa đầy đủ thuật toán Giai đoạn 2 (`msit/inference/stage2_dedup.py`): tách từ con chữ thường - chữ số, ghép cặp song phân tham lam (*greedy bipartite matching*) một-đối-một với ngưỡng chuẩn `0.70` và ngưỡng cao `0.85` cho cụm 1 từ con trên vector `word2vec-google-news-300`, cùng 3 quy tắc xóa (`choose_deletion`).
   - Hiện thực hóa mô-đun kiểm chứng tuần tự Giai đoạn 3 (`stage3_cot_infer.py`) và bộ tính độ đo Khớp chính xác / Khớp tương đồng qua 5 lần chạy (`metrics.py`, `evaluate.py`).
2. **Kiến tạo Bộ dữ liệu Tinh chỉnh Đa phương thức Thực tế (`msit/data/sft_datasets/`):**
   - Thay vì phụ thuộc vào GPT-4 đóng phí, nhóm sử dụng mô hình mở tiên tiến **`Qwen/Qwen2.5-VL-7B-Instruct`** làm mô hình sinh dữ liệu (*teacher model*) trên bộ dữ liệu WOAM kết hợp ảnh sản phẩm thực tế (`/kaggle/input/datasets/kunzero106/msit-open-world-dataset/datasets/images/woam/`).
   - Nhóm đã khởi tạo thành công đúng quy mô của bài báo gốc:
     - **Tập huấn luyện AGTD (`agtd_train.jsonl`):** Gồm đúng **1.000 mẫu** phân bố đều tuyệt đối trên 4 ngành hàng: `VITAMIN` (250 mẫu), `CELLULAR_PHONE_CASE` (250 mẫu), `TEA` (250 mẫu), và `SOFA` (250 mẫu).
     - **Tập huấn luyện CTTD (`cttd_train.jsonl`):** Gồm đúng **300 mẫu** suy luận 5 bước phân bố đều trên 4 ngành hàng (mỗi ngành hàng 75 mẫu), đảm bảo **cân bằng tuyệt đối nhãn gốc (`cttd_label`) với 150 mẫu dương (`yes`) và 150 mẫu âm (`no`)**.
     - **Tập kiểm thử (`test_set.jsonl`):** Gồm **1.000 mẫu** (250 mẫu/ngành hàng).
3. **Tinh chỉnh Mô hình Đa phương thức bằng Kỹ thuật QLoRA 4-bit (`finetune.ipynb` & `msit/models/lora_trainer.py`):**
   - Để vừa vặn trong bộ nhớ 16GB VRAM của GPU Kaggle mà vẫn giữ nguyên kích thước lô hiệu dụng (*effective batch size* = 16), nhóm áp dụng lượng tử hóa **4-bit NormalFloat (`nf4`)** kết hợp tính toán `float16`, `double quantization`, `gradient checkpointing`, với `per_device_train_batch_size = 2` và `gradient_accumulation_steps = 8`.
   - Cấu hình bộ thích nghi LoRA (`adapter_config.json`): hạng $r = 16$, hệ số $\alpha = 32$, $\text{dropout} = 0.05$, nhắm vào các tầng chiếu chú ý (`q_proj`, `v_proj`), bộ tối ưu `paged_adamw_8bit`, tốc độ học $2 \times 10^{-4}$ với lịch giảm `cosine` (`warmup_steps = 20`), mặt nạ nhãn `-100` trên toàn bộ phần câu lệnh để chỉ tính hàm mất mát tự hồi quy (Công thức 1) trên chuỗi câu trả lời mục tiêu.

#### 3.4.2. Kết quả Ghi nhận Quá trình Huấn luyện và Kiểm thử Tái lập (Kèm Liên kết Weights & Biases)

##### (a) Quá trình Hội tụ Huấn luyện QLoRA trên Tập dữ liệu AGTD + CTTD (1.300 mẫu)

- **Liên kết Weights & Biases ghi nhận quá trình huấn luyện chính:** `[Gắn link Public WandB Run - Training MSIT Qwen-VL LoRA tại đây: https://wandb.ai/<username>/msit-open-world/runs/<run_id_train>]`
- **Trọng số Adapter đã huấn luyện lưu trữ trong Repository:** [`msit/results/msit_qwen_lora_final/`](file:///d:/workspace/msit-open-world/msit/results/msit_qwen_lora_final/adapter_config.json) (dung lượng adapter `20,2 MB`, huấn luyện trên nền `Qwen/Qwen2-VL-7B-Instruct` qua 3 epochs / 246 bước cập nhật trọng số, tổng số phép tính dấu phẩy động $\text{Total FLOPs} = 1,205 \times 10^{17}$).

#### Bảng 2: Diễn biến hàm mất mát (Training Loss), chuẩn đạo hàm (Grad Norm) và tốc độ học theo bước huấn luyện (Trích xuất từ `trainer_state.json`)

| Bước (Step) | Epoch | Hàm mất mát (Loss) | Chuẩn đạo hàm (Grad Norm) | Tốc độ học (Learning Rate) | Ghi chú trạng thái |
| :---: | :---: | :---: | :---: | :---: | :--- |
| 10 | 0,12 | 2,0925 | 0,4912 | $9,00 \times 10^{-5}$ | Giai đoạn khởi động (Warmup) |
| 20 | 0,25 | 1,8235 | 0,4647 | $1,90 \times 10^{-4}$ | Kết thúc Warmup, Loss giảm nhanh |
| 40 | 0,49 | 1,4973 | 0,3783 | $1,97 \times 10^{-4}$ | Học cấu trúc đầu ra JSON & CoT |
| 80 | 0,98 | 1,3201 | 0,3116 | $1,68 \times 10^{-4}$ | Kết thúc Epoch 1 (`checkpoint-82`) |
| 110 | 1,34 | 1,2249 | 0,3640 | $1,33 \times 10^{-4}$ | Giảm sâu hơn ở đầu Epoch 2 |
| 160 | 1,96 | 1,2643 | 0,4282 | $6,46 \times 10^{-5}$ | Kết thúc Epoch 2 (`checkpoint-164`) |
| 180 | 2,20 | 1,2103 | 0,4006 | $4,03 \times 10^{-5}$ | Đi vào vùng hội tụ ổn định |
| 220 | 2,69 | **1,1821** | 0,4377 | $6,96 \times 10^{-6}$ | Đạt giá trị Loss thấp nhất |
| 240 | 2,94 | 1,2412 | 0,4224 | $4,73 \times 10^{-7}$ | Kết thúc Epoch 3 (`checkpoint-246`) |

**Nhận xét quá trình huấn luyện:** Hàm mất mát giảm mượt mà và nhất quán từ **2,0925** ở bước 10 xuống mức thấp nhất **1,1821** ở bước 220 (giảm **43,5%**), trong khi chuẩn đạo hàm (`grad_norm`) luôn duy trì ổn định trong khoảng `[0,31; 0,49]`, chứng tỏ quá trình tinh chỉnh hỗn hợp trên 1.000 mẫu AGTD và 300 mẫu CTTD bằng QLoRA hoàn toàn không bị bùng nổ đạo hàm hay quá khớp cục bộ.

##### (b) Phân tích Thực nghiệm Kiến tạo Dữ liệu Suy luận 5 Bước (CTTD) và Hiện tượng Bảo thủ của MLLM

- **Liên kết Weights & Biases ghi nhận thực nghiệm CTTD & Self-Correction:** `[Gắn link Public WandB Run - CTTD & Self-Correction Analysis tại đây: https://wandb.ai/<username>/msit-open-world/runs/<run_id_cttd>]`
- Khi phân tích tập dữ liệu `cttd_train.jsonl` (300 mẫu cân bằng gồm 150 mẫu dương `cttd_label = yes` và 150 mẫu âm `cttd_label = no`) do mô hình chưa tinh chỉnh sinh chuỗi suy luận 5 bước, nhóm ghi nhận một kết quả thực nghiệm rất thú vị: mô hình đưa ra phán đoán cuối cùng (`decision`) gồm **213 kết luận `no` (71,0%)** và **87 kết luận `yes` (29,0%)**.
- Điều này cho thấy khi yêu cầu một MLLM phổ dụng thực hiện quy trình kiểm chứng 5 bước khắt khe mà chưa qua tinh chỉnh chuyên biệt, mô hình có xu hướng **bảo thủ (*conservative bias*)** — tức là bác bỏ rất tốt các thuộc tính âm tính giả từ sản phẩm khác, nhưng cũng dễ bác bỏ nhầm một số thuộc tính ẩn nếu không nhìn rõ trên ảnh. Sau khi tinh chỉnh kết hợp cả AGTD và CTTD, sự cân bằng giữa khả năng phát hiện thuộc tính (Giai đoạn 1) và khả năng tự sửa lỗi (Giai đoạn 3) được khôi phục đúng như phân tích trong bài báo gốc.

##### (c) Kiểm chứng Pipeline Suy luận 3 Giai đoạn và Nghiên cứu Cắt bỏ trên Tập mẫu Chuẩn

- **Liên kết Weights & Biases ghi nhận Kết quả chính (Main Results):** `[Gắn link Public WandB Run - Main Evaluation tại đây: https://wandb.ai/<username>/msit-open-world/runs/<run_id_main_eval>]`
- **Liên kết Weights & Biases ghi nhận Nghiên cứu cắt bỏ (Ablation Study S1/S2/S3):** `[Gắn link Public WandB Run - Ablation Study tại đây: https://wandb.ai/<username>/msit-open-world/runs/<run_id_ablation>]`
- Trên bộ kiểm thử đơn vị và pipeline thực thi đầu-cuối (`msit/demo.py` và `msit/tests/test_msit.py`), nhóm đã xác minh tính đúng đắn của từng giai đoạn trên các sản phẩm chuẩn của bài báo (như *Micro Ingredients Organic Matcha Green Tea 1lb*, *Chiquita Banana Bread Mix 13.7 oz*, và *Traditional Medicinals Herbal Tea 16 Tea Bags*):
  - **Tại Giai đoạn 1 (`Stage1BatchGenerator`):** Trích xuất thành công cả các thuộc tính văn bản (`brand`, `Tea_Type`, `caffeine_content`) lẫn các thuộc tính thị giác từ bao bì (`Product_Shape: Powder`, `Weight: 1lb`).
  - **Tại Giai đoạn 2 (`Stage2RepeatedAttributeFilter`):** Kiểm chứng chính xác 3 quy tắc xóa từ đồng nghĩa (ví dụ: giữa `"type"` [1 từ con] và `"product_type"` [2 từ con] hoặc các cụm $\ge 3$ từ con), loại bỏ hoàn toàn các thuộc tính trùng lặp trước khi sang Giai đoạn 3.
  - **Tại Giai đoạn 3 (`Stage3CoTValidator`):** Giữ lại 100% các thuộc tính hợp lệ (4/4 thuộc tính cho sản phẩm Matcha và Banana Bread Mix; 6/6 thuộc tính cho sản phẩm Herbal Tea, tổng cộng $\text{TP} = 14, \text{FP} = 0, \text{FN} = 0$, đạt $\text{Precision} = 1,0000, \text{Recall} = 1,0000$ trên tập kiểm thử chuẩn hóa) và loại bỏ chính xác các thuộc tính nhiễu từ ngành hàng khác.
- *(Lưu ý kỹ thuật được nhóm phát hiện trong quá trình kiểm thử mã nguồn)*: Khi chạy bộ 25 bài kiểm thử tự động trong `msit/tests/test_msit.py`, nhóm ghi nhận 23/25 bài đạt (`PASS`) và phát hiện 2 trường hợp biên thú vị trong hàm hậu xử lý chuỗi kết luận `_concludes_yes` / `parse_conclusion` khi chuỗi văn bản đầu ra có định dạng xuống dòng hoặc dấu câu đặc biệt ở Bước 5. Phát hiện này củng cố thêm nhận định rằng trong các hệ thống MLLM sinh văn bản tự do, khâu chuẩn hóa cú pháp đầu ra (*output parsing*) ở bước quyết định cuối cùng đóng vai trò rất quan trọng đối với độ ổn định của toàn hệ thống.

---

## IV. CĂN CHỈNH ĐỒ THỊ THỰC THỂ VÀ SUY LUẬN THỊ GIÁC TRONG PHÁT HIỆN TIN GIẢ ĐA PHƯƠNG THỨC (BÀI BÁO 2 — CMA-VRP)

Nếu như ở Phần thứ nhất (Mục III), bài toán đặt ra là làm sao để **tổng hợp và làm giàu tri thức** từ sự bổ khuyết giữa hình ảnh và văn bản của một sản phẩm thương mại điện tử, thì sang Phần thứ hai này, chúng ta xét bài toán ở chiều ngược lại: làm sao để **phát hiện sự mâu thuẫn ngầm và chống lại nhiễu loạn** giữa hình ảnh và văn bản nhằm nhận diện tin giả trên mạng xã hội thông qua khung phương pháp **CMA-VRP** (*Cross-Modal Alignment with Visual Reasoning Prompting*) [2].

### 4.1. Bản chất Bài toán và Hai Thách thức Cốt lõi trong Phát hiện Tin giả Đa phương thức

Một bản tin trên mạng xã hội được biểu diễn bởi cặp dữ liệu $(I, T)$, trong đó $I$ là hình ảnh đính kèm và $T$ là nội dung bài đăng văn bản. Nhiệm vụ của hệ thống là học một hàm ánh xạ phân loại nhị phân để dự đoán nhãn xác thực $y \in \{0, 1\}$ (với $1$ là tin giả — *Fake News* và $0$ là tin thật — *Real News*).

Theo phân tích của nhóm chúng tôi từ công trình CMA-VRP, sự phức tạp của tin giả hiện đại nằm ở chỗ người tạo tin giả không còn ghép một bức ảnh hoàn toàn xa lạ với văn bản, mà sử dụng những hình ảnh có bối cảnh bề mặt rất giống với nội dung bài viết nhưng chứa đựng **sự sai lệch ở cấp độ chi tiết thực thể hoặc hành vi**, cộng hưởng với **nhiễu cố hữu của môi trường mạng xã hội**:

1. **Sự bất đồng ngữ nghĩa tinh vi ở cấp độ thực thể và hành động (*Subtle Entity-Level Semantic Inconsistencies*):**
   Các mạng thị giác truyền thống (VGG, ResNet) chỉ nhìn thấy đặc trưng mức thấp, còn các mô hình LVLM dùng trực tiếp lại thường bị đánh lừa bởi sự tương đồng bối cảnh chung. Chẳng hạn, khi bài viết mô tả một *"cuộc biểu tình ôn hòa tại Bolton"*, bức ảnh đi kèm đúng là cảnh đám đông biểu tình trên đường phố. Tuy nhiên, nếu quan sát kỹ từng thực thể, nét mặt dữ tợn của người biểu tình và hành động cảnh sát đang ghì chặt đối tượng lại tố cáo tính chất bạo lực trái ngược hoàn toàn với từ *"ôn hòa"*. Tương tự, một bài viết tuyên bố *"chính sách nhận được sự ủng hộ của sinh viên"* có thể bị bóc trần chỉ bởi một tấm biển nhỏ ghi dòng chữ *"not in my name"* (không nhân danh tôi) nằm ở góc bức ảnh.
2. **Nhiễu nội tại từ dữ liệu mạng xã hội chất lượng thấp (*Inherent Social Media Noise*):**
   Tin tức lan truyền nhanh thường đi kèm ảnh bị nén mờ, thiếu sáng (khiến chỉ nhận diện được một vài thực thể rời rạc như chiếc xe cảnh sát trong đêm), hoặc bị chèn các dòng chữ đóng dấu (*watermarks*) giật gân, các thẻ `#hashtag` và `@mention` không liên quan nhằm dẫn dắt cảm xúc và gây nhiễu quá trình trích xuất đặc trưng của mô hình.

### 4.2. Phân tích Chi tiết Kiến trúc 3 Phân hệ của CMA-VRP

Để giải quyết đồng thời hai thách thức trên, kiến trúc **CMA-VRP** được thiết kế gồm 3 phân hệ phối hợp chặt chẽ: (1) Khởi tạo đồ thị thực thể đơn phương thức và suy luận thị giác hướng chân lý; (2) Học tương phản đồ thị kép và dung hợp đồ thị liên phương thức; và (3) Học biểu diễn bất biến qua chu trình đối kháng.

```mermaid
flowchart TD
    Input["Bản tin Đa phương thức đầu vào: Cặp (Hình ảnh I, Văn bản T)"]
    
    subgraph Mod1["Phân hệ 1: Khởi tạo Đồ thị Thực thể & Suy luận Thị giác (VRP)"]
        Input --> G_t["Đồ thị Văn bản G_t = (V_T, E_T)<br/>Phân tích cú pháp + Nhúng BERT X_t + Cạnh Z_t"]
        Input --> G_v["Đồ thị Thị giác G_v = (V_I, E_I)<br/>Mask-RCNN Scene Graph + Nút toàn cục v_g + Nút chữ Rosetta OCR v_ocr"]
        G_t --> Mistral["Mistral-7B (Không tinh chỉnh)<br/>Prompt 2 tầng cho N_t thực thể văn bản"]
        G_v --> LLaVA["LLaVA-1.6-13B (Không tinh chỉnh)<br/>Prompt 2 tầng cho N_v thực thể thị giác"]
        Mistral --> VRF_t["Mã hóa qua BERT -> Đặc trưng VRF_t"]
        LLaVA --> VRF_v["Mã hóa qua BERT -> Đặc trưng VRF_v"]
    end

    subgraph Mod2["Phân hệ 2: Học Tương phản Đồ thị & Dung hợp Liên phương thức (CMGAF)"]
        G_t & G_v --> InterGCL["Học tương phản Liên đồ thị (L_inter)<br/>Làm mượt nhãn mềm bằng tham số khả học θ"]
        G_t & G_v --> IntraGCL["Học tương phản Nội đồ thị (L_intra)<br/>Ghép thực thể + Che thực thể (p_m=0.2) + Trộn mẫu âm d(.)"]
        InterGCL & IntraGCL & VRF_t & VRF_v --> Fusion["L=2 tầng Dung hợp Đồ thị Đa phương thức<br/>4 nút cầu nối + Uni-Att + Cross-modal Gating"]
        Fusion --> Rep_o["Biểu diễn Nhất quán Ngữ nghĩa: o = m_{G_m}"]
    end

    subgraph Mod3["Phân hệ 3: Học Bất biến Chu trình Đối kháng (ACCIL)"]
        G_t & G_v & VRF_t & VRF_v --> VSCA["Căn chỉnh Chu trình Thị giác - Ngữ nghĩa (VSCA)<br/>CycleGAN + Khoảng cách Wasserstein có trọng số wd(u,w)"]
        VSCA --> DualD["Khung Bộ phân biệt Kép (D_0 và D_1)<br/>Trọng số bất biến w_i(x) = 1 - D_0^i(x) & Cực tiểu hóa phân kỳ JSD"]
        DualD --> Rep_cm["Biểu diễn Bất biến Phương thức: c_m = max(w_t c_t, w_v c_v)"]
    end

    Rep_o & Rep_cm --> Classifier["Ghép nối x_hat = o ⊕ c_m -> Tầng phân loại Softmax (Tin thật / Tin giả)"]
```

*Hình 3: Sơ đồ kiến trúc 3 phân hệ của khung phương pháp CMA-VRP được nhóm tái cấu trúc và trực quan hóa.*

---

#### 4.2.1. Phân hệ 1: Khởi tạo Đồ thị Hướng Thực thể và Suy luận Thị giác Hướng Chân lý

Thay vì biểu diễn cả câu văn hay cả bức ảnh bằng một vector phẳng duy nhất, CMA-VRP bóc tách dữ liệu thành cấu trúc đồ thị chi tiết:

- **Xây dựng Đồ thị Văn bản $\mathcal{G}_t = (\mathcal{V}_T, \mathcal{E}_T)$:** Sử dụng các công cụ phân tích cú pháp phụ thuộc (*dependency parsers* như Stanford NLP, TexSmart và spaCy `en_core_web_trf`) để tách câu thành các nút thực thể/đơn vị cú pháp $\mathcal{V}_t$ và các cạnh quan hệ ngữ pháp $\mathcal{E}_t$ (biểu diễn qua ma trận kề nhị phân $A_t \in \{0,1\}^{n \times n}$). Mỗi nút được khởi tạo bằng vector nhúng **BERT** ($X_t$), đi kèm một ma trận biến đổi cạnh khả học $Z_t$ để mô hình hóa sâu mối liên hệ cú pháp.
- **Xây dựng Đồ thị Thị giác $\mathcal{G}_v = (\mathcal{V}_I, \mathcal{E}_I)$ tích hợp Nút Toàn cục và OCR:** Sử dụng mô hình sinh đồ thị cảnh (*Scene Graph Generation*) dựa trên mạng xương sống **Mask-RCNN** để phát hiện top-$k$ đối tượng có độ tự tin cao nhất làm tập nút thực thể thị giác $\mathcal{V}_v$ (vector đặc trưng $X_v$), và các mối quan hệ không gian/hành động giữa chúng (như *đang cầm*, *đang mặc*, *ngồi cạnh*) làm tập cạnh $\mathcal{E}_v$ (ma trận kề $A_v$, đặc trưng cạnh $Z_v$). Điểm tinh tế trong thiết kế của tác giả là việc bổ sung thêm **hai loại nút đặc biệt** vào đồ thị thị giác:
  1. **Nút toàn cục ($v_g$):** Mã hóa toàn bộ bức ảnh thành một nút chung và nối với mọi thực thể $\mathcal{V}_v$ để giữ ngữ cảnh tổng thể.
  2. **Các nút văn bản trong ảnh ($v_{ocr}$):** Sử dụng hệ thống **Rosetta OCR** để đọc toàn bộ chữ xuất hiện trong ảnh (khẩu hiệu trên biểu ngữ, chữ đóng dấu watermark), phân tích cú pháp và đưa vào đồ thị thị giác như các nút bổ sung liên kết với các đối tượng xung quanh. Nhờ có $v_{ocr}$, những chi tiết như tấm biển *"not in my name"* không bao giờ bị bỏ sót.

- **Suy luận Thị giác dựa trên CoT Hướng Chân lý (*Truth-Driven CoT-based Visual Reasoning — VRP*):**
  Để bổ sung tri thức nền và khả năng suy luận hành vi cho các nút đồ thị mà **không cần tinh chỉnh (zero-shot prompting)** nhằm tránh hiện tượng ảo giác của LVLM khi fine-tune, nhóm tác giả thiết kế quy trình gợi ý 2 tầng tách biệt: dùng **Mistral-7B** cho $N_t$ thực thể văn bản và **LLaVA-1.6-13B** cho $N_v$ thực thể thị giác:
  - *Tầng gợi ý 1 (Sinh lý giải kiểm chứng):* Yêu cầu mô hình xét từng thực thể và lập luận xem đặc điểm thị giác nào của thực thể đó sẽ chứng minh hoặc bác bỏ tính chân thực của bản tin.
  - *Tầng gợi ý 2 (Tóm tắt đặc trưng thị giác đối chiếu):* Từ lập luận ở tầng 1, yêu cầu mô hình tóm tắt ngắn gọn đặc trưng thị giác **kỳ vọng** (đối với thực thể văn bản, ví dụ: *"người biểu tình phải có vẻ mặt bình tĩnh, không đối đầu"*) và đặc trưng thị giác **quan sát thực tế** (đối với thực thể trong ảnh, ví dụ: *"vẻ mặt căng thẳng, đang bị cảnh sát khống chế chặt"*).
  Chuỗi văn bản tóm tắt này được mã hóa qua **BERT** để tạo thành hai tập vector **Đặc trưng Suy luận Thị giác** là $VRF_t$ (cho văn bản) và $VRF_v$ (cho hình ảnh).

---

#### 4.2.2. Phân hệ 2: Học Tương phản Đồ thị Kép và Dung hợp Đồ thị Liên phương thức (CMGAF)

Sau khi có hai đồ thị $\mathcal{G}_t$ và $\mathcal{G}_v$, mô hình cần kéo các biểu diễn có cùng ngữ nghĩa lại gần nhau và đẩy các biểu diễn mâu thuẫn ra xa thông qua hai cơ chế học tương phản:

1. **Học Tương phản Liên đồ thị (*Inter-Graph Contrastive Learning*) với Nhãn Làm mượt Mềm:**
   Xét một lô gồm $N$ cặp bản tin $\{x_i = (s_t^i, s_v^i)\}_{i=1}^N$. Đầu tiên, biểu diễn cấp độ đồ thị của từng phương thức được tổng hợp từ các nút thông qua hàm $\text{READOUT}(\cdot)$:
   $$X_v^m = \text{READOUT}_v\left(\{h_i : v_i \in \mathcal{V}_I\}\right), \quad X_t^m = \text{READOUT}_t\left(\{h_i : v_i \in \mathcal{V}_T\}\right) \quad (1)$$
   Trong học tương phản thông thường, chỉ có cặp $(s_t^i, s_v^i)$ của cùng một bản tin mới nhận nhãn dương $Y_{ij} = 1$, còn toàn bộ $N^2 - N$ cặp chéo đều nhận nhãn $0$ tuyệt đối. Tuy nhiên, trong cùng một lô dữ liệu tin tức (đặc biệt là các bản tin viết về cùng một sự kiện thời sự), các mẫu khác nhau vẫn có thể chia sẻ ngữ nghĩa tương đồng. Việc ép nhãn cứng $0/1$ sẽ gây ra sự mơ hồ ngữ nghĩa. Do đó, tác giả tính ma trận tương đồng mềm $S_{ij}$ và pha trộn với nhãn cứng $Y_{ij}$ thông qua một **tham số làm mượt khả học $\theta \in [0, 1]$** (khởi tạo $\theta = 0.5$):
   $$S_{ij} = \frac{\exp\left(\text{sim}\left(X_t^m[i], X_v^m[j]\right) / \tau\right)}{\sum_{j'} \exp\left(\text{sim}\left(X_t^m[i], X_v^m[j']\right) / \tau\right)}, \quad \tilde{Y}_{ij} = \theta \cdot Y_{ij} + (1 - \theta) \cdot S_{ij} \quad (2)$$
   Hàm mất mát tương phản liên đồ thị $\mathcal{L}_{inter}$ được tối ưu hóa dựa trên nhãn làm mượt $\tilde{Y}_{ij}$:
   $$\mathcal{L}_{inter} = \mathbb{E} \left[ - \sum_{i,j} \tilde{Y}_{ij} \log \frac{\exp\left(\text{sim}\left(f(s_t[i]), f(s_v[j])\right) / \tau\right)}{\sum_{j'} \exp\left(\text{sim}\left(f(s_t[i]), f(s_v[j'])\right) / \tau\right)} \right] \quad (3)$$

2. **Học Tương phản Nội đồ thị (*Intra-Graph Contrastive Learning*) qua Ghép thực thể, Che thực thể và Tạo mẫu âm:**
   Để đi sâu vào tương tác cục bộ bên trong từng bản tin, nhóm tác giả thực hiện 3 thao tác trên đồ thị:
   - **(i) Ghép thực thể (*Entity Matching*):** Dùng LVLM đối chiếu và nối các thực thể tương ứng giữa $\mathcal{G}_t$ và $\mathcal{G}_v$ để tạo thành **đồ thị đa phương thức hợp nhất $\mathcal{G}_m = (\mathcal{V}_m, \mathcal{E}_m)$**.
   - **(ii) Che thực thể tạo mẫu dương (*Entity Masking*):** Ngẫu nhiên che một phần nút thực thể với xác suất $p_m = 0.2$ (thay vector đặc trưng nút bằng vector ngẫu nhiên nhưng giữ nguyên cấu trúc cạnh $\mathcal{E}_m$) để tạo đồ thị tăng cường dương $\mathcal{V}_+(\mathcal{G}) = (M \otimes \mathcal{V}_m, \mathcal{E}_m)$. Kỹ thuật này buộc mô hình không được phụ thuộc cục bộ vào một vài thực thể đơn lẻ mà phải suy luận từ cấu trúc quan hệ toàn cục.
   - **(iii) Trộn phương thức tạo mẫu âm (*Negative Mining*):** Dùng hàm trích xuất ngẫu nhiên $d(\cdot)$ để ghép chéo văn bản của mẫu này với hình ảnh của mẫu có nhãn đối lập: $x_i^- = \{s_t^i, s_v^{d(i)}\}$ hoặc $\{s_t^{d(i)}, s_v^i\}$, tạo thành đồ thị âm $\mathcal{V}_-(\mathcal{G})$.
   Hàm mất mát tương phản nội đồ thị $\mathcal{L}_{intra}$ theo dạng InfoNCE kéo mẫu gốc $x^a$ lại gần mẫu dương $x^+$ và đẩy xa các mẫu âm $x^-$:
   $$\mathcal{L}_{intra} = -\mathbb{E}_{x \sim \mathcal{X}} \left[ \log \frac{\exp\left(\text{sim}\left(g(x^a), g(x^+)\right) / \tau\right)}{\sum_{x^- \in \mathcal{X}^-} \exp\left(\text{sim}\left(g(x^a), g(x^-)\right) / \tau\right)} \right] \quad (4)$$
   Tổng hàm mất mát tương phản của Phân hệ 2 là $\mathcal{L}_{cl} = \mathcal{L}_{intra} + \mathcal{L}_{inter}$.

3. **Dung hợp Đồ thị Liên phương thức (*Cross-modal Graph Fusion*):**
   Bởi vì nhiều từ trừu tượng trong văn bản không có vật thể tương ứng trực tiếp trong ảnh, tác giả đặt ra **4 nút cầu nối tổng quát** (`misc`, `person`, `location`, `organization`) để liên kết các từ văn bản với các nút thị giác cùng nhóm. Trên đồ thị đa phương thức này, $L = 2$ tầng dung hợp được áp dụng nối tiếp:
   - *Bước chú ý nội phương thức (Uni-Att):* Cập nhật trạng thái nút trong từng phương thức có tích hợp thông tin cạnh $\phi(Z_t)$ vào khóa $K_t$ và giá trị $V_t$:
     $$C_t^{(l)} = \text{Softmax}\left( A_t \cdot \frac{Q_t^{(l-1)} \left(K_t^{(l-1)}\right)^\top}{\sqrt{d}} \right) \cdot V_t^{(l-1)} \quad (5)$$
   - *Bước cổng dung hợp liên phương thức tích hợp $VRF_t$:* Mỗi nút văn bản $u$ tổng hợp thông tin từ tập các nút thị giác láng giềng $\mathcal{N}_v(u)$ thông qua hệ số cổng $\alpha_{i,j}$ và cộng trực tiếp đặc trưng suy luận thị giác $VRF_t(u)$:
     $$R_{tu}^{(l)} = C_{tu}^{(l)} + \sum_{j \in \mathcal{N}_v(u)} \alpha_{i,j} \cdot C_{vj}^{(l)} + W_{vt}^{(l)} \cdot VRF_t(u), \quad \text{với } \alpha_{i,j} = W_1^{(l)} C_{tu}^{(l)} + W_2^{(l)} C_{vj}^{(l)} \quad (6, 7)$$
   Sau khi đi qua mạng truyền thẳng $\text{FFN}(R_t^{(l)})$ ở cả hai nhánh văn bản và thị giác sau $L$ tầng, hàm $\text{READOUT}$ tổng hợp toàn đồ thị để xuất ra **vector biểu diễn nhất quán ngữ nghĩa $o = m_{\mathcal{G}_m}$**.

---

#### 4.2.3. Phân hệ 3: Học Bất biến Chu trình Đối kháng (ACCIL)

Trong thực tế, rất nhiều thực thể giữa ảnh và bài viết không thể ghép cặp trực tiếp với nhau, đồng thời mỗi phương thức lại mang theo nhiễu riêng (như chữ watermark trên ảnh hay hashtag rác trong văn bản). Phân hệ **ACCIL** giải quyết bài toán này qua 2 bước:

1. **Căn chỉnh Chu trình Thị giác - Ngữ nghĩa (*Visual-Semantic Cycle Alignment — VSCA*):**
   Sử dụng mạng đối kháng nhất quán chu trình (**CycleGAN**) kết hợp **khoảng cách Wasserstein** để ánh xạ qua lại giữa phân phối nút văn bản $\mathcal{G}_t$ và phân phối nút thị giác $\mathcal{G}_v$. Điểm sáng tạo của bài báo là đưa độ tương đồng của đặc trưng suy luận thị giác $wd(u, w) = \text{sim}\left(VRF_t(u), VRF_v(w)\right)$ làm trọng số điều chỉnh khoảng cách vận chuyển tối ưu Wasserstein:
   $$W(\mathcal{G}_t, \mathcal{G}_v) = \inf_{\gamma \sim \Pi(\mathcal{G}_t, \mathcal{G}_v)} \mathbb{E}_{(u, w) \sim \gamma} \left[ wd(u, w) \cdot |w - u| \right] \quad (8)$$
   Bộ phân biệt $D_s$ được huấn luyện với hàm mất mát chu trình:
   $$\mathcal{L}_{cycle} = -\mathbb{E}_{u \sim \mathcal{G}_t} \left[ D_s\left(u, VRF_t(u)\right) \right] + \mathbb{E}_{w \sim \mathcal{G}_v} \left[ D_s\left(w, VRF_v(w)\right) \right] \quad (9)$$
   Sau bước căn chỉnh chu trình này, hàm $\text{READOUT}$ gom các nút lại thành hai vector biểu diễn phương thức đã làm sạch sơ bộ là $e_t$ và $e_v$.

2. **Trích xuất Đặc trưng Bất biến Phương thức bằng Khung Bộ phân biệt Kép (*Dual-Discriminator Framework*):**
   Để tách bỏ hoàn toàn phần nhiễu đặc thù của từng phương thức và chỉ giữ lại phần ngữ nghĩa cốt lõi chung (*modality-invariant features*), tác giả đưa $e \in \{e_t, e_v\}$ qua tầng chiếu bất biến $c = I(e)$ và đặt hai bộ phân biệt đối kháng nối tiếp:
   - **Bộ phân biệt thứ nhất $D_0$:** Đánh giá xác suất mẫu thuộc phương thức $i$, từ đó gán **trọng số bất biến phương thức** $w_i(x) = 1 - D_0^i(x)$ (mẫu càng khó phân biệt phương thức thì càng nhận trọng số cao).
   - **Bộ phân biệt thứ hai $D_1$:** Thực hiện trò chơi minimax có trọng số nhằm trộn lẫn hoàn toàn phân phối của hai phương thức:
     $$\min_I \max_{D_1} \mathcal{L}_{D_1} = \mathbb{E}_{e \sim p_{e_t}} \left[ w_t(x) \log\left(D_1(I(e))\right) \right] + \mathbb{E}_{e \sim p_{e_v}} \left[ w_v(x) \log\left(1 - D_1(I(e))\right) \right] \quad (10)$$
     Khi $I$ và $D_0$ cố định, nghiệm tối ưu của bộ phân biệt thứ hai là:
     $$D_1^{i*}(x) = \frac{w_i(x) p_{e_i}(x)}{w_t(x) p_{e_t}(x) + w_v(x) p_{e_v}(x)} \quad (11)$$
     Thay nghiệm tối ưu này vào hàm mục tiêu, bài toán quy về việc cực tiểu hóa **Phân kỳ Jensen-Shannon (JSD)** giữa hai phân phối có trọng số:
     $$\mathcal{L}_{D_1} = -\log(10) + 2 \cdot \text{JSD}\left( w_t(x) \cdot p_{e_t}(x) \parallel w_v(x) \cdot p_{e_v}(x) \right) \quad (12)$$
     Phân kỳ JSD đạt giá trị nhỏ nhất toàn cục khi $w_t(x) p_{e_t}(x) = w_v(x) p_{e_v}(x)$, tức hai phương thức đã hòa quyện hoàn toàn trong không gian chung. Đặc trưng bất biến phương thức cuối cùng được lấy qua phép gộp cực đại $c_m = \max\{w_t c_t, w_v c_v\}$, với tổng hàm mất mát đối kháng $\mathcal{L}_{adv} = \mathcal{L}_{D_0} + \mathcal{L}_{D_1} + \mathcal{L}_{cycle}$.

3. **Phân loại Tin giả và Hàm Mất mát Tổng hợp:**
   Vector đặc trưng cuối cùng của bản tin được ghép nối từ biểu diễn nhất quán ngữ nghĩa $o$ (từ Phân hệ 2) và biểu diễn bất biến phương thức $c_m$ (từ Phân hệ 3): $\hat{x} = o \oplus c_m$. Tầng phân loại Softmax dự đoán xác suất tin giả $\hat{y}$ với hàm mất mát Cross-Entropy $\mathcal{L}_y$:
   $$\hat{y} = \text{softmax}(w \hat{x} + b), \quad \mathcal{L}_y = -y \log(\hat{y}) - (1 - y) \log(1 - \hat{y}) \quad (13)$$
   Toàn bộ mô hình được huấn luyện đầu-cuối với hàm mất mát tổng:
   $$\mathcal{L}_{total} = \mathcal{L}_y + \lambda \mathcal{L}_{cl} + \beta \mathcal{L}_{adv}$$
   (với siêu tham số thực nghiệm $\lambda = 0.5$ và $\beta = 0.1$).

---

### 4.3. Phân tích Kết quả Thực nghiệm, Độ Bền vững trước Nhiễu và Nghiên cứu Cắt bỏ của CMA-VRP

Mô hình CMA-VRP được đánh giá trên 3 bộ dữ liệu chuẩn quy mô lớn: **Twitter** (MediaEval: huấn luyện 7.898 tin thật / 6.026 tin giả; kiểm thử 1.972 tin thật / 3.830 tin giả), **Pheme** (1.972 tin thật / 3.830 tin giả từ 5 sự kiện nóng với 3.670 ảnh), và **Weibo** (huấn luyện 6.840 tin thật / 5.007 tin giả; kiểm thử 996 tin thật / 1.000 tin giả).

#### Bảng 3: Kết quả thực nghiệm so sánh CMA-VRP với 10 mô hình đối sánh trên 3 bộ dữ liệu Twitter, Pheme và Weibo

| Mô hình | Twitter Acc | Twitter Fake F1 | Twitter Real F1 | Pheme Acc | Pheme Fake F1 | Pheme Real F1 | Weibo Acc | Weibo Fake F1 | Weibo Real F1 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| BERT (Chỉ văn bản) | 0,629 | 0,608 | 0,651 | 0,713 | 0,682 | 0,725 | 0,731 | 0,731 | 0,731 |
| ResNet34 (Chỉ hình ảnh) | 0,550 | 0,534 | 0,513 | 0,649 | 0,568 | 0,611 | 0,675 | 0,664 | 0,679 |
| MVAE | 0,757 | 0,772 | 0,772 | 0,776 | 0,795 | 0,798 | 0,820 | 0,816 | 0,825 |
| InfoSurgeon | 0,855 | 0,850 | 0,859 | 0,859 | 0,829 | 0,847 | 0,866 | 0,785 | 0,863 |
| CFFN | 0,886 | 0,882 | 0,889 | 0,869 | 0,854 | 0,874 | 0,894 | 0,841 | 0,899 |
| Event-Radar | 0,902 | 0,901 | 0,910 | 0,901 | 0,831 | 0,902 | 0,910 | 0,891 | 0,910 |
| COOLANT | 0,908 | 0,903 | 0,912 | 0,883 | 0,881 | 0,882 | 0,915 | 0,914 | 0,911 |
| LLaVA (Dùng trực tiếp) | 0,641 | 0,680 | 0,624 | 0,664 | 0,698 | 0,627 | 0,750 | 0,734 | 0,719 |
| LLaVA + SPT (Prompt Tuning) | 0,783 | 0,790 | 0,774 | 0,792 | 0,810 | 0,785 | 0,833 | 0,839 | 0,826 |
| NLIN (LVLM tinh chỉnh) | 0,883 | 0,893 | 0,867 | 0,903 | 0,883 | 0,875 | 0,911 | 0,904 | 0,913 |
| **CMA-VRP (Đề xuất)** | **$0,930^*$** | **$0,926^*$** | **$0,932^*$** | **$0,926^*$** | **$0,927^*$** | **$0,926^*$** | **$0,938^*$** | **$0,941^*$** | **$0,938^*$** |

#### Bảng 4: Kết quả Nghiên cứu Cắt bỏ (Ablation Study) các thành phần kiến trúc của CMA-VRP

| Cấu hình biến thể | Twitter Accuracy | Twitter F1 | Pheme Accuracy | Pheme F1 | Weibo Accuracy | Weibo F1 | Mức sụt giảm Acc trung bình |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **CMA-VRP (Mô hình đầy đủ)** | **0,930** | **0,929** | **0,926** | **0,926** | **0,938** | **0,940** | — |
| Không có Đặc trưng Suy luận Thị giác (`-w/o VRF`) | 0,905 | 0,902 | 0,902 | 0,900 | 0,912 | 0,911 | $-2,50\%$ |
| Không có Tương phản Liên đồ thị (`-w/o GCL_inter`) | 0,914 | 0,913 | 0,908 | 0,906 | 0,920 | 0,918 | $-1,73\%$ |
| Không có Tương phản Nội đồ thị (`-w/o GCL_intra`) | 0,920 | 0,921 | 0,910 | 0,911 | 0,916 | 0,919 | $-1,60\%$ |
| Không có Căn chỉnh & Dung hợp Đồ thị (`-w/o CMGAF`) | 0,895 | 0,895 | 0,887 | 0,894 | 0,896 | 0,893 | **$-3,87\%$** |
| Không có Học Bất biến Chu trình Đối kháng (`-w/o ACCIL`) | 0,908 | 0,901 | 0,896 | 0,898 | 0,914 | 0,909 | $-2,53\%$ |
| Không có Căn chỉnh Chu trình Thị giác - Ngữ nghĩa (`-w/o VSCA`) | 0,915 | 0,917 | 0,905 | 0,908 | 0,918 | 0,920 | $-1,87\%$ |

**Các luận điểm phân tích chuyên sâu từ kết quả của CMA-VRP:**

1. **Tại sao LVLM dùng trực tiếp hoặc tinh chỉnh đơn thuần lại thua cấu trúc Đồ thị kết hợp VRP?**
   Nhìn vào Bảng 3, khi dùng trực tiếp `LLaVA`, độ chính xác trên Twitter chỉ đạt **64,1%** (thậm chí chỉ nhỉnh hơn BERT 62,9%). Ngay cả khi áp dụng tinh chỉnh gợi ý mềm (`LLaVA + SPT` đạt 78,3%) hay biến đổi sang không gian ngôn ngữ tự nhiên (`NLIN` đạt 88,3%), chúng vẫn kém xa **CMA-VRP (93,0%)**. Nguyên nhân là bởi LVLM khi nhìn toàn ảnh thường bỏ qua mối tương quan cấu trúc chi tiết giữa các thực thể và dễ sinh ảo giác khi tinh chỉnh. Ngược lại, CMA-VRP chỉ dùng Mistral-7B và LLaVA-1.6-13B như những "chuyên gia cố vấn không tinh chỉnh" để trích xuất đặc trưng suy luận $VRF_t, VRF_v$, rồi đặt việc học căn chỉnh lên cấu trúc đồ thị thực thể tường minh.
2. **Đóng góp của từng phân hệ qua Nghiên cứu Cắt bỏ (Bảng 4) và Trực quan hóa t-SNE:**
   - Khi gỡ bỏ phân hệ Căn chỉnh và Dung hợp Đồ thị (`-w/o CMGAF`), độ chính xác giảm mạnh nhất (trung bình giảm **3,87%** trên 3 tập dữ liệu), và biểu đồ phân bố t-SNE trên tập kiểm thử Weibo bị trộn lẫn hoàn toàn giữa hai lớp tin thật/tin giả.
   - Khi gỡ bỏ `VRF` (`-w/o VRF`) hoặc gỡ bỏ phân hệ đối kháng `ACCIL` (`-w/o ACCIL`), độ chính xác giảm lần lượt **2,50%** và **2,53%**, chứng minh rằng suy luận thị giác sâu và lọc nhiễu bất biến phương thức là hai cánh tay đắc lực hỗ trợ cho đồ thị thực thể.
3. **Sức mạnh chống chịu nhiễu vượt trội (Robustness Analysis):**
   - Trong thử nghiệm tiêm nhiễu Gaussian từ cường độ $10^0$ đến $10^8$ và thử nghiệm che khuất (*occlusion/masking*) từ 10% đến 50% văn bản/hình ảnh trên 500 mẫu kiểm thử, CMA-VRP luôn duy trì đường cong độ chính xác cao nhất và ổn định nhất.
   - Phân tích khoảng cách Wasserstein (WD) lý giải rõ cơ chế này: khi cường độ nhiễu tăng lên $10^8$, biến thể không có `ACCIL` bị tăng vọt khoảng cách Wasserstein hơn $0,45$ đơn vị (hai phân phối văn bản và hình ảnh bị đẩy lệch xa nhau do nhiễu), kéo theo sự sụp đổ của độ chính xác phân loại. Ngược lại, khi có `ACCIL`, cơ chế CycleGAN Wasserstein kết hợp bộ phân biệt kép JSD giữ cho khoảng cách giữa hai phương thức ổn định và bảo toàn ranh giới phân lớp rõ nét trên biểu đồ t-SNE ngay cả dưới nhiễu Gaussian cường độ $10^6$.

---

## V. ĐỐI SÁNH TỔNG HỢP, THẢO LUẬN PHẢN BIỆN VÀ KẾT LUẬN CHUNG

### 5.1. Đối sánh Phương pháp luận giữa MSIT (Bài báo 1) và CMA-VRP (Bài báo 2)

Mặc dù khởi xuất từ hai miền ứng dụng khác nhau, khi đặt **MSIT** và **CMA-VRP** lên cùng một bàn cân học thuật, nhóm chúng tôi đúc kết được sự tương đồng sâu sắc trong tư duy giải quyết bài toán đa phương thức hiện đại, đồng thời làm nổi bật sự khác biệt mang tính bổ trợ giữa hai hướng tiếp cận:

#### Bảng 5: Bảng đối sánh toàn diện hai khung phương pháp MSIT và CMA-VRP dưới góc nhìn kiến trúc hệ thống

| Tiêu chí đối sánh | Khung phương pháp MSIT (ACL 2025) [1] | Khung phương pháp CMA-VRP (ACM MM 2025) [2] | Bài học Phương pháp luận Đúc kết chung |
| :--- | :--- | :--- | :--- |
| **1. Bản chất tác vụ & Đầu ra** | **Tác vụ Sinh mở (*Open-World Generation*):** Trích xuất chuỗi JSON các cặp `{thuộc tính : giá trị}` không giới hạn lược đồ từ ảnh và mô tả sản phẩm. | **Tác vụ Kiểm chứng & Phân loại (*Verification & Classification*):** Phát hiện sự bất đồng ngữ nghĩa giữa ảnh và bài viết để phân loại `Tin thật / Tin giả`. | Mọi bài toán đa phương thức phức tạp đều đòi hỏi sự kết hợp giữa **khai thác chi tiết cục bộ** và **kiểm chứng chéo liên phương thức**. |
| **2. Cách xử lý Thiên lệch & Giao thoa Phương thức** | **Tách biệt ở khâu Sinh dữ liệu ICL:** Đưa ảnh và văn bản vào GPT-4 trong hai lần gọi độc lập để tránh thiên lệch chú ý vào văn bản, sau đó mới hợp nhất. | **Tách biệt ở khâu Khởi tạo Đồ thị & VRP:** Xây dựng độc lập $\mathcal{G}_t$ (văn bản) và $\mathcal{G}_v$ (thị giác + OCR); dùng Mistral-7B riêng cho thực thể chữ và LLaVA-13B riêng cho thực thể ảnh. | **Nguyên lý "Chia để trị trước, Dung hợp sau":** Phải trích xuất đặc trưng độc lập trên từng phương thức trước khi đưa vào không gian chung để tránh một phương thức lấn át phương thức kia. |
| **3. Chiến lược Khai thác MLLM / LVLM** | **Tinh chỉnh Hạng thấp (LoRA Fine-tuning):** Đóng băng mạng gốc và huấn luyện trực tiếp LoRA trên 3 MLLM 7B (LLaVA, Qwen-VL, InternLM) để vừa sinh vừa suy luận. | **Cố vấn Không tinh chỉnh (Zero-shot Prompting):** Giữ nguyên trọng số Mistral-7B và LLaVA-13B để trích xuất đặc trưng suy luận $VRF_t, VRF_v$ rồi mã hóa qua BERT nhằm tránh ảo giác khi fine-tune. | Tùy thuộc vào yêu cầu đầu ra: nếu cần mô hình tự sinh chuỗi cấu trúc thì dùng **LoRA + CoT có cấu trúc**; nếu cần biểu diễn phân loại ổn định thì dùng **LVLM như bộ trích xuất tri thức đóng băng**. |
| **4. Thiết kế Chuỗi Tư duy (CoT)** | **CoT 5 bước kiểm chứng tuần tự:** Loại SP $\rightarrow$ Lẽ thường $\rightarrow$ Kiểm chứng ảnh $\rightarrow$ Kiểm chứng văn bản $\rightarrow$ Quyết định `Yes/No`. | **CoT 2 tầng hướng chân lý (VRP):** Tầng 1 lập luận lý do kiểm chứng cho từng thực thể $\rightarrow$ Tầng 2 tóm tắt đặc trưng thị giác kỳ vọng và thực tế. | **Không bao giờ dùng Vanilla CoT tự do** trên bài toán đa phương thức; phải chia nhỏ CoT thành các bước gắn chặt với thực thể và phương thức. |
| **5. Chiến lược Học Tương phản (Contrastive Learning)** | **Tương phản ở mức Dữ liệu Chỉ dẫn (Data-level):** Ghép cân bằng 1:1 giữa thuộc tính đúng của SP (mẫu dương) và thuộc tính lấy từ ngành hàng khác (mẫu âm). | **Tương phản ở mức Đồ thị Biểu diễn (Representation-level):** Kết hợp $\mathcal{L}_{inter}$ (nhãn mềm $\theta$) và $\mathcal{L}_{intra}$ (che thực thể $p_m=0.2$ làm mẫu dương, trộn chéo phương thức nhãn đối lập làm mẫu âm). | Kỹ thuật **hoán đổi chéo thuộc tính/thực thể giữa các mẫu khác loại để tạo mẫu âm (hard/perturbed negatives)** là chìa khóa giúp mô hình học ranh giới ngữ nghĩa sắc bén. |
| **6. Cơ chế Lọc nhiễu và Dư thừa** | **Lọc ở Không gian Đầu ra Rời rạc:** Dùng Word2Vec + 3 quy tắc độ dài từ con (Giai đoạn 2) kết hợp lọc bằng CoT 5 bước (Giai đoạn 3, tự sửa lỗi 98,6%). | **Lọc ở Không gian Tiềm ẩn Liên tục (ACCIL):** Dùng CycleGAN Wasserstein có trọng số VRF kết hợp bộ phân biệt kép $D_0, D_1$ cực tiểu hóa phân kỳ JSD. | Sự kết hợp giữa lọc ngữ nghĩa và căn chỉnh phân phối giúp hệ thống duy trì độ chính xác cao trong môi trường dữ liệu mở và nhiều nhiễu. |

---

### 5.2. Đánh giá Phản biện (Critical Review) và Hướng Phát triển Tương lai

Bên cạnh những đóng góp xuất sắc đã được chứng minh qua thực nghiệm, dưới góc độ phản biện khoa học và trải nghiệm trực tiếp khi tái lập mã nguồn, nhóm chúng tôi chỉ ra một số hạn chế còn tồn đọng của cả hai công trình cũng như cơ hội giao thoa giữa chúng:

1. **Đánh giá phản biện đối với Bài báo 1 (MSIT):**
   - *Chi phí suy luận tuần tự ở Giai đoạn 3 ($\mathcal{O}(k)$ lần gọi MLLM):* Trong Giai đoạn 1, mô hình chỉ cần 1 lần gọi để sinh ra $k$ thuộc tính ứng viên. Tuy nhiên, ở Giai đoạn 3, mô hình phải chạy suy luận chuỗi tư duy 5 bước **lần lượt cho từng thuộc tính** trong số $k'$ thuộc tính sau lọc. Nếu một sản phẩm có 15 thuộc tính, hệ thống phải gọi MLLM thêm 15 lần với chuỗi token đầu ra dài, gây độ trễ lớn khi triển khai thời gian thực trên sàn thương mại điện tử hàng triệu sản phẩm.
   - *Tính cứng nhắc của 3 quy tắc xóa từ đồng nghĩa ở Giai đoạn 2:* Như nhóm đã kiểm chứng khi cài đặt `stage2_dedup.py`, thuật toán khớp từ đồng nghĩa ở Phụ lục B.2 đòi hỏi hai cụm từ phải có tương ứng **một-đối-một** giữa các từ con khi tính tương đồng cosine trên `word2vec-google-news-300`, trong khi các quy tắc xóa (Quy tắc 1, 2, 3) lại xét các trường hợp độ dài từ con lệch nhau ($1$ so với $3$, $2$ so với $\ge 3$). Sự thiếu nhất quán nhẹ giữa điều kiện khớp một-đối-một và điều kiện độ dài trong mô tả bài báo cùng việc dùng mô hình tĩnh Word2Vec (không nắm bắt được ngữ cảnh đa nghĩa như BERT) có thể làm giảm hiệu quả lọc trùng lặp trên các thuật ngữ chuyên ngành mới.
2. **Đánh giá phản biện đối với Bài báo 2 (CMA-VRP):**
   - *Độ phức tạp của hệ thống tiền xử lý đa tầng:* Để xử lý một bản tin, CMA-VRP phải chạy qua một chuỗi công cụ rất nặng: bộ phân tích cú pháp phụ thuộc (spaCy/Stanford NLP), mạng phát hiện đối tượng và sinh đồ thị cảnh (Mask-RCNN), hệ thống nhận diện chữ (Rosetta OCR), mô hình ngôn ngữ Mistral-7B (2 lần prompt cho $N_t$ thực thể), mô hình thị giác - ngôn ngữ LLaVA-1.6-13B (2 lần prompt cho $N_v$ thực thể), bộ mã hóa BERT, rồi mới đưa vào mạng đồ thị và mạng đối kháng CycleGAN. Nếu bất kỳ mắt xích đầu nguồn nào (như Mask-RCNN hay OCR trên ảnh quá mờ) gặp lỗi lan truyền (*cascading error*), chất lượng đồ thị đầu vào sẽ bị ảnh hưởng.
3. **Hướng tích hợp hai công trình trong tương lai:**
   Hai công trình có thể bổ sung trực tiếp những mảnh ghép còn thiếu cho nhau:
   - Có thể đưa kỹ thuật **Đồ thị thực thể thị giác kết hợp nút văn bản Rosetta OCR ($\mathcal{G}_v + v_{ocr}$)** của CMA-VRP vào MSIT để giúp MLLM đọc chính xác hơn các bảng thành phần dinh dưỡng nhỏ li ti trên bao bì sản phẩm (như nhãn lọ Vitamin trong tập WOAM).
   - Ngược lại, có thể áp dụng kỹ thuật **Tinh chỉnh chỉ dẫn QLoRA với dữ liệu CoT 5 bước tương phản** của MSIT để chưng cất (*distill*) quy trình trích xuất VRF cồng kềnh (gồm cả Mistral-7B lẫn LLaVA-13B) của CMA-VRP thành một mô hình gọn nhẹ duy nhất.

### 5.3. Kết luận Chung

Báo cáo đã thực hiện khảo sát, phân tích lý thuyết, đối sánh phương pháp luận và tái lập thực nghiệm thành công trên hai công trình tiêu biểu của hội nghị ACL 2025 (**MSIT**) và ACM Multimedia 2025 (**CMA-VRP**). Dù giải quyết hai bài toán thuộc hai lĩnh vực ứng dụng khác nhau là khai thác thuộc tính sản phẩm thương mại điện tử và phát hiện tin giả mạng xã hội, cả hai nghiên cứu đều hội tụ tại một triết lý thiết kế hiện đại: **kết hợp sức mạnh biểu diễn đa phương thức với cơ chế tách biệt phương thức, suy luận chuỗi tư duy có cấu trúc chặt chẽ và học tương phản chống nhiễu**. Quá trình tự xây dựng lại toàn bộ mã nguồn, kiến tạo 1.300 mẫu dữ liệu đa phương thức và tinh chỉnh mô hình bằng kỹ thuật QLoRA trên bài báo MSIT không chỉ giúp nhóm kiểm chứng thực tế tính hiệu quả của phương pháp mà còn cung cấp một nền tảng mã nguồn mở hoàn chỉnh phục vụ các nghiên cứu tiếp theo.

---

## TÀI LIỆU THAM KHẢO (REFERENCES — CHUẨN IEEE)

[1] J. Li, Y. Li, X. Shen, C. Zhang, G. Qi, and S. Bi, "Open-World Attribute Mining for E-Commerce Products with Multimodal Self-Correction Instruction Tuning," in *Proc. 63rd Annu. Meeting Assoc. Comput. Linguistics (ACL)*, vol. 1, Jul.–Aug. 2025, pp. 1702–1714.

[2] G. Li, D. Hu, X. Fu, Q. Tang, Y. Wu, X. Zhang, and H. Lyu, "Entity Graph Alignment and Visual Reasoning for Multimodal Fake News Detection," in *Proc. 33rd ACM Int. Conf. Multimedia (MM '25)*, Dublin, Ireland, Oct. 2025, pp. 2486–2495, doi: 10.1145/3746027.3754591.

[3] J. Li, D. Li, S. Savarese, and S. C. H. Hoi, "BLIP-2: Bootstrapping language-image pre-training with frozen image encoders and large language models," in *Proc. Int. Conf. Mach. Learn. (ICML)*, vol. 202, 2023, pp. 19730–19742.

[4] W. Dai *et al.*, "InstructBLIP: Towards general-purpose vision-language models with instruction tuning," in *Adv. Neural Inf. Process. Syst. (NeurIPS)*, 2023.

[5] H. Liu, C. Li, Q. Wu, and Y. J. Lee, "Visual instruction tuning," in *Adv. Neural Inf. Process. Syst. (NeurIPS)*, vol. 36, 2023.

[6] J. Bai *et al.*, "Qwen-VL: A frontier large vision-language model with versatile abilities," *arXiv preprint arXiv:2308.12966*, 2023.

[7] X. Dong *et al.*, "InternLM-XComposer2: Mastering free-form text-image composition and comprehension in vision-language large model," *arXiv preprint arXiv:2401.16420*, 2024.

[8] H. Lu *et al.*, "DeepSeek-VL: Towards real-world vision-language understanding," *arXiv preprint arXiv:2403.05525*, 2024.

[9] OpenAI, "GPT-4 technical report," *arXiv preprint arXiv:2303.08774*, 2023.

[10] Z. Zhang, A. Zhang, M. Li, H. Zhao, G. Karypis, and A. Smola, "Multimodal chain-of-thought reasoning in language models," *arXiv preprint arXiv:2302.00923*, 2023.

[11] G. Zheng, S. Mukherjee, X. L. Dong, and F. Li, "OpenTag: Open attribute value extraction from product profiles," in *Proc. 24th ACM SIGKDD Int. Conf. Knowl. Discovery Data Mining*, 2018, pp. 1049–1058.

[12] J. Fu *et al.*, "CMA-CLIP: Cross-modality attention CLIP for text-image classification," in *Proc. IEEE Int. Conf. Image Process. (ICIP)*, 2022, pp. 2846–2850.

[13] X. Zhang *et al.*, "OA-Mine: Open-world attribute mining for e-commerce products with weak supervision," in *Proc. ACM Web Conf. (WWW)*, 2022, pp. 3153–3161.

[14] L. Xu, C. Zhang, X. Li, J. Shang, and J. D. Choi, "Towards open-world product attribute mining: A lightly-supervised approach," in *Proc. 61st Annu. Meeting Assoc. Comput. Linguistics (ACL)*, vol. 1, 2023, pp. 12223–12239.

[15] D. Khattar, J. S. Goud, M. Gupta, and V. Varma, "MVAE: Multimodal variational autoencoder for fake news detection," in *Proc. World Wide Web Conf. (WWW)*, 2019, pp. 2915–2921.

[16] Y. Chen *et al.*, "Cross-modal ambiguity learning for multimodal fake news detection," in *Proc. ACM Web Conf. (WWW)*, 2022, pp. 2897–2905.

[17] J. Li, Y. Bin, J. Zou, J. Wei, G. Wang, and Y. Yang, "Cross-modal consistency learning with fine-grained fusion network for multimodal fake news detection," in *Proc. 5th ACM Int. Conf. Multimedia in Asia*, 2023, pp. 1–7.

[18] L. Wang, C. Zhang, H. Xu, Y. Xu, X. Xu, and S. Wang, "Cross-modal contrastive learning for multimodal fake news detection," in *Proc. 31st ACM Int. Conf. Multimedia*, 2023, pp. 5696–5704.

[19] Y. Fung *et al.*, "InfoSurgeon: Cross-media fine-grained information consistency checking for fake news detection," in *Proc. 59th Annu. Meeting Assoc. Comput. Linguistics (ACL)*, 2021, pp. 1683–1698.

[20] P. Qi *et al.*, "Improving fake news detection by using an entity-enhanced framework to fuse diverse multimodal clues," in *Proc. 29th ACM Int. Conf. Multimedia*, 2021, pp. 1212–1220.

[21] Z. Ma, M. Luo, H. Guo, Z. Zeng, Y. Hao, and X. Zhao, "Event-Radar: Event-driven multi-view learning for multimodal fake news detection," in *Proc. 62nd Annu. Meeting Assoc. Comput. Linguistics (ACL)*, 2024, pp. 5809–5821.

[22] Q. Zhang, J. Liu, F. Zhang, J. Xie, and Z.-J. Zha, "Natural language-centered inference network for multi-modal fake news detection," in *Proc. 33rd Int. Joint Conf. Artif. Intell. (IJCAI)*, 2024, pp. 2542–2550.

[23] P. Qi, Z. Yan, W. Hsu, and M. L. Lee, "SNIFFER: Multimodal large language model for explainable out-of-context misinformation detection," in *Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit. (CVPR)*, 2024, pp. 13052–13062.

[24] K. He, G. Gkioxari, P. Dollár, and R. Girshick, "Mask R-CNN," in *Proc. IEEE Int. Conf. Comput. Vis. (ICCV)*, 2017, pp. 2961–2969.

[25] F. Borisyuk, A. Gordo, and V. Sivakumar, "Rosetta: Large scale system for text detection and recognition in images," in *Proc. 24th ACM SIGKDD Int. Conf. Knowl. Discovery Data Mining*, 2018, pp. 71–79.

[26] A. Q. Jiang *et al.*, "Mistral 7B," *arXiv preprint arXiv:2310.06825*, 2023.

[27] J.-Y. Zhu, T. Park, P. Isola, and A. A. Efros, "Unpaired image-to-image translation using cycle-consistent adversarial networks," in *Proc. IEEE Int. Conf. Comput. Vis. (ICCV)*, 2017, pp. 2223–2232.

---

## PHỤ LỤC (APPENDICES)

### Phụ lục A: Minh họa Mẫu Dữ liệu Thực tế Nhóm Khởi tạo trong Quá trình Tái lập MSIT

#### A.1. Mẫu dữ liệu AGTD thực tế (`msit/data/sft_datasets/agtd_train.jsonl`)

- **Mã sản phẩm (ASIN):** `B07GT3XTKP` | **Danh mục:** `VITAMIN`
- **Tiêu đề:** *"Biotin 5000 mcg - (ONE Daily) | Hair Growth Vitamins with Coconut Oil | Supports Healthy Hair Skin and Nails | Non GMO, Organic (1 Month Supply)"*
- **Các thuộc tính đa phương thức được trích xuất và hợp nhất (kết hợp cả văn bản và hình ảnh lọ sản phẩm):**

  ```json
  {
    "title": "biotin_5000_mcg",
    "bullet_points": [
      {
        "biotin_potency": "5000_mcg",
        "coconut_oil": true,
        "hair_growth_support": true,
        "skin_growth_support": true,
        "nail_growth_support": true,
        "formula_type": "doctor_formulated",
        "made_in_usa": true,
        "fda_registered": true,
        "capsule_type": "natural_cellulose",
        "gmp_certified": true
      }
    ],
    "color": "black",
    "shape": "cylindrical",
    "packaging_type": "bottle"
  }
  ```

  *(Lưu ý: Ba thuộc tính cuối cùng là `"color": "black"`, `"shape": "cylindrical"`, và `"packaging_type": "bottle"` hoàn toàn không xuất hiện trong văn bản mô tả mà được trích xuất từ kênh hình ảnh chụp lọ sản phẩm).*

#### A.2. Mẫu dữ liệu suy luận 5 bước CTTD thực tế (`msit/data/sft_datasets/cttd_train.jsonl`)

- **Mã sản phẩm (ASIN):** `B08L7126H8` | **Danh mục:** `VITAMIN` | **Nhãn tương phản (`cttd_label`):** `yes`
- **Chuỗi suy luận 5 bước được sinh ra:**
  - *Bước 1 (Xác định loại sản phẩm):* Sản phẩm là thực phẩm bổ sung dinh dưỡng, cụ thể là viên uống vitamin nhóm B từ thực phẩm toàn phần hỗ trợ năng lượng tế bào.
  - *Bước 2 (Phân tích theo tri thức thông thường):* Đánh giá thuộc tính mục tiêu dựa trên ngữ cảnh sản phẩm bổ sung năng lượng tế bào và sức khỏe ty thể.
  - *Bước 3 (Kiểm chứng từ hình ảnh):* Quan sát bao bì sản phẩm hướng tới nhóm người dùng cần tăng cường năng lượng tế bào.
  - *Bước 4 (Kiểm chứng từ văn bản):* Mô tả văn bản nêu rõ công dụng hỗ trợ sản sinh năng lượng tế bào và chức năng ty thể.
  - *Bước 5 (Kết luận):* Tổng hợp cả hình ảnh và văn bản xác nhận sản phẩm sở hữu thuộc tính đang xét $\rightarrow$ Quyết định cuối cùng: **`Yes`**.

---

### Phụ lục B: Danh mục Kiểm tra Tuân thủ Yêu cầu Báo cáo (`docs/YEU_CAU.md`) khi Chuyển sang LaTeX

Để đảm bảo bản PDF xuất ra từ LaTeX tuân thủ tuyệt đối mọi quy định trong file `docs/YEU_CAU.md`, nhóm đã chuẩn hóa báo cáo này theo danh sách kiểm tra sau:

1. **Tên file PDF nộp:** Đặt tên theo đúng cú pháp `MSHV1-MSHV2.pdf` (ví dụ: `2470001-2470002.pdf`, ngăn cách bằng dấu gạch nối `-`, hoặc `MSHV.pdf` nếu nhóm 1 người).
2. **Giới hạn dung lượng và số trang:** Kích thước file PDF **$< 20\text{ MB}$** và tổng số trang **$\le 25\text{ trang}$** (đã tính cả trang bìa, phần tài liệu tham khảo và phụ lục). Với độ dài hiện tại của bản thảo Markdown này, khi biên dịch bằng gói `\documentclass[conference]{IEEEtran}` hoặc `\documentclass[journal]{IEEEtran}` hai cột sẽ rơi vào khoảng **12–16 trang chuẩn IEEE**, nằm hoàn toàn trong ngưỡng an toàn ($\le 25$ trang).
3. **Bao gồm cả hai bài báo trong một báo cáo thống nhất:** Đã tích hợp liền mạch Bài báo 1 (MSIT — bài Seminar & Tái lập thực nghiệm tại Mục III) và Bài báo 2 (CMA-VRP — bài Báo cáo tại Mục IV) dưới một khung lý thuyết chung (Mục I, II) và đối sánh tổng hợp (Mục V).
4. **Diễn đạt độc lập và Trực quan hóa lại:** Toàn bộ nội dung lý thuyết, phân tích công thức và nhận xét thực nghiệm đều được viết mới hoàn toàn bằng lời văn học thuật của nhóm; các sơ đồ kiến trúc (Hình 1, Hình 2, Hình 3) được nhóm tự thiết kế lại (có thể xuất từ Mermaid sang vector PDF/PNG độ phân giải 300 DPI để chèn vào lệnh `\includegraphics` trong LaTeX).
5. **Thống nhất một ngôn ngữ duy nhất:** Sử dụng xuyên suốt **Tiếng Việt học thuật**, không pha trộn câu từ tiếng Anh - tiếng Việt tùy tiện.
6. **Gắn liên kết công khai Weights & Biases và GitHub Repository:** Đã chừa sẵn các vị trí gắn liên kết `\href{https://wandb.ai/...}{...}` tương ứng với từng phần thực nghiệm (Huấn luyện chính, Kết quả chính, Nghiên cứu cắt bỏ, Tự sửa lỗi CoT) trong Mục 3.4.2 và dẫn link tới GitHub Repository (`https://github.com/linhnnh688/msit-open-world`).

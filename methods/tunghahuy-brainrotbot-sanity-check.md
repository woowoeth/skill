---
name: sanity-check
description: Route CopyCat seed visual review to Antigravity before video prompting, so it can inspect source evidence and seeds, write the sanity report, and catch action-read, anatomy, physics, and continuity errors. Use after seed generation or repair; Codex fixes the reported seeds and prompts.
metadata:
  version: 1.5.0
---

# Sanity Check

Chặn seed lỗi trước khi lỗi đó bị khuếch đại sang video. Không PASS một ảnh chỉ
vì file tồn tại, prompt có vẻ đúng, hoặc từng vật thể riêng lẻ trông đẹp.

Antigravity đọc trước đúng project `style.md` mà CopyCat đã chọn, rồi đọc
`description.md`, `shots.json`, prompt ảnh, source clip, A/B/C và toàn bộ seed
liên quan trong thư mục dự án đang dùng (`seeds/` hoặc `gpt-seed/`).
Nó viết báo cáo bằng English vào `projects/<slug>/sanity-check.md`. Codex không
tự xem source/seed hay viết report: dùng `antigravity-taskgiving` cùng
`../antigravity-taskgiving/references/copycat-sanity.md` để giao review, rồi chỉ
sửa seed/image prompt theo báo cáo bàn giao.

## 1. Lập continuity group trước khi xét từng ảnh

Các shot liền kề thuộc cùng một continuity group khi chúng giữ nguyên sự kiện,
địa điểm, nhân vật và đạo cụ, chỉ đổi góc máy, cỡ cảnh hoặc thời điểm gần nhau.

Lập một bộ **continuity anchors bằng text** từ mô tả đã được quan sát. Những thứ
sau phải khóa:

- identity, face, skin tone, hair, age, height order và clothing;
- vehicle/prop shape, color, markings, wear và dimensions;
- environment layout, entrances, counters, freezer rim/interior và signage;
- time of day, key-light direction, color temperature và weather.

Camera và hành động được đổi theo mô tả shot; các invariant trên thì không.
Mọi seed phải text-to-image thuần prompt: không dùng source A/B/C, source shot,
master seed hay bất cứ image reference nào. Đừng generate từng góc với các mô tả
khác nhau rồi hy vọng chúng tự khớp.

## 2. Kiểm từng seed

1. **Description fidelity:** đúng chủ thể, số người, vị trí, trang phục, đạo cụ,
   camera, ánh sáng và frame state được mô tả.
2. **Action readability and geometry:** ảnh tĩnh phải làm hướng hành động sắp tới
   dễ hiểu. Quỹ đạo phải dẫn đến điểm tiếp cận hợp lý, không dẫn nhân vật vào
   vật cản, đầu xe, tường hoặc vị trí không thể thao tác.
3. **Anatomy:** tay có đúng năm ngón, khớp và cổ tay nối hợp lý; chi không dính,
   thừa, mất hoặc đổi skin tone; pose và tỷ lệ cơ thể khả thi.
4. **Physical plausibility:** kích thước vật, freezer basket, packaging, vapor,
   shadow, reflection và overlap phải tự nhiên; không vật bay, xuyên nhau hay
   biến dạng chỉ để vừa bố cục.
5. **Continuity:** so các seed trong group cạnh nhau; kiểm lại toàn bộ invariant,
   kể cả những chi tiết nền nhỏ giúp xác định đây là cùng một nơi và cùng vật.
6. **Text policy:** không bake title, subtitle hay watermark vào seed. Chỉ giữ
   chữ vật lý trên đạo cụ/sign khi `description.md` thực sự yêu cầu.
7. **Project style:** seed và continuity không vi phạm yêu cầu visual được ghi rõ
   trong `style.md`; title dành cho hậu kỳ vẫn không được bake vào seed.

## 3. Ghi gate report

Dùng bảng này trong `sanity-check.md`:

```markdown
# Seed sanity check

| Shot | Group | Continuity anchor | Description fidelity | Action read | Anatomy/physics | Continuity | Status | Required fix |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 01 | G1 | master | PASS | PASS | PASS | PASS | PASS | — |
```

Mỗi status chỉ là `PASS` hoặc `REVISE`. Với `REVISE`, ghi lỗi quan sát được,
invariant phải giữ, và một correction cụ thể. Sửa master trước; sau khi master
PASS, regenerate/edit toàn bộ dependent seed bị ảnh hưởng từ master đã duyệt.

Mặc định tối đa hai repair round cho mỗi seed sau lượt đầu. Nếu vẫn lỗi, ghi rõ
lỗi còn lại và giữ `REVISE`; không báo đạt và không viết prompt video cho shot đó.

## Gate hoàn thành

Chỉ chuyển sang video prompt khi:

- mọi seed bắt buộc đều `PASS`;
- mọi continuity group đã được so cạnh nhau, không chỉ duyệt từng ảnh riêng;
- mọi seed dùng đúng continuity anchor bằng text đã ghi;
- không còn lỗi action-read, anatomy hoặc physical plausibility nhìn thấy được.

Sau khi ghi report, chạy gate máy:

```bash
python scripts/cc_check.py --slug ten-goi --stage sanity
```

Validator kiểm đủ seed, image prompt, hàng báo cáo và status `PASS`; đánh giá
thị giác và continuity vẫn do agent thực hiện.

Antigravity không sửa seed, image prompt, video prompt hoặc `description.md` trong
task sanity. Codex sửa seed hoặc image prompt theo report. Khi gate PASS, giao
task video-prompt riêng cho Antigravity để nó xem seed + source evidence và viết
`prompts/video.md`. Nếu review chứng minh mô tả gốc sai, Codex giao lại bước
describe cho Antigravity thay vì tự xem source và sửa mô tả.

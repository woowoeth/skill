---
name: design-review
description: Kiểm tra giao diện đã dựng theo checklist accessibility, responsive, trạng thái và nhất quán trước khi bàn giao. Dùng sau khi hoàn thành bất kỳ thay đổi UI nào, hoặc khi được yêu cầu review giao diện.
---

# Design Review

Chạy checklist này TRƯỚC khi báo hoàn thành bất kỳ việc gì chạm giao diện.

## Cách chạy
1. Mở browser tại trang/màn hình vừa sửa
2. Chụp screenshot ở 375px, 768px, 1440px, lưu vào `.agents/artifacts/`
3. Đi qua từng mục dưới đây, đánh dấu đạt/không đạt
4. Báo cáo: mục nào không đạt + vị trí cụ thể + cách sửa

## Checklist

### Trạng thái (thiếu 1 = chưa xong)
- [ ] Loading — có skeleton hoặc chỉ báo, layout không nhảy
- [ ] Empty — giải thích lý do trống + hành động thoát ra
- [ ] Error — nói rõ lỗi gì, cách khắc phục, có nút thử lại
- [ ] Success/Data — hiển thị bình thường

### Responsive
- [ ] 375px: không cuộn ngang, không chữ tràn, không nút chồng nhau
- [ ] Bảng nhiều cột đã chuyển thành card/list trên mobile
- [ ] Touch target ≥ 44×44px
- [ ] Primary action nằm trong thumb zone trên mobile
- [ ] 1440px: nội dung không giãn quá rộng (max-width hợp lý)

### Accessibility
- [ ] Contrast ≥ 4.5:1 cho text, ≥ 3:1 cho icon và text lớn
- [ ] Tab đi qua đúng thứ tự, không bẫy focus
- [ ] Focus state nhìn thấy rõ trên mọi phần tử tương tác
- [ ] Escape đóng được modal/dropdown; focus trả về nơi mở
- [ ] Mọi input có label; icon-button có aria-label
- [ ] Không truyền tin chỉ bằng màu sắc
- [ ] Ảnh có alt phù hợp (alt rỗng nếu ảnh trang trí)

### Nhất quán
- [ ] Không hardcode màu / spacing / font-size — đều dùng token
- [ ] Spacing theo thang 4px
- [ ] Chỉ MỘT primary action trên màn hình
- [ ] Từ ngữ nhất quán với phần còn lại của sản phẩm
- [ ] Nút disabled có tooltip giải thích

### Nội dung
- [ ] Thông báo lỗi nói được cách khắc phục, không hiện mã lỗi trần
- [ ] Không còn văn bản mẫu (Lorem ipsum, "Tiêu đề ở đây")
- [ ] Số có đơn vị; ngày giờ có định dạng nhất quán

## Báo cáo

```
Đã kiểm: <trang/màn hình> tại 375 / 768 / 1440
Screenshot: .agents/artifacts/<tên>-{375,768,1440}.png

KHÔNG ĐẠT:
- <mục> tại <vị trí cụ thể> → sửa: <cách>

ĐẠT: <liệt kê nhóm đã qua>
```

Không viết "trông ổn". Nói rõ đã kiểm những gì.

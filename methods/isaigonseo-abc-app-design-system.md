---
name: app-design-system
description: Nguyên tắc thiết kế ứng dụng chuyên nghiệp kết hợp Material Design 3, Apple HIG, tâm lý học UX, Enterprise UX, dashboard và accessibility. Dùng khi thiết kế app, web app, dashboard, SaaS tool, admin panel, form phức tạp, data table, hoặc bất kỳ giao diện ứng dụng nào. Cũng dùng khi được hỏi về UX/UI best practices, design system, responsive design, accessibility.
---

# App Design System

Áp dụng cho web app (React/HTML) và đa nền tảng. Đọc file trong `references/` khi cần chi tiết.

## Bước 1 — Phân loại sản phẩm

| Loại | Chiến lược | Đọc thêm |
|---|---|---|
| Consumer (B2C) | Engagement, cảm xúc, onboarding nhanh | `references/design-foundations.md` |
| Enterprise/SaaS (B2B) | Task completion, mật độ dữ liệu cao, chính xác | `references/enterprise-ux.md` |
| Dashboard/Analytics | Phân cấp thị giác, data-ink ratio, KPI placement | `references/dashboard-dataviz.md` |
| AI-powered tool | Minh bạch, advisory mode, cognitive forcing | `references/ai-interaction.md` |

## Bước 2 — 6 định luật tâm lý học phải kiểm tra

1. **Fitts's Law** — Primary action phải lớn, dễ với tới. Mobile: đặt trong thumb zone. Touch target ≥ 44×44px.
2. **Miller's Law (7±2)** — Navigation ≤ 5-7 mục. Form dài → chia multi-step. Nhóm thông tin liên quan.
3. **Hick's Law** — Ít lựa chọn = quyết định nhanh. Ẩn option nâng cao qua progressive disclosure. Mỗi màn hình chỉ MỘT primary action.
4. **Tesler's Law** — Độ phức tạp không biến mất, chỉ chuyển chỗ. Gánh ở backend, giữ frontend đơn giản — nhưng không cắt tính năng cốt lõi.
5. **Zeigarnik Effect** — Progress bar cho quy trình nhiều bước. Hiển thị trạng thái chưa hoàn thành.
6. **Law of Common Region** — Nhóm trường liên quan bằng background hoặc border nhẹ.

## Bước 3 — Chọn design language

- **Đa nền tảng / Android / Web**: Material Design 3 — dynamic color, expressive components, shape mềm
- **iOS/macOS**: Apple HIG — tối ưu theo thiết bị, direct manipulation, depth qua blur/material
- **Web SaaS/Enterprise**: kết hợp + Enterprise UX — mật độ cao có cấu trúc, progressive disclosure, Command Palette (Cmd+K)

Chi tiết: `references/design-foundations.md`

## Bước 4 — Accessibility (BẮT BUỘC, không thương lượng)

- Contrast ≥ 4.5:1 text thường, ≥ 3:1 text lớn và icon
- Keyboard: Tab / Shift+Tab / Enter / Space / Escape phải chạy đúng
- Focus management: đóng dialog → focus trả về phần tử đã mở nó
- KHÔNG ghi đè phím đơn (h, j, k) — xung đột screen reader. Nếu dùng, phải cho tắt/remap
- Touch target ≥ 44×44px trên mobile
- ARIA label cho mọi interactive element không có text rõ ràng
- Focus state phải nhìn thấy được, không `outline: none` trần trụi

## Bước 5 — Responsive

- Mobile-first: viết cho 320px trước, mở rộng lên
- KHÔNG thu nhỏ bảng nhiều cột vào mobile → chuyển thành card hoặc list
- Fluid grid (Flexbox/CSS Grid) + media query
- Breakpoint: 320 / 768 / 1024 / 1440

## 7 nguyên tắc nền tảng

User-centricity · Consistency · Hierarchy · Context · User Control (luôn có undo/escape) · Accessibility · Usability trên thẩm mỹ.

## Anti-patterns — TUYỆT ĐỐI TRÁNH

- Nhồi mọi tính năng lên màn hình đầu
- Icon mơ hồ không có text label
- Nút disabled không giải thích lý do
- Đơn giản hoá giả tạo — cắt tính năng cốt lõi để "trông gọn"
- Biểu đồ 3D
- Pie chart cho > 5 nhóm
- Lạm dụng animation/humor trong công cụ enterprise
- Phím tắt ký tự đơn ghi đè screen reader
- Thiết kế theo giả định, bỏ qua người dùng thật

## Trước khi báo hoàn thành

Chạy checklist của skill `design-review`. Chưa qua checklist = chưa xong.

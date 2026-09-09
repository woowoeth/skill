---
name: web-design
description: Thiết kế website marketing, landing page, trang bán hàng và site giới thiệu doanh nghiệp — bao gồm cấu trúc trang, tối ưu chuyển đổi, hiệu năng và SEO kỹ thuật. Dùng khi thiết kế hoặc dựng website công khai, landing page, trang dịch vụ, blog, portfolio.
---

# Web Design — Website công khai

Khác với app: người dùng đến từ tìm kiếm hoặc quảng cáo, không có động lực sẵn, rời đi sau vài giây nếu không hiểu. Ưu tiên: hiểu ngay → tin tưởng → hành động.

## Bước 1 — Xác định trước khi dựng
- Trang này phục vụ MỘT mục tiêu chuyển đổi nào? (đăng ký / gọi / mua / tải)
- Người đọc đến từ đâu, đang biết gì, lo gì?
- Từ khoá mục tiêu (nếu là trang SEO)

## Bước 2 — Cấu trúc landing page

| Khối | Nhiệm vụ | Nguyên tắc |
|---|---|---|
| Hero | Trong 5 giây phải trả lời: đây là gì, cho ai, tại sao tốt hơn | 1 headline nói lợi ích cụ thể, 1 subline giải thích, 1 CTA chính |
| Social proof | Giảm rủi ro cảm nhận | Đặt ngay dưới hero: logo khách hàng, con số thật, đánh giá có tên thật |
| Vấn đề | Người đọc thấy mình trong đó | Mô tả nỗi đau bằng ngôn ngữ của họ, không phải thuật ngữ ngành |
| Giải pháp | Sản phẩm giải quyết ra sao | 3-5 điểm, mỗi điểm 1 lợi ích + 1 bằng chứng |
| Cách hoạt động | Giảm lo lắng về độ phức tạp | 3 bước, có hình minh hoạ |
| Bảng giá | Quyết định | Nêu rõ có gì, gói khuyến nghị đánh dấu sẵn |
| FAQ | Xử lý phản đối còn lại | Lấy từ câu hỏi thật của khách, không bịa |
| CTA cuối | Chốt | Lặp lại CTA chính, thêm cam kết giảm rủi ro |

## Bước 3 — Quy tắc chuyển đổi

- MỘT hành động chính trên toàn trang. CTA phụ phải nhạt hơn rõ rệt
- CTA ghi kết quả, không ghi thao tác: "Nhận báo giá" thay vì "Gửi"
- Không đặt form dài trước khi tạo được giá trị. Xin ít trường nhất có thể
- Hero không dùng ảnh stock chung chung — dùng ảnh sản phẩm thật hoặc kết quả thật
- Nội dung trên màn hình đầu (above the fold) phải đứng vững một mình
- Không popup trong 15 giây đầu

## Bước 4 — Hiệu năng (ảnh hưởng trực tiếp tới chuyển đổi và SEO)

- LCP < 2.5s, CLS < 0.1, INP < 200ms
- Ảnh: WebP/AVIF, `width`/`height` cố định để tránh nhảy layout, `loading="lazy"` trừ ảnh hero
- Font: tối đa 2 file, `font-display: swap`, preload font hero
- Không nhồi thư viện JS cho hiệu ứng có thể làm bằng CSS
- Trang tĩnh nên tĩnh — không dựng SPA cho trang giới thiệu

## Bước 5 — SEO kỹ thuật

- Mỗi trang: 1 thẻ `<h1>` duy nhất, khớp ý định tìm kiếm
- Title ≤ 60 ký tự, meta description ≤ 155 ký tự, viết cho người đọc
- URL ngắn, có nghĩa, không tham số thừa
- Schema markup phù hợp loại trang (Organization, Product, FAQPage, Article, LocalBusiness)
- Internal link tới trang liên quan bằng anchor mô tả, không "xem thêm"
- Ảnh có `alt` mô tả thật
- Canonical, sitemap.xml, robots.txt đầy đủ
- Hreflang nếu đa ngôn ngữ

## Bước 6 — Accessibility

Áp dụng đầy đủ mục Accessibility của skill `app-design-system`. Riêng website:
- Skip-to-content link
- Cấu trúc heading đúng thứ bậc, không nhảy từ h2 sang h4
- Contrast trên ảnh nền: luôn có lớp phủ hoặc nền chữ

## Anti-patterns

- Headline nói về công ty thay vì lợi ích của khách
- Carousel hero (gần như không ai xem slide 2)
- Auto-play video có tiếng
- Sticky banner chiếm quá 15% màn hình mobile
- Nhồi từ khoá làm câu văn gượng
- CTA "Tìm hiểu thêm" ở mọi chỗ — không dẫn tới hành động nào

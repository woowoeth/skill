---
name: music-prompt
description: Viết prompt sinh nhạc từ đặc tính thực sự nghe được trong video/audio, hoặc từ target music được project style hay user yêu cầu rõ. Dùng khi user gọi /music-prompt, yêu cầu reverse prompt nhạc, viết nhạc giống nguồn, hoặc khi CopyCat cần soundtrack theo source hay style của project.
metadata:
  version: 1.1.2
---

# Music Prompt

Tạo reverse prompt cho **nhạc**, dựa trên audio đã nghe thật. Đây không phải là
khôi phục prompt gốc và không phải là thay thế cho việc nghe file nguồn.

## Luật gốc

> Mọi chi tiết trong prompt nhạc phải truy được về audio đã nghe, hoặc về một
> yêu cầu target được ghi rõ trong project `style.md` hay yêu cầu của user.

Không nghe rõ thì ghi `unclear`. Không dùng tên bài hoặc nghệ sĩ làm lối tắt khi
có thể mô tả trực tiếp đặc tính âm nhạc. Không trộn thoại, voice-over, ambience
hoặc Foley/SFX vào prompt nhạc trừ khi user yêu cầu sound design tổng hợp.

## Hai chế độ

### Standalone

Khi user đưa video/audio và yêu cầu prompt nhạc, nghe file trước, sau đó bàn giao
một prompt thuần bằng **English**, không heading hay Markdown, dài **100–180
words**. Nếu không có nhạc, nói rõ không có nhạc để reverse prompt thay vì bịa
một track.

### CopyCat project

Khi có `projects/<slug>/source.mp4` và `description.md` schema v4:

1. Đọc `style.md` gần nhất đã được CopyCat chọn trước khi phân tích.
2. Nghe `source.mp4` để hiểu cấu trúc nhạc toàn video.
3. Nghe lại `source_clips/shot_NN.mp4` ở chỗ nhạc đổi, có vocal hoặc khó phân
   biệt với ambience.
4. Đối chiếu trường **Nhạc nền** và **Diễn tiến và đồng bộ audio** trong
   `description.md`. Nếu chúng mâu thuẫn với audio thật, sửa mô tả trước.
5. Ghi prompt thuần bằng English, dài 100–180 words vào
   `projects/<slug>/prompts/music.txt`.

Tạo `music.txt` khi source có nhạc, user yêu cầu rõ, hoặc project style quy định
nhạc cho output. Khi style yêu cầu một track thuộc một thời kỳ nhưng source không
có track đó, viết target composition từ đúng thời kỳ/chỉ dẫn đã xác minh; không
tuyên bố các đặc tính target là thứ đã nghe trong source. Nếu cả ba nguồn đều
không yêu cầu nhạc, ghi `không có` vào description và không tạo prompt giả.

## Những gì cần nghe

Chỉ ghi các đặc tính thực sự nghe được hoặc được target style/user yêu cầu rõ:

- Vai trò: background score, diegetic music hay foreground song.
- Thể loại/thời kỳ khi đủ bằng chứng.
- Tempo hoặc khoảng BPM, meter và groove.
- Tonality/key hoặc cảm giác major/minor/modal khi xác định được.
- Nhạc cụ, vocal, texture và timbre.
- Pattern trống, bass, hòa âm, density và energy.
- Cấu trúc theo thời gian: intro, build, peak, breakdown, outro hoặc loop.
- Production: không gian, reverb, distortion, stereo width, live/studio.
- Duration, cách mở/kết và yêu cầu loop nếu workflow cần.

Tách phần nhạc khỏi tiếng nói và SFX. Với vocal, mô tả số giọng, register,
delivery và ngôn ngữ chỉ khi nghe xác định được; không tự chép lời không rõ.

## Dạng prompt

Viết một đoạn độc lập, phù hợp để đưa vào công cụ sinh nhạc:

```text
<genre/era and role>, <tempo/meter>, <instrumentation and timbre>,
<rhythm/bass/harmony>, <timeline and dynamics>, <vocal if present>,
<production and space>, <duration and ending/loop behavior>
```

Khi user nêu engine đích, chỉ điều chỉnh cú pháp cho engine đó; không thêm chi
tiết âm nhạc mới. Trong CopyCat, `music.txt` là mô tả nhạc xuyên toàn video.
Prompt video từng shot chỉ lấy cue/timing liên quan, không sao chép toàn bộ
prompt nhạc vào mọi shot.

Skill này chỉ tạo prompt. Sinh file nhạc và mix track riêng vào video là công
việc khác, chỉ làm khi user yêu cầu.

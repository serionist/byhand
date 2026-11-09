"""Plain Vietnamese work text, invented, against the real catalogue. A strong or usual sign counts alone, so one that
fires on any of these accuses a person of writing like a machine. Office Vietnamese runs on the set forms of Decree
30/2020 (Kính gửi:, Căn cứ…, Trân trọng./, Nơi nhận:), on the Sino-Vietnamese verbs and connectors slop-gate lists
(do đó, đối với, thực hiện, tiến hành, trong trường hợp, tuy nhiên), and on what vietnamese-humanizer flags and keeps
in a letter, an official text or customer care: the passive with được… bởi, nominal openers (Việc…), "trong bối cảnh"
naming a change, "đóng vai trò quan trọng trong việc", "không chỉ… mà còn", "Tóm lại", "Hy vọng những thông tin trên
sẽ hữu ích". Reports quote what a speaker stressed (nhấn mạnh), and an abstract opens on "Bài viết này". People mix
pronouns (anh, chị, em, mình, bạn), write abbreviations (UBND, TP.HCM, ĐKKD) and, in chat, drop the diacritics. They
are a person's, never a sign. A weak sign may fire, but plain work text must not reach a cluster.

Vietnamese typography is how people write too: “ ” and straight quotes, the en dash in a range and to open a line of
dialogue, a dot between thousands (1.250.000 đồng) and dates in day/month order."""

import unicodedata

import pytest

from byhand import signs

# The dashes are written as escapes, as ruff refuses an en dash in source; the first test holds that they are real.
EN, EM = "\N{EN DASH}", "\N{EM DASH}"
# What a Vietnamese draft loads: the `any` signs and Vietnamese's, never another language's.
VIETNAMESE = ("any", "vi")

MAIL = [
    "Kính gửi: Ban Giám đốc Công ty TNHH Minh Phát\n\n"
    "Căn cứ Hợp đồng số 15/2026/HĐ-MP ngày 02/3/2026, Công ty Cổ phần Bao bì An Khang xin thông báo lô hàng thứ hai "
    "sẽ được giao vào ngày 20/11/2026 tại kho Bình Dương.\n\n"
    "Trân trọng./.\n\n"
    "Nơi nhận:\n- Như trên;\n- Lưu: VT, KD.",
    "Chào anh Tuấn,\n\n"
    "Em gửi anh báo cáo doanh thu tháng 10 trong file đính kèm. Số liệu chi nhánh Đà Nẵng em đã đối chiếu với kế toán "
    "hôm qua.\n\nEm cảm ơn anh ạ.\nThu Hà",
    "Kính gửi Quý khách,\n\n"
    "Đơn hàng số 88213 của Quý khách đã được bàn giao cho đơn vị vận chuyển. Hy vọng những thông tin trên sẽ hữu ích. "
    "Nếu cần hỗ trợ thêm, Quý khách vui lòng gọi hotline 1900 1234.\n\n"
    "Trân trọng,\nBộ phận Chăm sóc khách hàng",
    "Gửi các anh chị phòng Kinh doanh,\n\n"
    "Đối với các đơn đặt trước ngày 15/11, công ty vẫn giao như cũ. Tuy nhiên, trong trường hợp khách đổi địa chỉ, "
    "các anh chị cần báo lại kho trước 16h. Do đó, mong mọi người cập nhật danh sách trên hệ thống trong hôm nay.\n\n"
    "Thanks cả nhà,\nPhương",
    "Kính gửi các phòng ban,\n\n"
    "Phòng IT sẽ tiến hành bảo trì máy chủ từ 22h00 thứ Bảy đến 6h00 Chủ nhật. Đề nghị các phòng thực hiện sao lưu dữ "
    "liệu trước 20h00 thứ Bảy.\n\nTrân trọng,\nPhòng Công nghệ thông tin",
    "Chào chị Lan,\n\n"
    "Trong cuộc họp sáng nay, anh Khoa nhấn mạnh hạn nộp hồ sơ dự thầu là 20/11. Em gửi chị danh sách giấy tờ còn "
    "thiếu nha.\n\nEm Vy",
    "Kính gửi anh Bình,\n\n"
    "Trong bối cảnh giá hạt nhựa tăng 12% từ tháng 9, công ty buộc phải điều chỉnh đơn giá túi PE từ ngày 01/12. "
    "Bảng giá mới em gửi kèm theo đây.\n\nTrân trọng,\nNguyễn Thị Mai",
    "Trân trọng kính mời anh/chị tham dự Lễ tổng kết năm 2026 vào lúc 17h30 thứ Sáu, ngày 26/12/2026, tại Khách sạn "
    "Rex, 141 Nguyễn Huệ, Quận 1, TP.HCM.\n\nBan Tổ chức",
    "Chào bạn Hùng,\n\n"
    "Mình là Linh bên nhà sách Cánh Diều. Bạn gửi giúp mình số lượng sách cần đặt cho hội chợ trước thứ Tư nhé.\n\n"
    "Cảm ơn bạn,\nLinh",
    "Thưa thầy,\n\n"
    "Em xin phép nộp muộn bài tiểu luận một ngày vì em bị sốt. Em gửi kèm giấy khám bệnh ạ.\n\n"
    "Em cảm ơn thầy.\nSinh viên Lê Văn Nam, lớp K66-QTKD",
]
REPLIES = [
    "Dưới đây là phiên bản cuối của hợp đồng, anh xem giúp em:",
    "Dưới đây là phiên bản email mới của chị:",
    "Dưới đây là phiên bản cập nhật theo góp ý của bạn:",
    "Dưới đây là phiên bản tiếng Anh của văn bản, gửi bạn:",
    "Dưới đây là phiên bản 2.1 của phần mềm quản lý kho:",
    "Dưới đây là phiên bản thư mời gửi các bạn trong nhóm:",
    # a version made from the reader's mail, or sent to it, is not their text reworked (#62's review, F1)
    "Dưới đây là phiên bản đã sửa theo email của bạn:",
    "Dưới đây là phiên bản cập nhật theo tin nhắn của bạn:",
    "Dưới đây là phiên bản cập nhật theo nội dung email của bạn:",
    "Dưới đây là phiên bản hợp đồng mình đã gửi vào email của bạn:",
    "Dưới đây là phiên bản PDF của báo giá, đã gửi qua email của bạn:",
    "Dưới đây là phiên bản slide mình làm dựa trên email của bạn:",
    "Mình gửi lại bạn bản email hôm qua nhé:",
    "Nếu anh muốn trao đổi trực tiếp, em có thể gọi lại trong giờ hành chính.",
    "Nếu bạn cần bản in, mình để ở quầy lễ tân.",
    "Là trợ lý giám đốc, em không thể tự duyệt khoản chi này.",
    "Theo cập nhật mới nhất của hệ thống, tồn kho còn 12 thùng.",
    "Tính đến lần cập nhật gần nhất hôm thứ Ba, lô hàng vẫn ở cảng Hải Phòng.",
]
CHAT = [
    "ok a, e gui file roi nhe",
    "dc r, mai e qua lay",
    "ko sao đâu, để mai tính",
    "Anh ơi, họp lùi sang 3h chiều nha 🙏",
    "Tks chị nhiều ạ",
    "Mình đến muộn 10p nhé, kẹt xe quá",
    "Câu hỏi hay đó, để em hỏi lại chị Mai",
    "Chị nhấn mạnh lại giúp em hạn nộp được không ạ?",
    "Nhóm mình chốt phương án B nha mọi người",
    "Dạ vâng ạ",
    "uk, để t check lại",
    "Hôm nay ai trực kho vậy?",
    "Chúc mừng sinh nhật anh Đức 🎂 chúc anh nhiều sức khỏe!",
]
NOTES = [
    "BIÊN BẢN HỌP\n"
    "Thời gian: 9h00, ngày 05/11/2026\n"
    "Địa điểm: Phòng họp tầng 3\n"
    "Thành phần: anh Khoa, chị Hà, anh Tú\n"
    "Nội dung:\n"
    "- Giám đốc nhấn mạnh dự án phải xong trước 30/11.\n"
    "- Phòng Kế toán thực hiện đối chiếu công nợ.\n"
    "- Cuộc họp sau: 9h00 ngày 12/11.",
    "Việc cần làm:\n- Gọi luật sư\n- Gửi hợp đồng cho anh Sơn [chờ xác nhận]\n- Kiểm tra ngày giao hàng",
    "**Lưu ý**: từ thứ Hai, nhân viên quẹt thẻ khi vào cổng.",
    "Giờ làm việc: thứ Hai " + EN + " thứ Sáu, 8h00 " + EN + " 17h00; thứ Bảy làm buổi sáng.",
    "1. Chốt sổ tháng 10\n2. Thanh toán nhà cung cấp\n3. Gia hạn hợp đồng thuê kho",
]
REPORTS = [
    "Tóm tắt\n\n"
    "Bài viết này phân tích tác động của làm việc từ xa đến năng suất của 312 nhân viên ngân hàng tại TP.HCM. Kết quả "
    "nhấn mạnh vai trò của người quản lý trực tiếp trong việc giữ tiến độ.",
    "Đặt vấn đề\n\n"
    "Trong bài viết này, chúng tôi trình bày kết quả khảo sát 1.200 hộ trồng cà phê ở Đắk Lắk năm 2025. Không chỉ "
    "năng suất mà còn giá bán đều giảm so với năm 2024.",
    "Báo cáo quý III\n\n"
    "**Kết quả chính**\n\n"
    "Doanh thu đạt 48,6 tỷ đồng, tăng 9% so với cùng kỳ. Hội đồng quản trị nhấn mạnh chi phí logistics cần giảm. "
    "Trong bối cảnh chuyển đổi số ngày càng phát triển, phòng IT đóng vai trò quan trọng trong việc triển khai phần "
    "mềm kho mới từ tháng 8.",
    "Bài 5. Phân số\n\nTrong phần này, chúng ta sẽ ôn lại cách chia hai phân số.",
    "QUYẾT ĐỊNH\nVề việc bổ nhiệm Trưởng phòng Kinh doanh\n\n"
    "Căn cứ Luật Doanh nghiệp năm 2020;\n"
    "Căn cứ Điều lệ Công ty Cổ phần Thép Hòa An;\n"
    "Xét đề nghị của Trưởng phòng Hành chính - Nhân sự,\n\n"
    "Điều 1. Bổ nhiệm ông Trần Quốc Việt giữ chức Trưởng phòng Kinh doanh kể từ ngày 01/12/2026.",
    "Kết luận\n\nTóm lại, dự án hoàn thành 92% khối lượng trong quý III; phần còn lại chuyển sang tháng 1/2027.",
    "Câu hỏi thường gặp\n\n"
    "Phí đổi hàng là bao nhiêu? Miễn phí trong 7 ngày đầu. Hy vọng những thông tin trên sẽ hữu ích cho Quý khách.",
    "Hướng dẫn sử dụng\n\nKhông nhấn mạnh tay vào màn hình cảm ứng. Lau màn hình bằng khăn khô.",
    "Báo cáo được lập bởi Phòng Kế hoạch và được Ban Giám đốc thông qua ngày 06/11/2026.",
    "Việc kiểm kê kho được tiến hành vào cuối tháng. Việc đối chiếu số liệu do Phòng Kế toán phụ trách. Việc báo cáo "
    "kết quả gửi Ban Giám đốc trước ngày 05 tháng sau.",
    "Thông cáo báo chí\n\n"
    "Phát biểu tại hội nghị, Bộ trưởng nhấn mạnh việc giải ngân vốn đầu tư công. Bộ trưởng cũng nhấn mạnh rằng các "
    "địa phương phải báo cáo tiến độ hằng tháng.",
    "Đơn vị tính: triệu đồng\n\n"
    "Theo quy định hiện hành, đối với hợp đồng trên 50 triệu đồng, đơn vị phải thực hiện đấu thầu. Do đó, gói thầu "
    "sửa mái nhà kho được tách làm hai.",
]
POSTS = [
    "Sau 6 năm gắn bó với Công ty Logistics Sao Việt, hôm nay mình chính thức nghỉ việc. Cảm ơn anh Long và chị Thảo "
    "đã chỉ bảo mình từ ngày đầu. Từ 02/12 mình bắt đầu ở Tân Cảng. #logistics",
    "Khai trương chi nhánh mới tại 25 Nguyễn Thị Thập, Quận 7 🎉 Giảm 20% mọi đồ uống từ 7h đến 11h sáng thứ Bảy!",
    "Trong bài viết này, mình sẽ kể lại chuyến đi Đà Lạt 3 ngày với 2 triệu đồng.",
    "Hôm qua đội tình nguyện trồng được 300 cây sao đen ở Củ Chi. Cảm ơn 40 bạn đã đến 🌱",
]
TYPOGRAPHY = [
    "Giá: 1.250.000 đồng (đã gồm VAT 10%). Giao trong 3" + EN + "5 ngày làm việc.",
    EN + " Mai anh có lên văn phòng không?\n" + EN + " Có, tầm 9 giờ.",
    'Anh Minh nói: “Tuần sau ký hợp đồng.” Còn chị Hạnh thì bảo "để xem đã".',
    "UBND TP.HCM, Sở GD&ĐT; ĐKKD số 0312345678 do Sở KH&ĐT cấp ngày 09/11/2016.",
    "Hội trường A " + EM + " sức chứa 200 chỗ " + EM + " mở cửa từ 7h30.",
]

OFFICE = MAIL + REPLIES + CHAT + NOTES + REPORTS + POSTS + TYPOGRAPHY

KINDS = [
    *((text, "email") for text in MAIL + REPLIES),
    *((text, "message") for text in CHAT),
    *((text, "document") for text in NOTES + REPORTS + TYPOGRAPHY),
    *((text, "post") for text in POSTS),
]


def test_the_lines_are_precomposed_vietnamese():
    # The catalogue is in NFC, as a Vietnamese keyboard types by default; a line in combining form would pass every
    # test above by matching nothing.
    assert all(unicodedata.is_normalized("NFC", text) for text in OFFICE)
    assert unicodedata.name(EN) == "EN DASH"
    assert unicodedata.name(EM) == "EM DASH"
    assert sum(EN in text for text in OFFICE) >= 3
    for letter in "ăâđêôơư":
        assert any(letter in text.lower() for text in OFFICE), letter
    assert len(OFFICE) >= 50


@pytest.mark.parametrize(("text", "kind"), KINDS)
def test_no_sign_that_counts_alone_fires_on_plain_vietnamese_work_text(counted_alone, reads, text, kind):
    fired = [sign.id for sign in counted_alone if reads(sign, kind) and sign.pattern and sign.pattern.search(text)]
    assert fired == []


def test_no_vietnamese_check_counts_alone(counted_alone):
    # Until a native speaker reads them, every Vietnamese sign with a pattern is weak (#49): a Vietnamese sign with a
    # pattern that counts alone needs its lines in MACHINE below, a line per branch of its check.
    assert [sign.id for sign in counted_alone if sign.language == "vi"] == []


def test_every_vietnamese_sign_is_weak_until_a_native_review(catalogue):
    # stricter than the plan, which lets a usual or strong sign with no pattern in: none of these sources settles one
    assert [sign.id for sign in catalogue.signs.values() if sign.language == "vi" and sign.strength != "weak"] == []


# What each sign that counts alone exists to catch, inside Vietnamese text: a line per Vietnamese branch of its check,
# and one for each artefact, which is the same string in every language, so silence above can't come from a sign that
# finds nothing. Branches that read other languages' words have their lines in the other office tests.
MACHINE = [
    ("any-assistant-preamble", "Dưới đây là phiên bản đã chỉnh sửa của email của bạn:"),
    ("any-assistant-preamble", "Dưới đây là phiên bản trang trọng hơn của tin nhắn của bạn:"),
    ("any-assistant-preamble", "Dưới đây là phiên bản ngắn gọn của văn bản của bạn:"),
    ("any-emoji-markers", "- 🚀 Chương trình đào tạo mới"),
    ("any-emoji-markers", "## 📊 Số liệu tháng 10"),
    ("any-unfilled-placeholder", "Đăng ký tại: insert_link_here"),
    ("any-chatgpt-citation-markup", "Doanh số tăng 9%. :contentReference[oaicite:0]{index=0}"),
    ("any-chatgpt-citation-markup", "Doanh số tăng 9%. turn0search4"),
    ("any-chatbot-url-tag", "Nguồn: https://example.vn/bao-cao?utm_source=chatgpt.com"),
    ("any-gemini-citation-markup", "Nhà máy mở cửa năm 1998 [cite: 3]."),
    ("any-grok-citation-markup", "Nhà máy mở cửa năm 1998. grok_card"),
    ("any-deepseek-citation-markup", "Nhà máy mở cửa năm 1998【4†source】."),
    ("any-chat-tool-markup", "Theo tệp đính kèm[attached_file:1], biên lợi nhuận giảm."),
]


@pytest.mark.parametrize(("sign", "text"), MACHINE)
def test_the_signs_still_find_what_they_are_for_in_vietnamese(counted_alone, sign, text):
    pattern = {found.id: found.pattern for found in counted_alone}[sign]
    assert pattern is not None
    assert pattern.search(text), sign


@pytest.mark.parametrize(("text", "kind"), KINDS)
def test_plain_vietnamese_work_text_makes_no_weak_cluster(weak_hits, text, kind):
    for paragraph in text.split("\n\n"):
        assert weak_hits(paragraph, kind, VIETNAMESE) < signs.WEAK_CLUSTER, paragraph


def test_the_weak_counting_counts_a_cluster(weak_hits):
    # so the test above can fail: three different weak habits in one paragraph of a document
    text = "Trong bài viết này, chúng ta sẽ xem vì sao báo cáo nhấn mạnh **ba con số**."
    assert weak_hits(text, "document", VIETNAMESE) == signs.WEAK_CLUSTER


def test_one_habit_repeated_counts_once(weak_hits):
    text = "Báo cáo nhấn mạnh doanh thu, nhấn mạnh chi phí và nhấn mạnh tồn kho."
    assert weak_hits(text, "document", VIETNAMESE) == 1


def test_the_vietnamese_checks_read_posts_and_documents(catalogue):
    # the set forms of mail and chat (Kính gửi, Trân trọng, dạ vâng ạ) and what people stress in them would add up
    # there: no Vietnamese sign that reads mail or chat has a pattern.
    reading_mail = [
        sign.id
        for sign in catalogue.signs.values()
        if sign.language == "vi" and sign.pattern and {"any", "email", "message"} & set(sign.kinds)
    ]
    assert reading_mail == []


# A space stands between syllables, not words, so a term's edge is a syllable's: the forms a weak check must still
# find, beyond its own `flags`, and the plain forms around it it must leave alone.
FORMS = [
    ("vi-article-opener", "Ở phần này, chúng ta cùng xem bảng giá mới."),
    ("vi-article-opener", "Trong bài viết này chúng ta sẽ bàn về lương tháng 13."),
    ("vi-article-opener", "TRONG BÀI VIẾT NÀY, CHÚNG TA SẼ ĐI QUA BA BƯỚC."),
    ("vi-emphasise", "Sự nhấn mạnh này là cần thiết."),
    ("vi-emphasise", "Nhấn mạnh rằng hạn nộp không đổi."),
    ("vi-emphasise", "Báo cáo nhấn mạnh, một lần nữa, chi phí vận chuyển."),
    ("any-raw-markdown", "Cảm ơn anh. **Hai điểm** cần sửa."),
]

LEFT_ALONE = [
    ("vi-article-opener", "Trong bài viết này, chúng tôi trình bày kết quả khảo sát."),
    ("vi-article-opener", "Trong bài viết này, mình sẽ kể chuyện đi Đà Lạt."),
    ("vi-article-opener", "Bài viết này phân tích chi phí vận chuyển."),
    ("vi-article-opener", "Trong bài này, chúng ta sẽ học phép cộng."),
    ("vi-article-opener", "Trong phần này chúng tôi nêu ba kiến nghị."),
    ("vi-emphasise", "Anh ấy nhấn nút rồi đi ra."),
    ("vi-emphasise", "Chị nhấn chuông mạnh quá."),
    ("vi-emphasise", "Nhấn giữ nút nguồn trong 5 giây."),
    ("vi-emphasise", "Lực đẩy mạnh hơn sau khi thay pin."),
    # people close with it: the closing summary has no Vietnamese form (#58's review, F1)
    ("any-closing-summary", "Tóm lại, dự án hoàn thành đúng hạn."),
    ("any-closing-summary", "Kết luận, công ty giữ nguyên giá bán."),
]


@pytest.mark.parametrize(("sign", "text"), FORMS)
def test_a_weak_vietnamese_check_finds_its_forms(catalogue, sign, text):
    pattern = catalogue.signs[sign].pattern
    assert pattern is not None
    assert pattern.search(text), sign


@pytest.mark.parametrize(("sign", "text"), LEFT_ALONE)
def test_a_weak_vietnamese_check_leaves_plain_forms_alone(catalogue, sign, text):
    pattern = catalogue.signs[sign].pattern
    assert pattern is not None
    assert not pattern.search(text), sign

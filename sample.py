from swear_detector import detect_swearwords_from_text

# text = "سلام کارتون بد نبود قبلا هم خرید داشتم"
text = "این یک پیام آزمایشی است. س گ ص ف ته."
# text = "سلام محصولتون اصلا خوب نبود"
# text = "نمی خرم اصلا"
# text = "ادمین تون خیلی سسسس گگگگگ صصص*فففته"
# text = "خیلی من گ&ایییییییید*@م این کیفیت را"
# text = "خیلی من گ&ایییــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــییییید*@م این کیفیت را"

results , warning = detect_swearwords_from_text(text, threshold1=0.5 , threshold2=0.65)

if warning != "":
    # سخت گیری در تایید نظر
    print(f"اخطار:{warning}")



if len(results) >= 1 :
    for result in results:
        in_blacklist_database = result['in-blacklist']
        in_givenText = result["in-givenText"]
        sim_value = result["sim-value"]

        print(f"عبارت داده شده در متن: \"{in_givenText}\" ، با عبارت در دیتابیس: \"{in_blacklist_database}\" ، \"%{sim_value}\" شباهت داشت")

else:
    print("هیچ کلمه ناپسندی در متن یافت نشد")
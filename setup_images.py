from PIL import Image
import urllib.request

urllib.request.urlretrieve("https://raw.githubusercontent.com/SR-SHASHI-X/echat-app/main/logo.jpg", "logo.jpg")
img = Image.open("logo.jpg").convert("RGBA")
for folder, size in [("mdpi",48),("hdpi",72),("xhdpi",96),("xxhdpi",144),("xxxhdpi",192)]:
    r = img.resize((size,size), Image.LANCZOS)
    r.save("app/src/main/res/mipmap-" + folder + "/ic_launcher.png")
    r.save("app/src/main/res/mipmap-" + folder + "/ic_launcher_round.png")

urllib.request.urlretrieve("https://raw.githubusercontent.com/SR-SHASHI-X/echat-app/main/splash.png", "splash_dark.png")
dark = Image.open("splash_dark.png").convert("RGB")
dark.save("app/src/main/res/drawable-night/splash.jpg", "JPEG", quality=95)

urllib.request.urlretrieve("https://raw.githubusercontent.com/SR-SHASHI-X/echat-app/main/splash_light.png", "splash_light.png")
light = Image.open("splash_light.png").convert("RGB")
light.save("app/src/main/res/drawable/splash.jpg", "JPEG", quality=95)

print("All images done!")

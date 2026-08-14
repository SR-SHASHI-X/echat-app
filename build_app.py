import os, urllib.request
from PIL import Image

# ── Folders ──────────────────────────────────────────────
dirs = [
    "app/src/main/java/com/echat/app",
    "app/src/main/res/layout",
    "app/src/main/res/values",
    "app/src/main/res/values-night",
    "app/src/main/res/drawable",
    "app/src/main/res/drawable-night",
    "app/src/main/assets",
    "app/src/main/res/mipmap-mdpi",
    "app/src/main/res/mipmap-hdpi",
    "app/src/main/res/mipmap-xhdpi",
    "app/src/main/res/mipmap-xxhdpi",
    "app/src/main/res/mipmap-xxxhdpi",
    "gradle/wrapper",
]
for d in dirs:
    os.makedirs(d, exist_ok=True)

BASE = "https://raw.githubusercontent.com/SR-SHASHI-X/echat-app/main/"

# ── Images ────────────────────────────────────────────────
urllib.request.urlretrieve(BASE+"logo.jpg", "logo.jpg")
img = Image.open("logo.jpg").convert("RGBA")
for folder, size in [("mdpi",48),("hdpi",72),("xhdpi",96),("xxhdpi",144),("xxxhdpi",192)]:
    r = img.resize((size,size), Image.LANCZOS)
    r.save(f"app/src/main/res/mipmap-{folder}/ic_launcher.png")
    r.save(f"app/src/main/res/mipmap-{folder}/ic_launcher_round.png")

urllib.request.urlretrieve(BASE+"splash.png", "splash_dark.png")
Image.open("splash_dark.png").convert("RGB").save("app/src/main/res/drawable-night/splash.jpg","JPEG",quality=95)

urllib.request.urlretrieve(BASE+"splash_light.png", "splash_light.png")
Image.open("splash_light.png").convert("RGB").save("app/src/main/res/drawable/splash.jpg","JPEG",quality=95)
print("Images done!")

# ── Helper ────────────────────────────────────────────────
def w(path, content):
    with open(path, "w") as f:
        f.write(content)

# ── Gradle files ─────────────────────────────────────────
w("settings.gradle", """pluginManagement {
    repositories { google(); mavenCentral(); gradlePluginPortal() }
}
dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories { google(); mavenCentral() }
}
rootProject.name = "EchatApp"
include ':app'
""")

w("build.gradle", """plugins {
    id 'com.android.application' version '8.2.0' apply false
}
""")

w("gradle.properties", """org.gradle.jvmargs=-Xmx2048m
android.useAndroidX=true
""")

w("app/build.gradle", """plugins { id 'com.android.application' }
android {
    namespace 'com.echat.app'
    compileSdk 34
    defaultConfig {
        applicationId "com.echat.app"
        minSdk 21
        targetSdk 34
        versionCode 9
        versionName "2.0"
    }
    buildTypes {
        release { minifyEnabled false; signingConfig signingConfigs.debug }
    }
    compileOptions {
        sourceCompatibility JavaVersion.VERSION_1_8
        targetCompatibility JavaVersion.VERSION_1_8
    }
}
dependencies { implementation 'androidx.appcompat:appcompat:1.6.1' }
""")

# ── Manifest ─────────────────────────────────────────────
w("app/src/main/AndroidManifest.xml", """<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">
    <uses-permission android:name="android.permission.INTERNET"/>
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE"/>
    <uses-permission android:name="android.permission.CAMERA"/>
    <uses-permission android:name="android.permission.RECORD_AUDIO"/>
    <uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE"/>
    <uses-permission android:name="android.permission.READ_MEDIA_IMAGES"/>
    <uses-permission android:name="android.permission.READ_MEDIA_VIDEO"/>
    <uses-permission android:name="android.permission.VIBRATE"/>
    <uses-permission android:name="android.permission.WAKE_LOCK"/>
    <application
        android:label="eChat"
        android:icon="@mipmap/ic_launcher"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:theme="@style/Theme.AppCompat.DayNight.NoActionBar"
        android:usesCleartextTraffic="true"
        android:hardwareAccelerated="true"
        android:largeHeap="true">
        <activity android:name=".SplashActivity" android:exported="true"
            android:screenOrientation="portrait"
            android:theme="@style/SplashTheme">
            <intent-filter>
                <action android:name="android.intent.action.MAIN"/>
                <category android:name="android.intent.category.LAUNCHER"/>
            </intent-filter>
        </activity>
        <activity android:name=".MainActivity" android:exported="false"
            android:screenOrientation="portrait"
            android:configChanges="orientation|screenSize|keyboardHidden|keyboard|navigation"
            android:windowSoftInputMode="adjustResize"/>
    </application>
</manifest>
""")

# ── Styles ───────────────────────────────────────────────
STYLE = """<?xml version="1.0" encoding="utf-8"?>
<resources>
    <style name="SplashTheme" parent="Theme.AppCompat.DayNight.NoActionBar">
        <item name="android:windowBackground">@drawable/splash</item>
    </style>
</resources>
"""
w("app/src/main/res/values/styles.xml", STYLE)
w("app/src/main/res/values-night/styles.xml", STYLE)

# ── Layouts ──────────────────────────────────────────────
w("app/src/main/res/layout/activity_splash.xml", """<?xml version="1.0" encoding="utf-8"?>
<ImageView xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:src="@drawable/splash"
    android:scaleType="fitXY"/>
""")

# ── SplashActivity ───────────────────────────────────────
w("app/src/main/java/com/echat/app/SplashActivity.java", """package com.echat.app;
import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.os.Handler;
public class SplashActivity extends Activity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_splash);
        new Handler().postDelayed(() -> {
            startActivity(new Intent(this, MainActivity.class));
            finish();
        }, 2500);
    }
}
""")

# ── MainActivity ─────────────────────────────────────────
w("app/src/main/java/com/echat/app/MainActivity.java", """package com.echat.app;
import android.annotation.SuppressLint;
import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.Color;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.view.Gravity;
import android.view.View;
import android.view.ViewGroup;
import android.view.WindowManager;
import android.webkit.CookieManager;
import android.webkit.GeolocationPermissions;
import android.webkit.JavascriptInterface;
import android.webkit.PermissionRequest;
import android.webkit.ValueCallback;
import android.webkit.WebChromeClient;
import android.webkit.WebResourceRequest;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.RelativeLayout;
import android.widget.TextView;
import android.widget.Toast;
public class MainActivity extends Activity {
    WebView webView;
    ImageView loadingView;
    LinearLayout offlineBanner;
    ValueCallback<Uri[]> filePathCallback;
    static final int FILE_CHOOSER = 100;
    static final String HOME_URL = "https://echat.whf.bz/app.html";
    long backPressedTime = 0;
    Toast backToast;
    String currentScreen = "home";
    @SuppressLint({"SetJavaScriptEnabled","AddJavascriptInterface"})
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.LOLLIPOP) {
            getWindow().setStatusBarColor(Color.TRANSPARENT);
            getWindow().addFlags(WindowManager.LayoutParams.FLAG_DRAWS_SYSTEM_BAR_BACKGROUNDS);
        }
        RelativeLayout layout = new RelativeLayout(this);
        layout.setBackgroundColor(Color.WHITE);
        webView = new WebView(this);
        webView.setVisibility(View.INVISIBLE);
        RelativeLayout.LayoutParams fullParams = new RelativeLayout.LayoutParams(
            RelativeLayout.LayoutParams.MATCH_PARENT, RelativeLayout.LayoutParams.MATCH_PARENT);
        layout.addView(webView, fullParams);
        loadingView = new ImageView(this);
        loadingView.setImageResource(R.drawable.splash);
        loadingView.setScaleType(ImageView.ScaleType.FIT_XY);
        layout.addView(loadingView, fullParams);
        offlineBanner = new LinearLayout(this);
        offlineBanner.setOrientation(LinearLayout.HORIZONTAL);
        offlineBanner.setGravity(Gravity.CENTER);
        offlineBanner.setBackgroundColor(0xFFD32F2F);
        offlineBanner.setPadding(0, dp(8), 0, dp(8));
        offlineBanner.setVisibility(View.GONE);
        TextView offlineText = new TextView(this);
        offlineText.setText("No internet connection");
        offlineText.setTextColor(0xFFFFFFFF);
        offlineText.setTextSize(13);
        offlineBanner.addView(offlineText);
        RelativeLayout.LayoutParams bannerParams = new RelativeLayout.LayoutParams(
            RelativeLayout.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT);
        bannerParams.addRule(RelativeLayout.ALIGN_PARENT_TOP);
        layout.addView(offlineBanner, bannerParams);
        setContentView(layout);
        setupWebView();
        webView.addJavascriptInterface(new Object() {
            @JavascriptInterface
            public void setScreen(String screen) { currentScreen = screen; }
            @JavascriptInterface
            public void getFcmToken() {
                runOnUiThread(() ->
                    webView.evaluateJavascript("window.onFcmToken&&window.onFcmToken(null);", null));
            }
        }, "AndroidBridge");
        webView.setWebViewClient(new WebViewClient() {
            @Override
            public void onPageStarted(WebView view, String url, Bitmap favicon) {
                loadingView.setVisibility(View.VISIBLE);
                webView.setVisibility(View.INVISIBLE);
                currentScreen = "home";
            }
            @Override
            public void onPageFinished(WebView view, String url) {
                loadingView.setVisibility(View.GONE);
                webView.setVisibility(View.VISIBLE);
                CookieManager.getInstance().flush();
                updateOfflineBanner();
                view.evaluateJavascript(
                    "(function(){if(window.__echatHooked)return;window.__echatHooked=true;" +
                    "var _show=window.showScreen;if(_show)window.showScreen=function(n){" +
                    "try{AndroidBridge.setScreen(n);}catch(e){}return _show.apply(this,arguments);};" +
                    "var _close=window.closeChat;if(_close)window.closeChat=function(){" +
                    "try{AndroidBridge.setScreen('home');}catch(e){}return _close.apply(this,arguments);};" +
                    "})();", null);
            }
            @Override
            public void onReceivedError(WebView view, WebResourceRequest request, android.webkit.WebResourceError error) {
                if (request.isForMainFrame()) {
                    loadingView.setVisibility(View.GONE);
                    webView.setVisibility(View.VISIBLE);
                    offlineBanner.setVisibility(View.VISIBLE);
                }
            }
            @Override
            public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest request) {
                String url = request.getUrl().toString();
                if (url.contains("echat.whf.bz")||url.contains("echat.unaux.com")) return false;
                try { startActivity(new Intent(Intent.ACTION_VIEW, Uri.parse(url))); } catch (Exception e) {}
                return true;
            }
        });
        webView.setWebChromeClient(new WebChromeClient() {
            @Override
            public void onPermissionRequest(PermissionRequest request) { request.grant(request.getResources()); }
            @Override
            public void onGeolocationPermissionsShowPrompt(String origin, GeolocationPermissions.Callback callback) {
                callback.invoke(origin, true, false);
            }
            @Override
            public boolean onShowFileChooser(WebView view, ValueCallback<Uri[]> callback, FileChooserParams params) {
                if (filePathCallback != null) filePathCallback.onReceiveValue(null);
                filePathCallback = callback;
                Intent intent = new Intent(Intent.ACTION_GET_CONTENT);
                intent.addCategory(Intent.CATEGORY_OPENABLE);
                intent.setType("*/*");
                intent.putExtra(Intent.EXTRA_MIME_TYPES, new String[]{"image/*","video/*"});
                startActivityForResult(Intent.createChooser(intent, "Choose File"), FILE_CHOOSER);
                return true;
            }
            @Override
            public void onProgressChanged(WebView view, int newProgress) {
                if (newProgress > 60) {
                    loadingView.setVisibility(View.GONE);
                    webView.setVisibility(View.VISIBLE);
                }
            }
        });
        webView.loadUrl(HOME_URL);
    }
    @SuppressLint("SetJavaScriptEnabled")
    private void setupWebView() {
        WebSettings s = webView.getSettings();
        s.setJavaScriptEnabled(true);
        s.setDomStorageEnabled(true);
        s.setDatabaseEnabled(true);
        s.setCacheMode(WebSettings.LOAD_CACHE_ELSE_NETWORK);
        s.setMediaPlaybackRequiresUserGesture(false);
        s.setMixedContentMode(WebSettings.MIXED_CONTENT_ALWAYS_ALLOW);
        s.setLoadsImagesAutomatically(true);
        s.setUseWideViewPort(true);
        s.setLoadWithOverviewMode(true);
        s.setSupportZoom(true);
        s.setBuiltInZoomControls(true);
        s.setDisplayZoomControls(false);
        s.setAllowFileAccess(true);
        s.setAllowContentAccess(true);
        s.setDefaultTextEncodingName("UTF-8");
        s.setGeolocationEnabled(true);
        s.setJavaScriptCanOpenWindowsAutomatically(true);
        s.setUserAgentString(s.getUserAgentString()+" EchatApp/2.0");
        CookieManager cm = CookieManager.getInstance();
        cm.setAcceptCookie(true);
        cm.setAcceptThirdPartyCookies(webView, true);
        webView.setLayerType(View.LAYER_TYPE_HARDWARE, null);
        webView.setOverScrollMode(View.OVER_SCROLL_NEVER);
        webView.setScrollBarStyle(View.SCROLLBARS_INSIDE_OVERLAY);
        webView.setHorizontalScrollBarEnabled(false);
        webView.setVerticalScrollBarEnabled(false);
    }
    private int dp(int v) { return (int)(v*getResources().getDisplayMetrics().density); }
    private boolean isNetworkAvailable() {
        ConnectivityManager cm=(ConnectivityManager)getSystemService(Context.CONNECTIVITY_SERVICE);
        if(cm==null) return false;
        NetworkInfo info=cm.getActiveNetworkInfo();
        return info!=null&&info.isConnected();
    }
    private void updateOfflineBanner() {
        offlineBanner.setVisibility(isNetworkAvailable()?View.GONE:View.VISIBLE);
    }
    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        if (requestCode==FILE_CHOOSER&&filePathCallback!=null) {
            Uri[] results=null;
            if (resultCode==RESULT_OK&&data!=null) {
                if (data.getClipData()!=null) {
                    int count=data.getClipData().getItemCount();
                    results=new Uri[count];
                    for(int i=0;i<count;i++) results[i]=data.getClipData().getItemAt(i).getUri();
                } else if (data.getData()!=null) {
                    results=new Uri[]{data.getData()};
                }
            }
            filePathCallback.onReceiveValue(results);
            filePathCallback=null;
        }
        super.onActivityResult(requestCode, resultCode, data);
    }
    @Override
    public void onBackPressed() {
        if (currentScreen.equals("chat")||currentScreen.equals("group")) {
            webView.evaluateJavascript("showScreen('home');", null);
            currentScreen="home";
        } else {
            if (backPressedTime+2000>System.currentTimeMillis()) {
                if(backToast!=null) backToast.cancel();
                finish();
            } else {
                backToast=Toast.makeText(this,"Press back again to exit",Toast.LENGTH_SHORT);
                backToast.show();
            }
            backPressedTime=System.currentTimeMillis();
        }
    }
    @Override protected void onResume() { super.onResume(); webView.onResume(); webView.resumeTimers(); updateOfflineBanner(); }
    @Override protected void onPause() { super.onPause(); webView.onPause(); webView.pauseTimers(); }
    @Override protected void onDestroy() { if(webView!=null){webView.stopLoading();webView.destroy();} super.onDestroy(); }
}
""")

# ── Gradle wrapper ───────────────────────────────────────
w("gradle/wrapper/gradle-wrapper.properties", """distributionBase=GRADLE_USER_HOME
distributionPath=wrapper/dists
distributionUrl=https\\://services.gradle.org/distributions/gradle-8.4-bin.zip
zipStoreBase=GRADLE_USER_HOME
zipStorePath=wrapper/dists
""")

# ── Build ────────────────────────────────────────────────
os.system("gradle wrapper --gradle-version 8.4")
os.system("chmod +x gradlew")
os.system("./gradlew assembleDebug --stacktrace")
print("Build done!")

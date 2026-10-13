import os
import glob
import subprocess
import urllib.request
import urllib.parse
import json
import hashlib

def get_sha256(filepath):
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

def upload_document(token, chat_id, filepath, caption, content_type="application/zip"):
    filename = os.path.basename(filepath)
    file_size_mb = os.path.getsize(filepath) / (1024 * 1024)
    print(f"Uploading {filename} ({file_size_mb:.2f} MB) to Telegram chat {chat_id}...")

    boundary = '----WebKitFormBoundary7MA4YWxkTrZu0gW'
    body = []
    body.append(f'--{boundary}\r\nContent-Disposition: form-data; name="chat_id"\r\n\r\n{chat_id}\r\n')
    body.append(f'--{boundary}\r\nContent-Disposition: form-data; name="parse_mode"\r\n\r\nHTML\r\n')
    body.append(f'--{boundary}\r\nContent-Disposition: form-data; name="caption"\r\n\r\n{caption}\r\n')
    body.append(f'--{boundary}\r\nContent-Disposition: form-data; name="document"; filename="{filename}"\r\nContent-Type: {content_type}\r\n\r\n')

    with open(filepath, 'rb') as f:
        file_bytes = f.read()

    full_body = "".join(body).encode('utf-8') + file_bytes + f'\r\n--{boundary}--\r\n'.encode('utf-8')
    req = urllib.request.Request(
        f"https://api.telegram.org/bot{token}/sendDocument",
        data=full_body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"}
    )
    with urllib.request.urlopen(req) as resp:
        res_data = resp.read().decode('utf-8')
        print(f"Telegram upload success ({filename}): {res_data[:120]}...")
        return json.loads(res_data)

def send_message(token, chat_id, text):
    print(f"Posting announcement message to Telegram chat {chat_id}...")
    data = urllib.parse.urlencode({
        'chat_id': chat_id,
        'text': text,
        'parse_mode': 'HTML',
        'disable_web_page_preview': 'true'
    }).encode('utf-8')
    req = urllib.request.Request(
        f"https://api.telegram.org/bot{token}/sendMessage",
        data=data
    )
    with urllib.request.urlopen(req) as resp:
        res_data = resp.read().decode('utf-8')
        print(f"Telegram message post success: {res_data[:120]}...")
        return json.loads(res_data)

def main():
    token = os.environ.get('TG_TOKEN', '') or '8076560051:AAEDNzRjLDg-i8zCBnC74voDuG8I2eK3flY'
    chat_id = os.environ.get('TG_CHAT', '') or '-1004359090071'
    
    # Determine version tag from mystic_version.sh
    tag = os.environ.get('RELEASE_TAG', '')
    if not tag:
        try:
            val = subprocess.check_output(
                ["bash", "-c", ". ./mystic_version.sh >/dev/null 2>&1 && echo $MYSTIC_VERSION"]
            ).decode().strip()
            if val:
                tag = f"v{val}"
        except Exception:
            pass
    if not tag:
        tag = 'v1.0.38'

    if not token or not chat_id:
        print("Telegram token or chat_id not provided. Skipping Telegram upload.")
        return

    # 1. Kernel AnyKernel3 Zip
    zip_files = glob.glob(f'release_out/*{tag}*AnyKernel3.zip')
    if not zip_files:
        zip_files = glob.glob('release_out/*AnyKernel3.zip')
    if not zip_files:
        print("No release AnyKernel3 zip file found!")
        return
    kernel_zip = zip_files[0]
    kernel_sha = get_sha256(kernel_zip)

    # 2. ReSukiSU Root Manager APK
    apk_files = glob.glob('release_out/ReSukiSU_v4.2.0-rc3_35184*.apk')
    if not apk_files:
        apk_files = glob.glob('release_out/*.apk')
    if not apk_files:
        print("No ReSukiSU APK found!")
        return
    resukisu_apk = apk_files[0]
    apk_sha = get_sha256(resukisu_apk)

    # 3. Logger Module Zip
    logger_files = glob.glob('release_out/Logger_v*.zip')
    if not logger_files:
        logger_files = glob.glob('/home/myzanori/Desktop/projects/Oneplus_9R/Mystic_Releases/Logger_v*.zip')
    if not logger_files:
        print("No Logger module zip found!")
        return
    logger_zip = logger_files[0]
    logger_sha = get_sha256(logger_zip)

    # Upload all 3 files FIRST (at the top of the post)
    print("\n--- Sending Release Files (Top of post) ---")
    
    kernel_caption = f"""📦 <b>Mystic Kernel {tag} — Universal Kona (9R / 8T)</b>
• <b>Target</b>: OnePlus 9R (lemonades) &amp; OnePlus 8T (kebab)
• <b>Format</b>: Flashable AnyKernel3 Zip
• <b>SHA-256</b>: <code>{kernel_sha}</code>"""

    apk_caption = f"""📱 <b>ReSukiSU Manager App (35184)</b>
• <b>Target</b>: Official Root Manager for Mystic Kernel {tag}
• <b>Architecture</b>: arm64-v8a (OnePlus 9R / 8T)
• <b>Installation</b>: Direct APK — Tap file to install
• <b>SHA-256</b>: <code>{apk_sha}</code>"""

    logger_caption = f"""🛠 <b>Logger Module v1.2 (Zero-Overhead)</b>
• <b>Target</b>: Autonomous on-device diagnostic logger
• <b>Installation</b>: Flash via KernelSU / ReSukiSU Modules
• <b>On-Demand Trigger</b>: <code>su -c mystic_snapshot</code>
• <b>SHA-256</b>: <code>{logger_sha}</code>"""

    upload_document(token, chat_id, kernel_zip, kernel_caption, content_type="application/zip")
    upload_document(token, chat_id, resukisu_apk, apk_caption, content_type="application/vnd.android.package-archive")
    upload_document(token, chat_id, logger_zip, logger_caption, content_type="application/zip")

    # Post the Master Announcement & Changelog right below the files
    print("\n--- Sending Master Announcement & Changelog Post ---")
    post_text = f"""🔥 <b>MYSTIC KERNEL {tag} — UNIVERSAL KONA</b> 🔥
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
<i>The ultimate stable, smooth &amp; battery-optimized daily driver for OnePlus 9R &amp; 8T</i>

📱 <b>Supported Devices:</b>
• OnePlus 9R (lemonades / LE2101)
• OnePlus 8T (kebab / KB2001 / KB2000)

💿 <b>ROM &amp; Android Compatibility:</b>
• OxygenOS 14 (Android 14)
• ColorOS 14 / 15 / 17 (Android 14–17)

⚡ <b>Core Architecture &amp; Stealth:</b>
• <b>Linux Kernel</b>: 4.19.325-perf-Mystic-Kona-myzanori-{tag}
• <b>Root Framework</b>: ReSukiSU v4.1.0 / BakaSU (35184)
• <b>Kernel-side Stealth</b>: SUSFS v2.3.0 (Non-GKI Inline Hooks)
• <b>Path Redirection</b>: NoMount v2.1.0 (Lockless RCU VFS)
• <b>SELinux</b>: Enforcing &amp; Fully Compatible

🚀 <b>Performance &amp; Battery Optimizations:</b>
• <b>Memory &amp; Swap</b>: Enforced LZ4 ZRAM swap (3.7:1 ratio, zero CPU overhead)
• <b>Storage I/O</b>: Smooth UFS 3.1 writeback (<code>dirty_background_ratio=5%</code>)
• <b>Governor</b>: Schedutil anti-flap rate limits (<code>up=500us</code>, <code>down=2000us</code>)
• <b>Network</b>: Google BBR TCP Congestion Control + FQ-CoDel
• <b>Audio &amp; Camera</b>: Full 8/8 Camera LDO rails online + TFA98xx audio amp fix

📝 <b>Changelog ({tag}):</b>
<blockquote>
• <b>Zero-Lag UFS Writeback:</b> Tuned dirty page writeback to 5% and 15% to eliminate background sync micro-stutters.
• <b>Clean Boot Logs:</b> Silenced speculative MTP high-order buffer allocation dumps with __GFP_NOWARN.
• <b>Memory Allocation Fix:</b> Resolved page_alloc atomic reclaim check warning in zsmalloc via GFP_RECLAIM_MASK preservation.
• <b>Driver Guard:</b> Added multi-PMIC protection to eliminate duplicate /proc/pmicWd registration warnings.
• <b>Logger v1.2:</b> Replaced live background logger with a zero-overhead snapshot tool (0% background CPU/disk usage).
• <b>Verified 100% Clean:</b> 0 Warnings, 0 Bugs, 0 Call Traces across entire boot cycle.
</blockquote>

📦 <b>Files Attached Above:</b>
1. <code>{os.path.basename(kernel_zip)}</code>
2. <code>{os.path.basename(resukisu_apk)}</code>
3. <code>{os.path.basename(logger_zip)}</code>

👨‍💻 <b>Developer:</b> @myzanori
💬 <b>Channel:</b> @mystickernel9r
━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""

    send_message(token, chat_id, post_text)
    print("\n✅ All 3 release files and the master announcement post successfully sent to Telegram!")

if __name__ == '__main__':
    main()

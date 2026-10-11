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

def main():
    token = os.environ.get('TG_TOKEN', '') or '8076560051:AAEDNzRjLDg-i8zCBnC74voDuG8I2eK3flY'
    chat_id = os.environ.get('TG_CHAT', '') or '-1004359090071'
    # Determine version tag from mystic_version.sh or target zip
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
        tag = 'v1.0.35'

    if not token or not chat_id:
        print("Telegram token or chat_id not provided. Skipping Telegram upload.")
        return

    # 1. Look for the single AnyKernel3 zip
    zip_files = glob.glob('release_out/*AnyKernel3.zip')
    if not zip_files:
        zip_files = glob.glob('*AnyKernel3.zip')
    if not zip_files:
        zip_files = glob.glob('ak3/*AnyKernel3.zip')
    if not zip_files:
        print("No release AnyKernel3 zip file found!")
        return

    target_zip = zip_files[0]
    sha256 = get_sha256(target_zip)

    caption = f"""<b>Mystic Kernel {tag} — Universal Kona (9R / 8T)</b>

• <b>Devices</b>: OnePlus 9R (lemonades) &amp; OnePlus 8T (kebab)
• <b>ROM Support</b>: OxygenOS 14 &amp; ColorOS 17 (Android 14–17)
• <b>Kernel</b>: Linux 4.19.325-perf-Mystic-Kona-myzanori-{tag}
• <b>Root &amp; Stealth</b>: ReSukiSU / BakaSU + SUSFS v2.3.0 + NoMount v2.1.0
• <b>Camera &amp; Audio</b>: Full 8/8 camera sensors + TFA98xx audio fix
• <b>Tuning</b>: LZ4 ZRAM + Deadline I/O + BBR TCP + FQ-CoDel
• <b>SELinux</b>: Enforcing | <b>Dev</b>: @myzanori

<b>Changelog:</b>
<blockquote>
• Added <code>opkona</code>, <code>ossi</code>, and <code>kona</code> device codenames to AnyKernel3 installation verification for ColorOS 17
• Extended supported Android versions in AnyKernel3 to Android 11–18
• Fixed mm/page_alloc atomic reclaim check condition syntax
• Fixed hung_task_enhance false positive timeouts on uid_add/remove_thread
• Universal SM8250 Kona compatibility for both OnePlus 9R and 8T
• Pre-configured NoMount v2.1.0 and SUSFS v2.3.0 kernel hooks
</blockquote>
<b>SHA-256:</b> <code>{sha256}</code>"""

    try:
        upload_document(token, chat_id, target_zip, caption, content_type="application/zip")
    except Exception as e:
        print(f"Telegram upload error (Kernel): {e}")
        raise

    # 2. Look for the BakaSU Manager APK (direct 1-tap install)
    apk_files = glob.glob('release_out/*.apk') + glob.glob('build_tools/manager/*.apk')
    if apk_files:
        target_apk = apk_files[0]
        apk_sha = get_sha256(target_apk)
        apk_caption = f"""<b>BakaSU Manager v4.2.0-rc3 (35212)</b>

• <b>Target</b>: Official Root Manager for Mystic Kernel {tag}
• <b>Device Support</b>: OnePlus 9R &amp; ARM64 (OxygenOS 14)
• <b>Root Framework</b>: BakaSU (formerly ReSukiSU)
• <b>Installation</b>: Direct APK — Tap file to install
• <b>SHA-256</b>: <code>{apk_sha}</code>"""

        try:
            upload_document(token, chat_id, target_apk, apk_caption, content_type="application/vnd.android.package-archive")
        except Exception as e:
            print(f"Telegram upload error (Manager APK): {e}")

if __name__ == '__main__':
    main()

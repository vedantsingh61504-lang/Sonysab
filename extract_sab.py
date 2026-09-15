import urllib.request

ORIGINAL_URL = "https://premiumplugx.com/VIP/pluglist.php"
OUTPUT_FILE = "sony_sab_sd.m3u"
TARGET_KEYWORD = "sab"  # More flexible keyword search


def extract_single_channel():
  print("Fetching latest playlist from provider...")
  try:
    req = urllib.request.urlopen(ORIGINAL_URL)
    playlist_data = req.read().decode("utf-8", errors="ignore")
  except Exception as e:
    print(f"Error fetching playlist: {e}")
    return

  lines = playlist_data.splitlines()
  extracted_lines = ["#EXTM3U"]

  found = False
  for i in range(len(lines)):
    # Check if target keyword is in the line and it's an EXTINF line
    if TARGET_KEYWORD.lower() in lines[i].lower() and lines[i].startswith(
        "#EXTINF:"
    ):
      extracted_lines.append(lines[i])
      if i + 1 < len(lines):
        extracted_lines.append(lines[i + 1])
      found = True
      print(f"Found matching line: {lines[i]}")
      break

  if found:
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
      f.write("\n".join(extracted_lines))
    print(f"Success! Saved to '{OUTPUT_FILE}'.")
  else:
    print(
        f"Could not find any channel containing '{TARGET_KEYWORD}' in the"
        " playlist."
    )


if __name__ == "__main__":
  extract_single_channel()

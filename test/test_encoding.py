
try:
    # The mojibake string from the log
    mojibake = "鍏风姸浜" 
    # Try to recover
    recovered = mojibake.encode('gbk').decode('utf-8')
    print(f"Recovered: {recovered}")
except Exception as e:
    print(f"Error: {e}")

mojibake_full = "鍏风姸浜猴細涓鑿遍挗缁撴瀯鑲′唤鏈夐檺鍏鍙"
try:
    recovered_full = mojibake_full.encode('gbk').decode('utf-8')
    print(f"Recovered Full: {recovered_full}")
except Exception as e:
    print(f"Error Full: {e}")

def format_response(data):
    """格式化响应数据为可读字符串"""
    return "\n".join(f"{key}: {value}" for key, value in data.items())

def validate_bin(bin_number):
    """验证BIN号码是否有效"""
    return bin_number.isdigit() and (6 <= len(bin_number) <= 8)

def extract_currency_info(currency_data):
    """提取货币信息"""
    return {
        "currency": currency_data.get("currency", "未知"),
        "symbol": currency_data.get("currency_symbol", ""),
        "name": currency_data.get("currency_name", "未知")
    }
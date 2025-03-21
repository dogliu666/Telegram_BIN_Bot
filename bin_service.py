import os
import requests
import re
from dotenv import load_dotenv
from config import validate_bin, format_response

# 加载环境变量
load_dotenv()

# 获取API密钥
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
RAPIDAPI_HOST = os.getenv("RAPIDAPI_HOST")

def get_exchange_rate(from_currency, to_currency):
    """获取实时汇率"""
    try:
        url = f"https://www.google.com/finance/quote/{from_currency}-{to_currency}"
        response = requests.get(url)
        response.raise_for_status()
        
        # 从Google Finance页面提取汇率数据
        pattern = r'data-last-price="([0-9\.]+)"'
        match = re.search(pattern, response.text)
        
        if match:
            rate = float(match.group(1))
            return rate
        else:
            return None
    except Exception as e:
        print(f"获取汇率时出错: {str(e)}")
        return None

def check_bin(bin_number):
    """
    检查BIN号码并返回相关信息
    """
    # 验证BIN号码
    if not validate_bin(bin_number):
        return "请输入有效的6-8位BIN号码"
    
    # 设置API请求头和参数
    url = "https://bin-ip-checker.p.rapidapi.com/"
    
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": RAPIDAPI_HOST,
        "Content-Type": "application/json"
    }
    
    payload = {"bin": bin_number}
    querystring = {"bin": bin_number}  # 添加查询参数
    
    try:
        # 发送API请求 - 添加params参数
        response = requests.post(url, json=payload, headers=headers, params=querystring)
        response.raise_for_status()
        
        data = response.json()
        
        if data.get('success') and data.get('BIN'):
            bin_info = data.get('BIN')
            country_info = bin_info.get('country', {})
            issuer_info = bin_info.get('issuer', {})
            
            # 获取货币汇率
            currency = country_info.get('currency', 'USD')
            
            # 默认汇率值，以防API调用失败
            currency_to_usd = 1.0
            usd_to_cny = 7.23
            
            # 尝试获取实时汇率
            if currency != 'USD':
                rate = get_exchange_rate(currency, 'USD')
                if rate:
                    currency_to_usd = rate
            
            # 获取USD到CNY的汇率
            usd_cny_rate = get_exchange_rate('USD', 'CNY')
            if usd_cny_rate:
                usd_to_cny = usd_cny_rate
            
            currency_to_cny = currency_to_usd * usd_to_cny
            
            # 格式化结果为字典
            result_info = {
                "卡头": bin_info.get('number', bin_number),
                "品牌": bin_info.get('brand', '未知'),
                "类型": bin_info.get('type', '未知'),
                "种类": bin_info.get('scheme', '未知'),
                "级别": bin_info.get('level', '未知'),
                "商业": '是' if bin_info.get('is_commercial') == 'true' else '否',
                "预付": '是' if bin_info.get('is_prepaid') == 'true' else '否',
                "卡行": issuer_info.get('name', '未知'),
                "国家": f"{country_info.get('name', '未知')} {country_info.get('flag', '')}",
                "代码": country_info.get('alpha2', ''),
                "区号": country_info.get('idd', ''),
                "地区": country_info.get('region', '未知'),
                "货币": f"{country_info.get('currency', '')} {country_info.get('currency_symbol', '')} ({country_info.get('currency_name', '')})"
            }
            
            # 添加汇率信息
            if currency != 'USD' and currency != 'CNY':
                result_info["汇率"] = f"1 {currency} = {currency_to_usd:.2f} USD\n1 {currency} = {currency_to_cny:.2f} CNY\n1 USD = {usd_to_cny:.2f} CNY"
            
            return format_response(result_info)
        else:
            return f"查询失败: {data.get('message', '未知错误')}"
        
    except requests.exceptions.RequestException as e:
        return f"查询失败: {str(e)}"
    except Exception as e:
        return f"处理数据时出错: {str(e)}"
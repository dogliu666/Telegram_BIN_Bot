import requests
import json

def get_exchange_rate(from_currency, to_currency):
    """获取实时汇率"""
    try:
        url = f"https://www.google.com/finance/quote/{from_currency}-{to_currency}"
        response = requests.get(url)
        response.raise_for_status()
        
        # 从Google Finance页面提取汇率数据
        import re
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
    url = "https://bin-ip-checker.p.rapidapi.com/"
    
    querystring = {"bin": bin_number}
    payload = {"bin": bin_number}
    
    headers = {
        "x-rapidapi-key": "788dc11cd7mshd3ffbd9b1555bbdp12862bjsnc9378f0de4c5",
        "x-rapidapi-host": "bin-ip-checker.p.rapidapi.com",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, params=querystring)
        response.raise_for_status()  # 检查请求是否成功
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
            
            # 格式化输出
            output = f"""卡头：{bin_info.get('number')}
品牌：{bin_info.get('brand')}
类型：{bin_info.get('type')}
种类：{bin_info.get('scheme')}
级别：{bin_info.get('level')}
商业：{'是' if bin_info.get('is_commercial') == 'true' else '否'}
预付：{'是' if bin_info.get('is_prepaid') == 'true' else '否'}
卡行：{issuer_info.get('name', '未知')}
国家：{country_info.get('name', '未知')} {country_info.get('flag', '')}
代码：{country_info.get('alpha2', '')}
区号：{country_info.get('idd', '')}
地区：{country_info.get('region', '未知')}
货币：{country_info.get('currency', '')} {country_info.get('currency_symbol', '')} ({country_info.get('currency_name', '')})"""
            
            # 添加汇率信息
            if currency != 'USD' and currency != 'CNY':
                output += f"\n1 {currency} = {currency_to_usd:.2f} USD"
                output += f"\n1 {currency} = {currency_to_cny:.2f} CNY"
                output += f"\n1 USD = {usd_to_cny:.2f} CNY"
            
            return output
        else:
            return f"查询失败: {data.get('message', '未知错误')}"
    
    except requests.exceptions.RequestException as e:
        return f"请求出错: {str(e)}"
    except json.JSONDecodeError:
        return "解析响应失败"
    except Exception as e:
        return f"发生错误: {str(e)}"

def main():
    print("BIN查询工具")
    while True:
        bin_number = input("请输入6位或8位BIN号码 (输入'q'退出): ")
        if bin_number.lower() == 'q':
            break
            
        if not bin_number.isdigit() or len(bin_number) < 4 or len(bin_number) > 8:
            print("请输入有效的BIN号码 (通常为6位数字)")
            continue
            
        result = check_bin(bin_number)
        print("\n" + result + "\n")

if __name__ == "__main__":
    main()
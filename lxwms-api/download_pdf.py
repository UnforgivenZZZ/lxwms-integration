import requests
import os, time
url = 'https://wms.xlwms.com/gateway/wms/appendix/getPreviewAndDownLoadUrl?fileKey=prd%2Foms%2F2505%2Foutbound%2F9200190388302841790169_40f6f946-61d2-4de2-bb26-ef912c1085ac_mark1924548315938713600_DO0032505230S7.pdf&fileName=9200190388302841790169.pdf&customerCode=6159003&whCode=SFO'
headers = {
    "content-type": "application/json",
    'accept-encoding': 'gzip, deflate, br, zstd',
    "cookie": "AGL_USER_ID=1d3c269c-e267-4cdb-8ca0-d0a7e71fdca6; _hjSessionUser_3119560=eyJpZCI6IjYyNDE1YTcxLTM3MzMtNTI5NS04MTIwLTUzMWVjNjY1ZjViMiIsImNyZWF0ZWQiOjE3MzUyNjA5NDk1MzEsImV4aXN0aW5nIjp0cnVlfQ==; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22194059ccbc111cb-094ae2da6cdc888-1e525636-1484784-194059ccbc22d4b%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTk0MDU5Y2NiYzExMWNiLTA5NGFlMmRhNmNkYzg4OC0xZTUyNTYzNi0xNDg0Nzg0LTE5NDA1OWNjYmMyMmQ0YiJ9%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%7D; _gcl_au=1.1.1780769461.1743225601; TDC_itoken=727647188%3A1743487552; version=prod; _uetvid=76b142c00c5d11f0b49a8b31172b2cd2; _clck=1ecjduw%7C2%7Cfv4%7C0%7C1914; language=cn; _gid=GA1.2.1860561975.1747023273; _hjSession_3119560=eyJpZCI6IjgwMzE1MTlhLWU4MGUtNDQxOC04MTUwLWQyODE2YmNlZTYyNyIsImMiOjE3NDcxNzMwMTI3MTQsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MH0=; sidebarStatus=1; _ga_NRLS16EKKE=GS2.1.s1747177903$o113$g1$t1747179305$j0$l0$h0; _ga=GA1.1.1106603163.1735260948; _ga_2HTV43T3DN=GS2.1.s1747177896$o124$g1$t1747179845$j0$l0$h0; prod=always",
    "authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIlN0IlMjJidXNpbmVzc1R5cGUlMjIlM0ElMjJ3bXMlMjIlMkMlMjJsb2dpbkFjY291bnQlMjIlM0ElMjJuZWlsczAxJTIyJTJDJTIydXNlck5hbWVDbiUyMiUzQSUyMm5pY2slMjIlMkMlMjJ1c2VyTmFtZUVuJTIyJTNBJTIyJTIyJTJDJTIyY3VzdG9tZXJDb2RlJTIyJTNBbnVsbCUyQyUyMnRlbmFudENvZGUlMjIlM0ElMjI2MTU5JTIyJTJDJTIydGVybWluYWxUeXBlJTIyJTNBbnVsbCU3RCIsImlzcyI6InhpbmdsaWFuLnNlY3VyaXR5IiwiYnVzaW5lc3NUeXBlIjoid21zIiwiZXhwIjoxNzQzNjU1OTAwLCJpYXQiOjE3NDM1Njk1MDAsImp0aSI6IjNlNmE1OGRjLWZiZTAtNGM0YS1iMmNhLTBiMjVmM2IzYzJmNiJ9.ZQ60R81oP9wORF6dmJXi29yK5vVP7NnyysSYAcTWTLg"
}

req = requests.get(url, headers=headers)
print(req.json()['data']['downLoadUrl'])
def downLoadUrl(base_dir):
    file_path = os.path.join(base_dir, 'test.pdf')
    
        # Download the file
    response = requests.get(req.json()['data']['downLoadUrl'])
    response.raise_for_status()  # Check for HTTP errors
    
    # Save the file
    retries = 0
    while retries < 5:
        try:
            with open(file_path, 'wb') as f:
                f.write(response.content)
            
                # print( f"File successfully saved to: {os.path.abspath(file_path)}")
                return
        except Exception as e:
            retries+=1
            if retries == 5:
                raise e
            else:
                time.sleep(10)
                continue
            
downLoadUrl('.')
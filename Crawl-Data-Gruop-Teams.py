# Thay đổi thông tin cho phù hợp ở các line.
# Line 68: Số lượng muốn quét >4. Line 51: Api quét số lượng thành viên trong nhóm. Line 52: Lấy thông tin của từng cá nhân. Thay cả headers của mỗi trường.
import requests

# Hàm để lấy dữ liệu JSON từ một URL với các thông số headers và params tùy chọn
def get_json_data(url, headers=None, params=None):
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        json_data = response.json()
        return json_data
    else:
        print(f"Error: Unable to fetch data from {url}. Status code: {response.status_code}")
        return None

# Hàm để lấy danh sách các thành viên trong một thread dựa trên URL, headers và params
def fetch_thread_members(url, headers, params):
    # Gọi hàm get_json_data để lấy dữ liệu JSON về các thành viên
    json_data = get_json_data(url, headers=headers, params=params)
    if json_data:
        # Trích xuất ID của các thành viên có trường 'tenantId'
        return [member['id'] for member in json_data.get('members', []) if 'tenantId' in member]
    return []

# Hàm để lấy hồ sơ ngắn gọn của các thành viên dựa trên URL, headers và danh sách member_ids
def fetch_member_profiles(url, headers, member_ids):
    params = {
        'isMailAddress': 'false',
        'enableGuest': 'true',
        'includeIBBarredUsers': 'true',
        'skypeTeamsInfo': 'true',
    }
    
    # Gửi yêu cầu POST để lấy hồ sơ ngắn gọn của các thành viên
    response = requests.post(
        url,
        params=params,
        headers=headers,
        json=member_ids
    )
    
    if response.status_code == 200:
        return response.json().get('value', [])
    else:
        print(f"Error: Unable to fetch member profiles. Status code: {response.status_code}")
        return []

# Đoạn mã chính
if __name__ == "__main__":
    # Địa chỉ URL cho thread và hồ sơ ngắn gọn
    thread_url = "https://apac.ng.msg.teams.microsoft.com/v1/threads/19%3AdI6SJvY0sIl47ctCpnwJLQva0sUZURUpj0PuScuZklY1%40thread.tacv2/members"
    profile_url = "https://teams.microsoft.com/api/mt/apac/beta/users/fetchShortProfile"
    
    # Headers cho thread
    thread_headers = {
        "Accept": "application/json",
        "Authentication": "skypetoken=eyJhbGciOiJSUzI1NiIsImtpZCI6IjVFODQ4MjE0Qzc3MDczQUU1QzJCREU1Q0NENTQ0ODlEREYyQzRDODQiLCJ4NXQiOiJYb1NDRk1kd2M2NWNLOTVjelZSSW5kOHNUSVEiLCJ0eXAiOiJKV1QifQ.eyJpYXQiOjE2OTE4NDkwNzMsImV4cCI6MTY5MTkzMDEzMSwic2t5cGVpZCI6Im9yZ2lkOjBlZjFiYjc4LTU2ZmUtNGY4Zi05OTQzLTIxZjkxYjY5N2Q1NyIsInNjcCI6NzgwLCJjc2kiOiIxNjkxODQ4NzczIiwidGlkIjoiYzg1MmQ2MmItMzAzMi00Y2RjLTk2YWItMzBlNDM2OGZhYmQ3IiwicmduIjoiYXBhYyIsImFhZF91dGkiOiJHLVBMRmZXQ21rdVVBd2dRT3pnUEFBIiwiYWFkX2lhdCI6MTY5MTg0ODc3M30.ZtgBl2wt-hurOvxoANG0l0657Qlinivh039-vbtQNQx69Z-IFzlPn2uw_drNVdrRxqdDdQkwjJ880puQ_cuvxj2ITc9toc-KRl3Y9levy75b7SgbXAp9i1aW5jak9zlJg-me6ryv9tVw2XZn6wKhkzc3vzZkf_hnMHzROSX0oWY_JxwFNgdvbPsCLqItcIPT91XKjDysVe--vT1gX2QmNlYviY_9iOe11CY8TLk7fmQVWa3AALqRnKC4BAEkG0XfLKA_z8BuWtl6rJ9Sx2G5-abNaxrMQSp8fEobezyqpqMlZfAyVMZb1CgoePjJN_Nv2aF8SPYgkUmx1ZcDsgXBiQ",
        "Behavioroverride": "redirectAs404",
        "Clientinfo": "os=windows; osVer=10; proc=x86; lcid=vi-vn; deviceType=1; country=vn; clientName=skypeteams; clientVer=1415/1.0.0.2023080221; utcOffset=+07:00; timezone=Asia/Saigon",
        "Origin": "https://teams.microsoft.com",
        "Referer": "https://teams.microsoft.com/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }

    # Thông số params cho thread
    thread_params = {
        "view": "msnp24Equivalent",
        "pageSize": 10, # Số phải lớn hơn 4
        "selectMemberRoles": "User|Guest",
        "filterExplicitlyAdded": False
    }

    # Lấy danh sách các thành viên từ thread
    member_ids = fetch_thread_members(thread_url, headers=thread_headers, params=thread_params)

    if member_ids:
            # Headers cho hồ sơ ngắn gọn
            profile_headers = {
                "Accept": "application/json, text/plain, */*",
                "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJub25jZSI6ImJLTzV6S3BMNHE5XzJPNkdTa25FbUFNamE2U0FoTC13VDgxV1VNbFVRQ3MiLCJhbGciOiJSUzI1NiIsIng1dCI6Ii1LSTNROW5OUjdiUm9meG1lWm9YcWJIWkdldyIsImtpZCI6Ii1LSTNROW5OUjdiUm9meG1lWm9YcWJIWkdldyJ9.eyJhdWQiOiJodHRwczovL2FwaS5zcGFjZXMuc2t5cGUuY29tIiwiaXNzIjoiaHR0cHM6Ly9zdHMud2luZG93cy5uZXQvYzg1MmQ2MmItMzAzMi00Y2RjLTk2YWItMzBlNDM2OGZhYmQ3LyIsImlhdCI6MTY5MTg0ODc3MywibmJmIjoxNjkxODQ4NzczLCJleHAiOjE2OTE5MzAxMzEsImFjY3QiOjAsImFjciI6IjEiLCJhaW8iOiJBVlFBcS84VUFBQUFRcmxZY3VqU0dtbGw4V0wxeVUza1BINmZ6WW52ZElSZENzUnFNT1poTk9MWnl0MEZPd1ZVVEVrOUd6OGZqNnc1TkE1ZDJMQ0p2WFJVVHc1UmZUU0did2JyRWkrdWEvdkxvcGs4dlZoS2xpVT0iLCJhbXIiOlsicHdkIl0sImFwcGlkIjoiNWUzY2U2YzAtMmIxZi00Mjg1LThkNGItNzVlZTc4Nzg3MzQ2IiwiYXBwaWRhY3IiOiIwIiwiYXV0aF90aW1lIjoxNjkxODQ5MDMzLCJmYW1pbHlfbmFtZSI6IkFOIiwiZ2l2ZW5fbmFtZSI6Ik5HVVnhu4ROIEhPw4BORyIsImlwYWRkciI6IjI0MDI6ODAwOjYxYzQ6YmUwMDo0MGMyOmI0NDc6ZTU5Nzo1ZTU4IiwibmFtZSI6Ik5HVVnhu4ROIEhPw4BORyBBTiIsIm9pZCI6IjBlZjFiYjc4LTU2ZmUtNGY4Zi05OTQzLTIxZjkxYjY5N2Q1NyIsInB1aWQiOiIxMDAzMjAwMTg5N0IyQTJCIiwicmgiOiIwLkFUMEFLOVpTeURJdzNFeVdxekRrTm8tcjExZjlGY3hzTEJkQnFJeURzZFZyUzc0OUFLQS4iLCJzY3AiOiJ1c2VyX2ltcGVyc29uYXRpb24iLCJzaWQiOiJkOGYxMzgyYi05NDM3LTRiNGItODc0YS1iNzcwZDhjMjI4NDciLCJzaWduaW5fc3RhdGUiOlsia21zaSJdLCJzdWIiOiJnVDJFUzZSSVgyTlJYZmxJeHVwQ01xVHFVRnVTbDI3dUhzS01MNk13Z0lJIiwidGVuYW50X2N0cnkiOiJWTiIsInRpZCI6ImM4NTJkNjJiLTMwMzItNGNkYy05NmFiLTMwZTQzNjhmYWJkNyIsInVuaXF1ZV9uYW1lIjoiMjEyMTA1MDg4MUBzdHVkZW50Lmh1bWcuZWR1LnZuIiwidXBuIjoiMjEyMTA1MDg4MUBzdHVkZW50Lmh1bWcuZWR1LnZuIiwidXRpIjoiRy1QTEZmV0Nta3VVQXdnUU96Z1BBQSIsInZlciI6IjEuMCIsIndpZHMiOlsiYjc5ZmJmNGQtM2VmOS00Njg5LTgxNDMtNzZiMTk0ZTg1NTA5Il0sInhtc19jYyI6WyJDUDEiXSwieG1zX3NzbSI6IjEifQ.bD7RVt2jyYGW5RjOEWvoe63Z6e-f5hJdH-6_5gfFU5AeIvp6aK3tD82hMYakHl0oSAiusXi-a7GKyp94uyNsaxql8gVANHIOl1XbS_EpxHYgJdfiAFNS6zPYtShJZeOPQbAUtQmtb0TcUJVj_UynFlEZE1mAbNU9szAisdFZCrB0c9ww4U2zqXaPX1j5u-jT1rHiwQa-OB4XE8m2Wqr1rUIxzidUODIi1CsvauQeeWUspvHi-4kEPDZ09TxV6NNPemiuIIKNA2skmdA2-d_FNDvwSn5qZiXQ81c2X1iFQ4bTTWqrDZf24cZiZOs8_hUNNZX_rFUrW6FJ29VTAR8b4A",
                "Content-Type": "application/json",
                "Content-Length": "2200",
                "Content-Type": "application/json;charset=UTF-8",
                "Cookie": "MUIDB=221CCADAB98E6D6E1198D9B1B8E86CCF; clocale=vi-vn; firstTimeLaunch=1691849028052; TSPREAUTHCOOKIE=true; deviceId=4d33c898-3734-425a-950a-ec87d5bff8b2; DesiredAuth=msal2_dev3; multi-window-version=23071327116; TSREGIONCOOKIE=apac; platformid_asm=1415; skypetoken_asm=eyJhbGciOiJSUzI1NiIsImtpZCI6IjVFODQ4MjE0Qzc3MDczQUU1QzJCREU1Q0NENTQ0ODlEREYyQzRDODQiLCJ4NXQiOiJYb1NDRk1kd2M2NWNLOTVjelZSSW5kOHNUSVEiLCJ0eXAiOiJKV1QifQ.eyJpYXQiOjE2OTE4NDkwNzMsImV4cCI6MTY5MTkzMDEzMSwic2t5cGVpZCI6Im9yZ2lkOjBlZjFiYjc4LTU2ZmUtNGY4Zi05OTQzLTIxZjkxYjY5N2Q1NyIsInNjcCI6NzgwLCJjc2kiOiIxNjkxODQ4NzczIiwidGlkIjoiYzg1MmQ2MmItMzAzMi00Y2RjLTk2YWItMzBlNDM2OGZhYmQ3IiwicmduIjoiYXBhYyIsImFhZF91dGkiOiJHLVBMRmZXQ21rdVVBd2dRT3pnUEFBIiwiYWFkX2lhdCI6MTY5MTg0ODc3M30.ZtgBl2wt-hurOvxoANG0l0657Qlinivh039-vbtQNQx69Z-IFzlPn2uw_drNVdrRxqdDdQkwjJ880puQ_cuvxj2ITc9toc-KRl3Y9levy75b7SgbXAp9i1aW5jak9zlJg-me6ryv9tVw2XZn6wKhkzc3vzZkf_hnMHzROSX0oWY_JxwFNgdvbPsCLqItcIPT91XKjDysVe--vT1gX2QmNlYviY_9iOe11CY8TLk7fmQVWa3AALqRnKC4BAEkG0XfLKA_z8BuWtl6rJ9Sx2G5-abNaxrMQSp8fEobezyqpqMlZfAyVMZb1CgoePjJN_Nv2aF8SPYgkUmx1ZcDsgXBiQ; authtoken=Bearer%3DeyJ0eXAiOiJKV1QiLCJub25jZSI6ImJLTzV6S3BMNHE5XzJPNkdTa25FbUFNamE2U0FoTC13VDgxV1VNbFVRQ3MiLCJhbGciOiJSUzI1NiIsIng1dCI6Ii1LSTNROW5OUjdiUm9meG1lWm9YcWJIWkdldyIsImtpZCI6Ii1LSTNROW5OUjdiUm9meG1lWm9YcWJIWkdldyJ9.eyJhdWQiOiJodHRwczovL2FwaS5zcGFjZXMuc2t5cGUuY29tIiwiaXNzIjoiaHR0cHM6Ly9zdHMud2luZG93cy5uZXQvYzg1MmQ2MmItMzAzMi00Y2RjLTk2YWItMzBlNDM2OGZhYmQ3LyIsImlhdCI6MTY5MTg0ODc3MywibmJmIjoxNjkxODQ4NzczLCJleHAiOjE2OTE5MzAxMzEsImFjY3QiOjAsImFjciI6IjEiLCJhaW8iOiJBVlFBcS84VUFBQUFRcmxZY3VqU0dtbGw4V0wxeVUza1BINmZ6WW52ZElSZENzUnFNT1poTk9MWnl0MEZPd1ZVVEVrOUd6OGZqNnc1TkE1ZDJMQ0p2WFJVVHc1UmZUU0did2JyRWkrdWEvdkxvcGs4dlZoS2xpVT0iLCJhbXIiOlsicHdkIl0sImFwcGlkIjoiNWUzY2U2YzAtMmIxZi00Mjg1LThkNGItNzVlZTc4Nzg3MzQ2IiwiYXBwaWRhY3IiOiIwIiwiYXV0aF90aW1lIjoxNjkxODQ5MDMzLCJmYW1pbHlfbmFtZSI6IkFOIiwiZ2l2ZW5fbmFtZSI6Ik5HVVnhu4ROIEhPw4BORyIsImlwYWRkciI6IjI0MDI6ODAwOjYxYzQ6YmUwMDo0MGMyOmI0NDc6ZTU5Nzo1ZTU4IiwibmFtZSI6Ik5HVVnhu4ROIEhPw4BORyBBTiIsIm9pZCI6IjBlZjFiYjc4LTU2ZmUtNGY4Zi05OTQzLTIxZjkxYjY5N2Q1NyIsInB1aWQiOiIxMDAzMjAwMTg5N0IyQTJCIiwicmgiOiIwLkFUMEFLOVpTeURJdzNFeVdxekRrTm8tcjExZjlGY3hzTEJkQnFJeURzZFZyUzc0OUFLQS4iLCJzY3AiOiJ1c2VyX2ltcGVyc29uYXRpb24iLCJzaWQiOiJkOGYxMzgyYi05NDM3LTRiNGItODc0YS1iNzcwZDhjMjI4NDciLCJzaWduaW5fc3RhdGUiOlsia21zaSJdLCJzdWIiOiJnVDJFUzZSSVgyTlJYZmxJeHVwQ01xVHFVRnVTbDI3dUhzS01MNk13Z0lJIiwidGVuYW50X2N0cnkiOiJWTiIsInRpZCI6ImM4NTJkNjJiLTMwMzItNGNkYy05NmFiLTMwZTQzNjhmYWJkNyIsInVuaXF1ZV9uYW1lIjoiMjEyMTA1MDg4MUBzdHVkZW50Lmh1bWcuZWR1LnZuIiwidXBuIjoiMjEyMTA1MDg4MUBzdHVkZW50Lmh1bWcuZWR1LnZuIiwidXRpIjoiRy1QTEZmV0Nta3VVQXdnUU96Z1BBQSIsInZlciI6IjEuMCIsIndpZHMiOlsiYjc5ZmJmNGQtM2VmOS00Njg5LTgxNDMtNzZiMTk0ZTg1NTA5Il0sInhtc19jYyI6WyJDUDEiXSwieG1zX3NzbSI6IjEifQ.bD7RVt2jyYGW5RjOEWvoe63Z6e-f5hJdH-6_5gfFU5AeIvp6aK3tD82hMYakHl0oSAiusXi-a7GKyp94uyNsaxql8gVANHIOl1XbS_EpxHYgJdfiAFNS6zPYtShJZeOPQbAUtQmtb0TcUJVj_UynFlEZE1mAbNU9szAisdFZCrB0c9ww4U2zqXaPX1j5u-jT1rHiwQa-OB4XE8m2Wqr1rUIxzidUODIi1CsvauQeeWUspvHi-4kEPDZ09TxV6NNPemiuIIKNA2skmdA2-d_FNDvwSn5qZiXQ81c2X1iFQ4bTTWqrDZf24cZiZOs8_hUNNZX_rFUrW6FJ29VTAR8b4A%26Origin%3Dhttps%3A%2F%2Fteams.microsoft.com; clienttype=web; tenantId=c852d62b-3032-4cdc-96ab-30e4368fabd7; minimumVersionClientUpdateTries=0; ringFinder=%7B%22oid%22%3A%220ef1bb78-56fe-4f8f-9943-21f91b697d57%22%2C%22tid%22%3A%22c852d62b-3032-4cdc-96ab-30e4368fabd7%22%7D; TSAUTHCOOKIE=eyJ0eXAiOiJKV1QiLCJub25jZSI6ImJLTzV6S3BMNHE5XzJPNkdTa25FbUFNamE2U0FoTC13VDgxV1VNbFVRQ3MiLCJhbGciOiJSUzI1NiIsIng1dCI6Ii1LSTNROW5OUjdiUm9meG1lWm9YcWJIWkdldyIsImtpZCI6Ii1LSTNROW5OUjdiUm9meG1lWm9YcWJIWkdldyJ9.eyJhdWQiOiJodHRwczovL2FwaS5zcGFjZXMuc2t5cGUuY29tIiwiaXNzIjoiaHR0cHM6Ly9zdHMud2luZG93cy5uZXQvYzg1MmQ2MmItMzAzMi00Y2RjLTk2YWItMzBlNDM2OGZhYmQ3LyIsImlhdCI6MTY5MTg0ODc3MywibmJmIjoxNjkxODQ4NzczLCJleHAiOjE2OTE5MzAxMzEsImFjY3QiOjAsImFjciI6IjEiLCJhaW8iOiJBVlFBcS84VUFBQUFRcmxZY3VqU0dtbGw4V0wxeVUza1BINmZ6WW52ZElSZENzUnFNT1poTk9MWnl0MEZPd1ZVVEVrOUd6OGZqNnc1TkE1ZDJMQ0p2WFJVVHc1UmZUU0did2JyRWkrdWEvdkxvcGs4dlZoS2xpVT0iLCJhbXIiOlsicHdkIl0sImFwcGlkIjoiNWUzY2U2YzAtMmIxZi00Mjg1LThkNGItNzVlZTc4Nzg3MzQ2IiwiYXBwaWRhY3IiOiIwIiwiYXV0aF90aW1lIjoxNjkxODQ5MDMzLCJmYW1pbHlfbmFtZSI6IkFOIiwiZ2l2ZW5fbmFtZSI6Ik5HVVnhu4ROIEhPw4BORyIsImlwYWRkciI6IjI0MDI6ODAwOjYxYzQ6YmUwMDo0MGMyOmI0NDc6ZTU5Nzo1ZTU4IiwibmFtZSI6Ik5HVVnhu4ROIEhPw4BORyBBTiIsIm9pZCI6IjBlZjFiYjc4LTU2ZmUtNGY4Zi05OTQzLTIxZjkxYjY5N2Q1NyIsInB1aWQiOiIxMDAzMjAwMTg5N0IyQTJCIiwicmgiOiIwLkFUMEFLOVpTeURJdzNFeVdxekRrTm8tcjExZjlGY3hzTEJkQnFJeURzZFZyUzc0OUFLQS4iLCJzY3AiOiJ1c2VyX2ltcGVyc29uYXRpb24iLCJzaWQiOiJkOGYxMzgyYi05NDM3LTRiNGItODc0YS1iNzcwZDhjMjI4NDciLCJzaWduaW5fc3RhdGUiOlsia21zaSJdLCJzdWIiOiJnVDJFUzZSSVgyTlJYZmxJeHVwQ01xVHFVRnVTbDI3dUhzS01MNk13Z0lJIiwidGVuYW50X2N0cnkiOiJWTiIsInRpZCI6ImM4NTJkNjJiLTMwMzItNGNkYy05NmFiLTMwZTQzNjhmYWJkNyIsInVuaXF1ZV9uYW1lIjoiMjEyMTA1MDg4MUBzdHVkZW50Lmh1bWcuZWR1LnZuIiwidXBuIjoiMjEyMTA1MDg4MUBzdHVkZW50Lmh1bWcuZWR1LnZuIiwidXRpIjoiRy1QTEZmV0Nta3VVQXdnUU96Z1BBQSIsInZlciI6IjEuMCIsIndpZHMiOlsiYjc5ZmJmNGQtM2VmOS00Njg5LTgxNDMtNzZiMTk0ZTg1NTA5Il0sInhtc19jYyI6WyJDUDEiXSwieG1zX3NzbSI6IjEifQ.bD7RVt2jyYGW5RjOEWvoe63Z6e-f5hJdH-6_5gfFU5AeIvp6aK3tD82hMYakHl0oSAiusXi-a7GKyp94uyNsaxql8gVANHIOl1XbS_EpxHYgJdfiAFNS6zPYtShJZeOPQbAUtQmtb0TcUJVj_UynFlEZE1mAbNU9szAisdFZCrB0c9ww4U2zqXaPX1j5u-jT1rHiwQa-OB4XE8m2Wqr1rUIxzidUODIi1CsvauQeeWUspvHi-4kEPDZ09TxV6NNPemiuIIKNA2skmdA2-d_FNDvwSn5qZiXQ81c2X1iFQ4bTTWqrDZf24cZiZOs8_hUNNZX_rFUrW6FJ29VTAR8b4A; MC1=GUID=7294e46274094a2691c09a3becc42008&HASH=7294&LV=202308&V=4&LU=1691853949350; sessionId=848488c0-b0be-b761-a213-4386bcda8b01",
                "Origin": "https://teams.microsoft.com",
                "Referer": "https://teams.microsoft.com/_",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
            }

            # Lấy hồ sơ ngắn gọn của các thành viên
            member_profiles = fetch_member_profiles(profile_url, headers=profile_headers, member_ids=member_ids)

            # Mở tệp tin để ghi với mã Unicode
            with open('user_info.txt', 'w', encoding='utf-8') as file:
                # Trong vòng lặp for member in member_profiles
                for member in member_profiles:
                    user_principal_name = member.get('userPrincipalName')
                    display_name = member.get('displayName')
                    print(f"{user_principal_name}|{display_name}") # In ra màn hình
                    #file.write(f"{user_principal_name}|{display_name}\n") # Lưu vào file txt

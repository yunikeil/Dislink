from typing import List

from fastapi import HTTPException, Request


class IpCheck():
    def __init__(self, **kwargs) -> None:
        self.allowed_ips: List[str] = kwargs.get("allowed_ips")
    
    def is_ip_allowed(self, request: Request):
        client_ip = request.client.host
        if not self.allowed_ips or len(self.allowed_ips) == 0:
            return True
        if client_ip not in self.allowed_ips:
            raise HTTPException(status_code=403, detail="IP address is not allowed")






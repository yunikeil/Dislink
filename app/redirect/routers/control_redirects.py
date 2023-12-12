from typing import List

from fastapi import APIRouter, Request, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from core.database import get_session
from core.security import IpCheck
from core.settings import config
from app.redirect.services import redirects as RedirectDB
from app.redirect.schemas import redirect_info as RedirictDTO



checker = IpCheck(allowed_ips=config.control_redirects_allowed_ips)
router = APIRouter(dependencies=[Depends(checker.is_ip_allowed)])




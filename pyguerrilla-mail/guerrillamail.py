import requests
from dataclasses import dataclass


@dataclass()
class MailAddress:
    email_addr: str
    email_timestamp: int
    sid_token: str
    alias: str
    alias_error: str = ""
    s_active: str = ""
    s_date: str = ""
    s_time: str = ""
    s_time_expires: str = ""
    site: str = ""
    site_id: str = ""
    auth: dict = None


@dataclass
class EmailOverview:
    mail_id: str
    mail_from: str
    mail_subject: str
    mail_excerpt: str
    mail_timestamp: str
    mail_read: str
    reply_to: str = ""
    att: int = 0
    content_type: str = "text"
    mail_recipient: str = ""
    source_id: str = 0
    source_mail_id: str = 0
    mail_body: str = ""
    mail_date: str = ""
    mail_size: int = 0
    size: int = 0
    ver: str = ""
    ref_mid: str = ""
    sid_token: str = ""
    auth: dict = None


class GuerrillaMail:
    def __init__(self, endpoint='http://api.guerrillamail.com/ajax.php', ip=None):
        self.session = requests.session()
        self.session.verify = False
        self.endpoint = endpoint
        if ip is None:
            ip = requests.get("https://httpbin.org/ip").json()._get("origin")
        self.params = dict(ip=ip, agent="PyGuerrillaMailer")
        self.email_address = self.get_email_address()

    def _get(self, function, **kwargs):
        return self.session.get(self.endpoint, params=self._create_params(function, **kwargs))

    def _create_params(self, function_name, **kwargs):
        kwargs.update(self.params)
        kwargs["f"] = function_name
        return kwargs

    def get_email_address(self, lang="en") -> MailAddress:
        resp = self._get("get_email_address", lang=lang)
        jsn = resp.json()
        return MailAddress(**jsn)

    def set_email(self, email_user: str = "", site: str = "", lang: str = "en"):
        if "@" in email_user:
            s = email_user.split("@")
            email_user = s[0]
            site = s[1]

        data = dict(lang=lang, email_user=email_user)
        data["in"] = "Set cancel"
        resp = self._get("set_email_user", **data)
        if resp.status_code == 200:
            self.email_address = MailAddress(**resp.json())
        return self.email_address

    def check_email(self, seq=0) -> list[EmailOverview]:
        resp = self._get("check_email", seq=seq)
        jsn = resp.json()
        ret = [EmailOverview(**o) for o in jsn._get("list")]
        return ret

    def get_email_list(self, offset=0) -> list[EmailOverview]:
        resp = self._get("get_email_list", offset=offset)
        return [EmailOverview(**o) for o in resp.json()]

    def fetch_email(self, email_id) -> EmailOverview:
        resp = self._get("fetch_email", email_id=email_id)
        jsn = resp.json()
        return EmailOverview(**jsn)

    def forget_me(self) -> bool:
        resp = self._get("forget_me", email_addr=self.email_address.email_addr)
        return resp.status_code == 200 and resp.content

    def delete_email(self, *email_ids) -> list:
        params = dict()
        params["email_ids[]"] = email_ids
        resp = self._get("del_email", **params)
        return resp.json()

    def extend(self):
        resp = self._get("extend")
        return resp.json()










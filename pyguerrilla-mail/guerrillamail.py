import requests
from dataclasses import dataclass


@dataclass()
class MailAddress:
    """
    represents a mail address given by guerrillamail
    """
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
class Email:
    """Is either a small overview from an email containing only the subject, or the fully fetched email"""
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
    """
    Guerrillamail client implementing the guerrillamail api.
    """

    def __init__(self, endpoint='http://api.guerrillamail.com/ajax.php', ip=None):
        """
        Creates a new guerrillamail API client.
        :param endpoint: The endpoint of the API to use. Has a default, but should work with any go-guerrilla instance.
        :param ip: The clients ip if known. If not given it requests it externally.
        """
        self.session = requests.session()
        self.session.verify = False
        self.endpoint = endpoint
        if ip is None:
            ip = requests.get("https://httpbin.org/ip").json()._get("origin")
        self.params = dict(ip=ip, agent="PyGuerrillaMailer")
        self._email_address = None

    def email_address(self):
        if self._email_address is None:
            self._email_address = self._get_email_address()
        return self._email_address

    def _get(self, function, **kwargs):
        return self.session.get(self.endpoint, params=self._create_params(function, **kwargs))

    def _create_params(self, function_name, **kwargs):
        kwargs.update(self.params)
        kwargs["f"] = function_name
        return kwargs

    def _get_email_address(self, lang="en") -> MailAddress:
        """
        gets a new random email address
        :param lang: The language of the Mail Address
        :return: a random Mail address
        """
        resp = self._get("get_email_address", lang=lang)
        jsn = resp.json()
        return MailAddress(**jsn)

    def set_email(self, email_user: str = "", site: str = "", lang: str = "en") -> MailAddress:
        """
        Sets a new email-address
        :param email_user: the username to choose
        :param site: the guerrillamail domain. (should not be needed as emails for all domains are returned)
        :param lang: The language to use
        :return: the choosen MailAddress
        """
        if "@" in email_user:
            s = email_user.split("@")
            email_user = s[0]
            site = s[1]

        data = dict(lang=lang, email_user=email_user)
        data["in"] = "Set cancel"
        resp = self._get("set_email_user", **data)
        if resp.status_code == 200:
            self._email_address = MailAddress(**resp.json())
        return self._email_address

    def check_email(self, seq=0) -> list[Email]:
        """
        Check emails in current mailbox
        :param seq: the sequence number of the email to start from
        :return: a list of email overviews
        """
        resp = self._get("check_email", seq=seq)
        jsn = resp.json()
        ret = [Email(**o) for o in jsn._get("list")]
        return ret

    def get_email_list(self, offset=0) -> list[Email]:
        """
        like check_mail but supports an offset
        :param offset: The offset to get the email list
        :return: a list of Email overviews
        """
        resp = self._get("get_email_list", offset=offset)
        return [Email(**o) for o in resp.json()]

    def fetch_email(self, email_id) -> Email:
        """
        gets a specific email by its id.
        :param email_id: The email_id to fetch
        :return: The complete email if found
        """
        resp = self._get("fetch_email", email_id=email_id)
        jsn = resp.json()
        return Email(**jsn)

    def forget_me(self) -> bool:
        """Forgets the currently used email address"""
        resp = self._get("forget_me", email_addr=self.email_address.email_addr)
        if resp.status_code == 200 and resp.content:
            self._email_address = None
            return True
        return False

    def delete_email(self, *email_ids) -> list:
        """
        deletes a specific email by its id
        :param email_ids: the email_id to delete
        :return: the raw json response
        """
        params = dict()
        params["email_ids[]"] = email_ids
        resp = self._get("del_email", **params)
        return resp.json()

    def extend(self):
        """
        extend the usage of currently selected mail
        :return: the raw json response
        """
        resp = self._get("extend")
        return resp.json()










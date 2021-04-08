import scrapy
from scrapy.http import HtmlResponse
import re
import json
from urllib.parse import urlencode
from copy import deepcopy
from urllib.parse import quote
from instagram_parser.items import InstagramParserItem

class InstagramSpider(scrapy.Spider):
    name = 'instagram'
    allowed_domains = ['instagram.com']
    start_urls = ['http://instagram.com/']
    username = "olga.n.parshina"
    enc_password = "#PWD_INSTAGRAM_BROWSER:10:1617634278:AddQAJhgrQPNCqdvZZKCwtgX2IMN0rwIvMVd/uGLCcy8zq0e3/uYZOVFB4+qhJkbXluYshLbLnUcVOKbcavdaRUSl3dbeZuLELUVLzwmk7jSyTwopw0JHGWO7LrIi7PVSYj9q79+RyLZnRPwCC0="
    login_url = "https://www.instagram.com/accounts/login/ajax/"
    user_to_srapy_list = ["esquireru", "gdv.14"]
    user_to_srapy_1 = user_to_srapy_list[0]
    user_to_srapy_2 = user_to_srapy_list[1]
    graphql_url = 'https://www.instagram.com/graphql/query/?'
    subscribers_hash = "5aefa9893005572d237da5068082d8d5"
    his_subscriptions_hash = "3dec7e2c57367ef3da3d987d89f9dbc8"

    def parse(self, response: HtmlResponse):
        yield scrapy.FormRequest(
            self.login_url,
            callback=self.user_login,
            method='POST',
            formdata={"username": self.username, "enc_password": self.enc_password},
            headers={"X-CSRFToken": self.get_csrf_token(response.text)}
        )

    def user_login(self, response: HtmlResponse):
        json_data = response.json()
        if json_data["user"] and json_data["authenticated"]:
            self.user_id = json_data["userId"]
            user_to_scrapy_url = f"/{self.user_to_srapy_1}"
            yield response.follow(
                user_to_scrapy_url,
                callback=self.user_data_parse,
                cb_kwargs={"username": self.user_to_srapy_1}  # 'own_user_id': self.user_id
            )
            user_to_scrapy_url = f"/{self.user_to_srapy_2}"
            yield response.follow(
                user_to_scrapy_url,
                callback=self.user_data_parse,
                cb_kwargs={"username": self.user_to_srapy_2}  # 'own_user_id': self.user_id
            )

    def user_data_parse(self, response: HtmlResponse, username):
        user_id = self.get_user_id(response.text, username)
        variables = {"id": user_id, "first": 12}  # "first": 12
        str_variables = self.make_variables_string(variables)
        url_list = [self.graphql_url + f"query_hash={self.subscribers_hash}&variables={str_variables}",
                    self.graphql_url + f"query_hash={self.his_subscriptions_hash}&variables={str_variables}"]
        url = url_list[0]
        yield response.follow(
            url,
            callback=self.parse_posts,
            cb_kwargs={
                "username": username,
                "user_id": user_id,
                "variables": deepcopy(variables)
            },
        )
        url = url_list[1]
        yield response.follow(
            url,
            callback=self.parse_posts,
            cb_kwargs={
                "username": username,
                "user_id": user_id,
                "variables": deepcopy(variables)
            },
        )

    def make_variables_string(self, variables):
        # хардкод для кодирования словаря как в запросе Instagram
        # %7B"id"%3A"7709057810"%2C"first"%3A12%2C"after"%3A"QVFCblJDbklkd1F3bm1hWExXRVR2RVRDYWRXek5ORWUxOWtjY01mLWtGYS05Y25ZTkJ2c20zNzRGdjEwNGZmNnhQY1F2eGZZMXgzQUd1X3d5eWVMejczRw%3D%3D"%7D
        open_parenthesis = "%7B"  # {
        close_parenthesis = "%7D"  # }
        space = "%3A"
        comma = "%2C"  # ,
        s = []
        for i, (k, v) in enumerate(variables.items()):
            s.append('"' + k + '"')
            s.append(space)
            if isinstance(v, str):
                s.append('"' + v + '"')
            else:
                s.append(str(v))

            if i != len(variables) - 1:
                s.append(comma)
        s = [open_parenthesis] + s + [close_parenthesis]
        return "".join(s)

    def parse_posts(self, response: HtmlResponse, username, user_id, variables):
        global url_list, url
        data = response.json()
        try:
            data = data["data"]["user"]["edge_follow"]
            his_subscriptions = 1
            subscribers = 0
        except KeyError:
            data = data["data"]["user"]["edge_followed_by"]
            his_subscriptions = 0
            subscribers = 1
        page_info = data.get("page_info", None)
        if page_info is None:
            return

        if page_info["has_next_page"]:
            variables["after"] = page_info["end_cursor"]
            str_variables = self.make_variables_string(variables)
            url_subscribers = f"{self.graphql_url}query_hash={self.subscribers_hash}&variables={str_variables}"
            yield response.follow(
                url_subscribers,
                callback=self.parse_posts,
                cb_kwargs={
                    "username": username,
                    "user_id": user_id,
                    "variables": deepcopy(variables)
                }
            )
            url_his_subscriptions = f"{self.graphql_url}query_hash={self.his_subscriptions_hash}&variables={str_variables}"
            yield response.follow(
                url_his_subscriptions,
                callback=self.parse_posts,
                cb_kwargs={
                    "username": username,
                    "user_id": user_id,
                    "variables": deepcopy(variables)
                }
            )
        posts = data["edges"]
        for post in posts:
            tmp = post["node"]
            item = InstagramParserItem(
                user_id=tmp["id"],  # user_id,
                photo=tmp["profile_pic_url"],  # display_url
                name=tmp["full_name"],
                login=tmp["username"],
                user_to_srapy=username,
                his_subscriptions=his_subscriptions,
                subscribers=subscribers
            )
            print(item)
            yield item

    def parse_subscribed(self, response: HtmlResponse, username, user_id, variables):
        data_2 = response.json()
        try:
            data_2 = data_2["data"]["user"]["edge_follow"]
        except KeyError:
            data_2 = data_2["data"]["user"]["edge_followed_by"]
            page_info = data_2.get("page_info", None)
            if page_info["has_next_page"]:
                variables["after"] = page_info["end_cursor"]
            str_variables = self.make_variables_string(variables)
            url_list = [self.graphql_url + f"query_hash={self.subscribers_hash}&variables={str_variables}",
                        self.graphql_url + f"query_hash={self.his_subscriptions_hash}&variables={str_variables}"]
            url = url_list[1]
            yield response.follow(
                url,
                callback=self.parse_posts,
                cb_kwargs={
                    "username": username,
                    "user_id": user_id,
                    "variables": deepcopy(variables)
                }
            )
        posts = data_2["edges"]
        for n in posts:
            tmp = n["node"]
            item = InstagramParserItem(
                user_id=tmp["id"],  # user_id,
                photo=tmp["profile_pic_url"],  # display_url
                name=tmp["full_name"],
                login=tmp["username"],
                user_to_srapy=self.user_to_srapy_2,
                his_subscriptions=1,
                subscribers=0
            )
            yield item

    # получаем токен для авторизации
    def get_csrf_token(self, text):
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

    # Получаем id желаемого пользователя
    def get_user_id(self, text, username):
        matched_2 = re.search('{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text).group()
        return json.loads(matched_2).get('id')

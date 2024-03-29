import json
from http.server import BaseHTTPRequestHandler, HTTPServer

from views import (create_category, create_comment, create_post,
                    create_post_tag, create_subscription, create_tag,
                    create_user, delete_category, delete_comment, delete_post,
                    delete_post_tag, delete_subscription, delete_tag,
                    get_all_categories, get_all_comments, get_all_posts,
                    get_all_subscriptions, get_all_tags, get_all_users,
                    get_certain_post_tags, get_posts_by_author,
                    get_posts_by_category, get_posts_by_tag, get_single_post,
                    get_single_user, get_subs_by_follower, get_tags_by_label,
                    login_user, update_category, update_post, update_tag)
from views.post_requests import search_posts


class HandleRequests(BaseHTTPRequestHandler):
    """Handles the requests to this server"""

    def parse_url(self):
        """Parse the url into the resource and id"""
        path_params = self.path.split('/')
        resource = path_params[1]
        if '?' in resource:
            param = resource.split('?')[1]
            resource = resource.split('?')[0]
            pair = param.split('=')
            key = pair[0]
            value = pair[1]
            return (resource, key, value)
        else:
            id = None
            try:
                id = int(path_params[2])
            except (IndexError, ValueError):
                pass
            return (resource, id)

    def _set_headers(self, status):
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response

        Args:
            status (number): the status code to return to the front end
        """
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_OPTIONS(self):
        """Sets the OPTIONS headers
        """
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods',
                         'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers',
                         'X-Requested-With, Content-Type, Accept')
        self.end_headers()

    def do_GET(self):
        self._set_headers(200)
        response = {}

        parsed = self.parse_url()

        if len(parsed) == 2:
            (resource, id) = parsed
            if resource == "posts":
                if id is not None:
                    response = get_single_post(id)
                else:
                    response = get_all_posts()
            elif resource == "tags":
                response = get_all_tags()
            elif resource == "categories":
                response = get_all_categories()
            elif resource == 'users':
                if id is not None:
                    response = get_single_user(id)
                else:
                    response = get_all_users()
            elif resource == "comments":
                response = get_all_comments()
            elif resource == "subscriptions":
                # if id is not None:
                    
                # else:
                response = get_all_subscriptions()

        elif len(parsed) == 3:
            (resource, key, value) = parsed

            if resource == "tags" and key == "q":
                response = get_tags_by_label(value)
            elif resource == "posttags" and key == "post_id":
                response = get_certain_post_tags(value)
            elif resource == "posts" and key == "category_id":
                response = get_posts_by_category(value)
            elif resource == "posts" and key == "user_id":
                response = get_posts_by_author(value)
            elif resource == "posts" and key =="q":
                response = search_posts(value)
            elif resource == "subscriptions" and key == "follower_id":
                response = get_subs_by_follower(value)
            elif resource == "posts" and key == "tag_id":
                response = get_posts_by_tag(value)

        self.wfile.write(response.encode())

    def do_POST(self):
        """Make a post request to the server"""
        self._set_headers(201)
        content_len = int(self.headers.get('content-length', 0))
        post_body = json.loads(self.rfile.read(content_len))
        response = ''
        resource, _ = self.parse_url()

        if resource == 'login':
            response = login_user(post_body)
        if resource == 'register':
            response = create_user(post_body)
        if resource == 'tags':
            response = create_tag(post_body)
        if resource == 'categories':
            response = create_category(post_body)
        if resource == 'posts':
            response = create_post(post_body)
        elif resource == 'subscriptions':
            response = create_subscription(post_body)
        if resource == 'posttags':
            response = create_post_tag(post_body)
        elif resource == 'comments':
            response = create_comment(post_body)

        self.wfile.write(response.encode())

    def do_PUT(self):
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        (resource, id) = self.parse_url()

        success = False

        if resource == "posts":
            success = update_post(id, post_body)
        if resource == "tags":
            success = update_tag(id, post_body)
        if resource == "categories":
            success = update_category(id, post_body)

        if success:
            self._set_headers(204)
        else:
            self._set_headers(404)

        self.wfile.write("".encode())

    def do_DELETE(self):
        self._set_headers(204)

        (resource, id) = self.parse_url()

        if resource == "posts":
            delete_post(id)
        if resource == "posttags":
            delete_post_tag(id)
        if resource == "comments":
            delete_comment(id)
        if resource == "subscriptions":
            delete_subscription(id)
        if resource == "tags":
            delete_tag(id)
        if resource == "categories":
            delete_category(id)

        self.wfile.write("".encode())


def main():
    """Starts the server on port 8088 using the HandleRequests class
    """
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()

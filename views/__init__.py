from .category_requests import (create_category, delete_category,
                                get_all_categories, update_category)
from .comment_requests import create_comment, delete_comment, get_all_comments
from .post_requests import (create_post, create_post_tag, delete_post,
                            get_all_posts, get_posts_by_author,
                            get_posts_by_category, get_posts_by_tag,
                            get_single_post, search_posts, update_post)
from .post_tag_requests import delete_post_tag, get_certain_post_tags
from .subscription_requests import (create_subscription, delete_subscription,
                                    get_all_subscriptions,
                                    get_subs_by_follower)
from .tag_requests import (create_tag, delete_tag, get_all_tags,
                           get_tags_by_label, update_tag)
from .user_requests import (create_user, get_all_users, get_single_user,
                            login_user)

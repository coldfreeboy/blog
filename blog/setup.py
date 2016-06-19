from config import settings


def url(request):
    if settings.DEBUG:

        return {
            "staticUrl":"/static/blog/",
            "jq"        : "http://apps.bdimg.com/libs/jquery/2.1.4/jquery.min.js",

        }

    else:
        pass
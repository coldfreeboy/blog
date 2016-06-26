from config import settings


def url(request):
    if settings.DEBUG:

        return {
            "static":"/static/",
            "jq"        : "/static/blog/js/jq.js",
            

        }

    else:
        return {
            "static":"/static/",
            "jq"        : "http://apps.bdimg.com/libs/jquery/2.1.4/jquery.min.js",

        } 
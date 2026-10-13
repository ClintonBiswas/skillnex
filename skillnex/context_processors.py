from .models import SiteSettings


def site_settings(request):

    settings = (
        SiteSettings.objects
        .filter(is_active=True)
        .first()
    )

    return {
        "site_settings": settings,
    }
from enquiries.models import ProductEnquiry 


def enquiry_count(request):

    if not request.user.is_authenticated:
        return {
            "new_enquiry_count": 0,
        }

    if not getattr(request.user, "is_staff", False):
        return {
            "new_enquiry_count": 0,
        }

    return {
        "new_enquiry_count": ProductEnquiry.objects.filter(
            status="new"
        ).count(),
    }
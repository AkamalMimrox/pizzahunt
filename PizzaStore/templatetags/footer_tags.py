# footer_tags.py

from django import template
from PizzaStore.models import about
register = template.Library()

@register.inclusion_tag('footer/footer.html')
def render_footer():
    data = about.objects.first()
    social = about.objects.all()
    fsocial = None
    
    for s in social:
        fsocial = s.socialmedia.all()

    return {'data': data, 'fsocial': fsocial}
  

from django import template

register = template.Library()

# 커스텀 필터를 만들 것이다.
@register.filter
def hashtag_link(word):
    # word는 게시글 객체(review)

    # 마지막 단어도 공백을 붙여야 단어 형태로 인식
    content = word.content + ' '

    hashtags = word.hashtags.all()

    for hashtag in hashtags:
        content = content.replace(hashtag.content + ' ', f'<a href="/community/{hashtag.pk}/hashtag/" class="text-decoration-none">{hashtag.content}</a> ')
        # </a> 뒤에 공백이 반드시 존재해야 한다.
    
    return content



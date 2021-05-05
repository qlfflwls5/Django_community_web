from rest_framework import serializers
from .models import Review, Comment, Hashtag


class ReviewListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = ('id', 'title', 'movie_title', )


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('id', 'content', 'user_id', 'review_id', )


class ReviewSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    comment_count = serializers.IntegerField(source='comments.count', read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'title', 'movie_title', 'rank', 'content', 'image', 'created_at', 'updated_at', 'user_id', 'comments', 'comment_count', 'like_users', 'hashtags', )


class HashtagListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Comment
        fields = ('id', 'content', )